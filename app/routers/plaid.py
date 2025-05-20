from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Institution  # adjust import as needed
from app.services.plaid_client import plaid_client
from fastapi import APIRouter


router = APIRouter(prefix="/plaid", tags=["Plaid"])

@router.post("/import-institutions")
async def import_institutions(db: Session = Depends(get_db)):
    request = {
        "count": 20,
        "offset": 0,
        "country_codes": ["US"]
    }

    response = plaid_client.institutions_get(request)
    institutions = response.to_dict().get("institutions", [])

    imported = 0
    for inst in institutions:
        if db.query(Institution).filter_by(id=inst["institution_id"]).first():
            continue  # Omijaj jak już istnieje

        db_institution = Institution( #Schemat za którym wpisujemy nazwy instytucji bankowych do bazy SQL
            id=inst["institution_id"],
            name=inst["name"],
            country_codes=",".join(inst["country_codes"])
        )

        db.add(db_institution)
        imported += 1

    db.commit()
    return {"imported": imported, "total_fetched": len(institutions)}