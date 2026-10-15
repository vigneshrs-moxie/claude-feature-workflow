#!/usr/bin/env bash
# Links this repo's skills and agents into ~/.claude so Claude Code picks them up.
# Re-run after `git pull`; links point at the repo, so updates apply at once.
# Anything already at the target that isn't a link to this repo is moved aside as <name>.bak.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="${CLAUDE_DIR:-$HOME/.claude}"
mkdir -p "$CLAUDE_DIR/skills" "$CLAUDE_DIR/agents"

link() {
  local src="$1" dst="$2"
  if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$src" ]; then echo "ok       $dst"; return; fi
  if [ -e "$dst" ] || [ -L "$dst" ]; then mv "$dst" "$dst.bak"; echo "moved    $dst -> $dst.bak"; fi
  ln -s "$src" "$dst"; echo "linked   $dst"
}

for d in "$HERE"/skills/*/; do link "${d%/}" "$CLAUDE_DIR/skills/$(basename "$d")"; done
for f in "$HERE"/agents/*.md; do link "$f" "$CLAUDE_DIR/agents/$(basename "$f")"; done
echo "Done. Open Claude Code and type /feature to start."
