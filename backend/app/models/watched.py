import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Watched(Base):
    __tablename__ = "watched"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tmdb_id = Column(Integer)
    movie_title = Column(String)
    poster_path = Column(String, nullable=True)
    watched_at = Column(DateTime, default=datetime.datetime.utcnow)
    rewatch = Column(Boolean, default=False)
