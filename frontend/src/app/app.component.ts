import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Router } from '@angular/router';
import { debounceTime, distinctUntilChanged, switchMap, of } from 'rxjs';
import { AuthService } from './services/auth.service';
import { MovieService } from './services/movie.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  isLoggedIn: boolean = false;
  
  searchControl = new FormControl('');
  searchResults: any[] = [];
  showDropdown: boolean = false;

  constructor(
    private authService: AuthService,
    private movieService: MovieService,
    private router: Router
  ) {}

  ngOnInit() {
    this.authService.isLoggedIn$.subscribe(status => {
      this.isLoggedIn = status;
    });

    this.searchControl.valueChanges.pipe(
      debounceTime(300),
      distinctUntilChanged(),
      switchMap(query => {
        if (!query || query.length < 2) {
          return of({ results: [] });
        }
        return this.movieService.searchMovies(query);
      })
    ).subscribe((data: any) => {
      this.searchResults = data.results.slice(0, 5);
      this.showDropdown = this.searchResults.length > 0;
    });
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
    setTimeout(() => this.showDropdown = false, 200);
  }
}