from pydantic import BaseModel, Field
from typing import List


class CandidateCreate(BaseModel):
    email: str
    first_name: str
    experience: str
    last_name: str
    desired_salary: int

class Entity(BaseModel):
    offset: int
    length: int
    type: str


class FromF(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: str
    username: str
    language_code: str


class Chat(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    type: str


class Message(BaseModel):
    message_id: int
    from_f: FromF = Field(alias='from')
    chat: Chat
    date: int
    text: str
    entities: List[Entity]


class Answer(BaseModel):
    update_id: int
    message: Message



class UserCreate(BaseModel):
    email: str
    password: str
    is_active: bool = True