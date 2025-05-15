from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.transaction import Transaction
from datetime import datetime, timedelta

class ReportService:
    def __init__(self, db: Session):
        self.db = db

    def get_summary(self):
        last_month = datetime.now() - timedelta(days=30)
        total_spent = self.db.query(Transaction).filter(Transaction.date >= last_month).all()
        total_amount = sum([t.amount for t in total_spent])
        return {"total_spent": total_amount}