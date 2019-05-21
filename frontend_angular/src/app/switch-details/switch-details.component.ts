import {Component, OnInit} from '@angular/core';

import {Observable} from 'rxjs';
import {ActivatedRoute} from '@angular/router';

import {ModelSwitch} from '../api/model/modelSwitch';
import {SwitchService} from '../api/api/switch.service';

import {PortService} from '../api/api/port.service';
import {Port} from '../api/model/port';

import {SearchPage} from '../search-page';
import {BehaviorSubject} from 'rxjs';
import {PagingConf} from '../paging.config';

import {map} from 'rxjs/operators';

export interface PortListResult {
  ports: Array<Port>;
  item_count?: number;
  current_page?: number;
  items_per_page?: number;
}

@Component({
  selector: 'app-switch-details',
  templateUrl: './switch-details.component.html',
  styleUrls: ['./switch-details.component.css']
})
export class SwitchDetailsComponent extends SearchPage implements OnInit {

  switch$: Observable<ModelSwitch>;
  result$: Observable<PortListResult>;
  switchID: number;
  page_number = 1;
  item_count = 1;
  items_per_page: number = +PagingConf.item_count;
  private sub: any;
  private searchTerms = new BehaviorSubject<string>('');

  constructor(public switchService: SwitchService, private route: ActivatedRoute, public portService: PortService) {
    super();
  }

  search(term: string): void {
    this.searchTerms.next(term);
  }

  private fetchPorts(terms: string, page: number): Observable<PortListResult> {
    const n = +PagingConf.item_count;
    return this.portService.portGet(n, (page - 1) * n, this.switchID, undefined, terms, 'response')
      .pipe(
        map((response) => {
          return <PortListResult> {
            ports: response.body,
            item_count: +response.headers.get('x-total-count'),
            current_page: page,
            items_per_page: n,
          };
        }),
      );
  }

  ngOnInit() {
    super.ngOnInit();
    this.sub = this.route.params.subscribe(params => {
      this.switchID = +params['switchID'];
      this.switch$ = this.switchService.switchSwitchIDGet(this.switchID);
      this.result$ = this.getSearchResult((terms, page) => this.fetchPorts(terms, page));
    });
    // this.refreshPorts(1);
  }

}
