# Letterbox

## Description

Application web sociale inspirée de Letterboxd, permettant aux utilisateurs de découvrir des films, rédiger des critiques, créer des listes et suivre d'autres cinéphiles.

**Deux types d'utilisateurs :**
- **Utilisateur inscrit (Critic/Reviewer)** : peut s'inscrire, noter des films, écrire des reviews, créer des listes personnalisées, gérer sa watchlist, suivre d'autres membres
- **Visiteur (Browser)** : peut parcourir le catalogue de films, lire les reviews de la communauté, consulter les profils publics et les listes sans inscription

## Stack technique

- **Frontend** : Angular 13 + Tailwind CSS + RxJS
- **Backend** : Python FastAPI + SQLAlchemy + SQLite
- **API externe** : TMDB (The Movie Database) via proxy backend

---

## Lancement du Backend

### Prérequis
- Python 3.10+
- pip

### Installation

```bash
cd backend
pip install -r requirements.txt
```

### Configuration

Créer un fichier `.env` dans le dossier `backend/` :

```
TMDB_API_KEY=votre_cle_tmdb
DATABASE_URL=sqlite:///./letterboxd.db
SECRET_KEY=votre_cle_secrete
```

### Démarrage

```bash
cd backend
uvicorn main:app --reload
```

Le serveur sera accessible sur `http://127.0.0.1:8000`
Documentation API Swagger : `http://127.0.0.1:8000/docs`

---

## Lancement du Frontend

### Prérequis
- Node.js 14+ (recommandé 16+)
- npm

### Installation

```bash
cd frontend
npm install
```

### Démarrage

```bash
cd frontend
ng serve
```

L'application sera accessible sur `http://localhost:4200`

---

## Fonctionnalités principales

### Angular (Composants, Services, Routage, Forms)
- **10+ composants** : Home, Films, MovieDetail, Profile, Members, Feed, Lists, ListDetail, Login, Register
- **4 services** : AuthService, MovieService, UserActionService, NotificationService
- **Routage** avec AuthGuard, routerLinkActive, paramètres dynamiques (`:id`)
- **Reactive Forms** (FormBuilder + Validators) sur : Login, Register, Review, Création de liste
- **Observables RxJS** : debounceTime, distinctUntilChanged, switchMap, BehaviorSubject

### Backend
- **Proxy TMDB** : la clé API n'est jamais exposée côté client
- **Filtres** : tri, genre, année sur la page Films
- **Endpoints complets** : CRUD reviews, watchlist, listes, follow/unfollow, likes, stats, feed

### User Experience
- **Toast notifications** animées (succès/erreur/info)
- **Loading skeletons** sur toutes les pages
- **Design responsive** avec menu hamburger mobile
- **Sticky header** avec recherche instantanée
- **Transitions CSS** et animations (hover, scale, fade)

---

## Architecture du projet

```
backend/
├── main.py          # Routes API FastAPI
├── models.py        # Modèles SQLAlchemy (User, Review, Watchlist, MovieList, Follow, ReviewLike)
├── schemas.py       # Schémas Pydantic (validation)
├── database.py      # Configuration SQLAlchemy
├── .env             # Variables d'environnement
└── requirements.txt

frontend/src/app/
├── pages/           # Composants de pages
│   ├── home/
│   ├── films/
│   ├── movie-detail/
│   ├── profile/
│   ├── members/
│   ├── feed/
│   ├── lists/
│   ├── list-detail/
│   ├── login/
│   └── register/
├── services/        # Services Angular
│   ├── auth.service.ts
│   ├── movie.service.ts
│   ├── user-action.service.ts
│   └── notification.service.ts
├── interceptors/    # HTTP Interceptor (Auth + 401 handling)
├── guards/          # Route Guards (AuthGuard)
└── app.module.ts    # Module principal
```
