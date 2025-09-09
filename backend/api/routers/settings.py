from typing import Dict, List

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api-v1/settings", tags=["settings"])

settings_state: Dict[str, Dict] = {
    "tariffs": {},
    "provider": {},
    "prefixes": {},
    "fiscal": {},
    "branding": {},
    "email_template": {},
}


class FilesPayload(BaseModel):
    files: List[str]


@router.post("/ai/uploads")
async def ai_uploads(payload: FilesPayload):
    return {"filenames": payload.files}


@router.post("/ai/train")
async def ai_train():
    return {"status": "training"}


@router.get("/ai/status")
async def ai_status():
    return {"status": "idle"}


@router.post("/ai/reset")
async def ai_reset():
    return {"status": "reset"}


@router.get("/ai/model")
async def ai_model():
    return {"model": "default"}


class Tariffs(BaseModel):
    rate_hour: float
    min_minutes: int
    step_minutes: int
    markup_percent: float
    vat_percent: float
    travel_per_km: float


@router.put("/tariffs")
async def set_tariffs(data: Tariffs):
    settings_state["tariffs"] = data.model_dump()
    return settings_state["tariffs"]


class Provider(BaseModel):
    default_provider: str


@router.put("/provider")
async def set_provider(data: Provider):
    settings_state["provider"] = data.model_dump()
    return settings_state["provider"]


class FilePayload(BaseModel):
    file: str


@router.post("/provider/catalog")
async def upload_catalog(payload: FilePayload):
    return {"filename": payload.file}


class Prefixes(BaseModel):
    quote_prefix: str
    invoice_prefix: str
    work_prefix: str
    reset: Dict[str, int]


@router.put("/prefixes")
async def set_prefixes(data: Prefixes):
    settings_state["prefixes"] = data.model_dump()
    return settings_state["prefixes"]


class Fiscal(BaseModel):
    legal_name: str
    tax_id: str
    address: str
    city_zip: str


@router.put("/fiscal")
async def set_fiscal(data: Fiscal):
    settings_state["fiscal"] = data.model_dump()
    return settings_state["fiscal"]


@router.post("/branding/logo")
async def upload_logo(payload: FilePayload):
    return {"filename": payload.file}


class Branding(BaseModel):
    invoice_template: str
    quote_template: str


@router.put("/branding")
async def set_branding(data: Branding):
    settings_state["branding"].update(data.model_dump())
    return settings_state["branding"]


@router.get("/branding/preview")
async def branding_preview():
    return {"preview": True}


class EmailTemplate(BaseModel):
    subject: str
    body: str


@router.put("/email-template")
async def set_email_template(data: EmailTemplate):
    settings_state["email_template"] = data.model_dump()
    return settings_state["email_template"]


@router.get("")
async def get_settings():
    return settings_state

