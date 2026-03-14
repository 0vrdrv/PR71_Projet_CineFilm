# Letterbox

Clone de [Letterboxd](https://letterboxd.com/) — une plateforme sociale de découverte et de reviews de films.

## Stack technique

| Couche   | Technologie                          |
|----------|--------------------------------------|
| Frontend | Angular 13, TypeScript, Tailwind CSS |
| Backend  | FastAPI, SQLAlchemy, Pydantic        |
| Base de données | SQLite                        |
| API externe | TMDB (The Movie Database)         |
| Auth     | JWT (PyJWT + Passlib)                |

## Fonctionnalités

- **Authentification** — inscription, connexion avec tokens JWT
- **Découverte de films** — populaires, tendances, à l'affiche, recherche par titre
- **Reviews** — notes, commentaires, gestion des spoilers, date de visionnage
- **Diary** — historique des films vus avec possibilité de rewatch
- **Watchlist** — liste de films à voir
- **Favoris** — classement de ses films préférés
- **Listes personnalisées** — créer et partager des listes thématiques
- **Social** — follow/unfollow d'utilisateurs, likes sur les reviews, feed d'activité
- **Profil utilisateur** — bio, statistiques, diary, favoris

## Prérequis

- **Node.js** (v14+) et **npm**
- **Python** 3.11+

## Lancer le backend

```bash
cd backend

# Créer et activer un environnement virtuel
python -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur
python run.py
```

Le backend tourne sur **http://127.0.0.1:8000**

Documentation Swagger disponible sur **http://127.0.0.1:8000/docs**

## Lancer le frontend

```bash
cd frontend

# Installer les dépendances
npm install

# Lancer le serveur de développement
npm start
```

Le frontend tourne sur **http://localhost:4200**

## Seed de la base de données (optionnel)

Pour peupler la base avec des données d'exemple (films, utilisateurs, reviews) :

```bash
cd backend
python seed_database.py
```

