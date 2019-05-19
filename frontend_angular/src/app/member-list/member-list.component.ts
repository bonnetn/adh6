import {Component, OnInit} from '@angular/core';

import {Observable} from 'rxjs';


import {MemberService} from '../api/api/member.service';
import {Member} from '../api/model/member';
import {PagingConf} from '../paging.config';

import {map} from 'rxjs/operators';
import {SearchPage} from '../search-page';

class MemberListResponse {
  members?: Array<Member>;
  page_number?: number;
  item_count?: number;
  item_per_page?: number;
}

@Component({
  selector: 'app-members',
  templateUrl: './member-list.component.html',
  styleUrls: ['./member-list.component.css']
})
export class MemberListComponent extends SearchPage implements OnInit {

  result$: Observable<MemberListResponse>;

  constructor(public memberService: MemberService) {
    super();
  }

  ngOnInit() {
    super.ngOnInit();
    this.result$ = this.getSearchResult((terms, page) => this.fetchMembers(terms, page));
  }

  private fetchMembers(terms: string, page: number) {
    const n = +PagingConf.item_count;
    return this.memberService.memberGet(n, (page - 1) * n, terms, undefined, 'response')
      .pipe(
        // switch to new search observable each time the term changes
        map((response) => <MemberListResponse>{
          members: response.body,
          item_count: +response.headers.get('x-total-count'),
          page_number: page,
          item_per_page: n,
        }),
      );
  }

}
