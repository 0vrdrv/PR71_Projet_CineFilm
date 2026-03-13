import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../../services/auth.service';
import { MovieService } from '../../services/movie.service';
import { Review } from '../../models';

@Component({
  selector: 'app-feed',
  templateUrl: './feed.component.html',
  styleUrls: ['./feed.component.scss']
})
export class FeedComponent implements OnInit {
  feedReviews: (Review & { poster_path?: string })[] = [];
  isLoggedIn = false;
  loading = true;

  constructor(
    private http: HttpClient,
    private authService: AuthService,
    private movieService: MovieService
  ) {}

  ngOnInit(): void {
    this.authService.isLoggedIn$.subscribe(status => {
      this.isLoggedIn = status;
      if (status) {
        this.http.get<Review[]>('http://127.0.0.1:8000/feed').subscribe({
          next: reviews => {
            this.feedReviews = reviews;
            this.feedReviews.forEach(r => {
              this.movieService.getMovieDetails(r.tmdb_id).subscribe(movie => {
                r.poster_path = movie.poster_path ?? undefined;
              });
            });
            this.loading = false;
          },
          error: () => this.loading = false
        });
      } else {
        this.loading = false;
      }
    });
  }
}