from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routes import (
    auth_router,
    users_router,
    reviews_router,
    watchlist_router,
    lists_router,
    tmdb_router,
    favorites_router,
    watched_router,
)

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Letterboxd 2 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(reviews_router)
app.include_router(watchlist_router)
app.include_router(lists_router)
app.include_router(tmdb_router)
app.include_router(favorites_router)
app.include_router(watched_router)


@app.get("/")
def read_root():
    return {"message": "API Letterboxd 2 opérationnelle"}
