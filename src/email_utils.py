import os
import base64
import requests
from dotenv import load_dotenv

# Load .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

api_key = os.getenv("BREVO_API_KEY")
sender_name = os.getenv("SENDER_NAME")
sender_email = os.getenv("SENDER_EMAIL")

def send_email(to_email, subject, content, attachment_path=None):
    """
    Send an HTML email via Brevo API.
    """
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "sender": {"name": sender_name, "email": sender_email},
        "to": [{"email": to_email}],
        "subject": subject,
        "htmlContent": content  # always HTML now
    }

    if attachment_path and os.path.exists(attachment_path):
        try:
            with open(attachment_path, "rb") as f:
                encoded_file = base64.b64encode(f.read()).decode("utf-8")
            payload["attachment"] = [{"content": encoded_file, "name": os.path.basename(attachment_path)}]
        except Exception as e:
            print(f"⚠️ Failed to attach file: {e}")

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            print(f"✅ Email sent to {to_email}")
            return True
        else:
            print(f"❌ Email failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception sending email: {e}")
        return False
