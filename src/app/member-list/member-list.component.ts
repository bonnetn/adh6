import { Component, OnInit } from '@angular/core';

import {Observable} from 'rxjs/Observable';

import { UserService } from '../api/services/user.service'
import { User } from '../api/models/user'

@Component({
  selector: 'app-members',
  templateUrl: './member-list.component.html',
  styleUrls: ['./member-list.component.css']
})
export class MemberListComponent implements OnInit {

  members$: Observable<User[]>;
  
  constructor(public userService: UserService) { }

  ngOnInit() {
    this.members$ = this.userService.filterUser( {} );
  }

}
