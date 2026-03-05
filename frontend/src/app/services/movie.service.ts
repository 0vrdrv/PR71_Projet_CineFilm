import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class MovieService {
  private apiKey = 'e976deb8e625fe67f0f2e1b47aa57944';
  private baseUrl = 'https://api.themoviedb.org/3';

  constructor(private http: HttpClient) {}

  getNewReleases(): Observable<any> {
    return this.http.get(
      `${this.baseUrl}/movie/now_playing?api_key=${this.apiKey}&language=fr-FR&page=1`,
    );
  }

  getPopularMovies(): Observable<any> {
    return this.http.get(
      `${this.baseUrl}/movie/popular?api_key=${this.apiKey}&language=fr-FR&page=1`,
    );
  }

  // Récupérer la liste des genres (Action, Comédie, etc.)
  getGenres(): Observable<any> {
    return this.http.get(
      `${this.baseUrl}/genre/movie/list?api_key=${this.apiKey}&language=fr-FR`,
    );
  }

  // Le moteur de recherche avancé (Filtres et Tris)
  discoverMovies(
    page: number = 1,
    sortBy: string = 'popularity.desc',
    genreId: string = '',
    year: string = '',
  ): Observable<any> {
    let url = `${this.baseUrl}/discover/movie?api_key=${this.apiKey}&language=fr-FR&page=${page}&sort_by=${sortBy}`;

    if (genreId) {
      url += `&with_genres=${genreId}`;
    }
    if (year) {
      url += `&primary_release_year=${year}`;
    }

    return this.http.get(url);
  }

  getMovieDetails(movieId: string): Observable<any> {
    return this.http.get(
      `${this.baseUrl}/movie/${movieId}?api_key=${this.apiKey}&language=fr-FR`,
    );
  }

  getMovieCast(movieId: string): Observable<any> {
    return this.http.get(
      `${this.baseUrl}/movie/${movieId}/credits?api_key=${this.apiKey}&language=fr-FR`,
    );
  }

  searchMovies(query: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/search/movie?api_key=${this.apiKey}&language=fr-FR&query=${query}&page=1`);
  }

  
}
