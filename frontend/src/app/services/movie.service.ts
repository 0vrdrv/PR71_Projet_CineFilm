import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
// Assure-toi que le chemin d'import est correct selon ta structure
import { TmdbResponse, Movie, Genre } from '../models/movie.model';

// Interface spécifique pour la réponse du Casting (credits)
export interface CastMember {
  id: number;
  name: string;
  character: string;
  profile_path: string | null;
}

export interface CreditsResponse {
  id: number;
  cast: CastMember[];
}

@Injectable({
  providedIn: 'root',
})
export class MovieService {
  private apiKey = 'e976deb8e625fe67f0f2e1b47aa57944';
  private baseUrl = 'https://api.themoviedb.org/3';

  constructor(private http: HttpClient) {}

  // Retourne la structure paginée de TMDB
  getNewReleases(): Observable<TmdbResponse> {
    return this.http.get<TmdbResponse>(
      `${this.baseUrl}/movie/now_playing?api_key=${this.apiKey}&language=fr-FR&page=1`,
    );
  }

  getPopularMovies(): Observable<TmdbResponse> {
    return this.http.get<TmdbResponse>(
      `${this.baseUrl}/movie/popular?api_key=${this.apiKey}&language=fr-FR&page=1`,
    );
  }

  // Retourne un objet contenant un tableau de Genres
  getGenres(): Observable<{ genres: Genre[] }> {
    return this.http.get<{ genres: Genre[] }>(
      `${this.baseUrl}/genre/movie/list?api_key=${this.apiKey}&language=fr-FR`,
    );
  }

  // Recherche avec pagination
  discoverMovies(
    page: number = 1,
    sortBy: string = 'popularity.desc',
    genreId: string = '',
    year: string = '',
  ): Observable<TmdbResponse> {
    let url = `${this.baseUrl}/discover/movie?api_key=${this.apiKey}&language=fr-FR&page=${page}&sort_by=${sortBy}`;

    if (genreId) {
      url += `&with_genres=${genreId}`;
    }
    if (year) {
      url += `&primary_release_year=${year}`;
    }

    return this.http.get<TmdbResponse>(url);
  }

  searchMovies(query: string): Observable<TmdbResponse> {
    return this.http.get<TmdbResponse>(
      `${this.baseUrl}/search/movie?api_key=${this.apiKey}&language=fr-FR&query=${query}&page=1`,
    );
  }

  // Retourne UN SEUL film précis
  getMovieDetails(movieId: string | number): Observable<Movie> {
    return this.http.get<Movie>(
      `${this.baseUrl}/movie/${movieId}?api_key=${this.apiKey}&language=fr-FR`,
    );
  }

  // Retourne la structure des crédits
  getMovieCast(movieId: string | number): Observable<CreditsResponse> {
    return this.http.get<CreditsResponse>(
      `${this.baseUrl}/movie/${movieId}/credits?api_key=${this.apiKey}&language=fr-FR`,
    );
  }
}
