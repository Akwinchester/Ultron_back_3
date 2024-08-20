from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base
from src.models import TimestampMixin



class Entry(Base, TimestampMixin):
    __tablename__ = 'entry'

    id = Column(Integer, primary_key=True)
    activity_id = Column(Integer, ForeignKey('activity.id'))
    amount = Column(Integer)
    description = Column(String(300), default='')
    date_added = Column(String)
    # activity = relationship("Activity", back_populates="entries")