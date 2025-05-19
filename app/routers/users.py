from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
import uuid

# Klasa odpowiedzialna za logikę biznesową użytkowników
class UserService:
    def __init__(self, db: Session):
        self.db = db

    # Pobieranie wszystkich użytkowników
    def get_all(self):
        return self.db.query(User).all()

    # Tworzenie nowego użytkownika
    def create(self, plaid_user_id: str, email: str = None):
        # Sprawdzenie, czy użytkownik już istnieje
        if self.db.query(User).filter(User.plaid_user_id == plaid_user_id).first():
            raise HTTPException(status_code=400, detail="User already exists")
        user = User(id=uuid.uuid4(), plaid_user_id=plaid_user_id, email=email)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    # Usunięcie użytkownika
    def delete(self, user_id: uuid.UUID):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        self.db.delete(user)
        self.db.commit()
        return {"message": "User deleted successfully"}

# Router FastAPI dla użytkowników
router = APIRouter(prefix="/users", tags=["Users"])

# Endpoint: pobranie wszystkich użytkowników
@router.get("/")
def get_users(db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_all()

# Endpoint: utworzenie nowego użytkownika
@router.post("/")
def create_user(plaid_user_id: str, email: str = None, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.create(plaid_user_id, email)

# Endpoint: usunięcie użytkownika po ID
@router.delete("/{user_id}")
def delete_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.delete(user_id)
