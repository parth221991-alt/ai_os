import base64
import json
from pathlib import Path
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from core.config import get_settings, get_yaml_config


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
]


def _get_credentials() -> Credentials:
    cfg = get_yaml_config()
    token_path = Path(cfg["gmail"]["token_path"])
    creds_path = Path(cfg["gmail"]["credentials_path"])

    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
            creds = flow.run_local_server(port=0)
        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(creds.to_json())

    return creds


def get_gmail_service():
    creds = _get_credentials()
    return build("gmail", "v1", credentials=creds)


def _decode_body(payload: dict) -> str:
    if "body" in payload and payload["body"].get("data"):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="replace")
    if "parts" in payload:
        for part in payload["parts"]:
            if part.get("mimeType") == "text/plain":
                data = part.get("body", {}).get("data", "")
                if data:
                    return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
    return ""


def fetch_recent_career_emails(max_results: int = 50) -> list[dict]:
    cfg = get_yaml_config()
    keywords = cfg["gmail"]["career_filter_keywords"]
    query = " OR ".join(keywords) + " is:unread"
    service = get_gmail_service()

    result = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=max_results,
        labelIds=["INBOX"],
    ).execute()

    messages = result.get("messages", [])
    emails = []

    for msg_ref in messages:
        msg = service.users().messages().get(
            userId="me",
            id=msg_ref["id"],
            format="full",
        ).execute()

        headers = {h["name"].lower(): h["value"] for h in msg.get("payload", {}).get("headers", [])}
        body = _decode_body(msg.get("payload", {}))

        emails.append({
            "gmail_message_id": msg["id"],
            "gmail_thread_id": msg["threadId"],
            "subject": headers.get("subject", ""),
            "sender": headers.get("from", ""),
            "snippet": msg.get("snippet", ""),
            "body": body,
            "date": headers.get("date", ""),
        })

    return emails


def mark_as_read(message_id: str) -> None:
    service = get_gmail_service()
    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={"removeLabelIds": ["UNREAD"]},
    ).execute()


def setup_gmail_watch(topic_name: str) -> dict:
    """Register Gmail push notifications via Cloud Pub/Sub."""
    service = get_gmail_service()
    return service.users().watch(
        userId="me",
        body={
            "labelIds": ["INBOX"],
            "topicName": topic_name,
        },
    ).execute()
