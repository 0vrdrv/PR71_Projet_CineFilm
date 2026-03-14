import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { MovieService } from '../../services/movie.service';
import { UserActionService } from '../../services/user-action.service';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit {
  searchQuery: string = '';
  activeTab: 'films' | 'members' = 'films';
  filmResults: any[] = [];
  memberResults: any[] = [];
  loading: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private movieService: MovieService,
    private http: HttpClient
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      if (params['q']) {
        this.searchQuery = params['q'];
        this.search(this.searchQuery);
      }
    });
  }

  search(query: string) {
    if (!query || query.length < 2) return;
    this.loading = true;

    this.movieService.searchMovies(query).subscribe((data: any) => {
      this.filmResults = data.results || [];
      this.loading = false;
    });

    this.http.get<any[]>(`http://127.0.0.1:8000/users/search?q=${encodeURIComponent(query)}`).subscribe({
      next: (users) => this.memberResults = users,
      error: () => this.memberResults = []
    });
  }
}
