from sqlalchemy import Column, String
from app.db.database import Base

class Institution(Base):
    __tablename__ = "institutions"

    id = Column(String, primary_key=True, index=True)  # Plaid institution_id
    name = Column(String, nullable=False)
    country_codes = Column(String)  # Zapisz jako listę