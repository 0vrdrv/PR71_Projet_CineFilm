import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MovieService } from '../../services/movie.service';

@Component({
  selector: 'app-activity',
  templateUrl: './activity.component.html',
  styleUrls: ['./activity.component.scss']
})
export class ActivityComponent implements OnInit {
  recentReviews: any[] = [];
  loading: boolean = true;
  currentPage: number = 1;

  constructor(
    private http: HttpClient,
    private movieService: MovieService
  ) {}

  ngOnInit(): void {
    this.loadReviews(1);
  }

  loadReviews(page: number) {
    this.loading = true;
    this.http.get<any>(`http://127.0.0.1:8000/reviews/recent?page=${page}`).subscribe({
      next: (data) => {
        const reviews = data.reviews || [];
        reviews.forEach((r: any) => {
          this.movieService.getMovieDetails(r.tmdb_id).subscribe(movie => {
            r.poster_path = movie.poster_path ?? null;
          });
        });
        if (page === 1) {
          this.recentReviews = reviews;
        } else {
          this.recentReviews = [...this.recentReviews, ...reviews];
        }
        this.loading = false;
      },
      error: () => this.loading = false
    });
  }

  loadMore() {
    this.currentPage++;
    this.loadReviews(this.currentPage);
  }
}
