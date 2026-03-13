export interface MovieList {
  id: number;
  title: string;
  description: string | null;
  is_public: boolean;
  created_at: string;
  user_id: number;
  items: MovieListItem[];
}

export interface MovieListItem {
  id: number;
  list_id: number;
  tmdb_id: number;
  movie_title: string;
  poster_path: string | null;
  rank: number | null;
}

export interface WatchlistItem {
  id: number;
  tmdb_id: number;
  movie_title: string;
  poster_path: string | null;
  user_id: number;
  added_at: string;
}