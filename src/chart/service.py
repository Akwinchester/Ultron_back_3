from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from datetime import timedelta
from typing import List, Dict

from src.activity.models import Activity
from src.chart.utils import make_dataset, make_dataset_only_you
from src.dao_base import BaseDAO
from src.entry.models import Entry
from src.user.models import User


class ChartService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.entry_dao = BaseDAO(db, Entry)
        self.activity_dao = BaseDAO(db, Activity)

    async def formation_dataset_for_charts_only_you(self, activity_id: int) -> Dict[str, List]:
        print('только ты')
        query = (
            select(
                Entry.id.label('entry_id'),
                User.username.label('user_name'),
                User.id.label('user_id'),
                Entry.amount,
                Entry.date_added,
                Entry.description
            )
            .join(Activity, Entry.activity_id == Activity.id)
            .filter(Entry.activity_id == activity_id)
            .join(User, Activity.user_id == User.id)
        )

        result = await self.db.execute(query)
        data = result.all()
        print(data)

        dataset = make_dataset_only_you(data) if data else []
        return dataset

    async def formation_dataset_for_charts_rating(self, activity_id: int) -> Dict[str, List]:
        print('рейтинг')
        activity_ids = await self.get_related_activity_ids(activity_id)
        print(activity_ids)

        query = (
            select(
                Entry.id.label('entry_id'),
                User.username.label('user_name'),
                User.id.label('user_id'),
                Entry.amount,
                Entry.date_added,
                Entry.description
            )
            .join(Activity, Entry.activity_id == Activity.id)
            .filter(Entry.activity_id.in_(activity_ids))
            .join(User, Activity.user_id == User.id)
        )

        result = await self.db.execute(query)
        data = result.all()

        formatted_data = [
            {
                'id_user': row.user_id,
                'id_entry': row.entry_id,
                'name': row.user_name,
                'amount': row.amount,
                'date_added': str(row.date_added),
                'description': row.description
            }
            for row in data
        ]

        dataset = make_dataset(formatted_data) if formatted_data else []
        return dataset

    async def get_related_activity_ids(self, activity_id: int) -> List[int]:
        # Здесь нужно реализовать логику получения связанных активностей
        # Предполагается, что будет возвращен список идентификаторов связанных активностей
        activity = await self.activity_dao.get_by_id(activity_id, load_related=['related_activities'])
        related_activities = []
        if activity.related_activities:
            for related_activity in activity.related_activities:
                related_activities.append(related_activity)
        return [activity.id for activity in related_activities] + [activity_id]
