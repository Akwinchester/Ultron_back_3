from fastapi import APIRouter, Depends, HTTPException, status

from src.user.models import User
from src.user.utils import get_current_user

router = APIRouter()

@router.get("/Profile")
async def profile_endpoint(current_user: User = Depends(get_current_user)):
    """
    Эндпоинт для получения профиля пользователя.
    """
    # Заглушка для профиля пользователя
    return {"redirect_url": "/profile"}


@router.get("/home_page")
async def home_page_endpoint():
    """
    Эндпоинт для главной страницы.
    """
    # Заглушка для главной страницы
    return {"redirect_url": "/", "status": 0}


@router.get("/get_username")
async def get_username_endpoint(current_user: User = Depends(get_current_user)):
    """
    Эндпоинт для получения имени пользователя.

    :param current_user: Текущий аутентифицированный пользователь, полученный через Depends(get_current_user).
    :return: Имя пользователя.
    """
    if current_user:
        return {"userName": current_user.username}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
