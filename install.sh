#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$HOME/.claude/skills"

# Skill directories to install (add new ones here)
SKILLS=(svelte5)

usage() {
  echo "Usage: $0 [install|uninstall]"
  echo ""
  echo "  install    Create symlinks in ~/.claude/skills/ for each agent"
  echo "  uninstall  Remove symlinks from ~/.claude/skills/"
  exit 1
}

install() {
  mkdir -p "$SKILLS_DIR"

  for skill in "${SKILLS[@]}"; do
    local src="$SCRIPT_DIR/$skill"
    local dest="$SKILLS_DIR/$skill"

    if [ ! -d "$src" ]; then
      echo "Warning: $src does not exist, skipping"
      continue
    fi

    if [ -L "$dest" ]; then
      local current_target
      current_target="$(readlink "$dest")"
      if [ "$current_target" = "$src" ]; then
        echo "Already linked: $skill"
        continue
      fi
      echo "Updating link: $skill (was -> $current_target)"
      rm "$dest"
    elif [ -e "$dest" ]; then
      echo "Error: $dest exists and is not a symlink. Remove it manually."
      continue
    fi

    ln -s "$src" "$dest"
    echo "Linked: $skill -> $dest"
  done

  echo ""
  echo "Done. Restart Claude Code to pick up the new skills."
}

uninstall() {
  for skill in "${SKILLS[@]}"; do
    local dest="$SKILLS_DIR/$skill"

    if [ -L "$dest" ]; then
      rm "$dest"
      echo "Removed: $skill"
    elif [ -e "$dest" ]; then
      echo "Skipping: $dest is not a symlink (not managed by this script)"
    else
      echo "Not found: $skill"
    fi
  done

  echo ""
  echo "Done. Restart Claude Code to apply changes."
}

case "${1:-}" in
  install)  install ;;
  uninstall) uninstall ;;
  *) usage ;;
esac
