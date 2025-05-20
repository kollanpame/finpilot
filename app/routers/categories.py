from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.category import Category
import uuid

class CategoryService:
    def __init__(self, db: Session): #sesja bd
        self.db = db

    def get_all(self):
        return self.db.query(Category).all() # Pobieranie wszystkich kategorii z bazy danych

# Czy kategoria o podanej nazwie już istnieje?
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
            #Jeśli kategorii nie znaleziono:
            raise HTTPException(status_code=404, detail="Category not found")
        self.db.delete(category)
        self.db.commit()
        return {"message": "Category deleted successfully"}

# Tworzy się router FastAPI o prefixie /categories i tagu "Categories"
router = APIRouter(prefix="/categories", tags=["Categories"])

# Endpoint do pobierania wszystkich kategorii - SELECT *
@router.get("/")
def get_categories(db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.get_all()

#ENdpoint tworzący nową kategorię
@router.post("/")
def create_category(name: str, db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.create(name)

#Endpoint usuwający kategorie po ID
@router.delete("/{category_id}")
def delete_category(category_id: uuid.UUID, db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.delete(category_id)