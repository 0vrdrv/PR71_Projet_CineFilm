import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MovieService } from '../../services/movie.service';
import { UserActionService } from '../../services/user-action.service';
import { AuthService } from '../../services/auth.service';
import { NotificationService } from '../../services/notification.service';

@Component({
  selector: 'app-movie-detail',
  templateUrl: './movie-detail.component.html',
  styleUrls: ['./movie-detail.component.scss'],
})
export class MovieDetailComponent implements OnInit, OnDestroy {
  movie: any;
  cast: any[] = [];
  isLoggedIn: boolean = false;
  currentUserId: number | null = null;

  showReviewForm: boolean = false;
  reviewRating: number = 5;
  reviewComment: string = '';
  editingReviewId: number | null = null;

  hoverValue: number = 0;
  ratingValues: number[] = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5];

  movieReviews: any[] = [];

  similarMovies: any[] = [];

  showDeleteModal: boolean = false;
  reviewToDeleteId: number | null = null;

  isWatched: boolean = false;
  isInWatchlist: boolean = false;
  watchProviders: any = null;
  movieStats: any = null;
  reviewLikes: { [reviewId: number]: { liked: boolean; count: number } } = {};

  parallaxOffset: number = 0;
  private scrollListener: (() => void) | null = null;

  revealedSpoilers: Set<number> = new Set();
  expandedReviews: Set<number> = new Set();

  constructor(
    private route: ActivatedRoute,
    private movieService: MovieService,
    private userActionService: UserActionService,
    private authService: AuthService,
    private notificationService: NotificationService,
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
        this.loadMovieStats(Number(movieId));
        this.loadWatchProviders(Number(movieId));
        if (this.isLoggedIn) {
          this.loadStatuses(Number(movieId));
        }
      }
    });

    this.scrollListener = () => {
      this.parallaxOffset = window.scrollY * 0.25;
    };
    window.addEventListener('scroll', this.scrollListener);
  }

  ngOnDestroy(): void {
    if (this.scrollListener) {
      window.removeEventListener('scroll', this.scrollListener);
    }
  }

  fetchMovieData(id: string) {
    this.movieService.getMovieDetails(id).subscribe((data) => (this.movie = data));
    this.movieService.getMovieCast(id).subscribe((data) => (this.cast = data.cast.slice(0, 6)));
    this.movieService.getSimilarMovies(Number(id)).subscribe((data) => {
      this.similarMovies = data.results.slice(0, 6);
    });
  }

  loadStatuses(tmdbId: number) {
    this.userActionService.getWatchedStatus(tmdbId).subscribe((res: any) => {
      this.isWatched = res.watched;
    });
    this.userActionService.getWatchlistStatus(tmdbId).subscribe((res: any) => {
      this.isInWatchlist = res.in_watchlist;
    });
  }

  loadReviews(tmdbId: number) {
    this.userActionService.getMovieReviews(tmdbId).subscribe((reviews) => {
      this.movieReviews = reviews;
      reviews.forEach((r: any) => {
        this.reviewLikes[r.id] = { liked: false, count: r.likes_count || 0 };
        if (this.isLoggedIn) {
          this.userActionService.getReviewLikeStatus(r.id).subscribe((res: any) => {
            this.reviewLikes[r.id].liked = res.liked;
          });
        }
      });
    });
  }

  loadMovieStats(tmdbId: number) {
    this.userActionService.getMovieStats(tmdbId).subscribe((data: any) => {
      this.movieStats = data;
    });
  }

  loadWatchProviders(movieId: number) {
    this.movieService.getWatchProviders(movieId).subscribe((data: any) => {
      this.watchProviders = data;
    });
  }

  toggleWatched() {
    if (!this.isLoggedIn || !this.movie) return;
    if (this.isWatched) {
      this.userActionService.unmarkWatched(this.movie.id).subscribe(() => {
        this.isWatched = false;
        this.notificationService.info("Removed from watched");
      });
    } else {
      this.userActionService.markAsWatched(this.movie.id, this.movie.title, this.movie.poster_path).subscribe(() => {
        this.isWatched = true;
        this.notificationService.success("Marked as watched!");
      });
    }
  }

  toggleWatchlist() {
    if (!this.isLoggedIn || !this.movie) return;
    if (this.isInWatchlist) {
      this.userActionService.removeFromWatchlist(this.movie.id).subscribe(() => {
        this.isInWatchlist = false;
        this.notificationService.info("Removed from watchlist");
      });
    } else {
      this.userActionService.addToWatchlist(this.movie.id, this.movie.title, this.movie.poster_path).subscribe(() => {
        this.isInWatchlist = true;
        this.notificationService.success("Added to watchlist!");
      });
    }
  }

  toggleLike(reviewId: number) {
    if (!this.isLoggedIn) return;
    this.userActionService.toggleReviewLike(reviewId).subscribe((res: any) => {
      if (this.reviewLikes[reviewId]) {
        this.reviewLikes[reviewId].liked = res.liked;
        this.reviewLikes[reviewId].count += res.liked ? 1 : -1;
      }
    });
  }

  submitReview() {
    if (!this.isLoggedIn) return;

    if (this.editingReviewId) {
      this.userActionService.updateReview(this.editingReviewId, this.reviewRating, this.reviewComment).subscribe(() => {
        this.notificationService.success("Review updated!");
        this.showReviewForm = false;
        this.editingReviewId = null;
        this.loadReviews(this.movie.id);
      });
    } else {
      this.userActionService.addReview(this.movie.id, this.movie.title, this.reviewRating, this.reviewComment).subscribe(() => {
        this.notificationService.success("Review published!");
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
    this.reviewToDeleteId = reviewId;
    this.showDeleteModal = true;
  }

  confirmDeleteReview() {
    if (this.reviewToDeleteId) {
      this.userActionService.deleteReview(this.reviewToDeleteId).subscribe(() => {
        this.notificationService.info("Review deleted.");
        this.loadReviews(this.movie.id);
      });
    }
    this.showDeleteModal = false;
    this.reviewToDeleteId = null;
  }

  cancelDelete() {
    this.showDeleteModal = false;
    this.reviewToDeleteId = null;
  }

  toggleSpoiler(reviewId: number) {
    if (this.revealedSpoilers.has(reviewId)) {
      this.revealedSpoilers.delete(reviewId);
    } else {
      this.revealedSpoilers.add(reviewId);
    }
  }

  toggleExpandReview(reviewId: number) {
    if (this.expandedReviews.has(reviewId)) {
      this.expandedReviews.delete(reviewId);
    } else {
      this.expandedReviews.add(reviewId);
    }
  }

  getStatsRatingKeys(): string[] {
    if (!this.movieStats?.rating_distribution) return [];
    return Object.keys(this.movieStats.rating_distribution);
  }

  getStatsMaxRating(): number {
    if (!this.movieStats?.rating_distribution) return 1;
    const vals = Object.values(this.movieStats.rating_distribution) as number[];
    return Math.max(...vals, 1);
  }

  getRatingColor(rating: number): string {
    if (rating < 2) return 'border-accent-red';
    if (rating < 3.5) return 'border-brand-500';
    return 'border-accent-green';
  }
}
