import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
// Imports des Modèles (étape 1)
import { User } from '../models/user.model';
import { WatchlistItem } from '../models/watchlist.model';
import { Review } from '../models/review.model';
import { CustomList, CustomListItem } from '../models/custom-list.model';

// Interface pour les réponses simples (ex: { "message": "Succès" })
export interface ActionResponse {
  message?: string;
  detail?: string;
}

@Injectable({
  providedIn: 'root',
})
export class UserActionService {
  private apiUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) {}

  // --- GESTION UTILISATEUR ---

  getCurrentUser(): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/users/me`);
  }

  getUserById(id: number): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/users/${id}`);
  }

  getAllUsers(): Observable<User[]> {
    return this.http.get<User[]>(`${this.apiUrl}/users/`);
  }

  updateProfile(bio: string, avatarUrl: string): Observable<User> {
    return this.http.put<User>(`${this.apiUrl}/users/me`, {
      bio,
      avatar_url: avatarUrl,
    });
  }

  // --- WATCHLIST & FAVORIS ---

  getWatchlist(userId: number): Observable<WatchlistItem[]> {
    return this.http.get<WatchlistItem[]>(
      `${this.apiUrl}/users/${userId}/watchlist`,
    );
  }

  addToWatchlist(
    tmdbId: number,
    movieTitle: string,
    posterPath: string | null,
  ): Observable<ActionResponse> {
    const body = {
      tmdb_id: tmdbId,
      movie_title: movieTitle,
      poster_path: posterPath,
    };
    return this.http.post<ActionResponse>(`${this.apiUrl}/watchlist/`, body);
  }

  // Pour le Top 5 (Favorites)
  getFavorites(userId: number): Observable<any[]> {
    // Note: Tu peux créer un modèle FavoriteFilm si tu veux être 100% strict ici aussi
    return this.http.get<any[]>(`${this.apiUrl}/users/${userId}/favorites`);
  }

  setFavorite(
    tmdbId: number,
    title: string,
    poster: string | null,
    rank: number,
  ): Observable<ActionResponse> {
    return this.http.post<ActionResponse>(`${this.apiUrl}/users/me/favorites`, {
      tmdb_id: tmdbId,
      movie_title: title,
      poster_path: poster,
      rank: rank,
    });
  }

  // --- REVIEWS (JOURNAL) ---

  getDiary(userId: number): Observable<Review[]> {
    return this.http.get<Review[]>(`${this.apiUrl}/users/${userId}/diary`);
  }

  getMovieReviews(tmdbId: number): Observable<Review[]> {
    return this.http.get<Review[]>(`${this.apiUrl}/movies/${tmdbId}/reviews`);
  }

  addReview(
    tmdbId: number,
    movieTitle: string,
    rating: number,
    comment: string = '',
    hasSpoilers: boolean = false,
  ): Observable<ActionResponse> {
    const body = {
      tmdb_id: tmdbId,
      movie_title: movieTitle,
      rating: rating,
      comment: comment,
      has_spoilers: hasSpoilers,
    };
    return this.http.post<ActionResponse>(`${this.apiUrl}/reviews/`, body);
  }

  deleteReview(reviewId: number): Observable<ActionResponse> {
    return this.http.delete<ActionResponse>(
      `${this.apiUrl}/reviews/${reviewId}`,
    );
  }

  updateReview(
    reviewId: number,
    rating: number,
    comment: string,
  ): Observable<ActionResponse> {
    const body = { rating: rating, comment: comment };
    return this.http.put<ActionResponse>(
      `${this.apiUrl}/reviews/${reviewId}`,
      body,
    );
  }

  // --- LISTES PERSONNALISÉES ---

  createList(title: string, description: string): Observable<CustomList> {
    return this.http.post<CustomList>(`${this.apiUrl}/lists/`, {
      title,
      description,
    });
  }

  getUserLists(userId: number): Observable<CustomList[]> {
    return this.http.get<CustomList[]>(`${this.apiUrl}/users/${userId}/lists`);
  }

  getAllLists(): Observable<CustomList[]> {
    return this.http.get<CustomList[]>(`${this.apiUrl}/lists/`);
  }

  getListById(listId: number): Observable<CustomList> {
    return this.http.get<CustomList>(`${this.apiUrl}/lists/${listId}`);
  }

  getListItems(listId: number): Observable<CustomListItem[]> {
    return this.http.get<CustomListItem[]>(
      `${this.apiUrl}/lists/${listId}/items`,
    );
  }

  addMovieToList(
    listId: number,
    tmdbId: number,
    movieTitle: string,
    posterPath: string | null,
  ): Observable<ActionResponse> {
    const body = {
      tmdb_id: tmdbId,
      movie_title: movieTitle,
      poster_path: posterPath,
    };
    return this.http.post<ActionResponse>(
      `${this.apiUrl}/lists/${listId}/items`,
      body,
    );
  }

  followUser(userId: number): Observable<any> {
  return this.http.post(`${this.apiUrl}/users/${userId}/follow`, {});
}

unfollowUser(userId: number): Observable<any> {
  return this.http.delete(`${this.apiUrl}/users/${userId}/follow`);
}

getUserStats(userId: number): Observable<any> {
  return this.http.get(`${this.apiUrl}/users/${userId}/stats`);
}

getFollowers(userId: number): Observable<any[]> {
  return this.http.get<any[]>(`${this.apiUrl}/users/${userId}/followers`);
}

getFollowing(userId: number): Observable<any[]> {
  return this.http.get<any[]>(`${this.apiUrl}/users/${userId}/following`);
}
}
