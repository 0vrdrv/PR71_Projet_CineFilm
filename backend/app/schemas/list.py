from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MovieListItemCreate(BaseModel):
    tmdb_id: int
    movie_title: str
    poster_path: Optional[str] = None
    rank: Optional[int] = None


class MovieListItemResponse(MovieListItemCreate):
    id: int
    list_id: int

    class Config:
        from_attributes = True


class MovieListCreate(BaseModel):
    title: str
    description: Optional[str] = None
    is_public: bool = True


class MovieListResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    is_public: bool
    created_at: datetime
    user_id: int
    items: List[MovieListItemResponse] = []

    class Config:
        from_attributes = True
