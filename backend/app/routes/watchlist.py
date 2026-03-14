from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.watchlist import Watchlist
from app.schemas.watchlist import WatchlistAdd

router = APIRouter(tags=["watchlist"])


@router.post("/watchlist/")
def add_to_watchlist(item: WatchlistAdd, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing = db.query(Watchlist).filter(
        Watchlist.user_id == current_user.id,
        Watchlist.tmdb_id == item.tmdb_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Film déjà dans la watchlist")
    db_item = Watchlist(**item.dict(), user_id=current_user.id)
    db.add(db_item)
    db.commit()
    return {"message": "Ajouté à la watchlist"}


@router.delete("/watchlist/{tmdb_id}")
def remove_from_watchlist(tmdb_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = db.query(Watchlist).filter(
        Watchlist.user_id == current_user.id,
        Watchlist.tmdb_id == tmdb_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Film introuvable dans la watchlist")
    db.delete(item)
    db.commit()
    return {"message": "Retiré de la watchlist"}


@router.get("/watchlist/{tmdb_id}/status")
def get_watchlist_status(tmdb_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing = db.query(Watchlist).filter(
        Watchlist.user_id == current_user.id,
        Watchlist.tmdb_id == tmdb_id
    ).first()
    return {"in_watchlist": existing is not None}


@router.get("/users/{user_id}/watchlist")
def get_user_watchlist(user_id: int, db: Session = Depends(get_db)):
    return db.query(Watchlist).filter(Watchlist.user_id == user_id).order_by(Watchlist.added_at.desc()).all()
