import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { UserActionService } from '../../services/user-action.service';

@Component({
  selector: 'app-members',
  templateUrl: './members.component.html',
  styleUrls: ['./members.component.scss']
})
export class MembersComponent implements OnInit {
  users: any[] = [];
  filteredUsers: any[] = [];
  searchControl = new FormControl('');
  loading: boolean = true;

  constructor(private userActionService: UserActionService) {}

  ngOnInit(): void {
    this.userActionService.getAllUsers().subscribe(data => {
      this.users = data;
      this.filteredUsers = data;
      this.loading = false;
    });

    this.searchControl.valueChanges.subscribe(query => {
      if (!query) {
        this.filteredUsers = this.users;
      } else {
        const q = query.toLowerCase();
        this.filteredUsers = this.users.filter(u =>
          u.username.toLowerCase().includes(q)
        );
      }
    });
  }
}
