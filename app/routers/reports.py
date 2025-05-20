from fastapi import APIRouter, Depends
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
        last_month = datetime.now() - timedelta(days=30)  # 30 days ago
        user_transactions = (
            self.db.query(Transaction)
            .filter(
                Transaction.user_id == user_id,     # Filter by specific user
                Transaction.date >= last_month      # Filter by date
            )
            .all()
        )
        total_amount = sum(t.amount for t in user_transactions)  # Total only user's amounts
        return {"total_spent": total_amount}
    
# Router FastAPI z prefixem /reports i tagiem "Reports"
router = APIRouter(prefix="/reports", tags=["Reports"])

#Endpoint do pobierania i podsumowania wydatków z ostatniego miesiąca
@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    service = ReportService(db)
    return service.get_summary()