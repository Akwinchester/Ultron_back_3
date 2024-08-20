from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base
from src.models import TimestampMixin, user_friend, user_activity
from passlib.context import CryptContext


class User(Base, TimestampMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    username = Column(String(50), unique=True, nullable=False)
    chat_id = Column(String(50))
    password = Column(String(128), nullable=False)
    nick = Column(String(50), default='')
    refresh_token = Column(String, nullable=True)

    activities = relationship('Activity', secondary=user_activity, backref='users', lazy='joined')
    friends = relationship('User',
                           secondary=user_friend,
                           primaryjoin=(id == user_friend.c.user_id),
                           secondaryjoin=(id == user_friend.c.friend_id),
                           backref='user_friends', lazy='joined')

    def add_friend(self, friend):
        if friend not in self.friends:
            self.friends.append(friend)
            friend.friends.append(self)

    def remove_friend(self, friend):
        if friend in self.friends:
            self.friends.remove(friend)
            friend.friends.remove(self)

    def verify_password(self, password: str) -> bool:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(password, self.password)


    def __repr__(self):
        return f'<User {self.username}>'