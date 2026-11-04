#!/usr/bin/env bash
# Usage: run.sh <claude|codex> <case> <rep> [new-output-directory]
set -euo pipefail
eval_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
exec python3 - "$eval_dir" "$@" <<'PY'
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import shutil
import signal
import subprocess
import sys
import tempfile
import time

eval_dir = Path(sys.argv[1])
repo = eval_dir.parent
if len(sys.argv) not in (5, 6):
    sys.exit("Usage: run.sh <claude|codex> <case> <rep> [new-output-directory]")
host, case_id, rep = sys.argv[2:5]
definitions = json.loads((eval_dir / "cases.json").read_text())
case = next((case for case in definitions["cases"] if case["id"] == case_id), None)
if not case or host not in case["hosts"] or not re.fullmatch(r"[A-Za-z0-9_]+", rep):
    sys.exit("Unknown case, unsupported host, or invalid repetition ID")
profile = definitions["profiles"][case["profile"]]
if not shutil.which(host):
    sys.exit("Host CLI not found: " + host)
timeout = int(os.environ.get("EVAL_TIMEOUT", "900"))
if timeout <= 0:
    sys.exit("EVAL_TIMEOUT must be positive")
if len(sys.argv) == 6:
    requested = Path(sys.argv[5])
    if requested.exists() or requested.is_symlink():
        sys.exit("Output directory already exists")
    output = requested.resolve()
    if output == repo or repo in output.parents:
        sys.exit("Output must be outside the skills checkout")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.mkdir()  # No overwrite, even for an empty directory.
else:
    parent = (Path(tempfile.gettempdir()) / "skills-evals").resolve()
    if parent == repo or repo in parent.parents:
        sys.exit("Temporary output must be outside the skills checkout")
    parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = Path(tempfile.mkdtemp(prefix=f"{stamp}-{host}-{case_id}-{rep}-", dir=parent)).resolve()
print(output, flush=True)
fixture = output / "fixture"
environment = os.environ.copy()
environment.update(PATH=str(eval_dir / "bin") + os.pathsep + environment.get("PATH", ""),
                   ZDOTDIR=str(output / "zdot"), GH_STUB_LOG=str(output / "gh-calls.jsonl"),
                   GH_STUB_STATE=str(output / "gh-state.json"), GIT_TERMINAL_PROMPT="0")
for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR"):
    environment.pop(key, None)
(output / "zdot").mkdir()
scorer = runpy.run_path(str(eval_dir / "score.py"))

def save(name, value):
    (output / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")

def capture(argv, cwd=repo):
    try:
        result = subprocess.run(argv, cwd=cwd, env=environment, text=True, capture_output=True, timeout=15)
        return dict(exit_code=result.returncode, stdout=result.stdout.strip(), stderr=result.stderr.strip())
    except (OSError, subprocess.TimeoutExpired) as exc:
        return dict(exit_code=None, stdout="", stderr=str(exc))

def revision(directory):
    top = capture(["git", "-C", str(directory), "rev-parse", "--show-toplevel"])
    if top["exit_code"] != 0 or Path(top["stdout"]).resolve() != directory.resolve():
        return "unknown"
    return capture(["git", "-C", str(directory), "rev-parse", "HEAD"])["stdout"] or "unknown"

def installation_record(name, directory, expected):
    path, source = directory / "SKILL.md", expected / "SKILL.md"
    record = compare_file(name, path, source)
    record.update(realpath=str(directory.resolve()), expected_realpath=str(expected.resolve()))
    if path.is_file():
        record["body_sha256"] = hashlib.sha256(scorer["skill_body"](path.read_text()).encode()).hexdigest()
    return record

def compare_file(name, path, expected):
    record = dict(name=name, path=str(path), realpath=str(path.resolve()),
                  expected_realpath=str(expected.resolve()), path_match=path.resolve() == expected.resolve(),
                  content_match=False, sha256=None, error=None)
    try:
        record["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        record["expected_sha256"] = hashlib.sha256(expected.read_bytes()).hexdigest()
        record["content_match"] = record["sha256"] == record["expected_sha256"]
    except OSError as exc:
        record["error"] = str(exc)
    return record

def codex_installation():
    # Inspect the documented user scope without changing global configuration.
    root = Path.home() / ".agents/skills"
    records = []
    for name in ("pr-writer", "code-wright", "humanizer"):
        expected = repo / ("external/humanizer" if name == "humanizer" else name)
        records.append(installation_record(name, root / name, expected))
    for name in ("pr-writer", "code-wright"):
        reference = (root / name).resolve().parent / "references/prose-editing.md"
        records.append(compare_file(name + ":prose-editing", reference, repo / "references/prose-editing.md"))
    matched = all(record["path_match"] and record["content_match"] for record in records)
    return dict(status="match" if matched else "install_mismatch", records=records,
                scope=str(root), limit="User-scope paths/content only; host skill selection, disabled skills, plugins, and other scopes are not verified")

model = os.environ.get("EVAL_MODEL", "sonnet" if host == "claude" else "gpt-6.1-sol")
effort = os.environ.get("EVAL_REASONING_EFFORT", "high") if host == "codex" else "host-default"
git_metadata_restricted = host == "codex" and profile["sandbox"] in ("read-only", "workspace-write")
command = (["claude", "-p", "--model", model, "--no-session-persistence", "--output-format", "stream-json", "--verbose",
            "--max-turns", "80", "--setting-sources", "project,local", "--permission-mode", profile["permission_mode"], "--add-dir", str(repo),
            "--allowedTools", *profile["allowed_tools"]] if host == "claude" else
           ["codex", "exec", "-c", 'approval_policy="never"', "-m", model,
            "-c", "model_reasoning_effort=" + json.dumps(effort),
            "-s", profile["sandbox"], "--ephemeral", "--json", "-C", str(fixture), "-"])
dirty = capture(["git", "status", "--porcelain", "--untracked-files=all"])
metadata = dict(schema_version=1, host=host, case=case_id, rep=rep,
                started_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                skills_commit=revision(repo), skills_dirty=bool(dirty["stdout"]) if dirty["exit_code"] == 0 else "unknown",
                humanizer_commit=revision(repo / "external/humanizer"),
                humanizer_gitlink=capture(["git", "ls-tree", "HEAD", "external/humanizer"])["stdout"],
                cases_sha256=hashlib.sha256((eval_dir / "cases.json").read_bytes()).hexdigest(),
                versions={name: capture([name, "--version"]) for name in ("claude", "codex", "git", "python3")},
                requested_model=model, observed_model="unknown", reasoning_effort=effort, observed_settings={},
                capabilities={"git_metadata_write": dict(
                    available=not git_metadata_restricted,
                    reason=f"Codex {profile['sandbox']} sandbox keeps .git read-only" if git_metadata_restricted
                    else "No Git metadata sandbox restriction declared; host permission checks still apply")},
                sandbox=profile["sandbox"] if host == "codex" else "host permissions; allowed tools are not a sandbox",
                approval_policy="never" if host == "codex" else "host permission checks",
                permission_mode=profile["permission_mode"] if host == "claude" else None,
                allowed_tools=profile["allowed_tools"] if host == "claude" else "user Codex configuration",
                installation=case["installation"] if host == "claude" else "user-global-as-is",
                installation_limit="Codex user-scope paths/content are checked; settings and other skill scopes remain active" if host == "codex" else "Claude runs use --setting-sources project,local, so user-scope settings, CLAUDE.md, and skills are not loaded; scopes outside that option can still affect a run",
                command=command, timeout_seconds=timeout, fixture=str(fixture),
                environment={key: environment[key] for key in ("PATH", "ZDOTDIR", "GH_STUB_LOG", "GH_STUB_STATE")})
save("metadata.json", metadata)
save("cases.json", definitions)
save("sources.json", scorer["collect_sources"](repo))
(output / "prompt.txt").write_text(case["prompt"] + "\n")
(output / "transcript.jsonl").touch()
(output / "stderr.log").touch()
execution = dict(status="preparing", exit_code=None)
process = None

def interrupted(signum, frame):
    raise InterruptedError("Received signal " + str(signum))

signal.signal(signal.SIGTERM, interrupted)
signal.signal(signal.SIGINT, interrupted)
try:
    subprocess.run(["bash", str(eval_dir / "fixtures.sh"), case["fixture"], str(fixture)],
                   env=environment, check=True, stdout=subprocess.DEVNULL)
    if host == "claude":
        skills_dir = fixture / ".claude/skills"
        skills_dir.mkdir(parents=True)
        if case["installation"].startswith("standalone:"):
            name = case["installation"].split(":", 1)[1]
            shutil.copytree(repo / name, skills_dir / name, symlinks=False)
        else:
            for name in scorer["SKILLS"]:
                if name == "humanizer" and case["installation"] == "full-no-humanizer-skill":
                    continue
                target = repo / ("external/humanizer" if name == "humanizer" else name)
                (skills_dir / name).symlink_to(target, target_is_directory=True)
        metadata["installed_skills"] = [installation_record(
            path.name, path, repo / ("external/humanizer" if path.name == "humanizer" else path.name))
            for path in sorted(skills_dir.iterdir())]
    else:
        metadata["installation_check"] = codex_installation()
    save("metadata.json", metadata)
    initial_pr = fixture / ".git/eval-pr.json"
    save("gh-state.json", json.loads(initial_pr.read_text()) if initial_pr.exists() else None)
    (output / "gh-calls.jsonl").touch()
    shell = os.environ.get("SHELL", "/bin/zsh" if Path("/bin/zsh").exists() else "/bin/bash")
    resolved = capture([shell, "-lc", "command -v gh"], fixture)
    remote = capture(["git", "remote", "get-url", "--all", "origin"], fixture)
    push_remote = capture(["git", "remote", "get-url", "--push", "--all", "origin"], fixture)
    expected_remote = str(fixture / ".remote.git")
    safe = (resolved["exit_code"] == 0 and resolved["stdout"] == str(eval_dir / "bin/gh")
            and remote["exit_code"] == push_remote["exit_code"] == 0
            and remote["stdout"] == push_remote["stdout"] == expected_remote)
    save("preflight.json", dict(shell=shell, gh=resolved, remote=remote, push_remote=push_remote, passed=safe))
    if not safe:
        raise RuntimeError("Preflight failed: login-shell gh must be the stub; fetch/push remotes must be the fixture bare repository")
    save("before.json", scorer["snapshot"](fixture))
    execution["status"] = "running"
    save("execution.json", execution)
    started = time.monotonic()
    with open(output / "prompt.txt") as prompt, open(output / "transcript.jsonl", "w") as transcript, open(output / "stderr.log", "w") as errors:
        process = subprocess.Popen(command, cwd=fixture, env=environment, stdin=prompt,
                                   stdout=transcript, stderr=errors, start_new_session=True)
        try:
            code = process.wait(timeout=timeout)
            execution.update(status="completed" if code == 0 else "failed", exit_code=code)
        except subprocess.TimeoutExpired:
            execution["status"] = "timeout"
    execution["elapsed_seconds"] = round(time.monotonic() - started, 3)
except (OSError, RuntimeError, subprocess.SubprocessError, InterruptedError) as exc:
    execution.update(status="interrupted" if isinstance(exc, InterruptedError) else "failed", error=str(exc))
finally:
    # Kill the process group, including leftover host children, on every exit path.
    if process is not None:
        try:
            os.killpg(process.pid, signal.SIGTERM)
            process.wait(timeout=5)
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
    if fixture.exists():
        try:
            after = scorer["snapshot"](fixture)
            after["checks"] = {}
            if process is not None and execution["status"] in ("completed", "failed", "timeout"):
                for check in case["checks"]:
                    try:
                        checked = subprocess.run(check["argv"], cwd=fixture, env=environment, text=True,
                                                 capture_output=True, timeout=check["timeout_seconds"])
                        after["checks"][check["id"]] = dict(exit_code=checked.returncode, stdout=checked.stdout, stderr=checked.stderr)
                    except (OSError, subprocess.TimeoutExpired) as exc:
                        after["checks"][check["id"]] = dict(exit_code=None, error=str(exc))
            save("after.json", after)
        except (OSError, RuntimeError) as exc:
            execution["snapshot_error"] = str(exc)
    observed = scorer["parse_transcript"](output / "transcript.jsonl", host)
    metadata.update(observed_model=sorted(observed.models) or "unknown", observed_settings=observed.settings,
                    finished_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
    save("metadata.json", metadata)
    save("execution.json", execution)
print(json.dumps(execution), flush=True)
sys.exit(0 if execution["status"] == "completed" else 1)
PY
