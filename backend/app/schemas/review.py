from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReviewCreate(BaseModel):
    tmdb_id: int
    movie_title: str
    rating: float
    comment: Optional[str] = None
    has_spoilers: bool = False
    watch_date: Optional[datetime] = None


class ReviewUpdate(BaseModel):
    rating: float
    comment: str


class ReviewResponse(ReviewCreate):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True
