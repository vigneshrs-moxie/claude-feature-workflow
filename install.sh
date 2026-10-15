#!/usr/bin/env bash
# Links this repo's skills and agents into ~/.claude so Claude Code picks them up,
# and clones (or updates) the git workflow docs the Foreman follows.
# Re-run any time; links point at this repo, so `git pull` here updates them at once.
# Anything already at a target that isn't a link to this repo is moved to
# ~/.claude/backups/claude-feature-workflow/ (outside skills/, so Claude Code won't load it twice).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="${CLAUDE_DIR:-$HOME/.claude}"
GIT_DOCS_DIR="${GIT_DOCS_DIR:-$HOME/Projects/moxie-portal-git-workflow}"
GIT_DOCS_REPO="https://github.com/vigneshrs-moxie/moxie-portal-git-workflow.git"
BACKUP_DIR="$CLAUDE_DIR/backups/claude-feature-workflow/$(date +%Y-%m-%d-%H%M%S)"
mkdir -p "$CLAUDE_DIR/skills" "$CLAUDE_DIR/agents"

link() {
  local src="$1" dst="$2"
  if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$src" ]; then echo "ok       $dst"; return; fi
  if [ -e "$dst" ] || [ -L "$dst" ]; then
    mkdir -p "$BACKUP_DIR/$(basename "$(dirname "$dst")")"
    mv "$dst" "$BACKUP_DIR/$(basename "$(dirname "$dst")")/"
    echo "backed up $dst -> $BACKUP_DIR/"
  fi
  ln -s "$src" "$dst"; echo "linked   $dst"
}

for d in "$HERE"/skills/*/; do link "${d%/}" "$CLAUDE_DIR/skills/$(basename "$d")"; done
for f in "$HERE"/agents/*.md; do link "$f" "$CLAUDE_DIR/agents/$(basename "$f")"; done

# The git workflow docs (branches, PR stages, releases) the Foreman reads first.
if [ -d "$GIT_DOCS_DIR/.git" ]; then
  git -C "$GIT_DOCS_DIR" pull --ff-only -q && echo "updated  $GIT_DOCS_DIR"
elif [ -e "$GIT_DOCS_DIR" ]; then
  echo "skipped  $GIT_DOCS_DIR exists but isn't a git clone. Rename it, then run this again."
else
  mkdir -p "$(dirname "$GIT_DOCS_DIR")"
  git clone -q "$GIT_DOCS_REPO" "$GIT_DOCS_DIR" && echo "cloned   $GIT_DOCS_DIR"
fi

echo "Done. Open Claude Code in your project and type /feature to start."
