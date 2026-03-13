from playwright.sync_api import sync_playwright
import smtplib
from email.mime.text import MIMEText
import datetime
import schedule
import time

# -----------------------------
# EMAIL CONFIG
# -----------------------------
SENDER_EMAIL = "pushparaj@fynro.in"
APP_PASSWORD = "yatd qbfq sanw tfeg"
RECEIVER_EMAIL = "pushparaj@fynro.in"

# -----------------------------
# SEND EMAIL
# -----------------------------
def send_email(subject, message):

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

# -----------------------------
# ATTENDANCE FUNCTION
# -----------------------------
def mark_attendance(action):

    today = datetime.datetime.today().weekday()

    if today >= 5:
        print("Weekend detected. Skipping attendance.")
        return

    try:

        with sync_playwright() as p:

            browser = p.chromium.launch_persistent_context(
                "user_data",
                headless=False
            )

            page = browser.new_page()

            page.goto("https://hrms.happymanbusiness.com/users/sign_in")

            print("Checking login session...")

            page.wait_for_timeout(5000)

            if action == "in":
                page.wait_for_selector("text=Punch In", timeout=30000)
                page.click("text=Punch In")
                print("Punch In done")

                send_email(
                    "Attendance Punch In Success",
                    "Your Punch In was successfully marked."
                )

            if action == "out":
                page.wait_for_selector("text=Punch Out", timeout=30000)
                page.click("text=Punch Out")
                print("Punch Out done")

                send_email(
                    "Attendance Punch Out Success",
                    "Your Punch Out was successfully marked."
                )

            page.wait_for_timeout(5000)
            browser.close()

    except Exception as e:

        print("Attendance Failed:", e)

        send_email(
            "Attendance FAILED",
            f"Attendance bot failed.\n\nError:\n{e}"
        )

# -----------------------------
# SCHEDULE
# -----------------------------
schedule.every().day.at("09:30").do(lambda: mark_attendance("in"))
schedule.every().day.at("18:30").do(lambda: mark_attendance("out"))

print("Attendance bot started...")

while True:
    schedule.run_pending()
    time.sleep(30)