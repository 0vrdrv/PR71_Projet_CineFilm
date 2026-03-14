from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.user import User, Follow
from app.models.review import Review, ReviewLike
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewResponse

router = APIRouter(tags=["reviews"])


@router.post("/reviews/", response_model=ReviewResponse)
def create_review(review: ReviewCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_review = Review(**review.dict(), user_id=current_user.id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@router.get("/users/{user_id}/diary", response_model=list[ReviewResponse])
def get_user_diary(user_id: int, db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.user_id == user_id).order_by(Review.watch_date.desc()).all()


@router.get("/movies/{tmdb_id}/reviews")
def get_movie_reviews(tmdb_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.tmdb_id == tmdb_id).order_by(Review.created_at.desc()).all()
    result = []
    for r in reviews:
        user = db.query(User).filter(User.id == r.user_id).first()
        likes_count = db.query(ReviewLike).filter(ReviewLike.review_id == r.id).count()
        result.append({
            "id": r.id,
            "tmdb_id": r.tmdb_id,
            "movie_title": r.movie_title,
            "rating": r.rating,
            "comment": r.comment,
            "has_spoilers": r.has_spoilers,
            "user_id": r.user_id,
            "username": user.username if user else "Utilisateur inconnu",
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "likes_count": likes_count,
        })
    return result


@router.get("/movies/{tmdb_id}/stats")
def get_movie_stats(tmdb_id: int, db: Session = Depends(get_db)):
    from sqlalchemy import func
    from app.models.watchlist import Watchlist
    from app.models.watched import Watched

    total_reviews = db.query(Review).filter(Review.tmdb_id == tmdb_id).count()
    avg_rating = db.query(func.avg(Review.rating)).filter(Review.tmdb_id == tmdb_id).scalar()
    total_watched = db.query(Watched).filter(Watched.tmdb_id == tmdb_id).count()
    total_watchlisted = db.query(Watchlist).filter(Watchlist.tmdb_id == tmdb_id).count()

    rating_distribution = {}
    for val in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]:
        count = db.query(Review).filter(Review.tmdb_id == tmdb_id, Review.rating == val).count()
        rating_distribution[str(val)] = count

    return {
        "total_reviews": total_reviews,
        "average_rating": round(float(avg_rating), 1) if avg_rating else 0,
        "total_watched": total_watched,
        "total_watchlisted": total_watchlisted,
        "rating_distribution": rating_distribution,
    }


@router.get("/reviews/recent")
def get_recent_reviews(page: int = 1, limit: int = 20, db: Session = Depends(get_db)):
    offset = (page - 1) * limit
    reviews = db.query(Review).order_by(Review.created_at.desc()).offset(offset).limit(limit).all()
    result = []
    for r in reviews:
        user = db.query(User).filter(User.id == r.user_id).first()
        result.append({
            "id": r.id, "tmdb_id": r.tmdb_id, "movie_title": r.movie_title,
            "rating": r.rating, "comment": r.comment, "has_spoilers": r.has_spoilers,
            "user_id": r.user_id, "username": user.username if user else "Inconnu",
            "created_at": r.created_at.isoformat() if r.created_at else None,
        })
    return {"reviews": result, "page": page}


@router.get("/reviews/popular-movies")
def get_popular_reviewed_movies(db: Session = Depends(get_db)):
    from sqlalchemy import func
    popular = db.query(
        Review.tmdb_id, Review.movie_title,
        func.count(Review.id).label("review_count"),
        func.avg(Review.rating).label("avg_rating")
    ).group_by(Review.tmdb_id, Review.movie_title).order_by(func.count(Review.id).desc()).limit(10).all()
    return [{"tmdb_id": p.tmdb_id, "movie_title": p.movie_title, "review_count": p.review_count, "avg_rating": round(float(p.avg_rating), 1) if p.avg_rating else 0} for p in popular]


@router.put("/reviews/{review_id}")
def update_review(review_id: int, review_data: ReviewUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    review = db.query(Review).filter(Review.id == review_id, Review.user_id == current_user.id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Avis introuvable ou non autorisé")
    review.rating = review_data.rating
    review.comment = review_data.comment
    db.commit()
    return {"message": "Avis mis à jour"}


@router.delete("/reviews/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    review = db.query(Review).filter(Review.id == review_id, Review.user_id == current_user.id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Avis introuvable ou non autorisé")
    db.delete(review)
    db.commit()
    return {"message": "Avis supprimé"}


@router.post("/reviews/{review_id}/like")
def like_review(review_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing = db.query(ReviewLike).filter(
        ReviewLike.user_id == current_user.id,
        ReviewLike.review_id == review_id
    ).first()
    if existing:
        db.delete(existing)
        db.commit()
        return {"message": "Like retiré", "liked": False}
    new_like = ReviewLike(user_id=current_user.id, review_id=review_id)
    db.add(new_like)
    db.commit()
    return {"message": "Like ajouté", "liked": True}


@router.get("/reviews/{review_id}/like/status")
def get_like_status(review_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing = db.query(ReviewLike).filter(
        ReviewLike.user_id == current_user.id,
        ReviewLike.review_id == review_id
    ).first()
    return {"liked": existing is not None}


@router.get("/feed")
def get_my_feed(page: int = 1, limit: int = 20, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    offset = (page - 1) * limit
    followed_users = db.query(Follow.followed_id).filter(Follow.follower_id == current_user.id).subquery()
    reviews = db.query(Review).filter(
        Review.user_id.in_(followed_users)
    ).order_by(Review.created_at.desc()).offset(offset).limit(limit).all()

    result = []
    for r in reviews:
        user = db.query(User).filter(User.id == r.user_id).first()
        result.append({
            "id": r.id,
            "tmdb_id": r.tmdb_id,
            "movie_title": r.movie_title,
            "rating": r.rating,
            "comment": r.comment,
            "user_id": r.user_id,
            "username": user.username if user else "Inconnu",
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "watch_date": r.watch_date.isoformat() if r.watch_date else None,
        })
    return {"reviews": result, "page": page}
