from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base
import uuid

class Category(Base):

    # Wskazujemy jak będzie nazywać się tabela w bazie danych
    __tablename__ = "categories"

    # Tworzymy kolumny wewnątrz tabeli
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, unique=True, nullable=False)

    # Tworzymy relację pomiędzy tabelami.
    transactions = relationship("Transaction", back_populates="category")
