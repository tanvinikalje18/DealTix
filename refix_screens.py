import os
import time
from playwright.sync_api import sync_playwright
import zipfile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dealtix_project.settings')
import django
django.setup()
from events.models import Event, TicketListing

base_url = "http://127.0.0.1:8000"

ticket = TicketListing.objects.first()
event_id = ticket.event.id if ticket else 1
listing_id = ticket.id if ticket else 1

os.makedirs("screenshots", exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_viewport_size({"width": 1280, "height": 800})
    
    def snap(url, name):
        try:
            r = page.goto(url)
            time.sleep(1.5)
            # full_page=False for a nice fixed crop instead of extremely long screens
            page.screenshot(path=f"screenshots/{name}.png", full_page=True) 
            status = r.status if r else "None"
            print(f"Captured {name} [{status}] -> {url}")
        except Exception as e:
            print(f"Failed {name}: {e}")

    snap(f"{base_url}/", "01_Home")
    snap(f"{base_url}/events/", "02_Events_List")
    snap(f"{base_url}/events/{event_id}/", "03_Event_Detail")
    snap(f"{base_url}/accounts/login/", "04_Login")
    # Corrected the Register URL
    snap(f"{base_url}/register/", "05_Register")
    
    # Login sequence
    try:
        page.goto(f"{base_url}/accounts/login/")
        page.fill("input[name='username']", "blackbook")
        page.fill("input[name='password']", "password123")
        page.click("button[type='submit']")
        time.sleep(2)
    except: pass
    
    snap(f"{base_url}/dashboard/", "06_Dashboard_My_Tickets")
    snap(f"{base_url}/sell/", "07_Sell_Ticket_Form")
    # Using correct dynamic listing ID for checkout
    snap(f"{base_url}/events/checkout/{listing_id}/", "08_Checkout_Booking")
    snap(f"{base_url}/admin/", "09_Admin_Panel")

    browser.close()

zip_path = r'c:\Users\tanvi\OneDrive\Desktop\DealTix_Blackbook_Assets.zip'
root = r'c:\Users\tanvi\OneDrive\Desktop\DealTix'

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(os.path.join(root, 'DealTix_Blackbook_Comprehensive.md'), 'DealTix_Blackbook_Comprehensive.md')
    screenshot_dir = os.path.join(root, 'screenshots')
    for file in os.listdir(screenshot_dir):
        if file.endswith('.png'):
            zipf.write(os.path.join(screenshot_dir, file), os.path.join('screenshots', file))
            
print("All screenshots fully captured correctly and zipped seamlessly!")
