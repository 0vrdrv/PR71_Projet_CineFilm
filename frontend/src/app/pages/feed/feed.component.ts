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
  currentPage = 1;

  constructor(
    private http: HttpClient,
    private authService: AuthService,
    private movieService: MovieService
  ) {}

  ngOnInit(): void {
    this.authService.isLoggedIn$.subscribe(status => {
      this.isLoggedIn = status;
      if (status) {
        this.loadFeed(1);
      } else {
        this.loading = false;
      }
    });
  }

  loadFeed(page: number) {
    this.loading = true;
    this.http.get<any>(`http://127.0.0.1:8000/feed?page=${page}&limit=20`).subscribe({
      next: data => {
        const reviews = data.reviews || data;
        const newReviews = Array.isArray(reviews) ? reviews : [];
        newReviews.forEach((r: any) => {
          this.movieService.getMovieDetails(r.tmdb_id).subscribe(movie => {
            r.poster_path = movie.poster_path ?? undefined;
          });
        });
        if (page === 1) {
          this.feedReviews = newReviews;
        } else {
          this.feedReviews = [...this.feedReviews, ...newReviews];
        }
        this.loading = false;
      },
      error: () => this.loading = false
    });
  }

  loadMore() {
    this.currentPage++;
    this.loadFeed(this.currentPage);
  }
}
