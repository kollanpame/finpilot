from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.transaction import Transaction
import uuid

class TransactionService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Transaction).all() #pobierannie wszysstkich transakcji z bd

    def create(self, name: str, amount: float, user_id: uuid.UUID): #tworzenie transakcji korzystając z wprowadzonych danych
        transaction = Transaction(id=uuid.uuid4(), name=name, amount=amount, user_id=user_id)
        self.db.add(transaction) #transakcja dodana do sesji bd
        self.db.commit() #zatwierdzenie zmian
        self.db.refresh(transaction) #Odśwież objekt transakcji
        return transaction
#Usuwanie transakcji
    def delete(self, transaction_id: uuid.UUID):
        transaction = self.db.query(Transaction).filter(Transaction.id == transaction_id).first() #znajdź ją po ID
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        self.db.delete(transaction)
        self.db.commit()
        return {"message": "Transaction deleted successfully"}
    
router = APIRouter(prefix="/transactions", tags=["Transactions"])

#endpoint do pobierania wszystkich transakcji
@router.get("/")
def get_transactions(db: Session = Depends(get_db)):
    service = TransactionService(db)
    return service.get_all()

#tworzenie transakcji
@router.post("/")
def create_transaction(name: str, amount: float, user_id: uuid.UUID, db: Session = Depends(get_db)):
    service = TransactionService(db)
    return service.create(name, amount, user_id)

#usuwanie jej za ID
@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: uuid.UUID, db: Session = Depends(get_db)):
    service = TransactionService(db)
    return service.delete(transaction_id)