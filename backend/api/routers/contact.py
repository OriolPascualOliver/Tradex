from datetime import datetime
from email.message import EmailMessage
import os
from pathlib import Path
import smtplib
from typing import Annotated

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field, StringConstraints

Str1 = Annotated[str, StringConstraints(min_length=1)]

router = APIRouter(prefix="/api-v1/contact", tags=["contact"])

CONTACT_FILE = Path(__file__).resolve().parents[3] / "contact.txt"

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
SMTP_SERVER = os.getenv("SMTP_SERVER", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "0"))
SENDER = os.getenv("EMAIL_FROM", EMAIL_ADDRESS)
SUBJECT = os.getenv(
    "EMAIL_SUBJECT", f"Contact for Fixhub - {datetime.now().date()}"
)
RECIPIENT_EMAIL = os.getenv("EMAIL_RECIPIENT", "")


class ContactRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: Str1
    email: Annotated[str, StringConstraints(pattern=r".+@.+")]
    message: Str1
    device_id: Str1 = Field(..., alias="deviceId")
    other: dict | None = None  # To capture any additional fields
     


def append_to_file(contact: ContactRequest) -> None:
    """Append the contact message to the contact.txt file."""
    sanitized_message = contact.message.replace("\n", " ").replace("\r", " ")
    log_entry = (
        f"{datetime.utcnow().isoformat()} | {contact.name} <{contact.email}> | "
        f"{contact.device_id} | {sanitized_message}\n"
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

    if (
        SMTP_SERVER
        and SMTP_PORT
        and EMAIL_ADDRESS
        and EMAIL_PASSWORD
        and SENDER
        and RECIPIENT_EMAIL
    ):
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)
        except Exception as exc:
            # Fail silently but log the error for debugging
            print(f"Failed to send contact email: {exc}")
    else:
        print("Email not sent. SMTP configuration is missing.")


@router.post("")
def send_contact_form(contact: ContactRequest):
    print("Received contact form:", contact)
    append_to_file(contact)
    send_email(contact.name, contact.email, contact.message, contact.device_id)
    return {"status": "ok"}
