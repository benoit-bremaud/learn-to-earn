"""Regression checks for the documentation: MCDA totals and internal links.

Every MCDA table must have weights summing to 100 and a "Total /500" row
equal to the weighted sum of its scores; a total row whose matrix could not
be parsed is an error, so no matrix is skipped silently. Every relative
Markdown link must point to an existing file. All errors are reported.
"""
import pathlib
import re
import subprocess
import sys
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
WEIGHT = re.compile(r"\((\d+)\s*%?\)")
SCORE = re.compile(r"\**(\d+)\b")
LINK = re.compile(r"\]\(([^)\s]+)")
CODE = re.compile(r"```.*?```|`[^`\n]*`", re.S)


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def parse_row(line):
    """Return (weight, scores) for a criterion row, or None."""
    if not line.startswith("|"):
        return None
    row = cells(line)
    weight = WEIGHT.search(row[0])
    scores = [SCORE.match(c) for c in row[1:]]
    if not weight or not scores or not all(scores):
        return None
    return int(weight.group(1)), [int(s.group(1)) for s in scores]


def check_total(where, line, rows):
    """Compare a "Total /500" row with the weighted sums of its matrix rows."""
    got = [int(m.group(1)) for m in (SCORE.match(c) for c in cells(line)[1:]) if m]
    if not rows:
        return [f"{where}: total row without a parsable matrix"]
    if any(len(s) != len(got) for _, s in rows):
        return [f"{where}: rows and total have different option counts"]
    errors = []
    weights = sum(w for w, _ in rows)
    want = [sum(w * s[i] for w, s in rows) for i in range(len(got))]
    if weights != 100:
        errors.append(f"{where}: weights sum to {weights}, not 100")
    if got != want:
        errors.append(f"{where}: totals {got}, computed {want}")
    return errors


def check_matrices(path, text):
    errors, rows = [], []
    for number, line in enumerate(text.splitlines(), 1):
        if "Total /500" in line:
            errors += check_total(f"{path}:{number}", line, rows)
            rows = []
        elif parse_row(line):
            rows.append(parse_row(line))
        elif not line.startswith("|"):
            rows = []
    return errors


def check_links(path, text, root):
    errors = []
    for target in LINK.findall(CODE.sub("", text)):
        target = urllib.parse.unquote(target.split("#")[0].split("?")[0])
        if not target or re.match(r"[a-z]+:|//", target):
            continue
        base = root if target.startswith("/") else path.parent
        if not (base / target.lstrip("/")).exists():
            errors.append(f"{path.relative_to(root)}: broken link {target}")
    return errors


def markdown_files(root):
    listed = subprocess.run(["git", "ls-files", "*.md"], cwd=root, capture_output=True, text=True)
    if listed.returncode == 0:
        return [root / name for name in listed.stdout.split()]
    return sorted(root.glob("**/*.md"))


def check_tree(root):
    errors = []
    for path in markdown_files(root):
        text = path.read_text(encoding="utf-8")
        errors += check_matrices(path.relative_to(root), text) + check_links(path, text, root)
    return errors


def main(root=ROOT):
    errors = check_tree(root)
    for error in errors:
        print(error)
    print(f"check_docs: {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
