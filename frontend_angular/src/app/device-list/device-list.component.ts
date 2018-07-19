import {Component, OnInit} from '@angular/core';
import {map} from 'rxjs/operators';
import {BehaviorSubject} from 'rxjs/BehaviorSubject';

import 'rxjs/add/operator/takeWhile';

import {DeviceService} from '../api/api/device.service';
import {Device} from '../api/model/device';

import {PagingConf} from '../paging.config';
import {Observable} from 'rxjs';
import {PagingUtils} from '../paging-utils';


export interface DeviceListResult {
  devices?: Array<Device>;
  item_count?: number;
  current_page?: number;
}

@Component({
  selector: 'app-device-list',
  templateUrl: './device-list.component.html',
  styleUrls: ['./device-list.component.css']
})
export class DeviceListComponent implements OnInit {

  result$: Observable<DeviceListResult>;

  readonly ITEMS_PER_PAGE: number = +PagingConf.item_count;

  private searchTerm$ = new BehaviorSubject<string>('');
  private pageNumber$ = new BehaviorSubject<number>(1);

  constructor(public deviceService: DeviceService) {
  }

  search(term: string): void {
    this.searchTerm$.next(term);
  }

  refreshDevices(page: number): void {
    this.pageNumber$.next(page);
  }

  ngOnInit() {
    this.result$ = PagingUtils.getSearchResult(this.searchTerm$, this.pageNumber$, (t, p) => this.getDevices(t, p));
  }

  private getDevices(term: string, page: number) {

    return this.deviceService.filterDevice(this.ITEMS_PER_PAGE, (page - 1) * this.ITEMS_PER_PAGE, undefined, term, 'response')
      .pipe(
        map(response => {
          return <DeviceListResult>{
            devices: response.body,
            item_count: +response.headers.get('x-total-count'),
            current_page: page,
          };
        }),
      );
  }

}
