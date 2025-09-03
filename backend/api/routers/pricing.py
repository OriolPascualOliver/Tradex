from fastapi import APIRouter

router = APIRouter(prefix="/api-v1/pricing", tags=["pricing"])

PRICING_DATA = {
    "currency": "EUR",
    "vatIncluded": False,
    "annualDiscount": 0.10,
    "solo": {"monthly": 49},
    "team": {
        "tiers": [
            {"maxSeats": 1, "price": 45},
            {"maxSeats": 2, "price": 45},
            {"maxSeats": 3, "price": 35},
            {"maxSeats": 4, "price": 33},
            {"maxSeats": 5, "price": 30},
            {"maxSeats": 6, "price": 28},
            {"maxSeats": 7, "price": 27},
            {"maxSeats": 99, "price": 27},
        ]
    },
}


@router.get("")
def get_pricing():
    return PRICING_DATA

