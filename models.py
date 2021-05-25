from pydantic import BaseModel, constr
from typing import Optional


class RegisterData(BaseModel):
    login: str
    email: str


class Message(BaseModel):
    content: Optional[constr(min_length=1, max_length=160)]
