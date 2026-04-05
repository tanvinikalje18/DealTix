import os

EXTENSIONS = {'.py', '.html', '.css', '.js', '.md', '.txt'}
EXCLUDE_DIRS = {'.git', '__pycache__', '.venv', 'venv', 'env', 'media', 'migrations', '.gemini'}
EXCLUDE_FILES = {'db.sqlite3', 'DealTix_Codebase_Dump.txt', 'zip_project.py', 'convert.py', 'DealTix_Project_Report.pdf'}

start_dir = r"c:\Users\tanvi\OneDrive\Desktop\DealTix"
output_file = r"c:\Users\tanvi\OneDrive\Desktop\DealTix_Codebase_Dump.txt"

with open(output_file, 'w', encoding='utf-8') as outfile:
    outfile.write("DealTix Codebase Dump\n")
    outfile.write("========================\n\n")
    
    for root, dirs, files in os.walk(start_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            if file in EXCLUDE_FILES:
                continue
            
            ext = os.path.splitext(file)[1]
            if ext in EXTENSIONS:
                filepath = os.path.join(root, file)
                relpath = os.path.relpath(filepath, start_dir)
                
                # Write a header for each file to distinguish them
                outfile.write(f"--- START FILE: {relpath} ---\n")
                try:
                    with open(filepath, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                except Exception as e:
                    outfile.write(f"\n[Error reading file: {e}]\n")
                outfile.write(f"\n--- END FILE: {relpath} ---\n\n\n")

print(f"Codebase dumped to {output_file}")
