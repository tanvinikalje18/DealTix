import os
import zipfile

zip_path = r'c:\Users\tanvi\OneDrive\Desktop\DealTix_Blackbook_Assets.zip'
root = r'c:\Users\tanvi\OneDrive\Desktop\DealTix'

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(os.path.join(root, 'DealTix_Blackbook_Comprehensive.md'), 'DealTix_Blackbook_Comprehensive.md')
    screenshot_dir = os.path.join(root, 'screenshots')
    for file in os.listdir(screenshot_dir):
        if file.endswith('.png'):
            zipf.write(os.path.join(screenshot_dir, file), os.path.join('screenshots', file))
print("Assets zipped!")
