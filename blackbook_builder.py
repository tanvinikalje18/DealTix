import os
import re

ROOT_DIR = r"c:\Users\tanvi\OneDrive\Desktop\DealTix"
OUTPUT_FILE = os.path.join(ROOT_DIR, "DealTix_Blackbook_Comprehensive.md")

EXCLUDE_DIRS = {'.git', '__pycache__', '.venv', 'venv', 'env', 'media', 'migrations', '.gemini'}

def get_tree(dir_path):
    tree_str = "```text\n"
    for root, dirs, files in os.walk(dir_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        level = root.replace(dir_path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        folder = os.path.basename(root)
        if folder == "": folder = "DealTix"
        tree_str += f"{indent}{folder}/\n"
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            tree_str += f"{subindent}{f}\n"
    tree_str += "```\n"
    return tree_str

def read_file(filepath, scrub_secret=False):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if scrub_secret:
                content = re.sub(r"SECRET_KEY\s*=\s*['\"].*?['\"]", "SECRET_KEY = 'HIDDEN_FOR_SECURITY'", content)
            return content
    except Exception as e:
        return f"Error reading file: {e}"

with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
    out.write("# DealTix Complete Blackbook Dump\n\n")
    
    out.write("## 1. Directory Tree\n")
    out.write(get_tree(ROOT_DIR))
    
    out.write("\n## 2. Requirements.txt\n```text\n")
    try:
        with open(os.path.join(ROOT_DIR, 'requirements.txt'), 'r') as req:
            out.write(req.read())
    except:
        out.write("# You can generate this by running `pip freeze > requirements.txt` via console.\n")
    out.write("\n```\n")

    files_to_dump = [
        ("dealtix_project/settings.py", True),
        ("dealtix_project/urls.py", False),
        ("events/models.py", False),
        ("events/views.py", False),
        ("events/urls.py", False),
        ("events/forms.py", False),
        ("events/admin.py", False),
        ("templates/base.html", False),
        ("templates/events/home.html", False),
        ("templates/events/event_list.html", False),
        ("templates/events/event_detail.html", False),
        ("templates/events/sell_ticket.html", False),
        ("templates/events/checkout.html", False),
        ("templates/registration/login.html", False),
        ("templates/registration/register.html", False),
    ]

    out.write("\n## 3. Source Code\n")
    for fpath, scrub in files_to_dump:
        full_path = os.path.join(ROOT_DIR, fpath.replace('/', os.sep))
        ext = os.path.splitext(fpath)[1][1:]
        if ext == 'py': lang = 'python'
        elif ext == 'html': lang = 'html'
        else: lang = 'text'
        
        out.write(f"### `{fpath}`\n")
        out.write(f"```{lang}\n")
        out.write(read_file(full_path, scrub))
        out.write("\n```\n\n")

print(f"Comprehensive dump saved to {OUTPUT_FILE}")
