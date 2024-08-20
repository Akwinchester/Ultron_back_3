from fastapi import APIRouter, Depends, HTTPException
from typing import List
from src.chart.schemas import ChartDataRequest, ChartResponse
from src.chart.service import ChartService
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.user.models import User
from src.user.utils import get_current_user

router = APIRouter()

@router.post("/data_for_chart", response_model=ChartResponse)
async def process_chart_data_endpoint(data: ChartDataRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Эндпоинт для обработки данных графиков на основе запроса.

    :param data: Запрос с данными для обработки.
    :param db: Асинхронная сессия SQLAlchemy.
    :return: Список обработанных данных для графиков.
    """
    service = ChartService(db)

    if data.StatusView:
        response_data = await service.formation_dataset_for_charts_rating(data.id)
    else:
        response_data = await service.formation_dataset_for_charts_only_you(data.id)

    if not response_data:
        raise HTTPException(status_code=404, detail="Data not found")

    return ChartResponse(**response_data)