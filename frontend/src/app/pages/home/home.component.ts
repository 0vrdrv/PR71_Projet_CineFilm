import { Component, OnInit } from '@angular/core';
import { MovieService } from '../../services/movie.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  movies: any[] = [];
  heroMovie: any = null;

  constructor(private movieService: MovieService) {}

  ngOnInit(): void {
    this.movieService.getNewReleases().subscribe((data: any) => {
      this.movies = data.results.slice(0, 8);
    });

    this.movieService.getPopularMovies().subscribe((data: any) => {
      this.heroMovie = data.results[0];
    });
  }
}