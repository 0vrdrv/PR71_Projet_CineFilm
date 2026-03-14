import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Router, NavigationEnd } from '@angular/router';
import { debounceTime, distinctUntilChanged, switchMap, of, filter } from 'rxjs';
import { trigger, transition, style, animate } from '@angular/animations';
import { AuthService } from './services/auth.service';
import { MovieService } from './services/movie.service';
import { UserActionService } from './services/user-action.service';
import { DarkModeService } from './services/dark-mode.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  animations: [
    trigger('routeAnimation', [
      transition('* <=> *', [
        style({ opacity: 0, transform: 'translateY(10px)' }),
        animate('300ms ease-out', style({ opacity: 1, transform: 'translateY(0)' }))
      ])
    ])
  ]
})
export class AppComponent implements OnInit, OnDestroy {
  isLoggedIn: boolean = false;
  scrolled: boolean = false;
  currentUserInitial: string = '';
  isDarkMode: boolean = false;

  searchControl = new FormControl('');
  searchResults: any[] = [];
  showDropdown: boolean = false;
  mobileMenuOpen = false;

  private scrollListener: (() => void) | null = null;

  constructor(
    private authService: AuthService,
    private movieService: MovieService,
    private userActionService: UserActionService,
    private router: Router,
    private darkModeService: DarkModeService,
  ) {}

  ngOnInit() {
    this.authService.isLoggedIn$.subscribe((status) => {
      this.isLoggedIn = status;
      if (status) {
        this.userActionService.getCurrentUser().subscribe((user: any) => {
          this.currentUserInitial = user.username?.charAt(0)?.toUpperCase() || '?';
        });
      } else {
        this.currentUserInitial = '';
      }
    });

    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe(() => {
      window.scrollTo(0, 0);
      this.mobileMenuOpen = false;
    });

    this.scrollListener = () => {
      this.scrolled = window.scrollY > 30;
    };
    window.addEventListener('scroll', this.scrollListener);

    this.darkModeService.isDarkMode$.subscribe((dark) => {
      this.isDarkMode = dark;
      if (dark) {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
    });

    this.searchControl.valueChanges
      .pipe(
        debounceTime(300),
        distinctUntilChanged(),
        switchMap((query) => {
          if (!query || query.length < 2) {
            return of({ results: [] });
          }
          return this.movieService.searchMovies(query);
        }),
      )
      .subscribe((data: any) => {
        this.searchResults = data.results.slice(0, 5);
        this.showDropdown = this.searchResults.length > 0;
      });
  }

  ngOnDestroy() {
    if (this.scrollListener) {
      window.removeEventListener('scroll', this.scrollListener);
    }
  }

  toggleDarkMode() {
    this.darkModeService.toggle();
  }

  logout() {
    this.authService.logout();
  }

  goToMovie(id: number) {
    this.showDropdown = false;
    this.searchControl.setValue('', { emitEvent: false });
    this.router.navigate(['/films', id]);
  }

  closeSearch() {
    setTimeout(() => (this.showDropdown = false), 200);
  }

  toggleMobileMenu() {
    this.mobileMenuOpen = !this.mobileMenuOpen;
  }

  onSearchEnter() {
    const query = this.searchControl.value;
    if (query && query.length >= 2) {
      this.showDropdown = false;
      this.searchControl.setValue('', { emitEvent: false });
      this.router.navigate(['/search'], { queryParams: { q: query } });
    }
  }
}
