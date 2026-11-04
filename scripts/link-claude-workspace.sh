#!/usr/bin/env bash
# Link this repository's skills into Claude Code for specific workspaces only.
#
# Usage: link-claude-workspace.sh [--dry-run] [--pr-rule] <workspace-dir>...
#
# Claude Code does not read a parent folder's .claude/skills from inside a
# child Git repository, so each workspace folder and every Git repository or
# worktree under it gets its own links. Links are added to that repository's
# .git/info/exclude so they stay out of version control. Existing entries are
# left untouched; rerun after adding a repository or worktree.
set -euo pipefail

repo=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
dry_run=false
pr_rule=false
workspaces=()
for arg in "$@"; do
  case "$arg" in
    --dry-run) dry_run=true ;;
    --pr-rule) pr_rule=true ;;
    -h|--help) sed -n '2,10p' "$0"; exit 0 ;;
    -*) echo "Unknown option: $arg" >&2; exit 2 ;;
    *) workspaces+=("$arg") ;;
  esac
done
[[ ${#workspaces[@]} -gt 0 ]] || { echo "Usage: $0 [--dry-run] [--pr-rule] <workspace-dir>..." >&2; exit 2; }

# Skill name -> source directory: every top-level skill plus the pinned Humanizer.
names=()
sources=()
for skill in "$repo"/*/SKILL.md; do
  dir=$(dirname "$skill")
  names+=("$(basename "$dir")")
  sources+=("$dir")
done
if [[ -f "$repo/external/humanizer/SKILL.md" ]]; then
  names+=(humanizer)
  sources+=("$repo/external/humanizer")
fi

marker="# yon-skills personal links (local only)"
rule='When writing or revising a pull request title or body, invoke the `humanizer` skill before drafting and apply it in embedded mode to the final text.'

run() {
  if $dry_run; then echo "  would: $*"; else "$@"; fi
}

link_skills() {
  local target=$1 i link
  run mkdir -p "$target/.claude/skills"
  for i in "${!names[@]}"; do
    link="$target/.claude/skills/${names[$i]}"
    if [[ -L "$link" || -e "$link" ]]; then
      if [[ "$(cd "$link" 2>/dev/null && pwd -P)" != "$(cd "${sources[$i]}" && pwd -P)" ]]; then
        echo "  keep existing ${names[$i]} (points elsewhere): $link"
      fi
    else
      run ln -s "${sources[$i]}" "$link"
      $dry_run || echo "  linked ${names[$i]}"
    fi
  done
}

exclude_links() {
  # Register links relative to the repository that contains the target, so a
  # workspace inside a repository subfolder stays out of version control too.
  local target=$1 top rel prefix exclude name
  top=$(git -C "$target" rev-parse --show-toplevel)
  rel=${target#"$top"}
  rel=${rel#/}
  prefix="/${rel:+$rel/}.claude/skills"
  exclude=$(git -C "$target" rev-parse --path-format=absolute --git-path info/exclude)
  [[ -f "$exclude" ]] || run mkdir -p "$(dirname "$exclude")"
  grep -qxF "$marker" "$exclude" 2>/dev/null || { $dry_run && echo "  would add exclude block to $exclude" || printf '\n%s\n' "$marker" >> "$exclude"; }
  for name in "${names[@]}"; do
    grep -qxF "$prefix/$name" "$exclude" 2>/dev/null || { $dry_run && echo "  would exclude $prefix/$name" || echo "$prefix/$name" >> "$exclude"; }
  done
}

for workspace in "${workspaces[@]}"; do
  workspace=$(cd -- "$workspace" && pwd -P)
  echo "== $workspace"
  targets=("$workspace")
  while IFS= read -r git_entry; do
    targets+=("$(dirname "$git_entry")")
  done < <(find "$workspace" -maxdepth 5 -name node_modules -prune -o -name .git -print 2>/dev/null | sort)
  for target in "${targets[@]}"; do
    echo "- $target"
    link_skills "$target"
    if git -C "$target" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
      exclude_links "$target"
    fi
  done
  if $pr_rule; then
    rule_file="$workspace/.claude/CLAUDE.md"
    if grep -qF "$rule" "$rule_file" 2>/dev/null; then
      echo "- PR rule already present: $rule_file"
    elif $dry_run; then
      echo "  would append PR rule to $rule_file"
    else
      mkdir -p "$workspace/.claude"
      printf '\n%s\n' "$rule" >> "$rule_file"
      echo "- appended PR rule: $rule_file"
    fi
  fi
done
