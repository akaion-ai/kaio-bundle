#!/bin/sh
# Installa la skill «kaio-bundle» in Claude Code senza il sistema dei plugin.
#   curl -fsSL https://raw.githubusercontent.com/akaion-ai/kaio-bundle/main/install.sh | sh            # per tutti i progetti (~/.claude/skills)
#   curl -fsSL https://raw.githubusercontent.com/akaion-ai/kaio-bundle/main/install.sh | sh -s -- --project   # solo in questo progetto (.claude/skills)
set -eu
REPO="https://github.com/akaion-ai/kaio-bundle.git"
if [ "${1:-}" = "--project" ]; then DEST=".claude/skills/kaio-bundle"; else DEST="$HOME/.claude/skills/kaio-bundle"; fi
TMP="$(mktemp -d)"
git clone --quiet --depth 1 "$REPO" "$TMP/kaio-bundle"
mkdir -p "$DEST"
cp -R "$TMP/kaio-bundle/skills/kaio-bundle/." "$DEST/"
# la skill lancia bundle_install.py e il kit legale dalla stessa cartella
cp "$TMP/kaio-bundle/bundle_install.py" "$DEST/"
cp -R "$TMP/kaio-bundle/legal" "$DEST/"
rm -rf "$TMP"
echo "Skill installata in $DEST. In Claude Code: /kaio-bundle (se non compare, /reload-skills)."
echo "MCP Akaion: claude mcp add --transport http akaion https://api.website.prod.akaion.com/mcp  poi /mcp per entrare."
