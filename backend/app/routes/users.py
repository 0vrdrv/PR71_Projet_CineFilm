from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.user import User, Follow
from app.models.review import Review
from app.models.watchlist import Watchlist
from app.models.list import MovieList
from app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/search", response_model=list[UserResponse])
def search_users(q: str = Query("", min_length=1), db: Session = Depends(get_db)):
    return db.query(User).filter(User.username.ilike(f"%{q}%")).all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return user


@router.get("/{user_id}/stats")
def get_user_stats(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    total_reviews = db.query(Review).filter(Review.user_id == user_id).count()
    avg_rating = db.query(func.avg(Review.rating)).filter(Review.user_id == user_id).scalar()
    watchlist_count = db.query(Watchlist).filter(Watchlist.user_id == user_id).count()
    lists_count = db.query(MovieList).filter(MovieList.user_id == user_id).count()
    followers_count = db.query(Follow).filter(Follow.followed_id == user_id).count()
    following_count = db.query(Follow).filter(Follow.follower_id == user_id).count()

    return {
        "total_reviews": total_reviews,
        "average_rating": round(float(avg_rating), 1) if avg_rating else 0,
        "watchlist_count": watchlist_count,
        "lists_count": lists_count,
        "followers_count": followers_count,
        "following_count": following_count,
    }


@router.get("/{user_id}/stats/detailed")
def get_detailed_stats(user_id: int, db: Session = Depends(get_db)):
    from app.models.watched import Watched

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    total_watched = db.query(Watched).filter(Watched.user_id == user_id).count()
    total_reviews = db.query(Review).filter(Review.user_id == user_id).count()
    avg_rating = db.query(func.avg(Review.rating)).filter(Review.user_id == user_id).scalar()
    watchlist_count = db.query(Watchlist).filter(Watchlist.user_id == user_id).count()
    lists_count = db.query(MovieList).filter(MovieList.user_id == user_id).count()
    followers_count = db.query(Follow).filter(Follow.followed_id == user_id).count()
    following_count = db.query(Follow).filter(Follow.follower_id == user_id).count()

    rating_distribution = {}
    for val in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]:
        count = db.query(Review).filter(Review.user_id == user_id, Review.rating == val).count()
        rating_distribution[str(val)] = count

    return {
        "total_watched": total_watched,
        "total_reviews": total_reviews,
        "average_rating": round(float(avg_rating), 1) if avg_rating else 0,
        "rating_distribution": rating_distribution,
        "watchlist_count": watchlist_count,
        "lists_count": lists_count,
        "followers_count": followers_count,
        "following_count": following_count,
        "hours_watched": total_watched * 120,
    }


@router.post("/{followed_id}/follow")
def follow_user(followed_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if followed_id == current_user.id:
        raise HTTPException(status_code=400, detail="Tu ne peux pas te suivre toi-même.")
    user_to_follow = db.query(User).filter(User.id == followed_id).first()
    if not user_to_follow:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    existing = db.query(Follow).filter(
        Follow.follower_id == current_user.id,
        Follow.followed_id == followed_id
    ).first()
    if existing:
        return {"message": "Tu suis déjà cet utilisateur.", "following": True}
    new_follow = Follow(follower_id=current_user.id, followed_id=followed_id)
    db.add(new_follow)
    db.commit()
    return {"message": f"Utilisateur {followed_id} suivi avec succès !", "following": True}


@router.delete("/{followed_id}/follow")
def unfollow_user(followed_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing = db.query(Follow).filter(
        Follow.follower_id == current_user.id,
        Follow.followed_id == followed_id
    ).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Tu ne suis pas cet utilisateur.")
    db.delete(existing)
    db.commit()
    return {"message": "Utilisateur unfollowed.", "following": False}


@router.get("/{user_id}/follow/status")
def get_follow_status(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing = db.query(Follow).filter(
        Follow.follower_id == current_user.id,
        Follow.followed_id == user_id
    ).first()
    return {"following": existing is not None}


@router.get("/{user_id}/followers", response_model=list[UserResponse])
def get_followers(user_id: int, db: Session = Depends(get_db)):
    follower_ids = db.query(Follow.follower_id).filter(Follow.followed_id == user_id).all()
    ids = [f[0] for f in follower_ids]
    return db.query(User).filter(User.id.in_(ids)).all()


@router.get("/{user_id}/following", response_model=list[UserResponse])
def get_following(user_id: int, db: Session = Depends(get_db)):
    following_ids = db.query(Follow.followed_id).filter(Follow.follower_id == user_id).all()
    ids = [f[0] for f in following_ids]
    return db.query(User).filter(User.id.in_(ids)).all()
