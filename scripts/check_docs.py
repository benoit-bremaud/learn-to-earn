"""Regression checks for the documentation: MCDA totals and internal links.

Every MCDA table must have weights summing to 100 and totals equal to the
weighted sum of its scores; every relative Markdown link must point to an
existing file. Exits non-zero on the first kind of failure found.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ROW = re.compile(r"\|\s*(.+?)\((\d+)\)\s*\|((?:\s*\d\s*\|)+)\s*$")
LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")


def check_matrices(path, text):
    errors, rows = [], []
    for number, line in enumerate(text.splitlines(), 1):
        row = ROW.match(line)
        if row:
            rows.append((int(row.group(2)), [int(x) for x in row.group(3).split("|") if x.strip()]))
        elif "Total /500" in line and rows:
            got = [int(x) for x in re.findall(r"\d+", line.split("|", 2)[2])]
            want = [sum(w * s[i] for w, s in rows) for i in range(len(rows[0][1]))]
            weights = sum(w for w, _ in rows)
            if weights != 100:
                errors.append(f"{path}:{number}: weights sum to {weights}, not 100")
            if got != want:
                errors.append(f"{path}:{number}: totals {got}, computed {want}")
            rows = []
        elif not line.startswith("|"):
            rows = []
    return errors


def check_links(path, text):
    errors = []
    for target in LINK.findall(text):
        if re.match(r"[a-z]+:", target):
            continue
        if not (path.parent / target).exists():
            errors.append(f"{path}: broken link {target}")
    return errors


def main():
    errors = []
    for path in sorted(ROOT.glob("**/*.md")):
        if ".claude" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        errors += check_matrices(path.relative_to(ROOT), text) + check_links(path, text)
    for error in errors:
        print(error)
    print(f"check_docs: {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
