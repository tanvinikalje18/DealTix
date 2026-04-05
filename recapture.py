import os
import time
from playwright.sync_api import sync_playwright
import zipfile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dealtix_project.settings')
import django
django.setup()
from events.models import Event, TicketListing

base_url = "http://127.0.0.1:8000"

event = Event.objects.first()
listing = TicketListing.objects.first()

event_id = event.id if event else 1
listing_id = listing.id if listing else 1

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_viewport_size({"width": 1280, "height": 800})
    
    try:
        page.goto(f"{base_url}/accounts/login/")
        page.fill("input[name='username']", "blackbook")
        page.fill("input[name='password']", "password123")
        page.click("button[type='submit']")
        time.sleep(2)
    except: pass
        
    try:
        # Event detail explicitly targeting a valid database ID
        page.goto(f"{base_url}/events/{event_id}/")
        time.sleep(1)
        page.screenshot(path=f"screenshots/03_Event_Detail.png")
    except: pass
    
    try:
        # Checkout page explicitly targeting a valid listing ID
        page.goto(f"{base_url}/events/checkout/{listing_id}/")
        time.sleep(1)
        page.screenshot(path=f"screenshots/08_Checkout_Booking.png")
    except: pass
    
    browser.close()

zip_path = r'c:\Users\tanvi\OneDrive\Desktop\DealTix_Blackbook_Assets.zip'
root = r'c:\Users\tanvi\OneDrive\Desktop\DealTix'

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(os.path.join(root, 'DealTix_Blackbook_Comprehensive.md'), 'DealTix_Blackbook_Comprehensive.md')
    screenshot_dir = os.path.join(root, 'screenshots')
    for file in os.listdir(screenshot_dir):
        if file.endswith('.png'):
            zipf.write(os.path.join(screenshot_dir, file), os.path.join('screenshots', file))
            
print("Fixed screenshots captured and zipped!")
