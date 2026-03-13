from playwright.sync_api import sync_playwright

print("Attendance bot started")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://hrms.happymanbusiness.com/users/sign_in")

    print("Opened HRMS login page")

    browser.close()
