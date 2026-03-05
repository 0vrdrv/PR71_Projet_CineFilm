import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FormControl } from '@angular/forms';
import { debounceTime, distinctUntilChanged, switchMap, of } from 'rxjs';
import { UserActionService } from '../../services/user-action.service';
import { MovieService } from '../../services/movie.service';

@Component({
  selector: 'app-list-detail',
  templateUrl: './list-detail.component.html',
  styleUrls: ['./list-detail.component.scss']
})
export class ListDetailComponent implements OnInit {
  listId!: number;
  listDetails: any = null;
  listItems: any[] = [];
  
  searchControl = new FormControl('');
  searchResults: any[] = [];
  showDropdown: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private userActionService: UserActionService,
    private movieService: MovieService
  ) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      const id = params.get('id');
      if (id) {
        this.listId = Number(id);
        this.fetchListDetails();
        this.fetchListItems();
      }
    });

    // Moteur de recherche instantané TMDb
    this.searchControl.valueChanges.pipe(
      debounceTime(300),
      distinctUntilChanged(),
      switchMap(query => {
        if (!query || query.length < 2) return of({ results: [] });
        return this.movieService.searchMovies(query);
      })
    ).subscribe((data: any) => {
      this.searchResults = data.results.slice(0, 5);
      this.showDropdown = this.searchResults.length > 0;
    });
  }

  fetchListDetails() {
    this.userActionService.getListById(this.listId).subscribe(data => this.listDetails = data);
  }

  fetchListItems() {
    this.userActionService.getListItems(this.listId).subscribe(data => this.listItems = data);
  }

  // Ajoute le film directement à la liste en cliquant sur le résultat
  addMovie(movie: any) {
    this.userActionService.addMovieToList(this.listId, movie.id, movie.title, movie.poster_path).subscribe(() => {
      this.searchControl.setValue('', { emitEvent: false });
      this.showDropdown = false;
      this.fetchListItems(); // Recharge la grille de la liste
    });
  }

  closeSearch() {
    setTimeout(() => this.showDropdown = false, 200);
  }
}