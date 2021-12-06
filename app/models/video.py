from datetime import date, timedelta

from sqlalchemy import Column, String, DateTime
from sqlalchemy import func

from app.models import Base


class Video(Base):
    __tablename__ = 'video'

    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)
    thumbnail_url = Column(String)
    published_on = Column(DateTime)

    @classmethod
    def add_video(cls, **doc):
        video = cls(**doc)
        return video

    @classmethod
    def apply_similarity(cls, session, title, description):
        print("_"*100, title, description)
        # title = [title]
        # even ilike will work here
        if title and not description:
            # title = str('tea')
            print("inside if")
            rows = (
                session.query(
                    cls,
                    func.similarity(title, cls.title).label('title_rank'),
                ).order_by(func.similarity(title, cls.title).desc()).all()
            )
        elif description and not title:
            print("inside elif")
            rows = (
                session.query(
                    cls,
                    func.similarity(title, cls.title).label('title_rank'),
                ).order_by(func.similarity(title, cls.title).desc()).all()
            )
        else:
            print("inside else")
            rows = (
                session.query(
                    cls,
                    func.similarity(title, cls.title).label('title_rank'),
                    func.similarity(description, cls.description).label('description_rank'),
                ).order_by(func.similarity(title, cls.title).desc()).all()
            )
        return rows

    def get_minified_json_dict(self):
        """
        For a given row of a video, returns the dict that we want to
        return in the json.
        """
        result = {
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'thumbnail_url': self.thumbnail_url,
            'published_on': self.published_on
        }
        return result
