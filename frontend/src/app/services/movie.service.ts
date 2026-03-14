import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Movie, MovieResponse, CastResponse, Genre } from '../models';

@Injectable({
  providedIn: 'root',
})
export class MovieService {
  private apiUrl = 'http://127.0.0.1:8000/api/tmdb';

  constructor(private http: HttpClient) {}

  getNewReleases(page: number = 1): Observable<MovieResponse> {
    return this.http.get<MovieResponse>(`${this.apiUrl}/now_playing`, { params: { page } });
  }

  getPopularMovies(page: number = 1): Observable<MovieResponse> {
    return this.http.get<MovieResponse>(`${this.apiUrl}/popular`, { params: { page } });
  }

  getGenres(): Observable<{ genres: Genre[] }> {
    return this.http.get<{ genres: Genre[] }>(`${this.apiUrl}/genres`);
  }

  discoverMovies(page: number = 1, sortBy: string = 'popularity.desc', genreId: string = '', year: string = ''): Observable<MovieResponse> {
    const params: any = { page, sort_by: sortBy };
    if (genreId) params.with_genres = genreId;
    if (year) params.primary_release_year = year;
    return this.http.get<MovieResponse>(`${this.apiUrl}/discover`, { params });
  }

  getMovieDetails(movieId: string | number): Observable<Movie> {
    return this.http.get<Movie>(`${this.apiUrl}/movie/${movieId}`);
  }

  getMovieCast(movieId: string | number): Observable<CastResponse> {
    return this.http.get<CastResponse>(`${this.apiUrl}/movie/${movieId}/credits`);
  }

  searchMovies(query: string): Observable<MovieResponse> {
    return this.http.get<MovieResponse>(`${this.apiUrl}/search`, { params: { query } });
  }

  getSimilarMovies(movieId: number): Observable<MovieResponse> {
    return this.http.get<MovieResponse>(`${this.apiUrl}/movie/${movieId}/similar`);
  }

  getTrending(): Observable<MovieResponse> {
    return this.http.get<MovieResponse>(`${this.apiUrl}/trending`);
  }

  getWatchProviders(movieId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/movie/${movieId}/providers`);
  }
}