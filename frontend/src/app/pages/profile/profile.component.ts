import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FormControl } from '@angular/forms';
import { debounceTime, distinctUntilChanged, switchMap, of } from 'rxjs';
import { UserActionService } from '../../services/user-action.service';
import { MovieService } from '../../services/movie.service';
import { NotificationService } from '../../services/notification.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'],
})
export class ProfileComponent implements OnInit {
  user: any = null;
  watchlist: any[] = [];
  diary: any[] = [];
  userLists: any[] = [];
  stats: any = null;

  activeTab: string = 'watchlist';
  isOwnProfile: boolean = false;
  isFollowing: boolean = false;
  currentUserId: number | null = null;
  loading: boolean = true;

  // Favorites
  favorites: any[] = [null, null, null, null];
  showFavoriteSearch: boolean = false;
  selectedRank: number = 1;
  favoriteSearchControl = new FormControl('');
  favoriteSearchResults: any[] = [];

  // Watched
  watchedFilms: any[] = [];

  // Detailed stats
  detailedStats: any = null;

  constructor(
    private userActionService: UserActionService,
    private movieService: MovieService,
    private notificationService: NotificationService,
    private route: ActivatedRoute,
  ) {}

  ngOnInit(): void {
    this.userActionService.getCurrentUser().subscribe({
      next: (user: any) => {
        this.currentUserId = user.id;
      },
      error: () => {
        this.currentUserId = null;
      }
    });

    this.route.paramMap.subscribe((params) => {
      const userId = params.get('id');

      if (userId) {
        this.isOwnProfile = false;
        this.loadOtherUser(Number(userId));
      } else {
        this.isOwnProfile = true;
        this.loadCurrentUser();
      }
    });

    this.favoriteSearchControl.valueChanges.pipe(
      debounceTime(300),
      distinctUntilChanged(),
      switchMap((query: string | null) => {
        if (!query || query.length < 2) return of({ results: [] });
        return this.movieService.searchMovies(query);
      })
    ).subscribe((data: any) => {
      this.favoriteSearchResults = data.results?.slice(0, 8) || [];
    });
  }

  loadCurrentUser() {
    this.userActionService.getCurrentUser().subscribe({
      next: (userData: any) => {
        this.user = userData;
        this.loadUserData(this.user.id);
      },
    });
  }

  loadOtherUser(id: number) {
    this.userActionService.getUserById(id).subscribe((userData: any) => {
      this.user = userData;
      this.loadUserData(id);

      if (this.currentUserId && this.currentUserId !== id) {
        this.userActionService.getFollowStatus(id).subscribe((res: any) => {
          this.isFollowing = res.following;
        });
      }
    });
  }

  loadUserData(userId: number) {
    this.loading = true;

    this.userActionService.getUserStats(userId).subscribe((data: any) => {
      this.stats = data;
    });

    this.userActionService.getWatchlist(userId).subscribe((data: any) => {
      this.watchlist = data;
    });

    this.userActionService.getUserLists(userId).subscribe((data: any) => {
      this.userLists = data;
    });

    this.userActionService.getDiary(userId).subscribe((data: any) => {
      this.diary = data;

      this.diary.forEach((review: any) => {
        if (!review.poster_path) {
          this.movieService
            .getMovieDetails(review.tmdb_id)
            .subscribe((movieData: any) => {
              review.poster_path = movieData.poster_path;
            });
        }
      });

      this.loading = false;
    });

    // Load favorites
    this.userActionService.getFavorites(userId).subscribe((data: any) => {
      this.favorites = [null, null, null, null];
      data.forEach((fav: any) => {
        if (fav.rank >= 1 && fav.rank <= 4) {
          this.favorites[fav.rank - 1] = fav;
        }
      });
    });

    // Load watched films
    this.userActionService.getUserWatched(userId).subscribe((data: any) => {
      this.watchedFilms = data;
    });

    // Load detailed stats
    this.userActionService.getDetailedStats(userId).subscribe((data: any) => {
      this.detailedStats = data;
    });
  }

  setTab(tab: string) {
    this.activeTab = tab;
  }

  toggleFollow() {
    if (!this.user || !this.currentUserId) return;

    if (this.isFollowing) {
      this.userActionService.unfollowUser(this.user.id).subscribe(() => {
        this.isFollowing = false;
        this.notificationService.info("Vous ne suivez plus cet utilisateur");
        if (this.stats) {
          this.stats.followers_count--;
        }
      });
    } else {
      this.userActionService.followUser(this.user.id).subscribe(() => {
        this.isFollowing = true;
        this.notificationService.success("Utilisateur suivi !");
        if (this.stats) {
          this.stats.followers_count++;
        }
      });
    }
  }

  removeFromWatchlist(tmdbId: number) {
    this.userActionService.removeFromWatchlist(tmdbId).subscribe(() => {
      this.watchlist = this.watchlist.filter(item => item.tmdb_id !== tmdbId);
      this.notificationService.info("Film retiré de la watchlist");
    });
  }

  // Favorites methods
  openFavoriteSelector(rank: number) {
    if (!this.isOwnProfile) return;
    this.selectedRank = rank;
    this.showFavoriteSearch = true;
    this.favoriteSearchResults = [];
    this.favoriteSearchControl.setValue('');
  }

  selectFavorite(movie: any) {
    this.userActionService.setFavorite(
      movie.id, movie.title, movie.poster_path, this.selectedRank
    ).subscribe(() => {
      this.favorites[this.selectedRank - 1] = {
        tmdb_id: movie.id,
        movie_title: movie.title,
        poster_path: movie.poster_path,
        rank: this.selectedRank
      };
      this.showFavoriteSearch = false;
      this.notificationService.success("Film favori ajouté !");
    });
  }

  removeFav(rank: number) {
    this.userActionService.removeFavorite(rank).subscribe(() => {
      this.favorites[rank - 1] = null;
      this.notificationService.info("Film favori retiré");
    });
  }

  closeFavoriteSearch() {
    this.showFavoriteSearch = false;
  }

  getRatingKeys(): string[] {
    if (!this.detailedStats?.rating_distribution) return [];
    return Object.keys(this.detailedStats.rating_distribution);
  }

  getMaxRating(): number {
    if (!this.detailedStats?.rating_distribution) return 1;
    const vals = Object.values(this.detailedStats.rating_distribution) as number[];
    return Math.max(...vals, 1);
  }
}
