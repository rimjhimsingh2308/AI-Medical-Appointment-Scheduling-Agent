import os
import requests
from dotenv import load_dotenv

# Load API token from .env
load_dotenv()
CALENDLY_API_TOKEN = os.getenv("CALENDLY_API_TOKEN")

BASE_URL = "https://api.calendly.com"
HEADERS = {
    "Authorization": f"Bearer {CALENDLY_API_TOKEN}",
    "Content-Type": "application/json"
}


def get_user():
    """
    Fetch current Calendly user info (name, email, URI).
    """
    resp = requests.get(f"{BASE_URL}/users/me", headers=HEADERS)
    if resp.status_code != 200:
        raise Exception(f"Calendly error: {resp.text}")
    return resp.json()["resource"]


def get_event_types(user_uri):
    """
    Fetch all event types for a user.
    """
    url = f"{BASE_URL}/event_types?user={user_uri}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        raise Exception(f"Calendly error: {resp.text}")
    return resp.json()


def get_scheduling_link(event_type_uri):
    """
    Generate a scheduling link for a specific event type.
    Requires the full event_type URI.
    """
    url = f"{BASE_URL}/scheduling_links"
    payload = {
        "max_event_count": 1,
        "owner": event_type_uri,
        "owner_type": "EventType"
    }
    resp = requests.post(url, headers=HEADERS, json=payload)
    if resp.status_code != 201:
        raise Exception(f"Calendly error: {resp.text}")
    return resp.json()["resource"]["booking_url"]
