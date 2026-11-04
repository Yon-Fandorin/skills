#!/usr/bin/env python3
"""Score observable evidence; semantic criteria always require manual review."""
import argparse
from dataclasses import dataclass, field
import difflib
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
SKILLS = ("agents-writer", "project-guide", "codebase-architecture", "code-wright",
          "dual-agent", "finish-task", "pr-writer", "skill-reviewer", "humanizer")
ANSI = re.compile(r"\x1b\[[0-9;]*m")
BLOCKED = re.compile(r"approv|permission|can't be checked|cannot be checked|denied", re.I)
READ_ERROR = re.compile(r"no such file|does not exist|not found|cannot open|can't open|access denied", re.I)


@dataclass
class Call:
    id: str
    name: str
    inputs: dict
    index: int
    output: str = ""
    error: bool = False
    complete: bool = False
    result_index: int = -1
    exit_code: int | None = None


@dataclass
class Transcript:
    calls: list = field(default_factory=list)
    skill_bodies: list = field(default_factory=list)
    models: set = field(default_factory=set)
    final: str = ""
    terminal: bool = False
    malformed: int = 0
    delegated: bool = False
    settings: dict = field(default_factory=dict)
    unsupported_items: set = field(default_factory=set)

    @property
    def complete(self):
        return self.terminal and not self.malformed and not self.unsupported_items and all(call.complete for call in self.calls)


def text_content(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(text_content(part) for part in value)
    if isinstance(value, dict):
        return text_content(value.get("text", value.get("content", "")))
    return ""


def parse_transcript(path, host):
    transcript, pending = Transcript(), {}
    injection_call = None
    for index, line in enumerate(Path(path).read_text(errors="replace").splitlines()):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except ValueError:
            transcript.malformed += 1
            injection_call = None
            continue
        if not isinstance(event, dict):
            transcript.malformed += 1
            injection_call = None
            continue
        if host == "claude":
            preceding_call, injection_call = injection_call, None
            message = event.get("message")
            message = message if isinstance(message, dict) else {}
            if message.get("model"):
                transcript.models.add(message["model"])
            if event.get("type") == "system" and event.get("subtype") == "init":
                if event.get("model"):
                    transcript.models.add(event["model"])
                transcript.settings = {key: event[key] for key in ("permissionMode", "tools", "skills") if key in event}
            content = message.get("content", [])
            launches = []
            for block in content if isinstance(content, list) else []:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "tool_use":
                    call = Call(block["id"], block["name"], block.get("input", {}), index)
                    pending[call.id] = call
                    transcript.calls.append(call)
                    transcript.delegated |= call.name in ("Agent", "Task")
                elif block.get("type") == "tool_result":
                    call = pending.get(block.get("tool_use_id"))
                    if call:
                        call.output = text_content(block.get("content", ""))
                        launch_result = event.get("tool_use_result")
                        call.error = bool(block.get("is_error")) or (isinstance(launch_result, dict) and launch_result.get("success") is False)
                        call.complete, call.result_index = True, index
                        if call.name == "Skill":
                            launches.append(call)
                elif (block.get("type") == "text" and event.get("type") == "user"
                      and event.get("isSynthetic") is True):
                    match = re.fullmatch(r"Base directory for this skill: ([^\n]+)\n\n(.*)",
                                         block.get("text", ""), re.S)
                    if match:
                        transcript.skill_bodies.append(dict(
                            call_id=preceding_call.id if preceding_call else None,
                            base_directory=match[1], body=match[2], index=index))
            # The injected user message carries no tool ID. Only the immediately
            # preceding, unambiguous Skill result establishes its provenance.
            if len(launches) == 1:
                injection_call = launches[0]
            if event.get("type") == "result":
                transcript.final = event.get("result", "")
                transcript.terminal = event.get("subtype") == "success" and not event.get("is_error", False)
                transcript.models.update(event.get("modelUsage", {}))
        else:
            if isinstance(event.get("model"), str):
                transcript.models.add(event["model"])
            item = event.get("item") or {}
            kind = item.get("type")
            if kind and kind not in ("agent_message", "reasoning", "command_execution", "file_change", "collab_tool_call"):
                transcript.unsupported_items.add(kind)
            if kind in ("command_execution", "mcp_tool_call", "collab_tool_call"):
                identifier = item.get("id", str(index))
                call = pending.get(identifier)
                if not call:
                    inputs = {"command": item.get("command", "")} if kind == "command_execution" else item.get("arguments", {})
                    inputs = inputs if isinstance(inputs, dict) else {"arguments": inputs}
                    call = Call(identifier, kind, inputs, index)
                    pending[identifier] = call
                    transcript.calls.append(call)
                if event.get("type") == "item.completed":
                    call.output = item.get("aggregated_output", text_content(item.get("result", "")))
                    call.exit_code = item.get("exit_code")
                    call.error = item.get("status") == "failed" or call.exit_code not in (None, 0) or bool(item.get("error"))
                    call.complete, call.result_index = True, index
                transcript.delegated |= kind == "collab_tool_call"
            if event.get("type") == "item.completed" and kind == "agent_message":
                transcript.final = item.get("text", "")
            if event.get("type") == "turn.completed":
                transcript.terminal = True
            if event.get("type") in ("turn.failed", "error"):
                transcript.terminal = False
    return transcript


def clean_output(output):
    output = ANSI.sub("", output)
    return re.sub(r"^[ \t]*\d+(?:\t|→)", "", output, flags=re.M).strip()


def source_key(path, sources):
    path = path.replace("\\", "/")
    if path.endswith("humanizer/SKILL.md"):
        return "external/humanizer/SKILL.md"
    for key in sorted(sources, key=len, reverse=True):
        if path == key or path.endswith("/" + key):
            return key
    return path


def read_range(call, key, sources, total):
    if call.name == "Read" and source_key(call.inputs.get("file_path", ""), sources) == key:
        start = call.inputs.get("offset", 1)
        return start, min(total, start + call.inputs.get("limit", total) - 1)
    try:
        lexer = shlex.shlex(call.inputs.get("command", ""), posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return None
    segments, segment = [], []
    for token in tokens + [";"]:
        if token and all(char in ";&|" for char in token):
            segments.append(segment)
            segment = []
        else:
            segment.append(token)
    for args in segments:
        if not args or not any(source_key(arg, sources) == key for arg in args[1:]):
            continue
        reader = Path(args[0]).name
        if reader == "sed" and "-n" in args:
            for arg in args[1:]:
                match = re.fullmatch(r"(\d+)(?:,(\d+|\$))?p", arg)
                if match:
                    return int(match[1]), min(total, total if match[2] == "$" else int(match[2] or match[1]))
        if reader in ("head", "tail"):
            options = [arg for arg in args[1:] if arg.startswith("-")]
            count = "10"
            if options:
                if len(options) != 1:
                    continue
                option = options[0]
                if option == "-n" and args.index(option) + 1 == len(args):
                    continue
                if option == "-n":
                    count = args[args.index(option) + 1]
                else:
                    count = option[2:] if option.startswith("-n") else option[1:]
            if not re.fullmatch(r"\+?\d+", count) or (reader == "head" and count.startswith("+")):
                continue
            if reader == "head":
                return 1, min(total, int(count))
            start = max(1, int(count)) if count.startswith("+") else max(1, total - int(count) + 1)
            return start, total
    return None


def coverage(output, source, requested=None, previous=()):
    lines = source.strip().splitlines()
    returned = clean_output(output).splitlines()
    if not lines:
        return [], 0, set()
    matcher = difflib.SequenceMatcher(None, lines, returned, autojunk=False)
    candidates = matcher.get_matching_blocks()
    blocks = [block for block in candidates if block.size >= min(3, len(lines))]
    anchors = set(previous) | {line for block in blocks for line in range(block.a + 1, block.a + block.size + 1)}
    for block in candidates:
        if not 0 < block.size < min(3, len(lines)):
            continue
        informative = any(line.strip() and not line.lstrip().startswith("#") for line in lines[block.a:block.a + block.size])
        if informative and (block.a in anchors or block.a + block.size + 1 in anchors):
            blocks.append(block)
            anchors.update(range(block.a + 1, block.a + block.size + 1))
    ranges = [[block.a + 1, block.a + block.size] for block in blocks]
    matched_output = {index for block in blocks for index in range(block.b, block.b + block.size)}
    # A known range anchors short output to its exact source position.
    if requested:
        start, end = requested
        if returned and 1 <= start <= end <= len(lines) and "\n".join(lines[start - 1:end]).strip() == clean_output(output):
            ranges.append([start, end])
            matched_output.update(range(len(returned)))
    # Numbered reader output disambiguates even a one-line final chunk.
    for output_index, line in enumerate(ANSI.sub("", output).strip().splitlines()):
        numbered = re.match(r"^[ \t]*(\d+)(?:\t|→)(.*)$", line)
        if numbered:
            index = int(numbered[1]) - 1
            if 0 <= index < len(lines) and lines[index] == numbered[2]:
                ranges.append([index + 1, index + 1])
                matched_output.add(output_index)
    covered = sorted({line for start, end in ranges for line in range(start, end + 1)})
    ranges = []
    for line in covered:
        if ranges and ranges[-1][1] == line - 1:
            ranges[-1][1] = line
        else:
            ranges.append([line, line])
    return ranges, len(lines), matched_output


def read_evidence(transcript, sources):
    evidence = []
    covered_by_source = {}
    for call in transcript.calls:
        inputs = call.inputs
        command = inputs.get("command", "")
        is_reader = call.name == "Read" or bool(re.search(r"\b(cat|bat|sed|head|tail)\b|read_text|\.read\(", command))
        paths = [inputs.get("file_path", "")] if call.name == "Read" else []
        if is_reader:
            paths += re.findall(r"[^\s'\";|<>`]+\.md", command)
        # Full returned bodies also resolve shell variables and symlink paths.
        output = clean_output(call.output)
        if is_reader and call.complete:
            paths += [key for key, value in sources.items() if value["text"].strip() and value["text"].strip() in output]
        matches = {key: coverage(call.output, sources[key]["text"],
                                 read_range(call, key, sources, len(sources[key]["text"].strip().splitlines())),
                                 covered_by_source.get(key, set()))
                   for key in {source_key(path, sources) for path in paths} if key in sources}
        matched_output = {index for _, _, indices in matches.values() for index in indices}
        diagnostics = [line for index, line in enumerate(output.splitlines()) if index not in matched_output]
        for path in dict.fromkeys(path for path in paths if path):
            key = source_key(path, sources)
            ranges, total, _ = matches.get(key, ([], 0, set()))
            covered = {line for start, end in ranges for line in range(start, end + 1)}
            if call.complete:
                covered_by_source.setdefault(key, set()).update(covered)
            error_lines = [line for line in diagnostics
                           if READ_ERROR.search(line) and (path in line or Path(path).name in line)]
            if not call.complete:
                status = "unknown"
            elif total and len(covered) == total:
                status = "full"
            elif covered:
                status = "partial"
            elif call.error and any(BLOCKED.search(line) for line in diagnostics):
                status = "blocked"
            elif error_lines:
                status = "failed"
            elif call.error:
                status = "failed"
            else:
                status = "unknown"
            evidence.append(dict(path=path, source=key, status=status, call_id=call.id,
                                 load_source="file_read",
                                 call_index=call.index, result_index=call.result_index,
                                 ranges=ranges if status in ("full", "partial") else [], total_lines=total,
                                 detail=("\n".join(error_lines or diagnostics)[:200]) if status in ("blocked", "failed") else ""))
    return evidence + dispatch_evidence(transcript, sources)


def skill_body(text):
    return re.sub(r"\A---\r?\n.*?\r?\n---(?:\r?\n|\Z)", "", text, count=1, flags=re.S).strip()


def skill_succeeded(call):
    name = call.inputs.get("skill", call.inputs.get("command", ""))
    return call.complete and not call.error and call.output.strip() == "Launching skill: " + name


def dispatch_evidence(transcript, sources):
    key = "external/humanizer/SKILL.md"
    source = sources.get(key, {})
    evidence = []
    for call in transcript.calls:
        if call.name != "Skill" or call.inputs.get("skill", call.inputs.get("command")) != "humanizer":
            continue
        bodies = [body for body in transcript.skill_bodies if body["call_id"] == call.id]
        status, detail = "unknown", "missing linked injected body or source real path"
        total = len(source.get("text", "").strip().splitlines())
        if not call.complete:
            detail = "missing dispatch result"
        elif not skill_succeeded(call):
            status = "blocked" if BLOCKED.search(call.output) else "failed"
            detail = "dispatch did not succeed"
        elif len(bodies) != 1:
            status, detail = "failed", "missing or ambiguous linked injected body"
        elif source.get("realpath") and source.get("text"):
            base = Path(bodies[0]["base_directory"])
            injected_body = bodies[0]["body"]
            args = call.inputs.get("args")
            if isinstance(args, str):
                injected_body = injected_body.removesuffix("\n\n\nARGUMENTS: " + args)
            if not base.is_absolute() or base.resolve() != Path(source["realpath"]).resolve().parent:
                status, detail = "failed", "injected base directory differs from pinned source"
            elif injected_body.strip() != skill_body(source["text"]):
                status, detail = "partial", "injected body does not match the full source body"
            else:
                status, detail = "full", "linked injected body matches pinned source without frontmatter"
        evidence.append(dict(path=bodies[0]["base_directory"] if len(bodies) == 1 else key,
                             source=key, status=status, load_source="skill_dispatch", call_id=call.id,
                             call_index=call.index, result_index=call.result_index,
                             injection_index=bodies[0]["index"] if len(bodies) == 1 else None,
                             ranges=[[1, total]] if status == "full" else [], total_lines=total, detail=detail))
    return evidence


def reference_result(assertion, evidence, complete):
    key = assertion["path"]
    reads = [read for read in evidence if read["source"] == key
             and (not assertion.get("load_source") or read["load_source"] == assertion["load_source"])]
    covered = {line for read in reads for start, end in read["ranges"] for line in range(start, end + 1)}
    total = max((read["total_lines"] for read in reads), default=0)
    if total and len(covered) == total:
        status, detail = "pass", "full returned content (possibly across reads)"
    elif any(read["status"] == "blocked" for read in reads):
        status, detail = "unknown", "blocked"
    elif any(read["status"] == "partial" for read in reads):
        status, detail = "fail", "partial"
    elif any(read["status"] == "failed" for read in reads):
        status, detail = "fail", "failed"
    else:
        status, detail = ("fail", "not observed") if complete and not reads else ("unknown", "insufficient evidence")
    return result(key, status, detail, [read["call_id"] for read in reads])


def result(identifier, status, detail="", evidence=None):
    return dict(id=identifier, status=status, detail=detail, evidence=evidence or [])


def rollup(assertions):
    statuses = {assertion["status"] for assertion in assertions}
    if "fail" in statuses:
        return "fail"
    if "unknown" in statuses:
        return "unknown"
    return "pass" if "pass" in statuses else "not_applicable"


def selection_results(expected, transcript, reads):
    selected, attempted, inspected, uncertain = set(), set(), set(), set()
    for call in transcript.calls:
        if call.name == "Skill":
            name = call.inputs.get("skill", call.inputs.get("command", "")).split(":")[-1]
            attempted.add(name)
            if skill_succeeded(call):
                selected.add(name)
            elif not call.complete or BLOCKED.search(call.output) or not call.error:
                uncertain.add(name)
    for name in SKILLS:
        matching = [read for read in reads if read["source"].endswith(name + "/SKILL.md")]
        if matching:
            if name in expected.get("inspection_only", []):
                inspected.add(name)
                continue
            attempted.add(name)
            assertion = {"path": matching[0]["source"]}
            if reference_result(assertion, matching, False)["status"] == "pass":
                selected.add(name)
            elif any(read["status"] in ("blocked", "unknown") for read in matching):
                uncertain.add(name)
    assertions = []
    complete = transcript.complete and not transcript.delegated
    for name in expected.get("required", []):
        status = "pass" if name in selected else "fail" if complete and name not in uncertain else "unknown"
        assertions.append(result("required:" + name, status, "successful dispatch or full body required"))
    for name in expected.get("forbidden", []):
        status = "fail" if name in selected else "pass" if complete and name not in uncertain else "unknown"
        assertions.append(result("forbidden:" + name, status, "child tool traces may be unavailable" if transcript.delegated else ""))
    return dict(status=rollup(assertions), selected=sorted(selected), attempted=sorted(attempted),
                inspected=sorted(inspected), assertions=assertions)


def git_output(root, *args):
    proc = subprocess.run(["git", "--no-optional-locks", "-C", str(root), *args], text=True, capture_output=True)
    if proc.returncode:
        raise RuntimeError(proc.stderr.strip())
    return proc.stdout.strip()


def snapshot(root):
    root = Path(root).resolve()
    files, directories = {}, []
    ignored = {".git", ".remote.git", ".claude", "__pycache__"}
    for directory, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = sorted(name for name in dirs if name not in ignored)
        for name in dirs[:]:
            path = Path(directory) / name
            if path.is_symlink():
                names.append(name)
                dirs.remove(name)
            else:
                directories.append(path.relative_to(root).as_posix())
        for name in sorted(names):
            if name in ignored:
                continue
            path = Path(directory) / name
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                files[relative] = dict(link=os.readlink(path))
            else:
                files[relative] = dict(sha256=hashlib.sha256(path.read_bytes()).hexdigest(), mode=path.stat().st_mode & 0o777)
    branches = dict(line.split(" ", 1) for line in git_output(root, "for-each-ref", "--format=%(refname:short) %(objectname)", "refs/heads").splitlines())
    worktrees = []
    for line in git_output(root, "worktree", "list", "--porcelain").splitlines():
        if line.startswith("worktree "):
            worktrees.append(os.path.relpath(line[9:], root))
    return dict(files=files, directories=sorted(directories), branches=branches, worktrees=sorted(worktrees),
                head=git_output(root, "rev-parse", "HEAD"), status=git_output(root, "status", "--porcelain", "--untracked-files=all"))


def state_result(assertion, before, after, metadata=None):
    op = assertion["op"]
    identifier = "state:" + op + ":" + str(assertion.get("paths", assertion.get("path", assertion.get("name", ""))))
    for requirement in assertion.get("requires", []):
        capability = (metadata or {}).get("capabilities", {}).get(requirement, {})
        if capability.get("available") is False:
            return result(identifier, "not_applicable", capability["reason"])
        if capability.get("available") is not True:
            return result(identifier, "unknown", "capability not recorded: " + requirement)
    if before is None or after is None:
        return result(identifier, "unknown", "initial/final snapshots unavailable")
    initial, final = before["files"], after["files"]
    if op == "unchanged":
        paths = {path for path in initial.keys() | final.keys() if any(fnmatch.fnmatchcase(path, pattern) for pattern in assertion["paths"])}
        if not paths:
            return result(identifier, "unknown", "patterns matched no files")
        ok = all(initial.get(path) == final.get(path) for path in paths)
        if assertion["paths"] == ["**"]:
            ok &= all(before[key] == after[key] for key in ("directories", "branches", "worktrees", "head", "status"))
    elif op == "absent":
        ok = all(path not in final and path not in after["directories"] for path in assertion["paths"])
    elif op == "changed":
        path = assertion["path"]
        ok = path in initial and path in final and initial[path] != final[path]
    elif op == "branch_absent":
        ok = assertion["name"] not in after["branches"]
    elif op == "branch_unchanged":
        name = assertion["name"]
        ok = name in before["branches"] and before["branches"][name] == after["branches"].get(name)
    elif op == "worktree_absent":
        ok = assertion["path"] not in after["worktrees"]
    else:
        raise ValueError("Unknown state operation: " + op)
    return result(identifier, "pass" if ok else "fail")


def gh_result(assertion, calls, state, complete=True):
    op = assertion["op"]
    identifier = "gh:" + op + ":" + " ".join(assertion.get("command", [assertion.get("name", "")]))
    if calls is None:
        return result(identifier, "unknown", "stub log unavailable")
    if op in ("existing_label", "readback") and state is None:
        return result(identifier, "unknown", "final PR state unavailable")
    successful = [call for call in calls if call["exit_code"] == 0]
    if op in ("successful", "forbidden"):
        matches = [call for call in calls if call["argv"][:2] == assertion["command"]]
        if op == "forbidden" and not matches and not complete:
            return result(identifier, "unknown", "incomplete run cannot prove absence")
        ok = not matches if op == "forbidden" else any(call["exit_code"] == 0 and all(flag in call["argv"] for flag in assertion.get("flags", [])) for call in matches)
    elif op == "existing_label":
        name = assertion["name"]
        listed = []
        for call in successful:
            if call["argv"][:2] != ["label", "list"]:
                continue
            try:
                returned = json.loads(call["stdout"])
            except ValueError:
                returned = call["stdout"].splitlines()
            values = returned if isinstance(returned, list) else [returned]
            if any((value.get("name") if isinstance(value, dict) else value) == name for value in values):
                listed.append(call)
        writes = [call for call in successful if call["argv"][:2] in (["pr", "create"], ["pr", "edit"])]
        ok = bool(state and name in [label["name"] for label in state["labels"]] and any(read["time"] < write["time"] for read in listed for write in writes))
    elif op == "readback":
        writes = [index for index, call in enumerate(calls) if call["exit_code"] == 0 and call["argv"][:2] in (["pr", "create"], ["pr", "edit"], ["pr", "ready"])]
        readback = {}
        for call in calls[max(writes, default=len(calls)) + 1:]:
            if call["exit_code"] != 0 or call["argv"][:2] != ["pr", "view"]:
                continue
            try:
                returned = json.loads(call["stdout"])
            except ValueError:
                continue
            if isinstance(returned, dict):
                readback.update(returned)
        ok = bool(state) and all(key in readback and readback[key] == state.get(key) for key in assertion["fields"])
        ok &= all(state.get(key) == value for key, value in assertion.get("values", {}).items())
    else:
        raise ValueError("Unknown gh operation: " + op)
    return result(identifier, "pass" if ok else "fail")


def load_json(path, default=None):
    return json.loads(Path(path).read_text()) if Path(path).exists() else default


def collect_sources(repo):
    repo = Path(repo)
    paths = [path for name in SKILLS if name != "humanizer" for path in (repo / name).rglob("*.md")]
    paths += list((repo / "references").glob("*.md")) + [repo / "external/humanizer/SKILL.md"]
    return {path.relative_to(repo).as_posix(): {"text": path.read_text(), "realpath": str(path.resolve())} for path in paths if path.is_file()}


def score(case, transcript, sources, before=None, after=None, calls=None, state=None, execution=None, metadata=None):
    expected = case["expected"]
    reads = read_evidence(transcript, sources)
    selection = selection_results(expected["selection"], transcript, reads)
    references = [reference_result(assertion, reads, transcript.complete and not transcript.delegated) for assertion in expected["references"]]
    functional = [state_result(assertion, before, after, metadata) for assertion in expected["file_state"]]
    complete = transcript.complete and (execution is None or execution.get("status") == "completed")
    functional += [gh_result(assertion, calls, state, complete) for assertion in expected["gh_calls"]]
    for check in case.get("checks", []):
        observed = (after or {}).get("checks", {}).get(check["id"])
        status = "unknown" if observed is None or observed.get("exit_code") is None else "pass" if observed["exit_code"] == 0 else "fail"
        functional.append(result("check:" + check["id"], status, "runner-executed fixture check"))
    functional += [result(assertion["id"], "unknown", "manual: " + assertion["criterion"]) for assertion in expected["transcript"]]
    if execution is not None and execution.get("status") != "completed":
        functional.append(result("execution", "unknown", str(execution)))
    if not transcript.complete:
        functional.append(result("capture", "unknown", "missing/unsupported events, unmatched tool result, or non-JSON output"))
    axes = dict(selection=selection, references=dict(status=rollup(references), assertions=references),
                functional=dict(status=rollup(functional), assertions=functional))
    installation = (metadata or {}).get("installation_check", {})
    mismatch = installation.get("status") == "install_mismatch"
    return dict(case=case["id"], status="install_mismatch" if mismatch else rollup([result(axis, value["status"]) for axis, value in axes.items()]),
                regression_eligible=not mismatch and ((metadata or {}).get("host") != "codex" or installation.get("status") == "match"),
                installation_check=installation,
                axes=axes, reads=reads, observed_models=sorted(transcript.models) or ["unknown"],
                capture=dict(complete=transcript.complete, malformed_lines=transcript.malformed,
                             unsupported_items=sorted(transcript.unsupported_items),
                             delegated=transcript.delegated, scope="parent transcript; child internal tools may be absent"))


def self_check():
    dispatch_self_check()
    sources = {"references/prose-editing.md": {"text": "# Shared prose\nOne\nTwo\nThree\nFour\nFive"}}
    failed = Call("failed", "Bash", {"command": "cat wrong/references/prose-editing.md; true"}, 0,
                  "wrong/references/prose-editing.md: No such file or directory", False, True, 1, 0)
    blocked = Call("blocked", "Read", {"file_path": "references/prose-editing.md"}, 2,
                   "Approval required", True, True, 3)
    partial = Call("partial", "Read", {"file_path": "references/prose-editing.md", "limit": 3}, 4,
                   "1\t# Shared prose\n2\tOne\n3\tTwo", False, True, 5)
    reads = read_evidence(Transcript(calls=[failed, blocked, partial], terminal=True), sources)
    assert [read["status"] for read in reads] == ["failed", "blocked", "partial"], reads
    assert reference_result({"path": "references/prose-editing.md"}, reads[-1:], True)["status"] == "fail"
    key = "code-wright/SKILL.md"
    body = (HERE.parent / key).read_text()
    assert BLOCKED.search(body), "Regression needs approval/permission words in the source"
    compound = Call("compound", "command_execution", {"command": "cat /skills/code-wright/SKILL.md && python -m pytest"}, 0,
                    body + "\n/bin/zsh: command not found: python", True, True, 1, 127)
    transcript = Transcript(calls=[compound], terminal=True)
    reads = read_evidence(transcript, {key: {"text": body}})
    assert reads and all(read["status"] == "full" for read in reads), reads
    assert selection_results({"required": ["code-wright"]}, transcript, reads)["status"] == "pass"

    # Unnumbered final chunks can be shorter than the general matching threshold.
    lines = body.splitlines()
    for commands in (("sed -n '1,80p'", "sed -n '81,160p'"),
                     ("head -n 80", "tail -n +81"),
                     ("head -80", f"tail -{len(lines) - 80}"),
                     ("cat", "cat")):
        calls = [Call(str(index), "Bash", {"command": command + " " + key}, index * 2,
                      "\n".join(chunk), False, True, index * 2 + 1)
                 for index, (command, chunk) in enumerate(zip(commands, (lines[:80], lines[80:])))]
        transcript = Transcript(calls=calls, terminal=True)
        reads = read_evidence(transcript, {key: {"text": body}})
        assert [read["status"] for read in reads] == ["partial", "partial"], (commands, reads)
        assert reference_result({"path": key}, reads, True)["status"] == "pass", (commands, reads)
        assert selection_results({"required": ["code-wright"]}, transcript, reads)["status"] == "pass"
        if commands[1] != "cat":
            isolated = read_evidence(Transcript(calls=calls[-1:]), {key: {"text": body}})
            assert isolated[0]["ranges"] == [[81, len(lines)]], (commands, isolated)
    generic_source = "# Heading\n\nFirst detail\nSecond detail\nThird detail"
    for output in ("\n", "# Heading", "\n# Heading\n", "Second detail"):
        call = Call("generic", "Bash", {"command": "cat " + key}, 0, output, False, True, 1)
        assert not read_evidence(Transcript(calls=[call]), {key: {"text": generic_source}})[0]["ranges"]
    wrong_range = Call("wrong-range", "Bash", {"command": "sed -n '4,5p' " + key}, 0,
                       "First detail\nSecond detail", False, True, 1)
    assert not read_evidence(Transcript(calls=[wrong_range]), {key: {"text": generic_source}})[0]["ranges"]
    blank_range = Call("blank-range", "Bash", {"command": "sed -n '2p' " + key}, 0, "\n", False, True, 1)
    assert not read_evidence(Transcript(calls=[blank_range]), {key: {"text": generic_source}})[0]["ranges"]
    for command, output, expected_range in (("head -n 2", "# Heading\n", [[1, 2]]),
                                             ("tail -n 1", "Third detail", [[5, 5]]),
                                             ("sed -n '4,5p'", "Second detail\nThird detail", [[4, 5]])):
        call = Call("short-range", "Bash", {"command": command + " " + key}, 0, output, False, True, 1)
        assert read_evidence(Transcript(calls=[call]), {key: {"text": generic_source}})[0]["ranges"] == expected_range
    assert coverage("# Heading", generic_source, previous={2})[0] == []

    # Definitive unsuccessful reads prove non-selection only in complete parent captures.
    selection_expected = {"required": ["code-wright"], "forbidden": ["code-wright"]}
    for kind, call in (
        ("partial", Call("partial", "Read", {"file_path": key, "limit": 3}, 0,
                         "\n".join(body.splitlines()[:3]), False, True, 1)),
        ("failed", Call("failed", "Read", {"file_path": key}, 0, key + ": No such file", True, True, 1)),
        ("blocked", Call("blocked", "Read", {"file_path": key}, 0, "Permission denied", True, True, 1)),
        ("missing", Call("missing", "Read", {"file_path": key}, 0)),
    ):
        for terminal, delegated in ((True, False), (False, False), (True, True)):
            transcript = Transcript(calls=[call], terminal=terminal, delegated=delegated)
            reads = read_evidence(transcript, {key: {"text": body}})
            assertions = selection_results(selection_expected, transcript, reads)["assertions"]
            expected_statuses = ["fail", "pass"] if kind in ("partial", "failed") and terminal and not delegated else ["unknown", "unknown"]
            assert [item["status"] for item in assertions] == expected_statuses, (kind, assertions)

    # Readback fields may be distributed across views after the final successful write.
    state = dict(title="Fix addition", body="Restore the sum.", isDraft=True, labels=[{"name": "bug"}])
    assertion = dict(op="readback", fields=list(state), values={"isDraft": True})
    write = dict(argv=["pr", "edit"], exit_code=0, stdout="")

    def view(fields, exit_code=0):
        return dict(argv=["pr", "view"], exit_code=exit_code, stdout=json.dumps(fields))

    first = view({key: state[key] for key in ("title", "body")})
    second = view({key: state[key] for key in ("isDraft", "labels")})
    assert gh_result(assertion, [write, first, second], state)["status"] == "pass"
    for calls in ([write, first], [first, write, second], [write, first, write, second],
                  [write, first, view({"isDraft": True, "labels": []})],
                  [write, first, view(state, 1)], [first, second]):
        assert gh_result(assertion, calls, state)["status"] == "fail", calls
    assert gh_result(assertion, [write, first, dict(argv=["pr", "edit"], exit_code=1), second], state)["status"] == "pass"
    assert gh_result(assertion, [write, view(state), view({"title": "stale"})], state)["status"] == "fail"
    assert gh_result(dict(assertion, values={"isDraft": False}), [write, first, second], state)["status"] == "fail"
    print("self-check: linked skill injection, install exclusion, read coverage, selection certainty, and merged PR readback regressions passed")


def dispatch_self_check():
    # Synthetic stream-json envelopes mirror Skill launch and body injection.
    # The source is deliberately tiny and independent of the upstream text.
    with tempfile.TemporaryDirectory(prefix="skills-dispatch-") as directory:
        root = Path(directory)
        pinned = root / "external/humanizer"
        pinned.mkdir(parents=True)
        alias = root / "humanizer-link"
        alias.symlink_to(pinned, target_is_directory=True)
        text = "---\nname: humanizer\ndescription: Synthetic editor\n---\n\n# Editor\n\nKeep conditions.\nKeep negation.\n"
        key = "external/humanizer/SKILL.md"
        sources = {key: dict(text=text, realpath=str(pinned / "SKILL.md"))}
        body = skill_body(text)
        path = root / "transcript.jsonl"

        def events(base=alias, injected=body, error=False, output="Launching skill: humanizer", success=True, name="humanizer", args=None):
            inputs = dict(skill=name)
            if args is not None:
                inputs["args"] = args
            return [
                dict(type="assistant", message=dict(role="assistant", content=[
                    dict(type="tool_use", id="dispatch-1", name="Skill", input=inputs)])),
                dict(type="user", message=dict(role="user", content=[
                    dict(type="tool_result", tool_use_id="dispatch-1", content=output, is_error=error)]),
                     tool_use_result=dict(success=success, commandName=name)),
                dict(type="user", message=dict(role="user", content=[
                    dict(type="text", text=f"Base directory for this skill: {base}\n\n{injected}")]), isSynthetic=True),
            ]

        args = "Load the guidance only.\nPreserve the caller's output."
        suffix = "\n\n\nARGUMENTS: " + args
        variants = [
            ("success", events(), True),
            ("matching arguments", events(injected=body + suffix, args=args), True),
            ("arguments without appended block", events(args=args), True),
            ("empty arguments", events(injected=body + "\n\n\nARGUMENTS: ", args=""), True),
            ("mismatched arguments", events(injected=body + suffix, args="Different request"), False),
            ("missing input arguments", events(injected=body + suffix), False),
            ("arguments whitespace differs", events(injected=body + suffix, args=args + " "), False),
            ("repeated arguments block", events(injected=body + suffix + suffix, args=args), False),
            ("nontrailing arguments block", events(injected=body + suffix + "\nExtra text", args=args), False),
            ("different arguments separator", events(injected=body + "\n\nARGUMENTS: " + args, args=args), False),
            ("partial body with arguments", events(injected="# Editor" + suffix, args=args), False),
            ("other path", events(base=root / "other/humanizer"), False),
            ("body mismatch", events(injected=body.replace("negation", "assertions")), False),
            ("partial body", events(injected="# Editor\n\nKeep conditions."), False),
            ("frontmatter included", events(injected=text), False),
            ("failed dispatch", events(error=True, success=False, output="Skill failed"), False),
            ("blocked dispatch", events(error=True, success=False, output="Permission denied"), False),
            ("failure metadata", events(success=False), False),
            ("namespace differs", events(name="plugin:humanizer", output="Launching skill: plugin:humanizer"), False),
        ]
        unlinked = events()
        unlinked.insert(2, dict(type="assistant", message=dict(role="assistant", content=[dict(type="text", text="Unrelated turn")])))
        variants.append(("unrelated body elsewhere", unlinked, False))
        variants.append(("body without dispatch", events()[2:], False))
        ordinary = events()
        ordinary[2].pop("isSynthetic")
        variants.append(("ordinary user body", ordinary, False))
        for label, fixture, loaded in variants:
            fixture.append(dict(type="result", subtype="success", result="Synthetic artifact"))
            path.write_text("\n".join(json.dumps(event) for event in fixture) + "\n")
            transcript = parse_transcript(path, "claude")
            reads = read_evidence(transcript, sources)
            assertion = dict(path=key, coverage="full")
            assert (reference_result(assertion, reads, transcript.complete)["status"] == "pass") == loaded, (label, reads)
            if loaded:
                assert reads[0]["call_id"] == "dispatch-1" and reads[0]["load_source"] == "skill_dispatch", reads
                assert reference_result(dict(assertion, load_source="file_read"), reads, True)["status"] == "fail"
                fallback = Call("fallback", "Read", dict(file_path=key), 4, text, False, True, 5)
                transcript.calls.append(fallback)
                assert reference_result(dict(assertion, load_source="file_read"), read_evidence(transcript, sources), True)["status"] == "pass"
        case = dict(id="synthetic", expected=dict(selection={}, references=[], file_state=[], gh_calls=[], transcript=[]))
        for status, eligible in (("match", True), ("install_mismatch", False), ("unknown", False)):
            report = score(case, Transcript(terminal=True), {}, metadata=dict(host="codex", installation_check=dict(status=status)))
            assert report["regression_eligible"] == eligible, report
            if status == "install_mismatch":
                assert report["status"] == "install_mismatch", report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", nargs="?", type=Path)
    parser.add_argument("--legacy", type=Path)
    parser.add_argument("--host", choices=("claude", "codex"))
    parser.add_argument("--case")
    parser.add_argument("--cases", type=Path, default=HERE / "cases.json")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        return
    if bool(args.run) == bool(args.legacy):
        parser.error("Supply a run directory OR --legacy transcript --host host --case id")
    metadata = load_json(args.run / "metadata.json", {}) if args.run else {}
    case_id = args.case or metadata.get("case")
    host = args.host or metadata.get("host")
    if not case_id or not host:
        parser.error("Host and case are required")
    definitions = load_json(args.run / "cases.json" if args.run else args.cases)
    if definitions.get("schema_version") != 1:
        parser.error("Unsupported schema version")
    case = next((case for case in definitions["cases"] if case["id"] == case_id), None)
    if case is None:
        parser.error("Unknown case: " + case_id)
    if host not in case["hosts"]:
        axes = {name: dict(status="not_applicable", assertions=[]) for name in ("selection", "references", "functional")}
        print(json.dumps(dict(case=case_id, status="not_applicable", axes=axes, detail="Host is outside this case's declared scope")))
        return
    transcript = parse_transcript(args.legacy or args.run / "transcript.jsonl", host)
    if args.run:
        sources = load_json(args.run / "sources.json", {})
        before, after = (load_json(args.run / (name + ".json")) for name in ("before", "after"))
        log = args.run / "gh-calls.jsonl"
        calls = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else None
        report = score(case, transcript, sources, before, after, calls, load_json(args.run / "gh-state.json"), load_json(args.run / "execution.json", {}), metadata)
    else:
        report = score(case, transcript, collect_sources(HERE.parent), metadata=dict(host=host))
        report["legacy_limits"] = "Current checkout text is a comparison aid, not proof of the historical source revision. Fixture state, child traces and run settings may be missing."
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, KeyError) as exc:
        sys.exit("score: " + str(exc))
