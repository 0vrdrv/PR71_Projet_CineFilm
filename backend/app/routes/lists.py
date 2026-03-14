from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.list import MovieList, MovieListItem
from app.schemas.list import MovieListCreate, MovieListResponse, MovieListItemCreate, MovieListItemResponse

router = APIRouter(tags=["lists"])


@router.post("/lists/", response_model=MovieListResponse)
def create_movie_list(movie_list: MovieListCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_list = MovieList(**movie_list.dict(), user_id=current_user.id)
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list


@router.get("/users/{user_id}/lists", response_model=list[MovieListResponse])
def get_user_lists(user_id: int, db: Session = Depends(get_db)):
    return db.query(MovieList).filter(MovieList.user_id == user_id).order_by(MovieList.created_at.desc()).all()


@router.get("/lists/public")
def get_public_lists(page: int = 1, limit: int = 12, db: Session = Depends(get_db)):
    offset = (page - 1) * limit
    lists_query = db.query(MovieList).filter(MovieList.is_public == True).order_by(MovieList.created_at.desc()).offset(offset).limit(limit).all()
    result = []
    for l in lists_query:
        owner = db.query(User).filter(User.id == l.user_id).first()
        items = db.query(MovieListItem).filter(MovieListItem.list_id == l.id).limit(4).all()
        result.append({
            "id": l.id,
            "title": l.title,
            "description": l.description,
            "user_id": l.user_id,
            "username": owner.username if owner else "Inconnu",
            "created_at": l.created_at.isoformat() if l.created_at else None,
            "item_count": db.query(MovieListItem).filter(MovieListItem.list_id == l.id).count(),
            "preview_posters": [i.poster_path for i in items if i.poster_path],
        })
    return {"lists": result, "page": page}


@router.get("/lists/{list_id}")
def get_list_by_id(list_id: int, db: Session = Depends(get_db)):
    movie_list = db.query(MovieList).filter(MovieList.id == list_id).first()
    if not movie_list:
        raise HTTPException(status_code=404, detail="Liste introuvable")
    owner = db.query(User).filter(User.id == movie_list.user_id).first()
    return {
        "id": movie_list.id,
        "title": movie_list.title,
        "description": movie_list.description,
        "is_public": movie_list.is_public,
        "created_at": movie_list.created_at.isoformat() if movie_list.created_at else None,
        "user_id": movie_list.user_id,
        "username": owner.username if owner else "Inconnu",
    }


@router.delete("/lists/{list_id}")
def delete_list(list_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_list = db.query(MovieList).filter(MovieList.id == list_id, MovieList.user_id == current_user.id).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="Liste introuvable ou non autorisée")
    db.delete(db_list)
    db.commit()
    return {"message": "Liste supprimée"}


@router.post("/lists/{list_id}/items", response_model=MovieListItemResponse)
def add_item_to_list(list_id: int, item: MovieListItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_list = db.query(MovieList).filter(MovieList.id == list_id).first()
    if not db_list or db_list.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Vous n'êtes pas autorisé à modifier cette liste.")
    existing = db.query(MovieListItem).filter(
        MovieListItem.list_id == list_id,
        MovieListItem.tmdb_id == item.tmdb_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Film déjà dans cette liste")
    db_item = MovieListItem(**item.dict(), list_id=list_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/lists/{list_id}/items")
def get_list_items(list_id: int, db: Session = Depends(get_db)):
    return db.query(MovieListItem).filter(MovieListItem.list_id == list_id).all()


@router.delete("/lists/{list_id}/items/{tmdb_id}")
def remove_item_from_list(list_id: int, tmdb_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_list = db.query(MovieList).filter(MovieList.id == list_id).first()
    if not db_list or db_list.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Non autorisé")
    item = db.query(MovieListItem).filter(
        MovieListItem.list_id == list_id,
        MovieListItem.tmdb_id == tmdb_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Film introuvable dans cette liste")
    db.delete(item)
    db.commit()
    return {"message": "Film retiré de la liste"}
