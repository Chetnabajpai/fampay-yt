from datetime import date, timedelta

from sqlalchemy import Column, String, DateTime

from app.models import Base


class Video(Base):
    __tablename__ = 'video'

    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    url = Column(String, nullable=False)
    thumbnail_url = Column(String)
    published_on = Column(DateTime)
