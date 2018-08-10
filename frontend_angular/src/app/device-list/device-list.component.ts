import {Component, OnInit} from '@angular/core';
import {map} from 'rxjs/operators';

import 'rxjs/add/operator/takeWhile';

import {DeviceService} from '../api/api/device.service';
import {Device} from '../api/model/device';

import {PagingConf} from '../paging.config';
import {Observable} from 'rxjs';
import {SearchPage} from '../search-page';


export interface DeviceListResult {
  devices?: Array<Device>;
  item_count?: number;
  current_page?: number;
  items_per_page?: number;
}

@Component({
  selector: 'app-device-list',
  templateUrl: './device-list.component.html',
  styleUrls: ['./device-list.component.css']
})
export class DeviceListComponent extends SearchPage implements OnInit {

  result$: Observable<DeviceListResult>;

  constructor(public deviceService: DeviceService) {
    super();
  }

  ngOnInit() {
    super.ngOnInit();
    this.result$ = this.getSearchResult((terms, page) => this.fetchDevices(terms, page));
  }

  private fetchDevices(term: string, page: number) {
    const n: number = +PagingConf.item_count;
    return this.deviceService.filterDevice(n, (page - 1) * n, undefined, term, 'response')
      .pipe(
        map(response => <DeviceListResult>{
          devices: response.body,
          item_count: +response.headers.get('x-total-count'),
          current_page: page,
          items_per_page: n,
        }),
      );
  }

}
