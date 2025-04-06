import unittest

from markdown_utils import extract_markdown_images, extract_markdown_links, markdown_to_blocks, block_to_block_type, BlockType, extract_title

class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        # Test multiple images
        matches = extract_markdown_images(
            "Here are two images: ![first](image1.jpg) and ![second](image2.png)"
        )
        self.assertListEqual([
            ("first", "image1.jpg"),
            ("second", "image2.png")
        ], matches)

        # Test empty text
        matches = extract_markdown_images("")
        self.assertListEqual([], matches)

        # Test text with no images
        matches = extract_markdown_images("Just plain text")
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)

        # Test multiple links
        matches = extract_markdown_links(
            "Here are two links: [first](https://first.com) and [second](https://second.com)"
        )
        self.assertListEqual([
            ("first", "https://first.com"),
            ("second", "https://second.com")
        ], matches)

        # Test empty text
        matches = extract_markdown_links("")
        self.assertListEqual([], matches)

        # Test text with no links
        matches = extract_markdown_links("Just plain text")
        self.assertListEqual([], matches)

    def test_markdown_to_blocks(self):
        # Test basic markdown blocks
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        # Test empty input
        self.assertEqual(markdown_to_blocks(""), [])
        
        # Test whitespace only input
        self.assertEqual(markdown_to_blocks("   \n\n  \n  "), [])

    def test_markdown_to_blocks_single_block(self):
        # Test single block without newlines
        self.assertEqual(markdown_to_blocks("Single block"), ["Single block"])
        
        # Test single block with internal newlines
        self.assertEqual(
            markdown_to_blocks("Line 1\nLine 2\nLine 3"), 
            ["Line 1\nLine 2\nLine 3"]
        )

    def test_markdown_to_blocks_multiple_newlines(self):
        # Test handling of multiple consecutive newlines
        md = """First block


Second block


Third block"""
        self.assertEqual(
            markdown_to_blocks(md),
            ["First block", "Second block", "Third block"]
        )

    def test_markdown_to_blocks_with_lists(self):
        # Test handling of markdown lists
        md = """Regular paragraph

- List item 1
- List item 2
  - Subitem 2.1
  - Subitem 2.2

Final paragraph"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "Regular paragraph",
                "- List item 1\n- List item 2\n  - Subitem 2.1\n  - Subitem 2.2",
                "Final paragraph"
            ]
        )

    def test_block_to_block_type(self):
        # Basic tests
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("## Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("> Quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("- List item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. List item"), BlockType.ORDERED_LIST)

        # Test longer heading with multiple #s
        self.assertEqual(
            block_to_block_type("### This is a longer heading with multiple words"),
            BlockType.HEADING
        )

        # Test code block with content
        self.assertEqual(
            block_to_block_type("```python\ndef hello_world():\n    print('Hello World!')\n```"),
            BlockType.CODE
        )

        # Test multi-line quote
        self.assertEqual(
            block_to_block_type("> This is a longer quote\n> that spans multiple lines\n> with various content"),
            BlockType.QUOTE
        )

        # Test unordered list with multiple items
        self.assertEqual(
            block_to_block_type("- First item\n- Second item\n  - Sub-item\n- Third item"),
            BlockType.UNORDERED_LIST
        )

        # Test ordered list with multiple items
        self.assertEqual(
            block_to_block_type("1. First item\n2. Second item\n   1. Sub-item\n3. Third item"),
            BlockType.ORDERED_LIST
        )

        # Test regular paragraph with multiple lines
        self.assertEqual(
            block_to_block_type("This is a regular paragraph\nwith multiple lines\nof text in it."),
            BlockType.PARAGRAPH
        )

    def test_extract_title(self):
        with self.assertRaises(Exception) as context:
            extract_title("")
        self.assertEqual(str(context.exception), "No title found in markdown")
        
        self.assertEqual(extract_title("# Heading"), "Heading")
        self.assertEqual(extract_title("# Heading "), "Heading")
        
        with self.assertRaises(Exception) as context:
            extract_title("This is a paragraph")
        self.assertEqual(str(context.exception), "No title found in markdown")
        
        self.assertEqual(extract_title("This is a paragraph\n# Heading"), "Heading")
if __name__ == "__main__":
    unittest.main()
