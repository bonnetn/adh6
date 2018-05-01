import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';

import { Observable } from 'rxjs/Observable';

import "rxjs/add/operator/takeWhile";

import { DeviceService } from '../api/services/device.service';
import { Device } from '../api/models/device';

import { BehaviorSubject }    from 'rxjs/BehaviorSubject';
import { NgxPaginationModule } from 'ngx-pagination';
import { PagingConf } from '../paging.config'

import {
   debounceTime, distinctUntilChanged, switchMap
 } from 'rxjs/operators';

@Component({
  selector: 'app-device-list',
  templateUrl: './device-list.component.html',
  styleUrls: ['./device-list.component.css']
})
export class DeviceListComponent implements OnInit {

  devices$: Observable<Device[]>;
  alive: boolean = true;

  page_number : number = 1;
  item_count : number = 1;
  items_per_page : number = +PagingConf.item_count;
  private searchTerms = new BehaviorSubject<string>("");

  constructor(public deviceService: DeviceService, private router: Router) { }
  
  search(term: string): void {
    this.searchTerms.next(term);
  }

  refreshDevices(page:number) : void {
    this.devices$ = this.searchTerms.pipe(
      // wait 300ms after each keystroke before considering the term
      debounceTime(300),

      // ignore new term if same as previous term
      distinctUntilChanged(),

      // switch to new search observable each time the term changes
      switchMap((term: string) => this.deviceService.filterDeviceResponse( { 'terms':term, 'limit':this.items_per_page, 'offset':(page-1)*this.items_per_page} )),
      switchMap((response) => {
        this.item_count = +response.headers.get("x-total-count")
        this.page_number = page;  
        return Observable.of(response.body)
      }),
    );
  }


  ngOnInit() {
    this.refreshDevices(1);
  }

  ngOnDestroy() {
    this.alive = false;
  }

}

  

