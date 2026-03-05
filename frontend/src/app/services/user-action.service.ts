import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class UserActionService {
  private apiUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) {}

  getCurrentUser(): Observable<any> {
    return this.http.get(`${this.apiUrl}/users/me`);
  }

  getUserById(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/users/${id}`);
  }

  getAllUsers(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/users/`);
  }

  getWatchlist(userId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/users/${userId}/watchlist`);
  }

  getDiary(userId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/users/${userId}/diary`);
  }

  addToWatchlist(
    tmdbId: number,
    movieTitle: string,
    posterPath: string,
  ): Observable<any> {
    const body = {
      tmdb_id: tmdbId,
      movie_title: movieTitle,
      poster_path: posterPath,
    };
    return this.http.post(`${this.apiUrl}/watchlist/`, body);
  }

  addReview(
    tmdbId: number,
    movieTitle: string,
    rating: number,
    comment: string = '',
    hasSpoilers: boolean = false,
  ): Observable<any> {
    const body = {
      tmdb_id: tmdbId,
      movie_title: movieTitle,
      rating: rating,
      comment: comment,
      has_spoilers: hasSpoilers,
    };
    return this.http.post(`${this.apiUrl}/reviews/`, body);
  }

  getMovieReviews(tmdbId: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/movies/${tmdbId}/reviews`);
  }

  deleteReview(reviewId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/reviews/${reviewId}`);
  }

  updateReview(
    reviewId: number,
    rating: number,
    comment: string,
  ): Observable<any> {
    const body = { rating: rating, comment: comment };
    return this.http.put(`${this.apiUrl}/reviews/${reviewId}`, body);
  }

  createList(title: string, description: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/lists/`, { title, description });
  }

  getUserLists(userId: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/users/${userId}/lists`);
  }

  addMovieToList(
    listId: number,
    tmdbId: number,
    movieTitle: string,
    posterPath: string,
  ): Observable<any> {
    const body = {
      tmdb_id: tmdbId,
      movie_title: movieTitle,
      poster_path: posterPath,
    };
    return this.http.post(`${this.apiUrl}/lists/${listId}/items`, body);
  }

  getListItems(listId: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/lists/${listId}/items`);
  }

  getListById(listId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/lists/${listId}`);
  }
}
