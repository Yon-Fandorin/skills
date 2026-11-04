#!/usr/bin/env bash
# Usage: fixtures.sh <base|agents|bug|dual-profile|incomplete|pr|pr-open|finish> <new-directory>
set -euo pipefail
eval_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
fixture_kind=${1:?fixture kind required}
fixture_dir=${2:?new directory required}
case "$fixture_kind" in
  base|agents|bug|dual-profile|incomplete|pr|pr-open|finish) ;;
  *) echo "Unknown fixture: $fixture_kind" >&2; exit 2 ;;
esac
python3 - "$fixture_dir" "$eval_dir/.." <<'PY'
import pathlib, sys
requested = pathlib.Path(sys.argv[1])
if requested.exists() or requested.is_symlink():
    sys.exit("Fixture directory already exists")
target, repo = (pathlib.Path(p).resolve() for p in sys.argv[1:])
if target == repo or repo in target.parents:
    sys.exit("Fixture must be outside the skills checkout")
target.parent.mkdir(parents=True, exist_ok=True)
target.mkdir()  # Refuse existing directories, including empty ones.
PY
cd -- "$fixture_dir"
# Do not inherit signing, hooks, templates, or an outer repository.
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_COMMON_DIR
export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null
git init -q --initial-branch=main --template=
git config user.name 'Eval Author'
git config user.email 'eval@example.invalid'
git config core.hooksPath /dev/null
git config commit.gpgsign false
mkdir -p src tests
cat > .gitignore <<'EOF'
__pycache__/
.remote.git/
.worktrees/
.claude/
.env
EOF
cat > AGENTS.md <<'EOF'
# Agent instructions

Keep arithmetic helpers pure. Preserve their public functions.
Run `python3 -m unittest discover -s tests` for code changes.
PR descriptions use Korean. The comparison base for this task is `main`.
EOF
cat > README.md <<'EOF'
# Calc

Arithmetic helpers and invoice rendering for a batch billing job.
`src/calc.py` owns arithmetic; `src/billing.py` builds invoice text.

Run `python3 -m unittest discover -s tests`. Tests inject the tax rate.
EOF
cat > src/calc.py <<'EOF'
def add(a, b):
    return a + b


def multiply(a, b):
    return a * b
EOF
cat > src/billing.py <<'EOF'
import json
import sys
import urllib.request

from src.calc import add, multiply


def fetch_tax_rate(region):
    url = "https://tax.example.invalid/rates?region=" + region
    with urllib.request.urlopen(url) as response:
        return json.load(response)["rate"]


def build_invoice(items, region, fetch_rate=fetch_tax_rate):
    subtotal = sum(multiply(item["price"], item["quantity"]) for item in items)
    tax = int(subtotal * fetch_rate(region))
    lines = [f"{item['name']} x{item['quantity']}" for item in items]
    lines.extend([f"subtotal: {subtotal}", f"tax: {tax}", f"total: {add(subtotal, tax)}"])
    return "\n".join(lines)


def main(argv):
    with open(argv[1]) as handle:
        order = json.load(handle)
    print(build_invoice(order["items"], order["region"]))


if __name__ == "__main__":
    main(sys.argv)
EOF
touch src/__init__.py tests/__init__.py
cat > tests/test_calc.py <<'EOF'
import unittest
from src.calc import add, multiply


class ArithmeticTests(unittest.TestCase):
    def test_add(self):
        for a, b in [(2, 3), (-2, 3), (0, 0), (3, -7)]:
            self.assertEqual(add(a, b), a + b)

    def test_multiply(self):
        self.assertEqual(multiply(3, 4), 12)
        self.assertEqual(multiply(-2, 3), -6)
EOF
cat > tests/test_billing.py <<'EOF'
import unittest
from src.billing import build_invoice


class BillingTests(unittest.TestCase):
    def test_invoice(self):
        items = [{"name": "tea", "price": 100, "quantity": 2}]
        result = build_invoice(items, "test", fetch_rate=lambda _: 0.1)
        self.assertEqual(result, "tea x2\nsubtotal: 200\ntax: 20\ntotal: 220")
EOF
if [[ $fixture_kind == agents ]]; then
  cat >> AGENTS.md <<'EOF'

Always write good code. Be careful. Read files before editing them.
Arithmetic helpers must be pure. Do not add side effects to calc helpers.
Run the tests. Run `python3 -m unittest discover -s tests` when editing code.
EOF
fi
if [[ $fixture_kind == dual-profile ]]; then
  printf 'version = 1\n' > .dualagent.toml
fi
if [[ $fixture_kind == bug || $fixture_kind == dual-profile || $fixture_kind == pr || $fixture_kind == pr-open ]]; then
  python3 -c 'from pathlib import Path; p=Path("src/calc.py"); p.write_text(p.read_text().replace("return a + b", "return a - b"))'
elif [[ $fixture_kind == incomplete ]]; then
  python3 -c 'from pathlib import Path; p=Path("src/calc.py"); p.write_text(p.read_text().replace("return a + b", "raise NotImplementedError"))'
fi
git add .
git commit -qm 'Add arithmetic and billing helpers'
if [[ $fixture_kind == pr || $fixture_kind == pr-open ]]; then
  git checkout -qb fix/add
  python3 -c 'from pathlib import Path; p=Path("src/calc.py"); p.write_text(p.read_text().replace("return a - b", "return a + b"))'
  git add src/calc.py
  git commit -qm 'Fix addition'
elif [[ $fixture_kind == finish ]]; then
  mkdir -p docs
  cat > docs/progress.md <<'EOF'
# 작업 현황

## multiply 문서
- 상태: 진행 중
- PR: 생성 전
- 임시 PR 본문: `tmp/pr-body.md`에 보관 중
EOF
  git add docs/progress.md
  git commit -qm 'Track multiply documentation'
  git checkout -qb feature/multiply-docs
  printf '# multiply\n\n`multiply(a, b)` returns the product of `a` and `b`.\n' > docs/multiply.md
  git add docs/multiply.md
  git commit -qm 'Document multiply'
  git checkout -q main
  git merge --squash feature/multiply-docs >/dev/null
  git commit -qm 'Document multiply (#12)'
  git branch feature/experiment
  git checkout -q feature/experiment
  printf 'Unmerged user experiment\n' > docs/experiment.md
  git add docs/experiment.md
  git commit -qm 'Try an alternative documentation layout'
  git checkout -q main
  mkdir -p .worktrees tmp scratch notes
  git worktree add -q .worktrees/multiply-docs feature/multiply-docs
  printf 'Draft PR body\n' > tmp/pr-body.md
  printf '{"debug": true}\n' > scratch/debug_output.json
  printf 'User notes: preserve this file.\n' > notes/user-ideas.md
  printf 'EVAL_SECRET=synthetic-do-not-delete\n' > .env
  python3 - <<'PY'
import json, subprocess
def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()
state = dict(number=12, url="https://github.example.invalid/eval/calc/pull/12",
             state="MERGED", title="Document multiply", body="Document multiply.",
             isDraft=False, baseRefName="main", headRefName="feature/multiply-docs",
             labels=[{"name": "documentation"}], mergeCommit={"oid": git("rev-parse", "HEAD")},
             files=[{"path": "docs/multiply.md"}],
             commits=[{"oid": git("rev-parse", "feature/multiply-docs")}],
             diff=git("diff", "HEAD^", "HEAD", "--", "docs/multiply.md"))
with open(".git/eval-pr.json", "w") as handle:
    json.dump(state, handle)
PY
fi
git init -q --bare --initial-branch=main --template= .remote.git
git remote add origin "$PWD/.remote.git"
git push -q origin main
git branch --set-upstream-to=origin/main main >/dev/null
if [[ $fixture_kind == pr-open ]]; then
  git push -qu origin fix/add
  python3 - <<'PY'
import json, subprocess
def git(*args):
    return subprocess.check_output(["git", *args], text=True)
base_oid = git("rev-parse", "main^{commit}").strip()
head_oid = git("rev-parse", "fix/add^{commit}").strip()
paths = git("diff", "--name-only", "-z", base_oid + "..." + head_oid, "--").split("\0")
commits = git("rev-list", base_oid + ".." + head_oid, "--").splitlines()
state = dict(number=7, url="https://github.example.invalid/eval/calc/pull/7",
             state="OPEN", title="덧셈 버그 수정",
             body="## 변경 사항\n\n음수 입력을 별도로 처리하는 로직을 추가했습니다.\n\n"
                  "## 검증\n\n뺄셈 테스트를 추가하고 전체 테스트 통과를 확인했습니다.\n",
             isDraft=True, baseRefName="main", headRefName="fix/add",
             labels=[{"name": "bug"}], files=[{"path": path} for path in paths if path],
             commits=[{"oid": oid} for oid in commits], headRefOid=head_oid,
             diff=git("diff", base_oid + "..." + head_oid, "--"))
with open(".git/eval-pr.json", "w") as handle:
    json.dump(state, handle, ensure_ascii=False)
PY
fi
printf '%s\n' "$PWD"
