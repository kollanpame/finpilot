from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.transaction import Transaction
from datetime import datetime, timedelta

class ReportService:
    def __init__(self, db: Session):
        self.db = db

    def get_summary(self):
        last_month = datetime.now() - timedelta(days=30) #oblicza daty sprzed ostatnie 30 dni
        total_spent = self.db.query(Transaction).filter(Transaction.date >= last_month).all() #pobiera wszystko z tego okresu
        total_amount = sum([t.amount for t in total_spent]) #Sumuje wszystkie kwoty z podanego okresu
        return {"total_spent": total_amount} #Zwrocenie wyniku słownie
    
# Router FastAPI z prefixem /reports i tagiem "Reports"
router = APIRouter(prefix="/reports", tags=["Reports"])

#Endpoint do pobierania icpodsumowania wydatków z ostatniego miesiąca
@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    service = ReportService(db)
    return service.get_summary()