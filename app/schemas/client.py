from pydantic import BaseModel

class ClientCreate(BaseModel):
    client_name: str