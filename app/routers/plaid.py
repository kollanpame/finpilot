from fastapi import APIRouter
from app.services.plaid_client import plaid_client

router = APIRouter(prefix="/plaid", tags=["Plaid"])

@router.get("/institutions")
async def list_institutions():
    # Пример запроса — получаем список банков
    request = {
        "count": 10,
        "offset": 0,
        "country_codes": ["US"]
    }
    response = plaid_client.institutions_get(request)
    return response.to_dict()