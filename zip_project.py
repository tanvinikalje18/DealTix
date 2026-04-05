import os
import zipfile

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        # Directories to exclude from the zip
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', '.venv', 'venv', 'env', 'media')]
        
        for file in files:
            # Files to exclude from the zip to keep it lightweight for an AI tool
            if file in ('db.sqlite3', 'DealTix_Export.zip', 'zip_project.py', 'convert.py'):
                continue
            if file.endswith('.pdf') or file.endswith('.pyc') or file.endswith('.jpg') or file.endswith('.png'):
                continue
            
            filepath = os.path.join(root, file)
            # Make the path relative to the root directory
            arcname = os.path.relpath(filepath, path)
            ziph.write(filepath, arcname)

zip_path = r'c:\Users\tanvi\OneDrive\Desktop\DealTix_Codepack.zip'
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipdir(r'c:\Users\tanvi\OneDrive\Desktop\DealTix', zipf)

print(f"Project Codebase zipped successfully to {zip_path}")
