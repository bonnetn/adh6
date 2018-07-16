import { Component, OnInit } from '@angular/core';

import { Observable } from 'rxjs/Observable';
import { BehaviorSubject }    from 'rxjs/BehaviorSubject';
import { NgxPaginationModule } from 'ngx-pagination';


import { UserService } from '../api/services/user.service'
import { User } from '../api/models/user'
import { PagingConf } from '../paging.config'

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
  page_number : number = 1;
  item_count : number = 1;
  items_per_page : number = +PagingConf.item_count;
  private searchTerms = new BehaviorSubject<string>("");
  
  constructor(public userService: UserService) { }

  search(term: string): void {
    this.searchTerms.next(term);
  }

  refreshMembers(page:number) : void {
    this.members$ = this.searchTerms.pipe(
      // wait 300ms after each keystroke before considering the term
      debounceTime(300),

      // ignore new term if same as previous term
      distinctUntilChanged(),

      // switch to new search observable each time the term changes
      switchMap((term: string) => this.userService.filterUserResponse( { 'terms':term, 'limit':this.items_per_page, 'offset':(page-1)*this.items_per_page} )),
      switchMap((response) => {
        this.item_count = +response.headers.get("x-total-count")
        this.page_number = page;  
        return Observable.of(response.body)
      }),
    );
  }

  ngOnInit() {
    this.refreshMembers(1)
    //this.searchTerms.next("c");
  }

}
