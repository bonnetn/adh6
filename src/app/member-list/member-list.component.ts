import { Component, OnInit } from '@angular/core';

import {Observable} from 'rxjs/Observable';
import { BehaviorSubject }    from 'rxjs/BehaviorSubject';


import { UserService } from '../api/services/user.service'
import { User } from '../api/models/user'

import {
   debounceTime, distinctUntilChanged, switchMap
 } from 'rxjs/operators';

@Component({
  selector: 'app-members',
  templateUrl: './member-list.component.html',
  styleUrls: ['./member-list.component.css']
})
export class MemberListComponent implements OnInit {

  members$: Observable<User[]>;
  private searchTerms = new BehaviorSubject<string>("");
  
  constructor(public userService: UserService) { }

  search(term: string): void {
    this.searchTerms.next(term);
  }

  ngOnInit() {
    this.members$ = this.searchTerms.pipe(
      // wait 300ms after each keystroke before considering the term
      debounceTime(300),

      // ignore new term if same as previous term
      distinctUntilChanged(),

      // switch to new search observable each time the term changes
      switchMap((term: string) => this.userService.filterUser( { 'terms':term } )),
    );
    //this.searchTerms.next("c");
  }

}
