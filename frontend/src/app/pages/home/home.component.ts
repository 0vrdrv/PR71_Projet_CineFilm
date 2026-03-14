import { Component, OnInit, OnDestroy } from '@angular/core';
import { MovieService } from '../../services/movie.service';
import { UserActionService } from '../../services/user-action.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit, OnDestroy {
  movies: any[] = [];
  heroMovies: any[] = [];
  currentHeroIndex: number = 0;
  trendingMovies: any[] = [];
  loading: boolean = true;

  popularReviews: any[] = [];
  popularLists: any[] = [];

  private heroInterval: any;

  constructor(
    private movieService: MovieService,
    private userActionService: UserActionService
  ) {}

  ngOnInit(): void {
    this.movieService.getNewReleases().subscribe((data: any) => {
      this.movies = data.results.slice(0, 8);
      this.loading = false;
    });

    this.movieService.getPopularMovies().subscribe((data: any) => {
      this.heroMovies = data.results.slice(0, 4);
    });

    this.movieService.getTrending().subscribe((data: any) => {
      this.trendingMovies = data.results.slice(0, 8);
    });

    this.userActionService.getRecentReviews().subscribe((data: any) => {
      this.popularReviews = (data.reviews || []).slice(0, 4);
    });

    this.userActionService.getPublicLists().subscribe((data: any) => {
      this.popularLists = (data.lists || []).slice(0, 4);
    });

    this.heroInterval = setInterval(() => {
      if (this.heroMovies.length > 0) {
        this.currentHeroIndex = (this.currentHeroIndex + 1) % this.heroMovies.length;
      }
    }, 6000);
  }

  ngOnDestroy(): void {
    if (this.heroInterval) {
      clearInterval(this.heroInterval);
    }
  }

  setHeroIndex(index: number) {
    this.currentHeroIndex = index;
  }

  get currentHero(): any {
    return this.heroMovies[this.currentHeroIndex] || null;
  }

  getRatingColor(rating: number): string {
    if (rating < 2) return 'border-accent-red';
    if (rating < 3.5) return 'border-brand-500';
    return 'border-accent-green';
  }
}
