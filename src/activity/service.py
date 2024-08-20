from typing import List, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.dao_base import BaseDAO
from src.activity.models import Activity
from src.activity.schemas import ActivityCreate, ActivityUpdate

class ActivityService:
    """
    Сервис для управления активностями, предоставляющий методы для создания, обновления, получения и удаления активностей.
    """

    def __init__(self, db: AsyncSession):
        """
        Инициализация сервиса с DAO для работы с активностями.

        :param db: Асинхронная сессия SQLAlchemy.
        """
        self.dao = BaseDAO(db, Activity)

    async def create_activity(self, activity_data: ActivityCreate, user_id: int) -> Activity:
        """
        Создает новую активность.

        :param activity_data: Данные для создания активности.
        :param user_id: Идентификатор пользователя, который создает активность.
        :return: Созданная активность.
        """
        new_activity = Activity(
            name=activity_data.name,
            user_id=user_id,
            notification_text=activity_data.notification_text,
            status=activity_data.status
        )
        return await self.dao.create(new_activity)

    async def get_activity_by_id(self, activity_id: int) -> Optional[Activity]:
        """
        Получает активность по её идентификатору.

        :param activity_id: Идентификатор активности.
        :return: Найденная активность или None.
        """
        return await self.dao.get_by_id(activity_id, load_related=['related_activities'])

    async def get_activities_by_user(self, user_id: int, status: Optional[bool] = None) -> List[Activity]:
        """
        Получает список активностей для пользователя с опциональной фильтрацией по статусу.

        :param user_id: Идентификатор пользователя.
        :param status: Опциональный статус активности (True/False).
        :return: Список активностей.
        """
        filters = [Activity.user_id == user_id]
        if status is not None:
            filters.append(Activity.status == status)

        return await self.dao.get_all(filters=filters, load_related=['related_activities'])

    async def update_activity(self, activity_id: int, activity_data: ActivityUpdate) -> Optional[Activity]:
        """
        Обновляет активность по её идентификатору.

        :param activity_id: Идентификатор активности.
        :param activity_data: Данные для обновления активности.
        :return: Обновленная активность или None.
        """
        activity = await self.dao.get_by_id(activity_id, load_related=['related_activities'])
        if activity:
            for field, value in activity_data.dict(exclude_unset=True).items():
                setattr(activity, field, value)
            return await self.dao.update(activity)
        return None

    async def delete_activity(self, activity_id: int) -> None:
        """
        Удаляет активность по её идентификатору.

        :param activity_id: Идентификатор активности.
        """
        activity = await self.dao.get_by_id(activity_id)
        if activity:
            await self.dao.delete(activity)
