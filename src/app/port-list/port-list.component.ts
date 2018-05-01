import { Component, OnInit } from '@angular/core';

import { Observable } from 'rxjs/Observable';

import { PortService } from '../api/services/port.service';
import { Port } from '../api/models/port';

import { BehaviorSubject }    from 'rxjs/BehaviorSubject';
import { NgxPaginationModule } from 'ngx-pagination';
import { PagingConf } from '../paging.config'

import {
   debounceTime, distinctUntilChanged, switchMap
 } from 'rxjs/operators';


@Component({
  selector: 'app-port-list',
  templateUrl: './port-list.component.html',
  styleUrls: ['./port-list.component.css']
})
export class PortListComponent implements OnInit {

  ports$: Observable<Port[]>;

  page_number : number = 1;
  item_count : number = 1;
  items_per_page : number = +PagingConf.item_count;
  private searchTerms = new BehaviorSubject<string>("");

  constructor(public portService: PortService) { }

  search(term: string): void {
    this.searchTerms.next(term);
  }

  refreshPorts(page:number) : void {
    this.ports$ = this.searchTerms.pipe(
      // wait 300ms after each keystroke before considering the term
      debounceTime(300),

      // ignore new term if same as previous term
      distinctUntilChanged(),

      // switch to new search observable each time the term changes
      switchMap((term: string) => this.portService.filterPortResponse( { 'terms':term, 'limit':this.items_per_page, 'offset':(page-1)*this.items_per_page} )),
      switchMap((response) => {
        this.item_count = +response.headers.get("x-total-count")
        this.page_number = page;  
        return Observable.of(response.body)
      }),
    );
  }

  ngOnInit() {
    this.refreshPorts(1);
  }

}
