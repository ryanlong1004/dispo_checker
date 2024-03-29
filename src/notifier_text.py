import json
import os
import pathlib
import smtplib
import ssl

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
config = json.load(
    open(pathlib.Path(ROOT_DIR, "./config.json"), "r+", encoding="utf-8")
)
config["root_dir"] = os.path.dirname(os.path.abspath(__file__))


def send_email(subject, text, password):
    """
    Send an email with gmail.
    """
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "<add_sender_here>"  # Enter your address
    receiver_email = "<add_receiver_here>"  # Enter receiver address

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, f"Subject: {subject}\n\n{text}")
