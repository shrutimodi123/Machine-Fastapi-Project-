from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

project_users = Table(
    "project_users",
    Base.metadata,
    Column("project_id", ForeignKey("projects.id")),
    Column("user_id", ForeignKey("users.id"))
)

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String(100))
    client_id = Column(Integer, ForeignKey("clients.id"))

    users = relationship("User", secondary=project_users)