from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.transaction import Transaction
from app.models.user import User
from datetime import datetime, timedelta
import uuid

class ReportService:
    def __init__(self, db: Session):
        self.db = db

    def get_summary(self, user_id: uuid.UUID):
        # Sprawdzenie, czy użytkownik istnieje
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Obliczenie daty sprzed 30 dni
        last_month = datetime.now() - timedelta(days=30)

        # Pobranie transakcji danego użytkownika z ostatnich 30 dni
        transactions = (
            self.db.query(Transaction)
            .filter(Transaction.user_id == user_id, Transaction.date >= last_month)
            .all()
        )

        # Sumowanie wydatków
        total_amount = sum([t.amount for t in transactions])
        return {"total_spent": total_amount}
    
# Router FastAPI z prefixem /reports i tagiem "Reports"
router = APIRouter(prefix="/reports", tags=["Reports"])

#Endpoint do pobierania i podsumowania wydatków z ostatniego miesiąca
@router.get("/summary")
def get_user_summary(user_id: uuid.UUID, db: Session = Depends(get_db)):
    service = ReportService(db)
    return service.get_summary(user_id)