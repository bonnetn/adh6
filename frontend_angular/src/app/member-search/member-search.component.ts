import {Component, OnInit} from '@angular/core';

import {Observable} from 'rxjs/Observable';
import {BehaviorSubject} from 'rxjs/BehaviorSubject';


import {MemberService} from '../api/api/member.service';
import {Member} from '../api/model/member';
import {PagingConf} from '../paging.config';

import {map, tap} from 'rxjs/operators';
import {PagingUtils} from '../paging-utils';

class MemberListResponse {
  members?: Array<Member>;
  page_number?: number;
  item_count?: number;
}

@Component({
  selector: 'app-members',
  templateUrl: './member-search.component.html',
  styleUrls: ['./member-search.component.css']
})
export class MemberSearchComponent implements OnInit {

  result$: Observable<MemberListResponse>;

  ITEMS_PER_PAGE: number = +PagingConf.item_count;
  private searchTerm$ = new BehaviorSubject<string>('');
  private pageNumber$ = new BehaviorSubject<number>(1);

  constructor(public memberService: MemberService) {
  }

  search(term: string): void {
    this.searchTerm$.next(term);
  }

  refreshMembers(page: number): void {
    this.pageNumber$.next(page);
  }

  ngOnInit() {
    this.refreshMembers(1);
    this.result$ = PagingUtils.getSearchResult(this.searchTerm$, this.pageNumber$, (terms, page) => this.buildRequest(terms, page));
  }

  private buildRequest(terms: string, page: number) {
    return this.memberService.filterMember(this.ITEMS_PER_PAGE, (page - 1) * this.ITEMS_PER_PAGE, terms, undefined, 'response')
      .pipe(
        // switch to new search observable each time the term changes
        map((response) => <MemberListResponse>{
          members: response.body,
          item_count: +response.headers.get('x-total-count'),
          page_number: page,
        }),
        tap( (response) => console.log(response)),
      );
  }

}
