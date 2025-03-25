# -----------------------------
# timetable_exporter/send_email_with_ics.py
# -----------------------------

import smtplib
from email.message import EmailMessage
from pathlib import Path
from dotenv import load_dotenv
import os

# Betöltjük a .env fájlt
load_dotenv()

def send_email_with_ics(ics_path: str):
    msg = EmailMessage()
    msg["From"] = os.getenv("SENDER_EMAIL")
    msg["To"] = os.getenv("RECEIVER_EMAIL")
    msg["Subject"] = "Adattudomány MSc órarend - .ics fájl"
    
    with open("email_template", "rb", encoding="utf-8") as f:
        e_mail_content = f.read()
        
    # TODO:
    # Modify the e-mail content to include the 3 most important events.
    # The events should be selected based on the start date.
    # The e-mail has the first SVG a little off the center, please fix it.
    # Do not use SVG, use <img> tag instead.
    
    msg.set_content(e_mail_content)

    with open(ics_path, "rb", encoding="utf-8") as f:
        ics_data = f.read()

    msg.add_attachment(
        ics_data,
        maintype="text",
        subtype="calendar",
        filename=Path(ics_path).name
    )

    # E-mail küldés
    with smtplib.SMTP_SSL(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))) as server:
        server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD"))
        server.send_message(msg)

    print(f"E-mail sent to: {os.getenv('RECEIVER_EMAIL')}")
