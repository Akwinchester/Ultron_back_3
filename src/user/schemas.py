from pydantic import BaseModel
from typing import List, Optional

# Схема для создания пользователя (User)
class UserCreate(BaseModel):
    name: str
    username: str
    chat_id: Optional[str] = None
    password: str
    nick: Optional[str] = None

# Схема для обновления пользователя (User)
class UserUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    chat_id: Optional[str] = None
    password: Optional[str] = None
    nick: Optional[str] = None

# Схема для отображения пользователя (User)
class User(BaseModel):
    id: int
    name: str
    username: str
    chat_id: Optional[str] = None
    nick: Optional[str] = None


class UserFull(User):
    activities: List['Activity'] = []
    friends: List['User'] = []

    class Config:
        from_attributes = True

    # Схема для отображения активности (Activity), используемая в схеме User
class Activity(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

