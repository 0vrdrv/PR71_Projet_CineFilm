from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
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

# --- SÉCURITÉ & HACHAGE ---
SECRET_KEY = "une_cle_tres_secrete_et_tres_longue" # À mettre dans le .env en prod !
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 jours

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

# --- LE VIGILE (Vérifie le Token) ---
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

# ==========================================
# ROUTES DE L'API
# ==========================================

@app.get("/")
def read_root():
    return {"message": "API Letterboxd 2 opérationnelle"}

# --- AUTHENTIFICATION ---
@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter((models.User.email == user.email) | (models.User.username == user.username)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email ou Pseudo déjà utilisé")
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

# --- TMDB (PUBLIC) ---
@app.get("/movies/popular")
def get_popular():
    return requests.get(f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=fr-FR").json()

# --- REVIEWS & DIARY ---
@app.post("/reviews/", response_model=schemas.ReviewResponse)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_review = models.Review(**review.dict(), user_id=current_user.id) # On utilise le vigile ici !
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@app.get("/users/{user_id}/diary", response_model=list[schemas.ReviewResponse])
def get_user_diary(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Review).filter(models.Review.user_id == user_id).order_by(models.Review.watch_date.desc()).all()

@app.get("/users/me", response_model=schemas.UserResponse)
def get_current_user_info(current_user: models.User = Depends(get_current_user)):
    return current_user

@app.get("/users/", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return user

# --- WATCHLIST ---
@app.post("/watchlist/")
def add_to_watchlist(item: schemas.WatchlistAdd, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    existing = db.query(models.Watchlist).filter(models.Watchlist.user_id == current_user.id, models.Watchlist.tmdb_id == item.tmdb_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Film déjà dans la watchlist")
    db_item = models.Watchlist(**item.dict(), user_id=current_user.id)
    db.add(db_item)
    db.commit()
    return {"message": "Ajouté à la watchlist"}

@app.get("/users/{user_id}/watchlist")
def get_user_watchlist(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Watchlist).filter(models.Watchlist.user_id == user_id).all()

# --- LISTES PERSONNALISÉES ---
@app.post("/lists/", response_model=schemas.MovieListResponse)
def create_movie_list(movie_list: schemas.MovieListCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_list = models.MovieList(**movie_list.dict(), user_id=current_user.id)
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list

@app.post("/lists/{list_id}/items/", response_model=schemas.MovieListItemResponse)
def add_item_to_list(list_id: int, item: schemas.MovieListItemCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_list = db.query(models.MovieList).filter(models.MovieList.id == list_id).first()
    if not db_list or db_list.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Vous n'êtes pas autorisé à modifier cette liste.")
    db_item = models.MovieListItem(**item.dict(), list_id=list_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/users/{user_id}/lists", response_model=list[schemas.MovieListResponse])
def get_user_lists(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.MovieList).filter(models.MovieList.user_id == user_id).all()

# --- SOCIAL (FOLLOWS, LIKES, FEED) ---
@app.post("/users/{followed_id}/follow")
def follow_user(followed_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if followed_id == current_user.id:
        raise HTTPException(status_code=400, detail="Tu ne peux pas te suivre toi-même.")
    existing_follow = db.query(models.Follow).filter(models.Follow.follower_id == current_user.id, models.Follow.followed_id == followed_id).first()
    if existing_follow:
        return {"message": "Tu suis déjà cet utilisateur."}
    new_follow = models.Follow(follower_id=current_user.id, followed_id=followed_id)
    db.add(new_follow)
    db.commit()
    return {"message": f"Utilisateur {followed_id} suivi avec succès !"}

@app.get("/feed")
def get_my_feed(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Affiche les avis des personnes auxquelles je suis abonné."""
    followed_users = db.query(models.Follow.followed_id).filter(models.Follow.follower_id == current_user.id).subquery()
    return db.query(models.Review).filter(models.Review.user_id.in_(followed_users)).order_by(models.Review.created_at.desc()).limit(20).all()

from pydantic import BaseModel

class ReviewUpdate(BaseModel):
    rating: float
    comment: str

@app.get("/movies/{tmdb_id}/reviews")
def get_movie_reviews(tmdb_id: int, db: Session = Depends(get_db)):
    reviews = db.query(models.Review).filter(models.Review.tmdb_id == tmdb_id).all()
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
            "username": user.username if user else "Utilisateur inconnu"
        })
    return result

@app.delete("/reviews/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    review = db.query(models.Review).filter(models.Review.id == review_id, models.Review.user_id == current_user.id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Avis introuvable ou non autorisé")
    db.delete(review)
    db.commit()
    return {"message": "Avis supprimé"}

@app.put("/reviews/{review_id}")
def update_review(review_id: int, review_data: ReviewUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    review = db.query(models.Review).filter(models.Review.id == review_id, models.Review.user_id == current_user.id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Avis introuvable ou non autorisé")
    
    review.rating = review_data.rating
    review.comment = review_data.comment
    db.commit()
    return {"message": "Avis mis à jour"}

class ListCreate(BaseModel):
    title: str
    description: str | None = None

class ListItemCreate(BaseModel):
    tmdb_id: int
    movie_title: str
    poster_path: str | None = None

@app.post("/lists/")
def create_list(list_data: ListCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_list = models.MovieList(title=list_data.title, description=list_data.description, user_id=current_user.id)
    db.add(new_list)
    db.commit()
    db.refresh(new_list)
    return new_list

@app.get("/users/{user_id}/lists")
def get_user_lists(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.MovieList).filter(models.MovieList.user_id == user_id).all()

@app.post("/lists/{list_id}/items")
def add_item_to_list(list_id: int, item_data: ListItemCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_item = models.MovieListItem(
        list_id=list_id, 
        tmdb_id=item_data.tmdb_id, 
        movie_title=item_data.movie_title, 
        poster_path=item_data.poster_path
    )
    db.add(new_item)
    db.commit()
    return {"message": "Film ajouté à la liste"}

@app.get("/lists/{list_id}/items")
def get_list_items(list_id: int, db: Session = Depends(get_db)):
    return db.query(models.MovieListItem).filter(models.MovieListItem.list_id == list_id).all()

@app.get("/lists/{list_id}")
def get_list_by_id(list_id: int, db: Session = Depends(get_db)):
    movie_list = db.query(models.MovieList).filter(models.MovieList.id == list_id).first()
    if not movie_list:
        raise HTTPException(status_code=404, detail="Liste introuvable")
    return movie_list