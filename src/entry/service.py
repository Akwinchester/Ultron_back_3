from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.dao_base import BaseDAO
from src.entry.models import Entry
from src.entry.schemas import EntryCreate, EntryUpdate

class EntryService:
    """
    Сервис для управления записями (Entry), предоставляющий методы для создания, обновления, получения и удаления записей.
    """

    def __init__(self, db: AsyncSession):
        """
        Инициализация сервиса с DAO для работы с записями.

        :param db: Асинхронная сессия SQLAlchemy.
        """
        self.dao = BaseDAO(db, Entry)

    async def create_entry(self, entry_data: EntryCreate, activity_id: int) -> Entry:
        """
        Создает новую запись.

        :param entry_data: Данные для создания записи.
        :param activity_id: Идентификатор активности, к которой относится запись.
        :return: Созданная запись.
        """
        new_entry = Entry(
            activity_id=activity_id,
            amount=entry_data.amount,
            description=entry_data.description,
            date_added=entry_data.date_added
        )
        return await self.dao.create(new_entry)

    async def create_entries_bulk(self, entries_data: List[EntryCreate], activity_id: int) -> List[Entry]:
        """
        Массовое создание записей.

        :param entries_data: Список данных для создания записей.
        :param activity_id: Идентификатор активности, к которой относятся записи.
        :return: Список созданных записей.
        """
        entries = [
            Entry(
                activity_id=activity_id,
                amount=data.amount,
                description=data.description,
                date_added=data.date_added
            ) for data in entries_data
        ]
        return await self.dao.create_bulk(entries)

    async def get_entry_by_id(self, entry_id: int) -> Entry:
        """
        Получает запись по её идентификатору.

        :param entry_id: Идентификатор записи.
        :return: Найденная запись, если существует.
        """
        return await self.dao.get_by_id(entry_id)

    async def update_entry(self, entry_id: int, entry_data: EntryUpdate) -> Entry:
        """
        Обновляет запись по её идентификатору.

        :param entry_id: Идентификатор записи для обновления.
        :param entry_data: Данные для обновления записи.
        :return: Обновленная запись.
        """
        entry = await self.dao.get_by_id(entry_id)
        if entry:
            for field, value in entry_data.dict(exclude_unset=True).items():
                setattr(entry, field, value)
            return await self.dao.update(entry)
        return None

    async def update_entries_bulk(self, entries_data: List[EntryUpdate], entry_ids: List[int]) -> List[Entry]:
        """
        Массовое обновление записей.

        :param entries_data: Список данных для обновления записей.
        :param entry_ids: Список идентификаторов записей для обновления.
        :return: Список обновленных записей.
        """
        entries = []
        for i, entry_id in enumerate(entry_ids):
            entry = await self.dao.get_by_id(entry_id)
            if entry:
                for field, value in entries_data[i].dict(exclude_unset=True).items():
                    setattr(entry, field, value)
                entries.append(entry)
        return await self.dao.update_bulk(entries)

    async def delete_entry(self, entry_id: int) -> None:
        """
        Удаляет запись по её идентификатору.

        :param entry_id: Идентификатор записи для удаления.
        """
        entry = await self.dao.get_by_id(entry_id)
        if entry:
            await self.dao.delete(entry)

    async def delete_entries_bulk(self, entry_ids: List[int]) -> None:
        """
        Массовое удаление записей по их идентификаторам.

        :param entry_ids: Список идентификаторов записей для удаления.
        """
        await self.dao.delete_by_ids(entry_ids)
