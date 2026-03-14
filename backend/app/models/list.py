import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class MovieList(Base):
    __tablename__ = "movie_lists"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="movie_lists")
    items = relationship("MovieListItem", back_populates="parent_list", cascade="all, delete-orphan")


class MovieListItem(Base):
    __tablename__ = "movie_list_items"
    id = Column(Integer, primary_key=True, index=True)
    list_id = Column(Integer, ForeignKey("movie_lists.id"))

    tmdb_id = Column(Integer)
    movie_title = Column(String)
    poster_path = Column(String, nullable=True)
    rank = Column(Integer, nullable=True)

    parent_list = relationship("MovieList", back_populates="items")
