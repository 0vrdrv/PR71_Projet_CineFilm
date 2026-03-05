import { Component, OnInit } from '@angular/core';
import { UserActionService } from '../../services/user-action.service';

@Component({
  selector: 'app-members',
  templateUrl: './members.component.html',
  styleUrls: ['./members.component.scss']
})
export class MembersComponent implements OnInit {
  users: any[] = [];

  constructor(private userActionService: UserActionService) {}

  ngOnInit(): void {
    this.userActionService.getAllUsers().subscribe(data => {
      this.users = data;
    });
  }
}