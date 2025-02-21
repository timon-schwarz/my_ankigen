import unittest
from parser.ts_table_parser import TsTableParser
from parser.models import Flashcard
from parser.mask_generator import RowColumnMaskGenerator

class TestTsTableParser(unittest.TestCase):
    def setUp(self):
        # A sample markdown table with a header row and left header column.
        self.markdown_table = """
|       | EIGRP | OSPF  |
|-------|-------|-------|
| Hello | 5     | 10    |
| Dead  | 3     | 8     |
        """.strip()
        self.parser = TsTableParser()
        self.expected_table = [
            ["", "EIGRP", "OSPF"],
            ["Hello", "5", "10"],
            ["Dead", "3", "8"]
        ]
    
    def test_parse_markdown_table(self):
        table = self.parser.parse_markdown_table(self.markdown_table)
        self.assertEqual(table, self.expected_table)
    
    def test_empty_markdown_table(self):
        # When content is empty, we expect an empty list.
        empty_content = ""
        table = self.parser.parse_markdown_table(empty_content)
        self.assertEqual(table, [])
        
        # When content contains only separator rows, it should return an empty list.
        sep_only = """
|---|---|
|---|---|
        """.strip()
        table = self.parser.parse_markdown_table(sep_only)
        self.assertEqual(table, [])
    
    def test_format_table(self):
        # Test formatting a 2D list as an HTML table.
        html = self.parser.format_table(self.expected_table)
        self.assertIn("<table>", html)
        self.assertIn("table_body", html)
        self.assertIn("table_header_top", html)
        self.assertIn("table_header_left", html)
    
    def test_generate_masks_dimensions(self):
        # Using the default RowColumnMaskGenerator from the parser.
        masks = self.parser.mask_generator.generate_masks(self.expected_table)
        # For a 3x3 table, we expect 3 row masks + 3 column masks = 6 masks.
        self.assertEqual(len(masks), 6)
        for mask in masks:
            self.assertEqual(len(mask), len(self.expected_table))
            for i, row in enumerate(mask):
                self.assertEqual(len(row), len(self.expected_table[i]))
                for mask_info in row:
                    self.assertTrue(hasattr(mask_info, "cell_format"))
    
    def test_apply_mask_default(self):
        # Test that applying a mask cloaks only the targeted row.
        masks = self.parser.mask_generator.generate_masks(self.expected_table)
        first_mask = masks[0]  # Assume this mask cloaks the first row.
        masked_table = self.parser.apply_mask(self.expected_table, first_mask, cloze_index=1)
        # The first row should contain cloze syntax.
        for j, cell in enumerate(masked_table[0]):
            if j == 0:
                self.assertEqual("", cell)
                continue
            self.assertEqual("[...]", cell)
        # The remaining rows should remain unchanged.
        for row in masked_table[1:]:
            for cell in row:
                self.assertNotIn("[...]", cell)
    
    def test_custom_cloze_formatter(self):
        # Test using a custom cloze formatter.
        def custom_formatter():
            return f"<cloze></cloze>"
        parser_custom = TsTableParser(cloze_formatter=custom_formatter)
        masks = parser_custom.mask_generator.generate_masks(self.expected_table)
        first_mask = masks[0]
        masked_table = parser_custom.apply_mask(self.expected_table, first_mask, cloze_index=2)
        # Verify that the custom formatter's pattern is present.
        for j, cell in enumerate(masked_table[0]):
            if j == 0:
                self.assertEqual("", cell)
                continue
            self.assertEqual("<cloze></cloze>", cell)
    
    def test_parse_method_output(self):
        # Test the overall parse method.
        metadata = {"note_type": "ts_table", "deck": "TestDeck"}
        flashcards = self.parser.parse(self.markdown_table, metadata)
        # For our table (3x3), expect 3 row masks + 3 column masks = 6 flashcards.
        self.assertEqual(len(flashcards), 6)
        for card in flashcards:
            self.assertIsInstance(card, Flashcard)
            self.assertTrue(card.front)
            self.assertTrue(card.back)
        # All flashcards should have the same full table as the answer.
        backs = {card.back for card in flashcards}
        self.assertEqual(len(backs), 1)
    
    def test_row_column_mask_generator(self):
        # Directly test the default mask generator.
        generator = RowColumnMaskGenerator()
        masks = generator.generate_masks(self.expected_table)
        self.assertEqual(len(masks), 6)
        for mask in masks:
            for row in mask:
                for mask_info in row:
                    self.assertTrue(hasattr(mask_info, "cell_format"))

if __name__ == '__main__':
    unittest.main()
