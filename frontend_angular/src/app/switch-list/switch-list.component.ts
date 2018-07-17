import { Component, OnInit } from '@angular/core';

import { Observable } from 'rxjs/Observable';

import { SwitchService } from '../api/api/switch.service';
import { ModelSwitch } from '../api/model/modelSwitch';

import { BehaviorSubject }    from 'rxjs/BehaviorSubject';
import { NgxPaginationModule } from 'ngx-pagination';
import { PagingConf } from '../paging.config'

import {
   debounceTime, distinctUntilChanged, switchMap
 } from 'rxjs/operators';

@Component({
  selector: 'app-switch-list',
  templateUrl: './switch-list.component.html',
  styleUrls: ['./switch-list.component.css']
})
export class SwitchListComponent implements OnInit {

  switches$: Observable<Array<ModelSwitch>>;

  page_number : number = 1;
  item_count : number = 1;
  items_per_page : number = +PagingConf.item_count;
  private searchTerms = new BehaviorSubject<string>("");

  constructor(public switchService: SwitchService) { }

  search(term: string): void {
    this.searchTerms.next(term);
  }


  refreshSwitchs(page:number) : void {
    this.switches$ = this.searchTerms.pipe(
      // wait 300ms after each keystroke before considering the term
      debounceTime(300),

      // ignore new term if same as previous term
      distinctUntilChanged(),

      // switch to new search observable each time the term changes
      switchMap((term: string) => this.switchService.filterSwitch(this.items_per_page, (page-1)*this.items_per_page, term, 'response')),
      switchMap((response) => {
        this.item_count = +response.headers.get("x-total-count")
        this.page_number = page;
        return Observable.of(response.body)
      }),
    );
  }

  ngOnInit() {
    this.refreshSwitchs(1);
  }

}
