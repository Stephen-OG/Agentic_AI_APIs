from pydantic import BaseModel

class Character(BaseModel):
    name: str
    personality: str
    description: str