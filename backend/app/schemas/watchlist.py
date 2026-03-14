from pydantic import BaseModel
from typing import Optional


class WatchlistAdd(BaseModel):
    tmdb_id: int
    movie_title: str
    poster_path: Optional[str] = None
