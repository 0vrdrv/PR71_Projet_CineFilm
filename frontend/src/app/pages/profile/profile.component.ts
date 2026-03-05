import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { UserActionService } from '../../services/user-action.service';
import { MovieService } from '../../services/movie.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'],
})
export class ProfileComponent implements OnInit {
  user: any = null;
  watchlist: any[] = [];
  diary: any[] = [];

  activeTab: string = 'watchlist';
  isOwnProfile: boolean = false;

  constructor(
    private userActionService: UserActionService,
    private movieService: MovieService,
    private route: ActivatedRoute,
  ) {}

  ngOnInit(): void {
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
    });
  }

  loadUserData(userId: number) {
    this.userActionService.getWatchlist(userId).subscribe((data: any) => {
      this.watchlist = data;
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
    });
  }

  setTab(tab: string) {
    this.activeTab = tab;
  }
}
