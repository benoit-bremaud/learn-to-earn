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
    def check(self, text):
        return check_docs.check_matrices("a.md", text)

    def test_correct_matrix_passes(self):
        self.assertEqual(self.check(GOOD), [])

    def test_wrong_total_is_reported(self):
        self.assertEqual(self.check(GOOD.replace("340", "345")), ["a.md:5: totals [345, 280], computed [340, 280]"])

    def test_bold_total_is_checked(self):
        self.assertEqual(self.check(GOOD.replace("| 340 |", "| **345** |")), ["a.md:5: totals [345, 280], computed [340, 280]"])

    def test_weights_not_summing_to_100_are_reported(self):
        text = GOOD.replace("(40)", "(30)").replace("| 340 | 280 |", "| 330 | 240 |")
        self.assertEqual(self.check(text), ["a.md:5: weights sum to 90, not 100"])

    def test_justified_cells_percent_weights_and_inner_parentheses(self):
        text = GOOD.replace("Cost (60) | 5 | 2", "Cost (money) (60 %) | 5 : cheap | **2** : dear")
        self.assertEqual(self.check(text), [])

    def test_unparsable_matrix_is_an_error(self):
        text = GOOD.replace("| 5 | 2 |", "| high | low |").replace("| 1 | 4 |", "| low | high |")
        self.assertEqual(self.check(text), ["a.md:5: total row without a parsable matrix"])

    def test_ragged_table_is_an_error(self):
        self.assertEqual(self.check(GOOD.replace("| 340 | 280 |", "| 340 |")), ["a.md:5: rows and total have different option counts"])

    def test_text_between_tables_resets_rows(self):
        self.assertEqual(self.check("| Old (50) | 1 | 1 |\n\nprose\n" + GOOD), [])


class LinkAndTreeTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.dir.name)
        (self.root / "my target.md").write_text("ok", encoding="utf-8")

    def tearDown(self):
        self.dir.cleanup()

    def links(self, text):
        return check_docs.check_links(self.root / "doc.md", text, self.root)

    def test_valid_links_pass(self):
        text = "[a](my%20target.md#part) [b](https://x.org) [c](mailto:x@y.z) [d](#top) [e](/my%20target.md) ![i](//cdn/x.png)"
        self.assertEqual(self.links(text), [])

    def test_links_in_code_are_ignored(self):
        self.assertEqual(self.links("`[a](nope.md)`\n```\n[b](nope.md)\n```"), [])

    def test_broken_link_is_reported(self):
        self.assertEqual(self.links("[a](missing.md)"), ["doc.md: broken link missing.md"])

    def test_tree_without_git_and_main_status(self):
        self.assertEqual(check_docs.main(self.root), 0)
        (self.root / "bad.md").write_text("[a](nope.md)", encoding="utf-8")
        self.assertEqual(check_docs.main(self.root), 1)

    def test_tree_uses_git_tracked_files(self):
        self.assertTrue(all(p.suffix == ".md" for p in check_docs.markdown_files(check_docs.ROOT)))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
