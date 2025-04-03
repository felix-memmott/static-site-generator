import unittest


from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_basic(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "italic")
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_all_types(self):
        # Test BOLD
        node = TextNode("**bold** text", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(nodes[0].text_type, TextType.BOLD)

        # Test ITALIC
        node = TextNode("*italic* text", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(nodes[0].text_type, TextType.ITALIC)

        # Test CODE
        node = TextNode("`code` text", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(nodes[0].text_type, TextType.CODE)

    def test_split_nodes_delimiter_unclosed(self):
        node = TextNode("This is *italic text", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", TextType.ITALIC)

    def test_split_nodes_delimiter_non_text(self):
        # Test with each TextType
        for text_type in TextType:
            if text_type != TextType.TEXT:
                node = TextNode("This is text", text_type)
                nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
                self.assertEqual(len(nodes), 1)
                self.assertEqual(nodes[0].text_type, text_type)

    def test_split_nodes_delimiter_multiple_nodes(self):
        nodes = [
            TextNode("*italic* text", TextType.TEXT),
            TextNode("**bold** text", TextType.TEXT),
            TextNode("`code` text", TextType.TEXT)
        ]
        
        # Test each delimiter and type combination
        delimiters_types = [
            ("*", TextType.ITALIC),
            ("**", TextType.BOLD),
            ("`", TextType.CODE)
        ]
        
        for i, (delimiter, text_type) in enumerate(delimiters_types):
            result = split_nodes_delimiter([nodes[i]], delimiter, text_type)
            self.assertTrue(any(node.text_type == text_type for node in result))


class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image_basic(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        nodes = split_nodes_image([node])
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "This is text with an ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "image")
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[1].url, "https://i.imgur.com/zjjcJKZ.png")

    def test_split_nodes_image_multiple(self):
        node = TextNode(
            "Start ![first](image1.jpg) middle ![second](image2.png) end", 
            TextType.TEXT
        )
        nodes = split_nodes_image([node])
        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[0].text, "Start ")
        self.assertEqual(nodes[1].text, "first")
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[1].url, "image1.jpg")
        self.assertEqual(nodes[2].text, " middle ")
        self.assertEqual(nodes[3].text, "second") 
        self.assertEqual(nodes[3].text_type, TextType.IMAGE)
        self.assertEqual(nodes[3].url, "image2.png")
        self.assertEqual(nodes[4].text, " end")

    def test_split_nodes_image_no_images(self):
        node = TextNode("Just plain text", TextType.TEXT)
        nodes = split_nodes_image([node])
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "Just plain text")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link_basic(self):
        node = TextNode("Here is a [link](https://example.com)", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "Here is a ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "link")
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[1].url, "https://example.com")

    def test_split_nodes_link_multiple(self):
        node = TextNode(
            "Start [first](https://first.com) middle [second](https://second.com) end",
            TextType.TEXT
        )
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[0].text, "Start ")
        self.assertEqual(nodes[1].text, "first")
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[1].url, "https://first.com")
        self.assertEqual(nodes[2].text, " middle ")
        self.assertEqual(nodes[3].text, "second")
        self.assertEqual(nodes[3].text_type, TextType.LINK)
        self.assertEqual(nodes[3].url, "https://second.com")
        self.assertEqual(nodes[4].text, " end")

    def test_split_nodes_link_no_links(self):
        node = TextNode("Just plain text", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "Just plain text")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_basic(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_text_to_textnodes_multiple_types(self):
        text = "This is **bold** and *italic* and `code` text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 7)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " and ")
        self.assertEqual(nodes[3].text, "italic")
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(nodes[4].text, " and ")
        self.assertEqual(nodes[5].text, "code")
        self.assertEqual(nodes[5].text_type, TextType.CODE)
        self.assertEqual(nodes[6].text, " text")

    def test_text_to_textnodes_with_links(self):
        text = "This is a [link](https://example.com) in the text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is a ")
        self.assertEqual(nodes[1].text, "link")
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[1].url, "https://example.com")
        self.assertEqual(nodes[2].text, " in the text")

    def test_text_to_textnodes_with_images(self):
        text = "This is an ![image](https://example.com/image.png) in the text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is an ")
        self.assertEqual(nodes[1].text, "image")
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[1].url, "https://example.com/image.png")
        self.assertEqual(nodes[2].text, " in the text")

    def test_text_to_textnodes_complex(self):
        text = "This is **bold** with a [link](https://example.com) and an ![image](https://example.com/image.png) and *italic* text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 9)
        # Check each node's type and content
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " with a ")
        self.assertEqual(nodes[3].text, "link")
        self.assertEqual(nodes[3].text_type, TextType.LINK)
        self.assertEqual(nodes[3].url, "https://example.com")
        self.assertEqual(nodes[4].text, " and an ")
        self.assertEqual(nodes[5].text, "image")
        self.assertEqual(nodes[5].text_type, TextType.IMAGE)
        self.assertEqual(nodes[5].url, "https://example.com/image.png")
        self.assertEqual(nodes[6].text, " and ")
        self.assertEqual(nodes[7].text, "italic")
        self.assertEqual(nodes[7].text_type, TextType.ITALIC)
        self.assertEqual(nodes[8].text, " text")


if __name__ == "__main__":
    unittest.main()

