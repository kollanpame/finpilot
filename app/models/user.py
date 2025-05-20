from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base
import uuid

class User(Base):

    # Wskazujemy jak będzie nazywać się tabela w bazie danych
    __tablename__ = "users"

    # Tworzymy kolumny wewnątrz tabeli
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    plaid_user_id = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=True)

    # Tworzymy relację pomiędzy tabelami.
    transactions = relationship("Transaction", back_populates="user")
    