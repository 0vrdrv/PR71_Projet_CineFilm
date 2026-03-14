import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Watchlist(Base):
    __tablename__ = "watchlist"
    id = Column(Integer, primary_key=True, index=True)
    tmdb_id = Column(Integer)
    movie_title = Column(String)
    poster_path = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    added_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="watchlists")
