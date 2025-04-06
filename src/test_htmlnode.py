import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode, text_node_to_html_node, markdown_to_html_node
from textnode import TextNode, TextType

class TestHtmlNode(unittest.TestCase):
    def test_init_empty(self):
        node = HtmlNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value) 
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_with_values(self):
        node = HtmlNode("p", "Hello", ["child1", "child2"], {"class": "text"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, ["child1", "child2"])
        self.assertEqual(node.props, {"class": "text"})

    def test_props_to_html_empty(self):
        node = HtmlNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props(self):
        node = HtmlNode(props={"class": "text", "id": "para"})
        self.assertTrue(' class="text"' in node.props_to_html())
        self.assertTrue(' id="para"' in node.props_to_html())

    def test_repr(self):
        node = HtmlNode("div", "content", ["child"], {"class": "text"})
        expected = 'HtmlNode(tag=div, value=content, children=[\'child\'], props={\'class\': \'text\'})'
        self.assertEqual(repr(node), expected)

    def test_to_html_not_implemented(self):
        node = HtmlNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

class TestLeafNode(unittest.TestCase):
    def test_init_with_value(self):
        node = LeafNode("p", "Hello", {"class": "text"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.props, {"class": "text"})
        self.assertIsNone(node.children)

    def test_init_without_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)

    def test_to_html_with_tag(self):
        node = LeafNode("p", "Hello", {"class": "text"})
        self.assertEqual(node.to_html(), '<p class="text">Hello</p>')

    def test_to_html_without_tag(self):
        node = LeafNode(None, "Hello")
        self.assertEqual(node.to_html(), "Hello")

    def test_to_html_with_none_value(self):
        node = LeafNode("p", "Hello")
        node.value = None
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_url(self):
        node = LeafNode("a", "Click me", {"href": "https://www.example.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.example.com">Click me</a>')

    def test_to_html_with_multiple_urls(self):
        node = LeafNode("img", "Image", {
            "src": "https://www.example.com/image.jpg",
            "data-url": "https://www.example.com/data"
        })
        self.assertEqual(
            node.to_html(),
            '<img src="https://www.example.com/image.jpg" data-url="https://www.example.com/data">Image</img>'
        )

class TestParentNode(unittest.TestCase):
    def test_init_with_children(self):
        child1 = LeafNode("p", "Child 1")
        child2 = LeafNode("p", "Child 2")
        node = ParentNode("div", [child1, child2], {"class": "parent"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 2)
        self.assertEqual(node.props, {"class": "parent"})
        self.assertIsNone(node.value)

    def test_init_without_tag(self):
        child = LeafNode("p", "Child")
        with self.assertRaises(ValueError):
            ParentNode(None, [child])

    def test_init_without_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None)

    def test_to_html_with_children(self):
        child1 = LeafNode("p", "Child 1")
        child2 = LeafNode("p", "Child 2")
        node = ParentNode("div", [child1, child2], {"class": "parent"})
        expected = '<div class="parent">\n<p>Child 1</p><p>Child 2</p>\n</div>'
        self.assertEqual(node.to_html(), expected)

    def test_to_html_with_nested_children(self):
        inner_child = LeafNode("span", "Inner")
        outer_child = ParentNode("p", [inner_child])
        node = ParentNode("div", [outer_child])
        expected = '<div>\n<p>\n<span>Inner</span>\n</p>\n</div>'
        self.assertEqual(node.to_html(), expected)

    def test_to_html_with_none_tag(self):
        child = LeafNode("p", "Child")
        node = ParentNode("div", [child])
        node.tag = None
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_none_children(self):
        node = ParentNode("div", [LeafNode("p", "Child")])
        node.children = None
        with self.assertRaises(ValueError):
            node.to_html()

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_node_to_html_node_text(self):
        text_node = TextNode("Hello world", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "Hello world")
        self.assertIsNone(html_node.tag)

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.tag, "b")

    def test_text_node_to_html_node_italic(self):
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.tag, "i")

    def test_text_node_to_html_node_code(self):
        text_node = TextNode("Code text", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "Code text")
        self.assertEqual(html_node.tag, "code")

    def test_text_node_to_html_node_link(self):
        text_node = TextNode("Link text", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "Link text")
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "https://www.example.com"})

    def test_text_node_to_html_node_image(self):
        text_node = TextNode("Image alt", TextType.IMAGE, "https://www.example.com/image.jpg")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": "https://www.example.com/image.jpg", "alt": "Image alt"})

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_markdown_to_html_node_paragraph(self):
        markdown = "This is a paragraph of text."
        node = markdown_to_html_node(markdown)
        self.assertIsInstance(node, ParentNode)
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)
        self.assertIsInstance(node.children[0], ParentNode)
        self.assertEqual(node.children[0].tag, "p")
        self.assertEqual(len(node.children[0].children), 1)
        self.assertEqual(node.children[0].children[0].value, "This is a paragraph of text.")

    def test_markdown_to_html_node_heading(self):
        markdown = "# Heading 1"
        node = markdown_to_html_node(markdown)
        self.assertIsInstance(node.children[0], ParentNode)
        self.assertEqual(node.children[0].tag, "h1")
        self.assertEqual(node.children[0].children[0].value, "Heading 1")

    def test_markdown_to_html_node_code(self):
        markdown = "```\ncode block\n```"
        node = markdown_to_html_node(markdown)
        self.assertIsInstance(node.children[0], ParentNode)
        self.assertEqual(node.children[0].tag, "pre")
        self.assertEqual(node.children[0].children[0].tag, "code")
        self.assertEqual(node.children[0].children[0].value, "code block")

    def test_markdown_to_html_node_quote(self):
        markdown = "> This is a quote"
        node = markdown_to_html_node(markdown)
        self.assertIsInstance(node.children[0], ParentNode)
        self.assertEqual(node.children[0].tag, "blockquote")
        self.assertEqual(node.children[0].children[0].value, "This is a quote")

    def test_markdown_to_html_node_unordered_list(self):
        markdown = "- List item"
        node = markdown_to_html_node(markdown)
        self.assertIsInstance(node.children[0], ParentNode)
        self.assertEqual(node.children[0].tag, "ul")
        self.assertEqual(node.children[0].children[0].value, "- List item")

    def test_markdown_to_html_node_ordered_list(self):
        markdown = "1. List item"
        node = markdown_to_html_node(markdown)
        self.assertIsInstance(node.children[0], ParentNode)
        self.assertEqual(node.children[0].tag, "ol")
        self.assertEqual(node.children[0].children[0].value, "1. List item")

    def test_markdown_to_html_node_multiple_blocks(self):
        markdown = """
# Heading

Paragraph 1

> Quote

Paragraph 2
"""
        node = markdown_to_html_node(markdown)
        self.assertEqual(len(node.children), 4)
        self.assertEqual(node.children[0].tag, "h1")
        self.assertEqual(node.children[1].tag, "p")
        self.assertEqual(node.children[2].tag, "blockquote")
        self.assertEqual(node.children[3].tag, "p")

        
if __name__ == "__main__":
    unittest.main()
