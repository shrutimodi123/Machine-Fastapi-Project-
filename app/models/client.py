from sqlalchemy import Column, Integer, String
from app.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(100))
    created_by = Column(Integer)