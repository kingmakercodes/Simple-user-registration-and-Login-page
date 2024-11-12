import smtplib
import os
from dotenv import load_dotenv


def test_email():
    # Load environment variables from .env file
    load_dotenv()

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = os.getenv("MAIL_USERNAME")
    password = os.getenv("MAIL_PASSWORD")
    recipient_email = "bansonmarc@gmail.com"  # Change this to your test email
    message = "Subject: Test Email\n\nThis is a test email from your Flask app SMTP setup."

    try:
        # Create an SMTP connection
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Upgrade the connection to secure (TLS)
            server.login(sender_email, password)  # Login to the email account
            server.sendmail(sender_email, recipient_email, message)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
