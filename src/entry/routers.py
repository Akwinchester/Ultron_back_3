from fastapi import APIRouter, Depends, Path
from typing import List
from src.entry.schemas import EntryCreate, EntryUpdate, Entry
from src.entry.service import EntryService
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.user.models import User
from src.user.utils import get_current_user

router = APIRouter()

@router.post("/entries/", response_model=Entry)
async def create_entry_endpoint(entry: EntryCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Эндпоинт для создания новой записи.

    :param entry: Данные для создания записи.
    :param db: Асинхронная сессия SQLAlchemy.
    :return: Созданная запись.
    """
    service = EntryService(db)
    return await service.create_entry(entry, activity_id=entry.activity_id)

@router.post("/entries/bulk/", response_model=List[Entry])
async def create_entries_bulk_endpoint(entries: List[EntryCreate], db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Эндпоинт для массового создания записей.

    :param entries: Список данных для создания записей.
    :param db: Асинхронная сессия SQLAlchemy.
    :return: Список созданных записей.
    """
    service = EntryService(db)
    return await service.create_entries_bulk(entries, activity_id=entries[0].activity_id)

@router.put("/entries/{entry_id}", response_model=Entry)
async def update_entry_endpoint(entry_id: int, entry: EntryUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Эндпоинт для обновления записи по её идентификатору.

    :param entry_id: Идентификатор записи.
    :param entry: Данные для обновления записи.
    :param db: Асинхронная сессия SQLAlchemy.
    :return: Обновленная запись.
    """
    service = EntryService(db)
    return await service.update_entry(entry_id, entry)

@router.put("/entries/bulk/", response_model=List[Entry])
async def update_entries_bulk_endpoint(entries: List[EntryUpdate], entry_ids: List[int], db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Эндпоинт для массового обновления записей.

    :param entries: Список данных для обновления записей.
    :param entry_ids: Список идентификаторов записей.
    :param db: Асинхронная сессия SQLAlchemy.
    :return: Список обновленных записей.
    """
    service = EntryService(db)
    return await service.update_entries_bulk(entries, entry_ids)

@router.delete("/entries/{entry_id}")
async def delete_entry_endpoint(entry_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Эндпоинт для удаления записи по её идентификатору.

    :param entry_id: Идентификатор записи для удаления.
    :param db: Асинхронная сессия SQLAlchemy.
    :return: Статус операции.
    """
    service = EntryService(db)
    await service.delete_entry(entry_id)
    return {"status": "deleted"}

@router.delete("/entries/bulk/")
async def delete_entries_bulk_endpoint(entry_ids: List[int], db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Эндпоинт для массового удаления записей.

    :param entry_ids: Список идентификаторов записей для удаления.
    :param db: Асинхронная сессия SQLAlchemy.
    :return: Статус операции.
    """
    service = EntryService(db)
    await service.delete_entries_bulk(entry_ids)
    return {"status": "deleted"}
