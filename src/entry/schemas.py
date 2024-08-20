from pydantic import BaseModel
from typing import Optional


# Схема для создания записи (Entry)
class EntryCreate(BaseModel):
    activity_id: int
    amount: int
    description: Optional[str] = ''
    date_added: str

# Схема для обновления записи (Entry)
class EntryUpdate(BaseModel):
    activity_id: Optional[int] = None
    amount: Optional[int] = None
    description: Optional[str] = None
    date_added: Optional[str] = None

# Схема для отображения записи (Entry)
class Entry(BaseModel):
    id: int
    activity_id: int
    amount: int
    description: str
    date_added: str

    class Config:
        from_attributes = True
