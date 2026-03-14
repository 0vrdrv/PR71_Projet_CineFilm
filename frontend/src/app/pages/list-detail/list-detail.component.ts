import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FormControl } from '@angular/forms';
import { debounceTime, distinctUntilChanged, switchMap, of } from 'rxjs';
import { UserActionService } from '../../services/user-action.service';
import { MovieService } from '../../services/movie.service';
import { NotificationService } from '../../services/notification.service';

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
    private movieService: MovieService,
    private notificationService: NotificationService
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

  addMovie(movie: any) {
    this.userActionService.addMovieToList(this.listId, movie.id, movie.title, movie.poster_path).subscribe(() => {
      this.notificationService.success("Film ajouté à la liste !");
      this.searchControl.setValue('', { emitEvent: false });
      this.showDropdown = false;
      this.fetchListItems();
    });
  }

  removeMovie(tmdbId: number) {
    this.userActionService.removeMovieFromList(this.listId, tmdbId).subscribe(() => {
      this.notificationService.info("Film retiré de la liste");
      this.fetchListItems();
    });
  }

  closeSearch() {
    setTimeout(() => this.showDropdown = false, 200);
  }
}
