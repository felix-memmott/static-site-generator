import os
import shutil

from textnode import TextNode
from markdown_utils import extract_title
from htmlnode import markdown_to_html_node

from generate_pages import generate_pages_recursive

MARKDOWN_PATH = "./content/index.md"
HTML_OUTPUT_PATH = "./public/index.html"
TEMPLATE_PATH = "./template.html"

def main():
    copy_static_to_public()
    generate_pages_recursive()
def copy_static_to_public():
    static_dir = "static"
    public_dir = "public"

    # Delete contents of public directory if it exists
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    # Create empty public directory
    os.makedirs(public_dir)

    def copy_recursive(src_path, dst_path):
        # Create destination directory if it doesn't exist
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
            print(f"Created directory: {dst_path}")

        # Iterate through items in source directory
        for item in os.listdir(src_path):
            src_item = os.path.join(src_path, item)
            dst_item = os.path.join(dst_path, item)

            if os.path.isdir(src_item):
                # Recursively copy subdirectories
                copy_recursive(src_item, dst_item)
            else:
                # Copy files
                shutil.copy2(src_item, dst_item)
                print(f"Copied file: {dst_item}")

    # Start recursive copy from static to public
    copy_recursive(static_dir, public_dir)


if __name__ == "__main__":
    main()
