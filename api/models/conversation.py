from pydantic import BaseModel

class Conversations(BaseModel):
    user_id: str
    character_id: str
    messages: str