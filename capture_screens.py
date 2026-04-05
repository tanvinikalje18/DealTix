import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dealtix_project.settings')
import django
django.setup()

from django.contrib.auth.models import User
if not User.objects.filter(username='blackbook').exists():
    User.objects.create_superuser('blackbook', 'admin@example.com', 'password123')
    print("Created superuser 'blackbook'")

import time
from playwright.sync_api import sync_playwright

os.makedirs("screenshots", exist_ok=True)
base_url = "http://127.0.0.1:8000"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_viewport_size({"width": 1280, "height": 800})
    
    def snap(path, name):
        try:
            page.goto(f"{base_url}{path}")
            time.sleep(1)
            page.screenshot(path=f"screenshots/{name}.png")
            print(f"Captured {name}")
        except Exception as e:
            print(f"Failed {name}: {e}")

    # Public pages
    snap("/", "01_Home")
    snap("/events/", "02_Events_List")
    snap("/events/1/", "03_Event_Detail")
    snap("/accounts/login/", "04_Login")
    snap("/accounts/register/", "05_Register")
    
    # Login
    try:
        page.goto(f"{base_url}/accounts/login/")
        page.fill("input[name='username']", "blackbook")
        page.fill("input[name='password']", "password123")
        page.click("button[type='submit']")
        time.sleep(2)
    except: pass
    
    # Auth pages
    snap("/dashboard/", "06_Dashboard_My_Tickets")
    snap("/sell/", "07_Sell_Ticket_Form")
    snap("/events/1/checkout/", "08_Checkout_Booking")
    snap("/admin/", "09_Admin_Panel")
    
    browser.close()
