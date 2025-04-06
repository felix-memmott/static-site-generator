from textnode import TextNode, TextType
from markdown_utils import markdown_to_blocks, block_to_block_type, BlockType
from split_nodes import split_nodes_image, split_nodes_link, split_nodes_delimiter

class HtmlNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    def props_to_html(self):
        if not self.props:
            return ""
        props_list = []
        for key, value in self.props.items():
            props_list.append(f'{key}="{value}"')
        return " " + " ".join(props_list)

    def __repr__(self):
        return f"HtmlNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    

class LeafNode(HtmlNode):
    def __init__(self, tag, value, props = None):
        if value is None:
            raise ValueError("LeafNode value cannot be None")
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode value cannot be None")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HtmlNode):
    def __init__(self, tag: str, children: list, props = None):
        if tag is None:
            raise ValueError("ParentNode tag cannot be None")
        if children is None:
            raise ValueError("ParentNode children cannot be None") 
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode tag cannot be None")
        if self.children is None:
            raise ValueError("ParentNode children cannot be None")
        
        children_html = []
        for child in self.children:
            children_html.append(child.to_html())
        
        return f"<{self.tag}{self.props_to_html()}>{''.join(children_html)}</{self.tag}>"
    

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError("Invalid text node type")

def text_to_children(text):
    # Convert text to text nodes
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Split by images first
    nodes = split_nodes_image(nodes)
    
    # Split by links
    nodes = split_nodes_link(nodes)
    
    # Split by bold
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    
    # Split by italic (both * and _)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    
    # Split by code
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    # Convert text nodes to HTML nodes
    return [text_node_to_html_node(node) for node in nodes]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children.append(ParentNode("p", text_to_children(block)))
        elif block_type == BlockType.HEADING:
            level = len(block.split(" ")[0])  # Count number of # symbols
            children.append(ParentNode(f"h{level}", text_to_children(block[level+1:])))
        elif block_type == BlockType.CODE:
            code_node = text_node_to_html_node(TextNode(block[3:-3].strip(), TextType.CODE))
            children.append(ParentNode("pre", [code_node]))
        elif block_type == BlockType.QUOTE:
            quote_text = block[2:].strip()  # Remove "> " prefix
            children.append(ParentNode("blockquote", text_to_children(quote_text)))
        elif block_type == BlockType.UNORDERED_LIST:
            # Split the block into individual list items
            items = [item.strip()[2:].strip() for item in block.split("\n") if item.strip()]
            list_items = []
            for item in items:
                list_items.append(ParentNode("li", text_to_children(item)))
            children.append(ParentNode("ul", list_items))
        elif block_type == BlockType.ORDERED_LIST:
            # Split the block into individual list items
            items = [item.strip()[item.find(".")+1:].strip() for item in block.split("\n") if item.strip()]
            list_items = []
            for item in items:
                list_items.append(ParentNode("li", text_to_children(item)))
            children.append(ParentNode("ol", list_items))
            
    return ParentNode("div", children)
