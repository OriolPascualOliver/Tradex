from fastapi import APIRouter
from pydantic import BaseModel, EmailStr, constr

router = APIRouter(prefix="/api-v1/contact", tags=["contact"])


class ContactRequest(BaseModel):
    name: constr(min_length=1)
    email: EmailStr
    message: constr(min_length=1)
    device_id: constr(min_length=1)


def send_email(name: str, email: str, message: str, device_id: str) -> None:
    """Stub function to simulate sending an email."""
    # In a real implementation, integrate with an email service here.
    print(f"Email from {name} <{email}>: {message} (device {device_id})")


@router.post("")
def send_contact_form(contact: ContactRequest):
    send_email(contact.name, contact.email, contact.message, contact.device_id)
    return {"status": "ok"}
