from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Follow(Base):
    __tablename__ = "follows"
    follower_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    followed_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ReviewLike(Base):
    __tablename__ = "review_likes"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    review_id = Column(Integer, ForeignKey("reviews.id"), primary_key=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    bio = Column(Text, nullable=True)
    
    reviews = relationship("Review", back_populates="owner")
    watchlists = relationship("Watchlist", back_populates="owner")
    movie_lists = relationship("MovieList", back_populates="owner")

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

class Watchlist(Base):
    __tablename__ = "watchlist"
    id = Column(Integer, primary_key=True, index=True)
    tmdb_id = Column(Integer)
    movie_title = Column(String)
    poster_path = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    added_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    owner = relationship("User", back_populates="watchlists")

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