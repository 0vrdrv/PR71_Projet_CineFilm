from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import func
from passlib.context import CryptContext
import jwt
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

import models, database, schemas

load_dotenv()
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Letterboxd 2 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY", "une_cle_tres_secrete_et_tres_longue")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 jours

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token invalide")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expiré. Veuillez vous reconnecter.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalide")

    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Utilisateur introuvable")
    return user


# Dépendance optionnelle : retourne l'utilisateur si connecté, None sinon
def get_optional_user(token: str | None = Depends(OAuth2PasswordBearer(tokenUrl="login", auto_error=False)), db: Session = Depends(get_db)):
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username:
            return db.query(models.User).filter(models.User.username == username).first()
    except Exception:
        pass
    return None


# ==========================================
# ROOT
# ==========================================

@app.get("/")
def read_root():
    return {"message": "API Letterboxd 2 opérationnelle"}


# ==========================================
# AUTHENTIFICATION
# ==========================================

@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(
        (models.User.email == user.email) | (models.User.username == user.username)
    ).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email ou Pseudo déjà utilisé")
    if len(user.password) < 6:
        raise HTTPException(status_code=400, detail="Le mot de passe doit contenir au moins 6 caractères")
    hashed_pw = get_password_hash(user.password)
    new_user = models.User(username=user.username, email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Pseudo ou mot de passe incorrect")
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


# ==========================================
# USERS
# ==========================================

@app.get("/users/me", response_model=schemas.UserResponse)
def get_current_user_info(current_user: models.User = Depends(get_current_user)):
    return current_user


@app.get("/users/", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.get("/users/search", response_model=list[schemas.UserResponse])
def search_users(q: str = Query("", min_length=1), db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.username.ilike(f"%{q}%")).all()


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return user


@app.get("/users/{user_id}/stats")
def get_user_stats(user_id: int, db: Session = Depends(get_db)):
    """Statistiques d'un utilisateur : nombre de films vus, note moyenne, nombre de reviews, etc."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    reviews = db.query(models.Review).filter(models.Review.user_id == user_id)
    total_reviews = reviews.count()
    avg_rating = db.query(func.avg(models.Review.rating)).filter(models.Review.user_id == user_id).scalar()
    watchlist_count = db.query(models.Watchlist).filter(models.Watchlist.user_id == user_id).count()
    lists_count = db.query(models.MovieList).filter(models.MovieList.user_id == user_id).count()
    followers_count = db.query(models.Follow).filter(models.Follow.followed_id == user_id).count()
    following_count = db.query(models.Follow).filter(models.Follow.follower_id == user_id).count()

    return {
        "total_reviews": total_reviews,
        "average_rating": round(float(avg_rating), 1) if avg_rating else 0,
        "watchlist_count": watchlist_count,
        "lists_count": lists_count,
        "followers_count": followers_count,
        "following_count": following_count,
    }


# ==========================================
# TMDB PROXY (protège la clé API)
# ==========================================

@app.get("/tmdb/popular")
def tmdb_popular(page: int = 1):
    return requests.get(
        f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=fr-FR&page={page}"
    ).json()


@app.get("/tmdb/now_playing")
def tmdb_now_playing(page: int = 1):
    return requests.get(
        f"https://api.themoviedb.org/3/movie/now_playing?api_key={TMDB_API_KEY}&language=fr-FR&page={page}"
    ).json()


@app.get("/tmdb/genres")
def tmdb_genres():
    return requests.get(
        f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=fr-FR"
    ).json()


@app.get("/tmdb/discover")
def tmdb_discover(page: int = 1, sort_by: str = "popularity.desc", with_genres: str = "", primary_release_year: str = ""):
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=fr-FR&page={page}&sort_by={sort_by}"
    if with_genres:
        url += f"&with_genres={with_genres}"
    if primary_release_year:
        url += f"&primary_release_year={primary_release_year}"
    return requests.get(url).json()


@app.get("/tmdb/movie/{movie_id}")
def tmdb_movie_detail(movie_id: int):
    return requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=fr-FR"
    ).json()


@app.get("/tmdb/movie/{movie_id}/credits")
def tmdb_movie_credits(movie_id: int):
    return requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={TMDB_API_KEY}&language=fr-FR"
    ).json()


@app.get("/tmdb/search")
def tmdb_search(query: str = ""):
    return requests.get(
        f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&language=fr-FR&query={query}&page=1"
    ).json()


# ==========================================
# REVIEWS
# ==========================================

@app.post("/reviews/", response_model=schemas.ReviewResponse)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_review = models.Review(**review.dict(), user_id=current_user.id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@app.get("/users/{user_id}/diary", response_model=list[schemas.ReviewResponse])
def get_user_diary(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Review).filter(models.Review.user_id == user_id).order_by(models.Review.watch_date.desc()).all()


@app.get("/movies/{tmdb_id}/reviews")
def get_movie_reviews(tmdb_id: int, db: Session = Depends(get_db)):
    reviews = db.query(models.Review).filter(models.Review.tmdb_id == tmdb_id).order_by(models.Review.created_at.desc()).all()
    result = []
    for r in reviews:
        user = db.query(models.User).filter(models.User.id == r.user_id).first()
        likes_count = db.query(models.ReviewLike).filter(models.ReviewLike.review_id == r.id).count()
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


@app.put("/reviews/{review_id}")
def update_review(review_id: int, review_data: schemas.ReviewUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    review = db.query(models.Review).filter(models.Review.id == review_id, models.Review.user_id == current_user.id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Avis introuvable ou non autorisé")
    review.rating = review_data.rating
    review.comment = review_data.comment
    db.commit()
    return {"message": "Avis mis à jour"}


@app.delete("/reviews/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    review = db.query(models.Review).filter(models.Review.id == review_id, models.Review.user_id == current_user.id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Avis introuvable ou non autorisé")
    db.delete(review)
    db.commit()
    return {"message": "Avis supprimé"}


# ==========================================
# REVIEW LIKES
# ==========================================

@app.post("/reviews/{review_id}/like")
def like_review(review_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    existing = db.query(models.ReviewLike).filter(
        models.ReviewLike.user_id == current_user.id,
        models.ReviewLike.review_id == review_id
    ).first()
    if existing:
        db.delete(existing)
        db.commit()
        return {"message": "Like retiré", "liked": False}
    new_like = models.ReviewLike(user_id=current_user.id, review_id=review_id)
    db.add(new_like)
    db.commit()
    return {"message": "Like ajouté", "liked": True}


@app.get("/reviews/{review_id}/like/status")
def get_like_status(review_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    existing = db.query(models.ReviewLike).filter(
        models.ReviewLike.user_id == current_user.id,
        models.ReviewLike.review_id == review_id
    ).first()
    return {"liked": existing is not None}


# ==========================================
# WATCHLIST
# ==========================================

@app.post("/watchlist/")
def add_to_watchlist(item: schemas.WatchlistAdd, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    existing = db.query(models.Watchlist).filter(
        models.Watchlist.user_id == current_user.id,
        models.Watchlist.tmdb_id == item.tmdb_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Film déjà dans la watchlist")
    db_item = models.Watchlist(**item.dict(), user_id=current_user.id)
    db.add(db_item)
    db.commit()
    return {"message": "Ajouté à la watchlist"}


@app.get("/users/{user_id}/watchlist")
def get_user_watchlist(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Watchlist).filter(models.Watchlist.user_id == user_id).order_by(models.Watchlist.added_at.desc()).all()


@app.delete("/watchlist/{tmdb_id}")
def remove_from_watchlist(tmdb_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    item = db.query(models.Watchlist).filter(
        models.Watchlist.user_id == current_user.id,
        models.Watchlist.tmdb_id == tmdb_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Film introuvable dans la watchlist")
    db.delete(item)
    db.commit()
    return {"message": "Retiré de la watchlist"}


# ==========================================
# LISTES PERSONNALISÉES
# ==========================================

@app.post("/lists/", response_model=schemas.MovieListResponse)
def create_movie_list(movie_list: schemas.MovieListCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_list = models.MovieList(**movie_list.dict(), user_id=current_user.id)
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list


@app.get("/users/{user_id}/lists", response_model=list[schemas.MovieListResponse])
def get_user_lists(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.MovieList).filter(models.MovieList.user_id == user_id).order_by(models.MovieList.created_at.desc()).all()


@app.get("/lists/{list_id}")
def get_list_by_id(list_id: int, db: Session = Depends(get_db)):
    movie_list = db.query(models.MovieList).filter(models.MovieList.id == list_id).first()
    if not movie_list:
        raise HTTPException(status_code=404, detail="Liste introuvable")
    owner = db.query(models.User).filter(models.User.id == movie_list.user_id).first()
    return {
        "id": movie_list.id,
        "title": movie_list.title,
        "description": movie_list.description,
        "is_public": movie_list.is_public,
        "created_at": movie_list.created_at.isoformat() if movie_list.created_at else None,
        "user_id": movie_list.user_id,
        "username": owner.username if owner else "Inconnu",
    }


@app.delete("/lists/{list_id}")
def delete_list(list_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_list = db.query(models.MovieList).filter(models.MovieList.id == list_id, models.MovieList.user_id == current_user.id).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="Liste introuvable ou non autorisée")
    db.delete(db_list)
    db.commit()
    return {"message": "Liste supprimée"}


@app.post("/lists/{list_id}/items", response_model=schemas.MovieListItemResponse)
def add_item_to_list(list_id: int, item: schemas.MovieListItemCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_list = db.query(models.MovieList).filter(models.MovieList.id == list_id).first()
    if not db_list or db_list.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Vous n'êtes pas autorisé à modifier cette liste.")
    # Vérifier si le film est déjà dans la liste
    existing = db.query(models.MovieListItem).filter(
        models.MovieListItem.list_id == list_id,
        models.MovieListItem.tmdb_id == item.tmdb_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Film déjà dans cette liste")
    db_item = models.MovieListItem(**item.dict(), list_id=list_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/lists/{list_id}/items")
def get_list_items(list_id: int, db: Session = Depends(get_db)):
    return db.query(models.MovieListItem).filter(models.MovieListItem.list_id == list_id).all()


@app.delete("/lists/{list_id}/items/{tmdb_id}")
def remove_item_from_list(list_id: int, tmdb_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_list = db.query(models.MovieList).filter(models.MovieList.id == list_id).first()
    if not db_list or db_list.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Non autorisé")
    item = db.query(models.MovieListItem).filter(
        models.MovieListItem.list_id == list_id,
        models.MovieListItem.tmdb_id == tmdb_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Film introuvable dans cette liste")
    db.delete(item)
    db.commit()
    return {"message": "Film retiré de la liste"}


# ==========================================
# SOCIAL (FOLLOWS & FEED)
# ==========================================

@app.post("/users/{followed_id}/follow")
def follow_user(followed_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if followed_id == current_user.id:
        raise HTTPException(status_code=400, detail="Tu ne peux pas te suivre toi-même.")
    user_to_follow = db.query(models.User).filter(models.User.id == followed_id).first()
    if not user_to_follow:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    existing = db.query(models.Follow).filter(
        models.Follow.follower_id == current_user.id,
        models.Follow.followed_id == followed_id
    ).first()
    if existing:
        return {"message": "Tu suis déjà cet utilisateur.", "following": True}
    new_follow = models.Follow(follower_id=current_user.id, followed_id=followed_id)
    db.add(new_follow)
    db.commit()
    return {"message": f"Utilisateur {followed_id} suivi avec succès !", "following": True}


@app.delete("/users/{followed_id}/follow")
def unfollow_user(followed_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    existing = db.query(models.Follow).filter(
        models.Follow.follower_id == current_user.id,
        models.Follow.followed_id == followed_id
    ).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Tu ne suis pas cet utilisateur.")
    db.delete(existing)
    db.commit()
    return {"message": "Utilisateur unfollowed.", "following": False}


@app.get("/users/{user_id}/follow/status")
def get_follow_status(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    existing = db.query(models.Follow).filter(
        models.Follow.follower_id == current_user.id,
        models.Follow.followed_id == user_id
    ).first()
    return {"following": existing is not None}


@app.get("/users/{user_id}/followers", response_model=list[schemas.UserResponse])
def get_followers(user_id: int, db: Session = Depends(get_db)):
    follower_ids = db.query(models.Follow.follower_id).filter(models.Follow.followed_id == user_id).all()
    ids = [f[0] for f in follower_ids]
    return db.query(models.User).filter(models.User.id.in_(ids)).all()


@app.get("/users/{user_id}/following", response_model=list[schemas.UserResponse])
def get_following(user_id: int, db: Session = Depends(get_db)):
    following_ids = db.query(models.Follow.followed_id).filter(models.Follow.follower_id == user_id).all()
    ids = [f[0] for f in following_ids]
    return db.query(models.User).filter(models.User.id.in_(ids)).all()


@app.get("/feed")
def get_my_feed(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Affiche les avis des personnes auxquelles je suis abonné."""
    followed_users = db.query(models.Follow.followed_id).filter(models.Follow.follower_id == current_user.id).subquery()
    reviews = db.query(models.Review).filter(
        models.Review.user_id.in_(followed_users)
    ).order_by(models.Review.created_at.desc()).limit(50).all()

    result = []
    for r in reviews:
        user = db.query(models.User).filter(models.User.id == r.user_id).first()
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
    return result
@app.delete("/users/{followed_id}/follow")
def unfollow_user(followed_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    follow = db.query(models.Follow).filter(
        models.Follow.follower_id == current_user.id,
        models.Follow.followed_id == followed_id
    ).first()
    if not follow:
        raise HTTPException(status_code=404, detail="Tu ne suis pas cet utilisateur.")
    db.delete(follow)
    db.commit()
    return {"message": "Unfollowed"}

@app.get("/users/{user_id}/followers")
def get_followers(user_id: int, db: Session = Depends(get_db)):
    followers = db.query(models.Follow).filter(models.Follow.followed_id == user_id).all()
    return [{"follower_id": f.follower_id} for f in followers]

@app.get("/users/{user_id}/following")
def get_following(user_id: int, db: Session = Depends(get_db)):
    following = db.query(models.Follow).filter(models.Follow.follower_id == user_id).all()
    return [{"followed_id": f.followed_id} for f in following]

@app.get("/users/{user_id}/stats")
def get_user_stats(user_id: int, db: Session = Depends(get_db)):
    reviews_count = db.query(models.Review).filter(models.Review.user_id == user_id).count()
    watchlist_count = db.query(models.Watchlist).filter(models.Watchlist.user_id == user_id).count()
    lists_count = db.query(models.MovieList).filter(models.MovieList.user_id == user_id).count()
    followers_count = db.query(models.Follow).filter(models.Follow.followed_id == user_id).count()
    following_count = db.query(models.Follow).filter(models.Follow.follower_id == user_id).count()
    return {
        "reviews": reviews_count,
        "watchlist": watchlist_count,
        "lists": lists_count,
        "followers": followers_count,
        "following": following_count
    }
    