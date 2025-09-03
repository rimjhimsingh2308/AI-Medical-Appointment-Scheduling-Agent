from calendly_utils import get_event_types

if __name__ == "__main__":
    # Your actual Calendly user URI
    USER_URI = "https://api.calendly.com/users/abc71535-6813-406a-b7c2-c9b76c8b6f34"

    try:
        response = get_event_types(USER_URI)
        event_types = response.get("collection", [])
        print("\n=== Your Calendly Event Types ===\n")
        for evt in event_types:
            name = evt.get("name")
            uuid = evt.get("uri", "").split("/")[-1]
            duration = evt.get("duration")
            print(f"Name: {name}\nUUID: {uuid}\nDuration: {duration} mins\n---")
    except Exception as e:
        print("Error fetching event types:", e)
