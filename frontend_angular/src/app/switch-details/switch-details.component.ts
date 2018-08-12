import {Component, OnInit} from '@angular/core';

import {Observable} from 'rxjs/Observable';
import {ActivatedRoute} from '@angular/router';

import {ModelSwitch} from '../api/model/modelSwitch';
import {SwitchService} from '../api/api/switch.service';

import {PortService} from '../api/api/port.service';
import {Port} from '../api/model/port';

import {BehaviorSubject} from 'rxjs/BehaviorSubject';
import {PagingConf} from '../paging.config';

import {debounceTime, distinctUntilChanged, switchMap} from 'rxjs/operators';


@Component({
  selector: 'app-switch-details',
  templateUrl: './switch-details.component.html',
  styleUrls: ['./switch-details.component.css']
})
export class SwitchDetailsComponent implements OnInit {

  switch$: Observable<ModelSwitch>;
  ports$: Observable<Array<Port>>;
  switchID: number;
  page_number = 1;
  item_count = 1;
  items_per_page: number = +PagingConf.item_count;
  private sub: any;
  private searchTerms = new BehaviorSubject<string>('');

  constructor(public switchService: SwitchService, private route: ActivatedRoute, public portService: PortService) {
  }

  search(term: string): void {
    this.searchTerms.next(term);
  }

  refreshPorts(page: number): void {
    this.ports$ = this.searchTerms.pipe(
      // wait 300ms after each keystroke before considering the term
      debounceTime(300),

      // ignore new term if same as previous term
      distinctUntilChanged(),

      // switch to new search observable each time the term changes
      switchMap((term: string) => this.portService.filterPort(this.items_per_page, (page - 1) * this.items_per_page,
        this.switchID, undefined, term, 'response')),
      switchMap((response) => {
        this.item_count = +response.headers.get('x-total-count');
        this.page_number = page;
        return Observable.of(response.body);
      }),
    );
  }

  ngOnInit() {
    this.sub = this.route.params.subscribe(params => {
      this.switchID = +params['switchID'];
      this.switch$ = this.switchService.getSwitch(this.switchID);
      // this.ports$ = this.portService.filterPort( { 'switchID': this.switchID } );
    });
    this.refreshPorts(1);
  }

}
