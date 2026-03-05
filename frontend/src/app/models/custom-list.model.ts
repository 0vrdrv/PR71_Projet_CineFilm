export interface CustomList {
  id: number;
  title: string;
  description?: string;
  user_id: number;
}

export interface CustomListItem {
  id?: number;
  list_id: number;
  tmdb_id: number;
  movie_title: string;
  poster_path?: string;
}