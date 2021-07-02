from email.message import EmailMessage
import os
import traceback
import smtplib
import time
import sys


def what_time():

    tm = time.localtime()
    current_time = time.strftime("%H:%M:%S", tm)

    return current_time


def check_os():
    if sys.platform == "linux":
        return "clear"
    elif sys.platform == "win32":
        return "CLS"


def email_err():

    EMAIL_ADDRESS = os.getenv("EMAIL")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASS")
    EMAIL_RECEIVER = os.getenv("EMAIL_REC")
    TRACEBACK = traceback.format_exc()

    msg = EmailMessage()
    msg["Subject"] = "Error has occured!"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_RECEIVER
    msg.set_content(f"{TRACEBACK}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
    except Exception as e:
        print(e.reason)
        input("Press anything to continue...")
