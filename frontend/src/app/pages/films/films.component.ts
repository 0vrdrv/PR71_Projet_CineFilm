import { Component, OnInit } from '@angular/core';
import { MovieService } from '../../services/movie.service';

@Component({
  selector: 'app-films',
  templateUrl: './films.component.html',
  styleUrls: ['./films.component.scss']
})
export class FilmsComponent implements OnInit {
  movies: any[] = [];
  genres: any[] = [];
  loading: boolean = true;

  currentPage: number = 1;
  totalResults: number = 0;
  selectedSort: string = 'popularity.desc';
  selectedGenre: string = '';
  selectedYear: string = '';
  viewMode: 'grid' | 'list' = 'grid';

  sortOptions = [
    { value: 'popularity.desc', label: 'Popularity (Desc)' },
    { value: 'popularity.asc', label: 'Popularity (Asc)' },
    { value: 'vote_average.desc', label: 'Highest Rated' },
    { value: 'primary_release_date.desc', label: 'Newest' },
    { value: 'primary_release_date.asc', label: 'Oldest' },
    { value: 'original_title.asc', label: 'A-Z' }
  ];

  constructor(private movieService: MovieService) {}

  ngOnInit(): void {
    this.loadGenres();
    this.loadMovies();
  }

  loadGenres() {
    this.movieService.getGenres().subscribe((data: any) => {
      this.genres = data.genres;
    });
  }

  loadMovies() {
    this.loading = true;
    this.movieService.discoverMovies(this.currentPage, this.selectedSort, this.selectedGenre, this.selectedYear)
      .subscribe((data: any) => {
        this.movies = data.results;
        this.totalResults = data.total_results || 0;
        this.loading = false;
      });
  }

  onFilterChange() {
    this.currentPage = 1;
    this.loadMovies();
  }

  nextPage() {
    this.currentPage++;
    this.loadMovies();
    window.scrollTo(0, 0);
  }

  prevPage() {
    if (this.currentPage > 1) {
      this.currentPage--;
      this.loadMovies();
      window.scrollTo(0, 0);
    }
  }
}
