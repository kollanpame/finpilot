from sqlalchemy import Column, String, Float, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime, timezone
import uuid

class Transaction(Base):
    
    # Wskazujemy jak będzie nazywać się tabela w bazie danych
    __tablename__ = "transactions"

    # Tworzymy kolumny wewnątrz tabeli
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)   
    name = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.now(timezone.utc))
    amount = Column(Float, nullable=False)  
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Tworzymy relację pomiędzy tabelami.
    category = relationship("Category", back_populates="transactions")
    user = relationship("User", back_populates="transactions")
    