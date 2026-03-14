from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.watched import Watched

router = APIRouter(tags=["watched"])


@router.post("/watched/")
def mark_as_watched(body: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tmdb_id = body.get("tmdb_id")
    movie_title = body.get("movie_title")
    poster_path = body.get("poster_path")

    existing = db.query(Watched).filter(
        Watched.user_id == current_user.id,
        Watched.tmdb_id == tmdb_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Film déjà marqué comme vu")

    watched = Watched(
        user_id=current_user.id,
        tmdb_id=tmdb_id,
        movie_title=movie_title,
        poster_path=poster_path
    )
    db.add(watched)
    db.commit()
    return {"message": "Film marqué comme vu"}


@router.delete("/watched/{tmdb_id}")
def unmark_watched(tmdb_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = db.query(Watched).filter(
        Watched.user_id == current_user.id,
        Watched.tmdb_id == tmdb_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Film non trouvé dans les vus")
    db.delete(item)
    db.commit()
    return {"message": "Marquage retiré"}


@router.get("/watched/{tmdb_id}/status")
def get_watched_status(tmdb_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing = db.query(Watched).filter(
        Watched.user_id == current_user.id,
        Watched.tmdb_id == tmdb_id
    ).first()
    return {"watched": existing is not None}


@router.get("/users/{user_id}/watched")
def get_user_watched(user_id: int, db: Session = Depends(get_db)):
    return db.query(Watched).filter(Watched.user_id == user_id).order_by(Watched.watched_at.desc()).all()


@router.get("/users/{user_id}/watched/count")
def get_watched_count(user_id: int, db: Session = Depends(get_db)):
    count = db.query(Watched).filter(Watched.user_id == user_id).count()
    return {"count": count}
