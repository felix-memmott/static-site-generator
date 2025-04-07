import os
from markdown_utils import extract_title
from htmlnode import markdown_to_html_node

def generate_pages_recursive(content_dir="./content", template_path="./template.html", public_dir="./public", base_path="/"):
    # Walk through all directories under content_dir
    for root, dirs, files in os.walk(content_dir):
        # Check if index.md exists in current directory
        if "index.md" in files:
            # Get relative path from content dir
            rel_path = os.path.relpath(root, content_dir)
            
            # Create corresponding output directory in public
            output_dir = os.path.join(public_dir, rel_path)
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate HTML for this index.md
            markdown_path = os.path.join(root, "index.md")
            html_output_path = os.path.join(output_dir, "index.html")
            
            # Use existing generate_page logic
            print(f"Generating page from {markdown_path} to {html_output_path} using template {template_path}")
            markdown = open(markdown_path, "r").read()
            template = open(template_path, "r").read()
            title = extract_title(markdown)
            html = markdown_to_html_node(markdown).to_html()
            html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
            html = html.replace('href="/', f'href="{base_path}')
            html = html.replace('src="/', f'src="{base_path}')
            open(html_output_path, "w").write(html)
    