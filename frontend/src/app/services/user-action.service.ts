import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { User } from '../models/user.model';
import { WatchlistItem } from '../models/watchlist.model';
import { Review } from '../models/review.model';
import { CustomList, CustomListItem } from '../models/custom-list.model';

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

  // --- WATCHLIST ---

  getWatchlist(userId: number): Observable<WatchlistItem[]> {
    return this.http.get<WatchlistItem[]>(`${this.apiUrl}/users/${userId}/watchlist`);
  }

  addToWatchlist(tmdbId: number, movieTitle: string, posterPath: string | null): Observable<ActionResponse> {
    return this.http.post<ActionResponse>(`${this.apiUrl}/watchlist/`, {
      tmdb_id: tmdbId, movie_title: movieTitle, poster_path: posterPath,
    });
  }

  removeFromWatchlist(tmdbId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/watchlist/${tmdbId}`);
  }

  getWatchlistStatus(tmdbId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/watchlist/${tmdbId}/status`);
  }

  // --- FAVORITES ---

  getFavorites(userId: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/users/${userId}/favorites`);
  }

  setFavorite(tmdbId: number, title: string, poster: string | null, rank: number): Observable<ActionResponse> {
    return this.http.post<ActionResponse>(`${this.apiUrl}/users/me/favorites`, {
      tmdb_id: tmdbId, movie_title: title, poster_path: poster, rank: rank,
    });
  }

  removeFavorite(rank: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/users/me/favorites/${rank}`);
  }

  // --- WATCHED ---

  markAsWatched(tmdbId: number, movieTitle: string, posterPath: string | null): Observable<any> {
    return this.http.post(`${this.apiUrl}/watched/`, {
      tmdb_id: tmdbId, movie_title: movieTitle, poster_path: posterPath,
    });
  }

  unmarkWatched(tmdbId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/watched/${tmdbId}`);
  }

  getWatchedStatus(tmdbId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/watched/${tmdbId}/status`);
  }

  getUserWatched(userId: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/users/${userId}/watched`);
  }

  getWatchedCount(userId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/users/${userId}/watched/count`);
  }

  // --- REVIEWS ---

  getDiary(userId: number): Observable<Review[]> {
    return this.http.get<Review[]>(`${this.apiUrl}/users/${userId}/diary`);
  }

  getMovieReviews(tmdbId: number): Observable<Review[]> {
    return this.http.get<Review[]>(`${this.apiUrl}/movies/${tmdbId}/reviews`);
  }

  addReview(tmdbId: number, movieTitle: string, rating: number, comment: string = '', hasSpoilers: boolean = false): Observable<ActionResponse> {
    return this.http.post<ActionResponse>(`${this.apiUrl}/reviews/`, {
      tmdb_id: tmdbId, movie_title: movieTitle, rating, comment, has_spoilers: hasSpoilers,
    });
  }

  deleteReview(reviewId: number): Observable<ActionResponse> {
    return this.http.delete<ActionResponse>(`${this.apiUrl}/reviews/${reviewId}`);
  }

  updateReview(reviewId: number, rating: number, comment: string): Observable<ActionResponse> {
    return this.http.put<ActionResponse>(`${this.apiUrl}/reviews/${reviewId}`, { rating, comment });
  }

  toggleReviewLike(reviewId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/reviews/${reviewId}/like`, {});
  }

  getReviewLikeStatus(reviewId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/reviews/${reviewId}/like/status`);
  }

  // --- LISTES ---

  createList(title: string, description: string): Observable<CustomList> {
    return this.http.post<CustomList>(`${this.apiUrl}/lists/`, { title, description });
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
    return this.http.get<CustomListItem[]>(`${this.apiUrl}/lists/${listId}/items`);
  }

  addMovieToList(listId: number, tmdbId: number, movieTitle: string, posterPath: string | null): Observable<ActionResponse> {
    return this.http.post<ActionResponse>(`${this.apiUrl}/lists/${listId}/items`, {
      tmdb_id: tmdbId, movie_title: movieTitle, poster_path: posterPath,
    });
  }

  removeMovieFromList(listId: number, tmdbId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/lists/${listId}/items/${tmdbId}`);
  }

  deleteList(listId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/lists/${listId}`);
  }

  // --- FOLLOW ---

  followUser(userId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/users/${userId}/follow`, {});
  }

  unfollowUser(userId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/users/${userId}/follow`);
  }

  getUserStats(userId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/users/${userId}/stats`);
  }

  getDetailedStats(userId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/users/${userId}/stats/detailed`);
  }

  getPublicLists(page: number = 1): Observable<any> {
    return this.http.get(`${this.apiUrl}/lists/public`, { params: { page } });
  }

  getRecentReviews(page: number = 1): Observable<any> {
    return this.http.get(`${this.apiUrl}/reviews/recent`, { params: { page } });
  }

  getPopularReviewedMovies(): Observable<any> {
    return this.http.get(`${this.apiUrl}/reviews/popular-movies`);
  }

  getMovieStats(tmdbId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/movies/${tmdbId}/stats`);
  }

  getFollowStatus(userId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/users/${userId}/follow/status`);
  }

  getFollowers(userId: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/users/${userId}/followers`);
  }

  getFollowing(userId: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/users/${userId}/following`);
  }
}
