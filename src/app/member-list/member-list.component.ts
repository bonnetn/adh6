import { Component, OnInit } from '@angular/core';

import {Observable} from 'rxjs/Observable';
import { BehaviorSubject }    from 'rxjs/BehaviorSubject';
import {NgxPaginationModule} from 'ngx-pagination';


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
  page_number : number = 0
  private searchTerms = new BehaviorSubject<string>("");
  private PAGE_SIZE : number = 10;
  
  constructor(public userService: UserService) { }

  search(term: string): void {
    this.searchTerms.next(term);
  }

  refreshMembers(page:number) : void {
    this.page_number = page;  
    this.members$ = this.searchTerms.pipe(
      // wait 300ms after each keystroke before considering the term
      debounceTime(300),

      // ignore new term if same as previous term
      distinctUntilChanged(),

      // switch to new search observable each time the term changes
      switchMap((term: string) => {
        return this.userService.filterUser( { 'terms':term, 'limit':this.PAGE_SIZE, 'offset':page*this.PAGE_SIZE} )
      }),
    );
  }

  ngOnInit() {
    this.refreshMembers(0)
    //this.searchTerms.next("c");
  }

}
