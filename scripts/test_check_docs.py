"""Unit tests for check_docs: MCDA totals, weights and internal links."""
import pathlib
import tempfile
import unittest

import check_docs

GOOD = """| Criterion (weight) | A | B |
|---|---|---|
| Cost (60) | 5 | 2 |
| Speed (40) | 1 | 4 |
| **Total /500** | 340 | 280 |
"""


class MatrixTest(unittest.TestCase):
    def test_correct_matrix_passes(self):
        self.assertEqual(check_docs.check_matrices("a.md", GOOD), [])

    def test_wrong_total_is_reported(self):
        errors = check_docs.check_matrices("a.md", GOOD.replace("340", "345"))
        self.assertEqual(errors, ["a.md:5: totals [345, 280], computed [340, 280]"])

    def test_weights_not_summing_to_100_are_reported(self):
        text = GOOD.replace("(40)", "(30)").replace("| 340 | 280 |", "| 330 | 240 |")
        self.assertEqual(check_docs.check_matrices("a.md", text), ["a.md:5: weights sum to 90, not 100"])

    def test_criterion_with_inner_parentheses_is_parsed(self):
        text = GOOD.replace("Cost (60)", "Cost (money) (60)")
        self.assertEqual(check_docs.check_matrices("a.md", text), [])

    def test_text_between_tables_resets_rows(self):
        text = "| Old (50) | 1 | 1 |\n\nprose\n" + GOOD
        self.assertEqual(check_docs.check_matrices("a.md", text), [])


class LinkAndTreeTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.dir.name)
        (self.root / "target.md").write_text("ok", encoding="utf-8")

    def tearDown(self):
        self.dir.cleanup()

    def test_existing_and_external_links_pass(self):
        text = "[a](target.md#part) [b](https://example.org) [c](mailto:x@y.z)"
        self.assertEqual(check_docs.check_links(self.root / "doc.md", text), [])

    def test_broken_link_is_reported(self):
        errors = check_docs.check_links(self.root / "doc.md", "[a](missing.md)")
        self.assertEqual(errors, [f"{self.root / 'doc.md'}: broken link missing.md"])

    def test_tree_skips_tool_folders_and_main_returns_status(self):
        (self.root / ".venv").mkdir()
        (self.root / ".venv" / "x.md").write_text("[a](nope.md)", encoding="utf-8")
        self.assertEqual(check_docs.main(self.root), 0)
        (self.root / "bad.md").write_text("[a](nope.md)", encoding="utf-8")
        self.assertEqual(check_docs.main(self.root), 1)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
