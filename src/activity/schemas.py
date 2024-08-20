from pydantic import BaseModel
from typing import List, Optional

# Схема для создания активности
class ActivityCreate(BaseModel):
    user_id: int
    name: str
    notification_text: Optional[str] = ''
    status: Optional[bool] = True

# Схема для обновления активности
class ActivityUpdate(BaseModel):
    name: Optional[str] = None
    notification_text: Optional[str] = None
    status: Optional[bool] = None


class RelatedActivity(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

# Схема для отображения активности
class Activity(BaseModel):
    id: int
    name: str
    user_id: int
    notification_text: str
    status: bool


class ActivityFull(Activity):
    related_activities: List[RelatedActivity]

    class Config:
        from_attributes = True
