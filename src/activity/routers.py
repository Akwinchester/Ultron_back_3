from fastapi import APIRouter, Depends, Path
from typing import List, Optional
from src.activity.schemas import ActivityCreate, ActivityUpdate, Activity, ActivityFull
from src.activity.service import ActivityService
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.user.models import User
from src.user.utils import get_current_user

router = APIRouter()

@router.post("/activities/", response_model=Activity)
async def create_activity_endpoint(activity: ActivityCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Эндпоинт для создания новой активности.

    :param activity: Данные для создания активности.
    :param db: Асинхронная сессия SQLAlchemy.
    :return: Созданная активность.
    """
    service = ActivityService(db)
    return await service.create_activity(activity, user_id=current_user.id)


@router.get("/activities/{activity_id}", response_model=ActivityFull)
async def get_activity_by_id_endpoint(activity_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Эндпоинт для получения активности по её идентификатору.

    :param activity_id: Идентификатор активности.
    :param db: Асинхронная сессия SQLAlchemy.
    :return: Найденная активность.
    """
    service = ActivityService(db)
    return await service.get_activity_by_id(activity_id)


@router.get("/activities/", response_model=List[ActivityFull])
async def get_activities_by_user_endpoint(db: AsyncSession = Depends(get_db), status: Optional[bool] = None, current_user: User = Depends(get_current_user)):
    """
    Эндпоинт для получения списка активностей с возможностью фильтрации по статусу.

    :param db: Асинхронная сессия SQLAlchemy.
    :param status: Фильтр по статусу активности (опционально).
    :return: Список активностей.
    """
    service = ActivityService(db)
    activities = await service.get_activities_by_user(user_id=current_user.id, status=status)
    return activities


@router.put("/activities/{activity_id}", response_model=ActivityFull)
async def update_activity_endpoint(activity_id: int, activity: ActivityUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Эндпоинт для обновления активности по её идентификатору.

    :param activity_id: Идентификатор активности.
    :param activity: Данные для обновления активности.
    :param db: Асинхронная сессия SQLAlchemy.
    :return: Обновленная активность.
    """
    service = ActivityService(db)
    return await service.update_activity(activity_id, activity)


@router.delete("/activities/{activity_id}")
async def delete_activity_endpoint(activity_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Эндпоинт для удаления активности по её идентификатору.

    :param activity_id: Идентификатор активности для удаления.
    :param db: Асинхронная сессия SQLAlchemy.
    :return: Статус операции.
    """
    service = ActivityService(db)
    await service.delete_activity(activity_id)
    return {"status": "deleted"}
