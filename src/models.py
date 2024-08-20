from src.database import Base
from sqlalchemy import Column, Integer, Boolean, ForeignKey, Table, DateTime, func
from sqlalchemy.ext.declarative import declared_attr


class TimestampMixin:
    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), server_default=func.now())

    @declared_attr
    def updated_at(cls):
        return Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


user_activity = Table('user_activity', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('activity_id', Integer, ForeignKey('activity.id'), primary_key=True),
    Column('address', Boolean, default=False),
    Column('add_entry', Boolean, default=False)
)

user_friend = Table('user_friend', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('friend_id', Integer, ForeignKey('user.id'), primary_key=True)
)



