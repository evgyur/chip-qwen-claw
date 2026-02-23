#!/bin/bash
# Replace groq/qwen3-32b with groq/qwen/qwen3-32b so Groq API receives model id qwen/qwen3-32b
set -e
CONFIG="${1:-$HOME/.openclaw/openclaw.json}"
if [[ ! -f "$CONFIG" ]]; then
  echo "Config not found: $CONFIG"
  exit 1
fi
sed -i.bak \
  -e 's|"primary": "groq/qwen3-32b"|"primary": "groq/qwen/qwen3-32b"|g' \
  -e 's|"groq/qwen3-32b":|"groq/qwen/qwen3-32b":|g' \
  "$CONFIG"
echo "Patched $CONFIG"
grep -E '"primary"|groq/qwen' "$CONFIG" || true
