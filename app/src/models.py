from sqlalchemy import Column, Integer, String

from db import Base


class User(Base):
    __tablename__ = "user_profile"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    avatar = Column(String)
    age = Column(Integer)
