from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.favorite import Favorite

router = APIRouter(tags=["favorites"])


@router.get("/users/{user_id}/favorites")
def get_user_favorites(user_id: int, db: Session = Depends(get_db)):
    return db.query(Favorite).filter(Favorite.user_id == user_id).order_by(Favorite.rank).all()


@router.post("/users/me/favorites")
def set_favorite(body: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tmdb_id = body.get("tmdb_id")
    movie_title = body.get("movie_title")
    poster_path = body.get("poster_path")
    rank = body.get("rank")

    if not tmdb_id or not movie_title or not rank or rank < 1 or rank > 4:
        raise HTTPException(status_code=400, detail="Invalid data. rank must be 1-4.")

    existing = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.rank == rank
    ).first()

    if existing:
        existing.tmdb_id = tmdb_id
        existing.movie_title = movie_title
        existing.poster_path = poster_path
    else:
        new_fav = Favorite(
            user_id=current_user.id,
            tmdb_id=tmdb_id,
            movie_title=movie_title,
            poster_path=poster_path,
            rank=rank
        )
        db.add(new_fav)

    db.commit()
    return {"message": "Favori enregistré"}


@router.delete("/users/me/favorites/{rank}")
def remove_favorite(rank: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    fav = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.rank == rank
    ).first()
    if not fav:
        raise HTTPException(status_code=404, detail="Favori introuvable")
    db.delete(fav)
    db.commit()
    return {"message": "Favori supprimé"}
