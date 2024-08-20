from typing import Type, TypeVar, Generic, Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from sqlalchemy.orm import Session, joinedload, class_mapper

# Универсальный тип модели
ModelType = TypeVar("ModelType")

class BaseDAO(Generic[ModelType]):
    """
    Базовый класс для Data Access Object (DAO), который инкапсулирует базовые операции CRUD и
    поддерживает массовые операции над моделями базы данных.
    """

    def __init__(self, db: AsyncSession, model: Type[ModelType]):
        """
        Инициализация DAO с объектом базы данных и моделью.

        :param db: Асинхронная сессия SQLAlchemy.
        :param model: Класс модели SQLAlchemy.
        """
        self.db = db
        self.model = model

    async def create(self, obj: ModelType) -> ModelType:
        """
        Создает новый объект в базе данных.

        :param obj: Экземпляр модели для создания.
        :return: Созданный экземпляр модели.
        """
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def create_bulk(self, objs: List[ModelType]) -> List[ModelType]:
        """
        Массовое создание объектов в базе данных.

        :param objs: Список экземпляров моделей для создания.
        :return: Список созданных экземпляров моделей.
        """
        self.db.add_all(objs)
        await self.db.commit()
        for obj in objs:
            await self.db.refresh(obj)
        return objs

    async def get_by_id(self, id: int, load_related: Optional[List[str]] = None) -> Optional[ModelType]:
        """
        Получает объект по его идентификатору с возможностью полной загрузки связанных сущностей.

        :param id: Идентификатор объекта.
        :param load_related: Список связанных полей для полной загрузки.
        :return: Экземпляр модели, если найден, иначе None.
        """
        query = select(self.model).where(self.model.id == id)

        if load_related:
            for relation in load_related:
                query = query.options(joinedload(getattr(self.model, relation)))

        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_all(self, filters: List[Any] = [], load_related: Optional[List[str]] = None) -> List[ModelType]:
        """
        Получает все объекты данной модели из базы данных с возможностью применения фильтров и полной загрузки связанных сущностей.

        :param filters: Список фильтров для применения к запросу.
        :param load_related: Список имен связанных сущностей для загрузки (например, ['related_activities']).
        :return: Список экземпляров модели.
        """
        query = select(self.model).filter(*filters)

        if load_related:
            for relation in load_related:
                query = query.options(joinedload(getattr(self.model, relation)))

        result = await self.db.execute(query)
        result = result.scalars().unique().all()
        return result

    async def update(self, obj: ModelType) -> ModelType:
        """
        Обновляет объект в базе данных.

        :param obj: Экземпляр модели для обновления.
        :return: Обновленный экземпляр модели.
        """
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def update_bulk(self, objs: List[ModelType]) -> List[ModelType]:
        """
        Массовое обновление объектов в базе данных.

        :param objs: Список экземпляров моделей для обновления.
        :return: Список обновленных экземпляров моделей.
        """
        for obj in objs:
            self.db.add(obj)
        await self.db.commit()
        for obj in objs:
            await self.db.refresh(obj)
        return objs

    async def delete(self, obj: ModelType) -> None:
        """
        Удаляет объект из базы данных.

        :param obj: Экземпляр модели для удаления.
        """
        await self.db.delete(obj)
        await self.db.commit()

    async def delete_bulk(self, objs: List[ModelType]) -> None:
        """
        Массовое удаление объектов из базы данных.

        :param objs: Список экземпляров моделей для удаления.
        """
        for obj in objs:
            await self.db.delete(obj)
        await self.db.commit()

    async def delete_by_ids(self, ids: List[int]) -> None:
        """
        Массовое удаление объектов по их идентификаторам.

        :param ids: Список идентификаторов для удаления.
        """
        stmt = delete(self.model).where(self.model.id.in_(ids))
        await self.db.execute(stmt)
        await self.db.commit()
