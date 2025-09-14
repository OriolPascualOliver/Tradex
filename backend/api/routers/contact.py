from datetime import datetime
from email.message import EmailMessage
import os
from pathlib import Path
import smtplib
from typing import Annotated
import base64
import hashlib

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field, constr, StringConstraints

Str1 = Annotated[str, StringConstraints(min_length=1)]

router = APIRouter(prefix="/api-v1/contact", tags=["contact"])

CONTACT_FILE = Path(__file__).resolve().parents[3] / "contact.txt"
RECIPIENT_EMAIL = "opotek+fixhub@protonmail.com"

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "t39474115@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "dvmk zoyl liam aoof")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER = os.getenv("EMAIL_FROM", EMAIL_ADDRESS)
SUBJECT = os.getenv(
    "EMAIL_SUBJECT", f"Contact for Fixhub - {datetime.now().date()}"
)


class ContactRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: Str1
    email: Annotated[str, StringConstraints(pattern=r".+@.+")]
    message: Str1
    device_id: Str1 = Field(..., alias="deviceId")
    other: dict | None = None  # To capture any additional fields
     


def append_to_file(contact: ContactRequest) -> None:
    """Append the contact message to the contact.txt file."""
    log_entry = (
        f"{datetime.utcnow().isoformat()} | {contact.name} <{contact.email}> | "
        f"{contact.device_id} | {contact.message.replace('\n', ' ').replace('\r', ' ')}\n"
    )
    try:
        with CONTACT_FILE.open("a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as exc:
        # Fail silently but log to stderr for debugging
        print(f"Failed to write contact log: {exc}")


def send_email(name: str, email: str, message: str, device_id: str) -> None:
    """Send an email with the contact message to the configured recipient."""
    msg = EmailMessage()
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER
    msg["To"] = RECIPIENT_EMAIL
    msg.set_content(
        f"Name: {name}\nEmail: {email}\nDevice: {device_id}\n\n{message}"
    )

    if SMTP_SERVER and EMAIL_ADDRESS and EMAIL_PASSWORD and SENDER:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
    else:
        print("Email not sent. SMTP configuration is missing.")


@router.post("")
def send_contact_form(contact: ContactRequest):
    print("Received contact form:", contact)
    append_to_file(contact)
    send_email(contact.name, contact.email, contact.message, contact.device_id)
    return {"status": "ok"}
