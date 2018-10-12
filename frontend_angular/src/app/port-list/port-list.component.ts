import {Component, OnInit} from '@angular/core';

import {Observable} from 'rxjs/Observable';

import {PortService} from '../api/api/port.service';
import {Port} from '../api/model/port';
import {PagingConf} from '../paging.config';

import {map} from 'rxjs/operators';
import {SearchPage} from '../search-page';

export interface PortListResult {
  ports?: Array<Port>;
  item_count?: number;
  current_page?: number;
  items_per_page?: number;
}

@Component({
  selector: 'app-port-list',
  templateUrl: './port-list.component.html',
  styleUrls: ['./port-list.component.css']
})
export class PortListComponent extends SearchPage implements OnInit {

  result$: Observable<PortListResult>;

  constructor(public portService: PortService) {
    super();
  }

  ngOnInit() {
    super.ngOnInit();
    this.result$ = this.getSearchResult((terms, page) => this.fetchPort(terms, page));
  }

  private fetchPort(terms: string, page: number): Observable<PortListResult> {
    const n = +PagingConf.item_count;
    return this.portService.filterPort(n, (page - 1) * n, undefined, undefined, terms, 'response')
      .pipe(
        map((response) => {
          return <PortListResult>{
            ports: response.body,
            item_count: +response.headers.get('x-total-count'),
            current_page: page,
            items_per_page: n,
          };
        }),
      );

  }

}
