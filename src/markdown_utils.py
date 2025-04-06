import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

# Extracts all markdown images from a string
def extract_markdown_images(text):
    pattern = r'!\[(.*?)\]\((.*?)\)'
    matches = re.findall(pattern, text)
    return matches

# Extracts all markdown links from a string
def extract_markdown_links(text):
    pattern = r'\[(.*?)\]\((.*?)\)'
    matches = re.findall(pattern, text)
    return matches

# Converts markdown to blocks of text
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    result = []
    for block in blocks:
        stripped = block.strip()
        if stripped:
            result.append(stripped)
    return result

def block_to_block_type(block):
    if block.startswith("#"):
        return BlockType.HEADING
    elif block.startswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif block.startswith("-"):
        return BlockType.UNORDERED_LIST
    elif block.startswith("1."):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
def extract_title(markdown):
    pattern = r'# (.*)'
    match = re.search(pattern, markdown)
    if match:
        return match.group(1).strip()
    else:
        raise Exception("No title found in markdown")
