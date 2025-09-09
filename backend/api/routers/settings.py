from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api-v1/settings", tags=["settings"])

SETTINGS_STORE = {
    "ai": {"status": "idle", "model": "default"},
    "tariffs": {},
    "provider": {},
    "prefixes": {},
    "fiscal": {},
    "branding": {},
    "email_template": {},
}


class FilesPayload(BaseModel):
    files: list[str]


@router.post("/ai/uploads")
def ai_uploads(payload: FilesPayload):
    return {"uploaded": len(payload.files)}


@router.post("/ai/train")
def ai_train():
    SETTINGS_STORE["ai"]["status"] = "training"
    return {"status": "training"}


@router.get("/ai/status")
def ai_status():
    return {"status": SETTINGS_STORE["ai"].get("status", "idle")}


@router.post("/ai/reset")
def ai_reset():
    SETTINGS_STORE["ai"]["status"] = "idle"
    return {"status": "reset"}


@router.get("/ai/model")
def ai_model():
    return {"model": SETTINGS_STORE["ai"].get("model", "default")}


class Tariffs(BaseModel):
    rate_hour: float
    min_minutes: int
    step_minutes: int
    markup_percent: float
    vat_percent: float
    travel_per_km: float


@router.put("/tariffs")
def put_tariffs(data: Tariffs):
    SETTINGS_STORE["tariffs"] = data.model_dump()
    return SETTINGS_STORE["tariffs"]


class Provider(BaseModel):
    default_provider: str


@router.put("/provider")
def put_provider(data: Provider):
    SETTINGS_STORE["provider"] = data.model_dump()
    return SETTINGS_STORE["provider"]


class FilePayload(BaseModel):
    file: str


@router.post("/provider/catalog")
def provider_catalog(payload: FilePayload):
    return {"filename": payload.file}


class Prefixes(BaseModel):
    quote_prefix: str
    invoice_prefix: str
    work_prefix: str
    reset: dict


@router.put("/prefixes")
def put_prefixes(data: Prefixes):
    SETTINGS_STORE["prefixes"] = data.model_dump()
    return SETTINGS_STORE["prefixes"]


class Fiscal(BaseModel):
    legal_name: str
    tax_id: str
    address: str
    city_zip: str


@router.put("/fiscal")
def put_fiscal(data: Fiscal):
    SETTINGS_STORE["fiscal"] = data.model_dump()
    return SETTINGS_STORE["fiscal"]


@router.post("/branding/logo")
def branding_logo(payload: FilePayload):
    return {"filename": payload.file}


class Branding(BaseModel):
    invoice_template: str
    quote_template: str


@router.put("/branding")
def put_branding(data: Branding):
    SETTINGS_STORE["branding"] = data.model_dump()
    return SETTINGS_STORE["branding"]


@router.get("/branding/preview")
def branding_preview():
    return {"preview": True}


class EmailTemplate(BaseModel):
    subject: str
    body: str


@router.put("/email-template")
def put_email_template(data: EmailTemplate):
    SETTINGS_STORE["email_template"] = data.model_dump()
    return SETTINGS_STORE["email_template"]


@router.get("")
def get_settings():
    return SETTINGS_STORE
