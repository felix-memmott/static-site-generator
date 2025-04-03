from textnode import TextNode, TextType
from extract_from_text import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        pieces = old_node.text.split(delimiter)
        if len(pieces) % 2 == 0:
            raise ValueError("Invalid markdown - unclosed delimiter")
            
        for i in range(len(pieces)):
            if i % 2 == 0:
                if pieces[i] != "":
                    new_nodes.append(TextNode(pieces[i], TextType.TEXT))
            else:
                if pieces[i] != "":
                    new_nodes.append(TextNode(pieces[i], text_type))
                
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        images = extract_markdown_images(old_node.text)
        if not images:
            new_nodes.append(old_node)
            continue
            
        curr_index = 0
        for image in images:
            alt_text, url = image
            image_node = TextNode(alt_text, TextType.IMAGE, url)
            
            text_before_image = old_node.text[curr_index:old_node.text.find(f"![{alt_text}]")]
            if text_before_image:
                new_nodes.append(TextNode(text_before_image, TextType.TEXT))
                
            new_nodes.append(image_node)
            curr_index = old_node.text.find(f"({url})") + len(url) + 2
            
        text_after_last_image = old_node.text[curr_index:]
        if text_after_last_image:
            new_nodes.append(TextNode(text_after_last_image, TextType.TEXT))
            
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue
            
        curr_index = 0
        for link in links:
            text, url = link
            link_node = TextNode(text, TextType.LINK, url)
            
            text_before_link = old_node.text[curr_index:old_node.text.find(f"[{text}]")]
            if text_before_link:
                new_nodes.append(TextNode(text_before_link, TextType.TEXT))
                
            new_nodes.append(link_node)
            curr_index = old_node.text.find(f"({url})") + len(url) + 2
            
        text_after_last_link = old_node.text[curr_index:]
        if text_after_last_link:
            new_nodes.append(TextNode(text_after_last_link, TextType.TEXT))
            
    return new_nodes

def text_to_textnodes(text):
    # Start with a single text node containing the entire text
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Split by images first
    nodes = split_nodes_image(nodes)
    
    # Then split by links
    nodes = split_nodes_link(nodes)
    
    # Finally split by delimiters
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    return nodes