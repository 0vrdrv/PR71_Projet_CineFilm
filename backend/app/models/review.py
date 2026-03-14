import datetime

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    tmdb_id = Column(Integer, index=True)
    movie_title = Column(String)
    rating = Column(Float)
    comment = Column(Text, nullable=True)
    has_spoilers = Column(Boolean, default=False)
    watch_date = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="reviews")


class ReviewLike(Base):
    __tablename__ = "review_likes"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    review_id = Column(Integer, ForeignKey("reviews.id"), primary_key=True)
