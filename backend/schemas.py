from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --- USERS & AUTH ---
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# --- REVIEWS ---
class ReviewCreate(BaseModel):
    tmdb_id: int
    movie_title: str
    rating: float
    comment: Optional[str] = None
    has_spoilers: bool = False
    watch_date: Optional[datetime] = None
    

class ReviewResponse(ReviewCreate):
    id: int
    created_at: datetime
    user_id: int 
    class Config:
        from_attributes = True

# --- WATCHLIST ---
class WatchlistAdd(BaseModel):
    tmdb_id: int
    movie_title: str
    poster_path: Optional[str] = None


# --- LISTES PERSONNALISÉES ---
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