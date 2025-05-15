from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.category import Category
import uuid

class CategoryService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Category).all()

    def create(self, name: str):
        if self.db.query(Category).filter(Category.name == name).first():
            raise HTTPException(status_code=400, detail="Category already exists")
        category = Category(id=uuid.uuid4(), name=name)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, category_id: uuid.UUID):
        category = self.db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        self.db.delete(category)
        self.db.commit()
        return {"message": "Category deleted successfully"}

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/")
def get_categories(db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.get_all()

@router.post("/")
def create_category(name: str, db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.create(name)

@router.delete("/{category_id}")
def delete_category(category_id: uuid.UUID, db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.delete(category_id)