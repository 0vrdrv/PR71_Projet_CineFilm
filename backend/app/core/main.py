from fastapi import FastAPI
from app.core.Routes import Movies, series, Anime

app = FastAPI(title="RateUrWatch", description="API pour le projet PR71")

app.include_router(Movies.router, prefix="/movies", tags=["Movies"])
app.include_router(series.router, prefix="/series", tags=["Series"])
app.include_router(Anime.router, prefix="/anime", tags=["Anime"])

@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API de notre site RateUrWatch"}