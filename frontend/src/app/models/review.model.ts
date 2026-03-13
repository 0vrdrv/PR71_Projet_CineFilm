export interface Review {
  id: number;
  tmdb_id: number;
  movie_title: string;
  rating: number;
  comment: string | null;
  has_spoilers: boolean;
  watch_date: string;
  created_at: string;
  user_id: number;
  username?: string;
  poster_path?: string;
}

export interface ReviewCreate {
  tmdb_id: number;
  movie_title: string;
  rating: number;
  comment?: string;
  has_spoilers?: boolean;
}