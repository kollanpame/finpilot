from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    plaid_user_id = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=True)

    transactions = relationship("Transaction", back_populates="user")
    