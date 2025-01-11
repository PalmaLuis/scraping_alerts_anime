from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
from datetime import datetime, timedelta
import pytz
import os

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def authenticte_google_calendar():
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return creds


def create_google_event(event_data):
    creds = authenticte_google_calendar()
    service = build("calendar", "v3", credentials=creds)

    tz = pytz.timezone("America/Lima")

    start_time = tz.localize(
        datetime.strptime(event_data["air_time"], "%Y-%m-%d %I:%M %p")
    )
    end_time = start_time + timedelta(minutes=5)

    event = {
        "summary": event_data["title"],
        "description": f'Episodio: {event_data['episode']}',
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": "America/Lima",
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": "America/Lima",
        },
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 5},
                {"method": "popup", "minutes": 5},
            ],
        },
    }

    event_result = service.events().insert(calendarId="primary", body=event).execute()
    print(f"Evento creado: {event_data['episode']} :{event_data['title']}")
