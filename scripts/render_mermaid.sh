#!/usr/bin/env bash
# Regression check: every Mermaid block in docs/ must render with mmdc.
set -euo pipefail
shopt -s nullglob
out=$(mktemp -d)
trap 'rm -rf "$out"' EXIT
printf '{"args":["--no-sandbox","--disable-gpu"]}' > "$out/puppeteer.json"
count=0
while IFS= read -r file; do
  python3 - "$file" "$out" <<'PY'
import pathlib, re, sys
src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
for i, block in enumerate(re.findall(r"```mermaid\n(.*?)```", src.read_text(), re.S), 1):
    (out / f"{src.stem}-{i}.mmd").write_text(block)
PY
done < <(grep -rl '```mermaid' docs || true)
for mmd in "$out"/*.mmd; do
  PUPPETEER_EXECUTABLE_PATH="${PUPPETEER_EXECUTABLE_PATH:-$(command -v google-chrome)}" \
    mmdc -q -p "$out/puppeteer.json" -i "$mmd" -o "${mmd%.mmd}.svg" \
    || { echo "render failed: $(basename "$mmd")"; exit 1; }
  count=$((count + 1))
done
echo "render_mermaid: $count diagram(s) rendered"
