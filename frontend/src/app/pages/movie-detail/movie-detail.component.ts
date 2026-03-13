import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MovieService } from '../../services/movie.service';
import { UserActionService } from '../../services/user-action.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-movie-detail',
  templateUrl: './movie-detail.component.html',
  styleUrls: ['./movie-detail.component.scss'],
})
export class MovieDetailComponent implements OnInit {
  movie: any;
  cast: any[] = [];
  isLoggedIn: boolean = false;
  currentUserId: number | null = null;
  actionMessage: string = '';

  showReviewForm: boolean = false;
  reviewRating: number = 5;
  reviewComment: string = '';
  editingReviewId: number | null = null;

  hoverValue: number = 0;
  ratingValues: number[] = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5];

  movieReviews: any[] = [];

  similarMovies: Movie[] = [];

  constructor(
    private route: ActivatedRoute,
    private movieService: MovieService,
    private userActionService: UserActionService,
    private authService: AuthService,
  ) {}

  ngOnInit(): void {
    this.authService.isLoggedIn$.subscribe((status) => {
      this.isLoggedIn = status;
      if (status) {
        this.userActionService.getCurrentUser().subscribe((user) => {
          this.currentUserId = user.id;
        });
      }
    });

    this.route.paramMap.subscribe((params) => {
      const movieId = params.get('id');
      if (movieId) {
        this.fetchMovieData(movieId);
        this.loadReviews(Number(movieId));
      }
    });
  }

  fetchMovieData(id: string) {
    this.movieService
      .getMovieDetails(id)
      .subscribe((data) => (this.movie = data));
    this.movieService
      .getMovieCast(id)
      .subscribe((data) => (this.cast = data.cast.slice(0, 6)));
    this.movieService.getSimilarMovies(Number(id)).subscribe((data) => {
      this.similarMovies = data.results.slice(0, 6);
    });
  }

  loadReviews(tmdbId: number) {
    this.userActionService.getMovieReviews(tmdbId).subscribe((reviews) => {
      this.movieReviews = reviews;
    });
  }

  addToWatchlist() {
    if (!this.isLoggedIn) return;
    this.userActionService
      .addToWatchlist(this.movie.id, this.movie.title, this.movie.poster_path)
      .subscribe({
        next: () => (this.actionMessage = 'Film ajouté à votre Watchlist !'),
        error: () => (this.actionMessage = "Erreur lors de l'ajout."),
      });
  }

  submitReview() {
    if (!this.isLoggedIn) return;

    if (this.editingReviewId) {
      this.userActionService
        .updateReview(
          this.editingReviewId,
          this.reviewRating,
          this.reviewComment,
        )
        .subscribe(() => {
          this.actionMessage = 'Avis mis à jour !';
          this.showReviewForm = false;
          this.editingReviewId = null;
          this.loadReviews(this.movie.id);
        });
    } else {
      this.userActionService
        .addReview(
          this.movie.id,
          this.movie.title,
          this.reviewRating,
          this.reviewComment,
        )
        .subscribe(() => {
          this.actionMessage = 'Avis publié !';
          this.showReviewForm = false;
          this.loadReviews(this.movie.id);
        });
    }
  }

  editReview(review: any) {
    this.showReviewForm = true;
    this.reviewRating = review.rating;
    this.reviewComment = review.comment;
    this.editingReviewId = review.id;
    window.scrollTo(0, 0);
  }

  deleteReview(reviewId: number) {
    if (confirm('Voulez-vous vraiment supprimer cet avis ?')) {
      this.userActionService.deleteReview(reviewId).subscribe(() => {
        this.actionMessage = 'Avis supprimé.';
        this.loadReviews(this.movie.id);
      });
    }
  }
}
