import unittest
from extract_from_text import extract_markdown_images, extract_markdown_links

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

if __name__ == "__main__":
    unittest.main()
