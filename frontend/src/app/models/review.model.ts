export interface Review {
  id: number;
  tmdb_id: number;
  movie_title: string;
  poster_path?: string;
  rating: number;
  comment: string;
  user_id: number;
  username?: string; 
  watch_date?: string;
}