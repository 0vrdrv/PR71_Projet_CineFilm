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
  
  // Paramètres par défaut
  currentPage: number = 1;
  selectedSort: string = 'popularity.desc';
  selectedGenre: string = '';
  selectedYear: string = '';

  // Options de tri pour le menu déroulant
  sortOptions = [
    { value: 'popularity.desc', label: 'Popularité (Décroissant)' },
    { value: 'popularity.asc', label: 'Popularité (Croissant)' },
    { value: 'vote_average.desc', label: 'Mieux notés' },
    { value: 'primary_release_date.desc', label: 'Plus récents' },
    { value: 'primary_release_date.asc', label: 'Plus anciens' },
    { value: 'original_title.asc', label: 'Ordre alphabétique (A-Z)' }
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
    this.movieService.discoverMovies(this.currentPage, this.selectedSort, this.selectedGenre, this.selectedYear)
      .subscribe((data: any) => {
        this.movies = data.results;
      });
  }

  // Appelée à chaque fois que l'utilisateur change un filtre
  onFilterChange() {
    this.currentPage = 1; // On remet à la page 1 si on change de filtre
    this.loadMovies();
  }

  // Pagination basique
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