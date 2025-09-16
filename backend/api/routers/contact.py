from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import json, re
from pathlib import Path
import smtplib
import ssl
from typing import Annotated

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field, StringConstraints

Str1 = Annotated[str, StringConstraints(min_length=1)]
CTRL_RE = re.compile(r"[\r\n\t]+")  # kill control chars

router = APIRouter(prefix="/api-v1/contact", tags=["contact"])


#CONTACT_FILE = Path(os.getenv("CONTACT_FILE", "/root/Tradex/contact.txt"))
CONTACT_FILE = Path("/root/Tradex/backend/contact.txt")

#EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "")
#EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
#SMTP_SERVER = os.getenv("SMTP_SERVER", "")
#SMTP_PORT = int(os.getenv("SMTP_PORT", "0"))
SMTP_PORT = 587
SMTP_SERVER = 'smtp.gmail.com'
EMAIL_ADDRESS = 't39474115@gmail.com'
EMAIL_PASSWORD = 'pkaoszhklayzbyay'
SUBJECT = 'TEST'
RECIPIENT_EMAIL = 'opotek@protonmail.com'
SENDER = EMAIL_ADDRESS
#SUBJECT = os.getenv("EMAIL_SUBJECT", f"Contact for Fixhub - {datetime.now().date()}")
#RECIPIENT_EMAIL = os.getenv("EMAIL_RECIPIENT", "")
#SMTP_USE_SSL = os.getenv("SMTP_USE_SSL", "false").lower() in {"1", "true", "yes"}  # optional
SMTP_USE_SSL = False

class ContactRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: Str1
    email: Str1 = Field(..., pattern=r".+@.+") 
    message: Str1
    device_id: Str1 = Field(..., alias="deviceId")
    other: dict | None = None  # capture additional fields

def append_to_file(contact: ContactRequest, path: Path = CONTACT_FILE) -> bool:
    """
    Append a single JSONL line. Returns True on success, False on failure.
    - JSONL makes later parsing/ETL trivial.
    - Strips control chars, caps message length to avoid huge lines.
    - UTC, ISO 8601 with 'Z' suffix.
    - File perms tightened to 0640 on first write.
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        # sanitize/limit message
        msg = CTRL_RE.sub(" ", contact.message).strip()
        if len(msg) > 4000:
            msg = msg[:4000] + "…"

        record = {
            "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "name": contact.name,
            "email": contact.email,
            "device_id": contact.device_id,
            "message": msg,
            "other": contact.other or {},
        }

        # open in append mode and write as one line
        is_new_file = not path.exists()
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        # tighten perms on first write (Linux containers)
        if is_new_file and os.name == "posix":
            os.chmod(path, 0o640)

        return True
    except Exception as exc:
        # swap print for logging if you have a logger
        print(f"[contact] Failed to write {path}: {exc}")
        return False
    
def send_email(
    name: str, email: str, message: str, device_id: str, other:dict
) -> None:
    """Send an email with the contact message to the configured recipient."""
    if not (SMTP_SERVER and SMTP_PORT and SENDER and RECIPIENT_EMAIL):
        print("Email not sent. SMTP configuration is missing.")
        return

    msg = MIMEMultipart()
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER
    msg["To"] = RECIPIENT_EMAIL
    body = (f"Name: {name}\nEmail: {email}\nDevice: {device_id}\n\n{message} \n\n {other}\n\n--\nSent from Fixhub")
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Enable security
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(SENDER, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        print(f"Contact email successfully sent to {RECIPIENT_EMAIL}.")
        return True
    except Exception as exc:
        print(f"Failed to send contact email: {exc}")

@router.post("")
def send_contact_form(contact: ContactRequest):
    print("Received contact form:", contact)
    print("file loading", append_to_file(contact))
    if send_email(contact.name, contact.email, contact.message, contact.device_id, contact.other):
        return {"status": "ok"}
    return {"status": "error"}
