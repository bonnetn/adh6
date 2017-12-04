import { Component, OnInit, OnDestroy } from '@angular/core';

import { Observable } from 'rxjs/Observable';

import { UserService } from '../api/services/user.service';
import { User } from '../api/models/user';

import { ActivatedRoute } from '@angular/router';


@Component({
  selector: 'app-member-details',
  templateUrl: './member-details.component.html',
  styleUrls: ['./member-details.component.css']
})
export class MemberDetailsComponent implements OnInit, OnDestroy {

  member$: Observable<User>;
  username: string;
  private sub: any;

  constructor(public userService: UserService, private route: ActivatedRoute) { }

  ngOnInit() {

     this.sub = this.route.params.subscribe(params => {
       this.username = params['username']; // (+) converts string 'id' to a number
       this.member$ = this.userService.getUser(this.username);
     });
  }
  ngOnDestroy() {
    this.sub.unsubscribe();
  }

}
