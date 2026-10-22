#!/usr/bin/env bash
# Regression check: every Mermaid block in docs/ must render with mmdc.
set -euo pipefail
command -v mmdc >/dev/null || { echo "mmdc is missing (npm i -g @mermaid-js/mermaid-cli)"; exit 1; }
chrome="${PUPPETEER_EXECUTABLE_PATH:-$(command -v google-chrome || true)}"
[ -n "$chrome" ] || { echo "Chrome is missing (set PUPPETEER_EXECUTABLE_PATH)"; exit 1; }
out=$(mktemp -d)
trap 'rm -rf "$out"' EXIT
# --no-sandbox: Chrome only renders local repository content here.
printf '{"args":["--no-sandbox","--disable-gpu"]}' > "$out/puppeteer.json"
python3 - "$out" <<'PY'
import pathlib, re, sys
out = pathlib.Path(sys.argv[1])
fence = re.compile(r"^[ \t]*```mermaid[ \t]*\r?\n(.*?)^[ \t]*```", re.M | re.S)
opening = re.compile(r"^[ \t]*```mermaid[ \t]*\r?$", re.M)
# A running number keeps names unique; the source path is kept for messages.
for n, src in enumerate(sorted(pathlib.Path("docs").glob("**/*.md"))):
    text = src.read_text(encoding="utf-8")
    blocks = fence.findall(text)
    # An unclosed fence yields no block: fail instead of rendering nothing.
    if len(blocks) != len(opening.findall(text)):
        sys.exit(f"render_mermaid: unclosed mermaid fence in {src}")
    for i, block in enumerate(blocks, 1):
        name = f"{n:04d}-{src.stem}-{i}"
        (out / f"{name}.mmd").write_text(block, encoding="utf-8")
        (out / f"{name}.src").write_text(f"{src} block {i}", encoding="utf-8")
PY
shopt -s nullglob
count=0
for mmd in "$out"/*.mmd; do
  PUPPETEER_EXECUTABLE_PATH="$chrome" mmdc -q -p "$out/puppeteer.json" -i "$mmd" -o "${mmd%.mmd}.svg" \
    || { echo "render failed: $(cat "${mmd%.mmd}.src")"; exit 1; }
  count=$((count + 1))
done
echo "render_mermaid: $count diagram(s) rendered"
