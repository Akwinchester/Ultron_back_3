from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.dao_base import BaseDAO
from src.user.models import User
from src.user.schemas import UserCreate, UserUpdate
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class UserService:
    """
    Сервис для управления пользователями (User), предоставляющий методы для создания, обновления, получения и удаления пользователей.
    """

    def __init__(self, db: AsyncSession):
        """
        Инициализация сервиса с DAO для работы с пользователями.

        :param db: Асинхронная сессия SQLAlchemy.
        """
        self.dao = BaseDAO(db, User)

    async def create_user(self, user_data: UserCreate) -> User:
        """
        Создает нового пользователя.

        :param user_data: Данные для создания пользователя.
        :return: Созданный пользователь.
        """
        new_user = User(
            name=user_data.name,
            username=user_data.username,
            chat_id=user_data.chat_id,
            nick=user_data.nick,
            password=pwd_context.hash(user_data.password)
        )
        return await self.dao.create(new_user)


    async def get_user_by_id(self, user_id: int) -> User:
        """
        Получает пользователя по его идентификатору.

        :param user_id: Идентификатор пользователя.
        :return: Найденный пользователь, если существует.
        """
        return await self.dao.get_by_id(user_id, load_related=['friends', 'activities'])

    async def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        """
        Обновляет пользователя по его идентификатору.

        :param user_id: Идентификатор пользователя для обновления.
        :param user_data: Данные для обновления пользователя.
        :return: Обновленный пользователь.
        """
        user = await self.dao.get_by_id(user_id, load_related=['friends', 'activities'])
        if user:
            update_data = user_data.dict(exclude_unset=True)
            if 'password' in update_data:
                # Хеширование пароля перед его обновлением
                update_data['password'] = pwd_context.hash(update_data['password'])

            for field, value in update_data.items():
                setattr(user, field, value)

            return await self.dao.update(user)
        return None

    async def delete_user(self, user_id: int) -> None:
        """
        Удаляет пользователя по его идентификатору.

        :param user_id: Идентификатор пользователя для удаления.
        """
        user = await self.dao.get_by_id(user_id)
        if user:
            await self.dao.delete(user)


class AuthService:

    def __init__(self, db: AsyncSession):
        self.dao = BaseDAO(db, User)

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = await self.dao.get_user_by_username(username)
        if user is None:
            return None
        # Проверяем, совпадает ли введенный пароль с хэшированным паролем в базе данных
        if not pwd_context.verify(password, user.password):
            return None
        return user