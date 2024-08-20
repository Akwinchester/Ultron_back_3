from typing import List, Dict, Optional
from pydantic import BaseModel

class ChartDataRequest(BaseModel):
    """
    Схема для запроса данных графика от клиента.
    """
    id: int
    StatusView: bool

    class Config:
        from_attributes = True  # Используется вместо orm_mode в Pydantic v2


class ChartDataEntry(BaseModel):
    """
    Схема для представления данных графика по каждому пользователю.
    """
    entry_id: List[Optional[int]]  # Список идентификаторов записей, может содержать None
    amount: List[int]  # Список значений по датам
    description: List[Optional[str]]  # Список описаний по датам

    class Config:
        from_attributes = True  # Используется вместо orm_mode в Pydantic v2


class ChartResponse(BaseModel):
    """
    Схема для ответа с данными графика.
    """
    date: List[str]  # Список дат
    amount: Dict[int, List[int]]  # Словарь с ключами user_id и значениями списков amount по датам
    entry_id: Dict[int, List[Optional[int]]]  # Словарь с ключами user_id и значениями списков entry_id по датам
    description: Dict[int, List[Optional[str]]]  # Словарь с ключами user_id и значениями списков description по датам
    user_id: List[int]  # Список user_id
    name: Dict[int, str]  # Словарь с ключами user_id и значениями имен пользователей

    class Config:
        from_attributes = True  # Используется вместо orm_mode в Pydantic v2
