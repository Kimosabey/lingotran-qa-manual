#!/usr/bin/env bash
# Concatenate ordered source fragments into the single-file manual.
# Fragment 01 carries <head> and opens <body>; fragment 06 closes them.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/dist/lingotran-qa-field-manual.html"

mkdir -p "$ROOT/dist"

shopt -s nullglob
PARTS=("$ROOT"/src/*.html)
if [ ${#PARTS[@]} -eq 0 ]; then
  echo "error: no fragments found in src/" >&2
  exit 1
fi

: > "$OUT"
for f in "${PARTS[@]}"; do
  printf '%s\n' "$(cat "$f")" >> "$OUT"
done

echo "built  $OUT"
echo "parts  ${#PARTS[@]}"
echo "bytes  $(wc -c < "$OUT" | tr -d ' ')"
