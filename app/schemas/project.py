from pydantic import BaseModel
from typing import List

class ProjectCreate(BaseModel):
    project_name: str
    client_id: int
    users: List[int]