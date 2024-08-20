from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from src.database import Base
from src.models import TimestampMixin


activity_activity = Table('activity_activity', Base.metadata,
    Column('activity_one_id', Integer, ForeignKey('activity.id'), primary_key=True),
    Column('activity_two_id', Integer, ForeignKey('activity.id'), primary_key=True)
)


class Activity(Base, TimestampMixin):
    __tablename__ = 'activity'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    user_id = Column(Integer, ForeignKey('user.id'))
    notification_text = Column(String(500), default='')
    status = Column(Boolean, default=True)
    # entries = relationship("Entry", back_populates="activity")

    related_activities = relationship('Activity',
                                      secondary=activity_activity,
                                      primaryjoin=id == activity_activity.c.activity_one_id,
                                      secondaryjoin=id == activity_activity.c.activity_two_id,
                                      backref='related_to')
