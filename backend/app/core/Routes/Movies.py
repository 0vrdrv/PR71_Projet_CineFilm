import os
import requests
from fastapi import APIRouter, HTTPException

router = APIRouter()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = os.getenv("TMDB_BASE_URL", "https://api.themoviedb.org/3")
TMDB_LANGUAGE = os.getenv("TMDB_LANGUAGE", "fr-FR")

@router.get("/popular")
def get_popular_movies():
    url = f"{TMDB_BASE_URL}/movie/popular"
    params = {
        "api_key": TMDB_API_KEY,
        "language": TMDB_LANGUAGE
    }
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Erreur TMDB")
        
    return response.json()