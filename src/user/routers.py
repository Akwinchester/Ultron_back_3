from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.user.schemas import UserCreate, UserUpdate, User, Token, UserFull
from src.user.service import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.user.utils import get_user_by_username, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_user, \
    create_refresh_token, verify_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/register", response_model=User)
async def create_user_endpoint(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Эндпоинт для создания нового пользователя.

    :param user: Данные для создания пользователя.
    :param db: Асинхронная сессия SQLAlchemy.
    :return: Созданный пользователь.
    """
    service = UserService(db)
    new_user = await service.create_user(user)
    return new_user


@router.get("/{user_id}", response_model=UserFull)
async def get_user_by_id_endpoint(user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Эндпоинт для получения пользователя по его идентификатору.

    :param user_id: Идентификатор пользователя.
    :param db: Асинхронная сессия SQLAlchemy.
    :return: Найденный пользователь.
    """
    service = UserService(db)
    return await service.get_user_by_id(user_id)

@router.put("/{user_id}", response_model=UserFull)
async def update_user_endpoint(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Эндпоинт для обновления пользователя по его идентификатору.

    :param user_id: Идентификатор пользователя.
    :param user: Данные для обновления пользователя.
    :param db: Асинхронная сессия SQLAlchemy.
    :return: Обновленный пользователь.
    """
    service = UserService(db)
    return await service.update_user(user_id, user)

@router.delete("/{user_id}")
async def delete_user_endpoint(user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Эндпоинт для удаления пользователя по его идентификатору.

    :param user_id: Идентификатор пользователя для удаления.
    :param db: Асинхронная сесссия SQLAlchemy.
    :return: Статус операции.
    """
    service = UserService(db)
    await service.delete_user(user_id)
    return {"status": "deleted"}


@router.post("/login", response_model=Token)
async def login_for_access_token(db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user_by_username(db, form_data.username)
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    # Создание и сохранение рефреш токена
    refresh_token = await create_refresh_token(data={"sub": user.username})
    user.refresh_token = refresh_token
    db.add(user)
    await db.commit()

    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}


@router.post("/refresh", response_model=Token)
async def refresh_access_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    """
    Эндпоинт для обновления access token используя refresh token.

    :param refresh_token: Рефреш токен для обновления access token.
    :param db: Асинхронная сессия SQLAlchemy.
    :return: Новый access token и рефреш токен.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = await verify_token(refresh_token, credentials_exception)
    user = await get_user_by_username(db, token_data.username)

    if user is None or user.refresh_token != refresh_token:
        raise credentials_exception

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    # Генерация нового рефреш токена
    new_refresh_token = await create_refresh_token(data={"sub": user.username})
    user.refresh_token = new_refresh_token
    db.add(user)
    await db.commit()

    return {"access_token": access_token, "token_type": "bearer", "refresh_token": new_refresh_token}