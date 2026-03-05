import { Component, OnInit } from '@angular/core';
import { UserActionService } from '../../services/user-action.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-lists',
  templateUrl: './lists.component.html',
  styleUrls: ['./lists.component.scss']
})
export class ListsComponent implements OnInit {
  isLoggedIn: boolean = false;
  currentUser: any = null;
  myLists: any[] = [];
  
  showCreateForm: boolean = false;
  newListTitle: string = '';
  newListDesc: string = '';

  constructor(
    private userActionService: UserActionService,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    this.authService.isLoggedIn$.subscribe(status => {
      this.isLoggedIn = status;
      if (status) {
        this.userActionService.getCurrentUser().subscribe(user => {
          this.currentUser = user;
          this.loadMyLists();
        });
      }
    });
  }

  loadMyLists() {
    this.userActionService.getUserLists(this.currentUser.id).subscribe(lists => {
      this.myLists = lists;
    });
  }

  createNewList() {
    if (!this.newListTitle) return;
    
    this.userActionService.createList(this.newListTitle, this.newListDesc).subscribe(() => {
      this.newListTitle = '';
      this.newListDesc = '';
      this.showCreateForm = false;
      this.loadMyLists();
    });
  }
}