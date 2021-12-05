from sqlalchemy import Column, String, Boolean

from app.models import Base


class ApiKey(Base):
    __tablename__ = 'api_key'

    key = Column(String, nullable=False)
    quota_exhausted = Column(Boolean, default=False)
