from datetime import datetime
from email.message import EmailMessage
import os
from pathlib import Path
import smtplib
import ssl
from typing import Annotated

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field, StringConstraints, EmailStr

Str1 = Annotated[str, StringConstraints(min_length=1)]

router = APIRouter(prefix="/api-v1/contact", tags=["contact"])


CONTACT_FILE = Path(os.getenv("CONTACT_FILE", "/root/Tradex/contact.txt"))

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
SMTP_SERVER = os.getenv("SMTP_SERVER", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "0"))
SENDER = os.getenv("EMAIL_FROM", EMAIL_ADDRESS)
SUBJECT = os.getenv("EMAIL_SUBJECT", f"Contact for Fixhub - {datetime.now().date()}")
RECIPIENT_EMAIL = os.getenv("EMAIL_RECIPIENT", "")
SMTP_USE_SSL = os.getenv("SMTP_USE_SSL", "false").lower() in {"1", "true", "yes"}  # optional

class ContactRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: Str1
    email: EmailStr 
    message: Str1
    device_id: Str1 = Field(..., alias="deviceId")
    other: dict | None = None  # capture additional fields

def append_to_file(contact: ContactRequest, path: Path = CONTACT_FILE) -> None:
    """Append the contact message to the contact.txt file."""
    sanitized_message = contact.message.replace("\n", " ").replace("\r", " ")
    log_entry = (
        f"{datetime.utcnow().isoformat()} | {contact.name} <{contact.email}> | "
        f"{contact.device_id} | {sanitized_message}\n"
    )
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as exc:
        print(f"Failed to write contact log: {exc}")

def send_email(
    name: str, email: str, message: str, device_id: str, smtp_cls=smtplib.SMTP
) -> None:
    """Send an email with the contact message to the configured recipient."""
    if not (SMTP_SERVER and SMTP_PORT and SENDER and RECIPIENT_EMAIL):
        print("Email not sent. SMTP configuration is missing.")
        return

    msg = EmailMessage()
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER
    msg["To"] = RECIPIENT_EMAIL
    msg.set_content(f"Name: {name}\nEmail: {email}\nDevice: {device_id}\n\n{message}")

    try:
        if SMTP_USE_SSL or SMTP_PORT == 465:
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
                if EMAIL_ADDRESS and EMAIL_PASSWORD:
                    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)
        else:
            with smtp_cls(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
                server.ehlo()
                if server.has_extn("starttls"):
                    server.starttls(context=ssl.create_default_context())
                    server.ehlo()
                if EMAIL_ADDRESS and EMAIL_PASSWORD:
                    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)
    except Exception as exc:
        print(f"Failed to send contact email: {exc}")

@router.post("")
def send_contact_form(contact: ContactRequest):
    print("Received contact form:", contact)
    append_to_file(contact)
    send_email(contact.name, contact.email, contact.message, contact.device_id)
    return {"status": "ok"}
