import os
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY", "une_cle_tres_secrete_et_tres_longue")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./letterboxd.db")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 jours
