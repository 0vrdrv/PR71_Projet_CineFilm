import { Component, OnInit } from '@angular/core';
import { UserActionService } from '../../services/user-action.service';
import { AuthService } from '../../services/auth.service';
import { NotificationService } from '../../services/notification.service';

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

  showDeleteModal: boolean = false;
  listToDeleteId: number | null = null;

  // Public lists
  activeListTab: string = 'my';
  publicLists: any[] = [];

  constructor(
    private userActionService: UserActionService,
    private authService: AuthService,
    private notificationService: NotificationService
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

    this.loadPublicLists();
  }

  loadMyLists() {
    this.userActionService.getUserLists(this.currentUser.id).subscribe(lists => {
      this.myLists = lists;
    });
  }

  loadPublicLists() {
    this.userActionService.getPublicLists().subscribe((data: any) => {
      this.publicLists = data.lists || [];
    });
  }

  createNewList() {
    if (!this.newListTitle) return;

    this.userActionService.createList(this.newListTitle, this.newListDesc).subscribe(() => {
      this.notificationService.success("Liste créée !");
      this.newListTitle = '';
      this.newListDesc = '';
      this.showCreateForm = false;
      this.loadMyLists();
    });
  }

  deleteList(listId: number) {
    this.listToDeleteId = listId;
    this.showDeleteModal = true;
  }

  confirmDeleteList() {
    if (this.listToDeleteId) {
      this.userActionService.deleteList(this.listToDeleteId).subscribe(() => {
        this.notificationService.info("Liste supprimée");
        this.loadMyLists();
      });
    }
    this.showDeleteModal = false;
    this.listToDeleteId = null;
  }

  cancelDeleteList() {
    this.showDeleteModal = false;
    this.listToDeleteId = null;
  }
}
