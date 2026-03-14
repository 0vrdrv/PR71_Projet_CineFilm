import requests
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.config import TMDB_API_KEY
from app.dependencies import get_db
from app.models.user import User

router = APIRouter(prefix="/api/tmdb", tags=["tmdb"])

TMDB_BASE_URL = "https://api.themoviedb.org/3"


def _tmdb_get(path: str, params: dict | None = None) -> dict:
    request_params = {"api_key": TMDB_API_KEY, "language": "fr-FR"}
    if params:
        request_params.update(params)
    response = requests.get(f"{TMDB_BASE_URL}{path}", params=request_params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Erreur TMDB")
    return response.json()


@router.get("/popular")
def tmdb_popular(page: int = 1):
    return _tmdb_get("/movie/popular", {"page": page})


@router.get("/now_playing")
def tmdb_now_playing(page: int = 1):
    return _tmdb_get("/movie/now_playing", {"page": page})


@router.get("/trending")
def tmdb_trending():
    return _tmdb_get("/trending/movie/week")


@router.get("/genres")
def tmdb_genres():
    return _tmdb_get("/genre/movie/list")


@router.get("/discover")
def tmdb_discover(
    page: int = 1,
    sort_by: str = "popularity.desc",
    with_genres: str = "",
    primary_release_year: str = "",
):
    params: dict = {"page": page, "sort_by": sort_by}
    if with_genres:
        params["with_genres"] = with_genres
    if primary_release_year:
        params["primary_release_year"] = primary_release_year
    return _tmdb_get("/discover/movie", params)


@router.get("/search")
def tmdb_search(query: str = ""):
    return _tmdb_get("/search/movie", {"query": query, "page": 1})


@router.get("/movie/{movie_id}")
def tmdb_movie_detail(movie_id: int):
    return _tmdb_get(f"/movie/{movie_id}")


@router.get("/movie/{movie_id}/credits")
def tmdb_movie_credits(movie_id: int):
    return _tmdb_get(f"/movie/{movie_id}/credits")


@router.get("/movie/{movie_id}/providers")
def tmdb_watch_providers(movie_id: int):
    return _tmdb_get(f"/movie/{movie_id}/watch/providers")


@router.get("/movie/{movie_id}/similar")
def tmdb_movie_similar(movie_id: int):
    return _tmdb_get(f"/movie/{movie_id}/similar")


@router.get("/search/global")
def global_search(q: str = "", db: Session = Depends(get_db)):
    users = db.query(User).filter(User.username.ilike(f"%{q}%")).limit(5).all()
    user_results = [{"id": u.id, "username": u.username, "email": u.email} for u in users]
    tmdb_results = _tmdb_get("/search/movie", {"query": q, "page": 1}) if q else {"results": []}
    return {"users": user_results, "movies": tmdb_results.get("results", [])[:10]}
