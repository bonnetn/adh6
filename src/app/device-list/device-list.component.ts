import { Component, OnInit, OnDestroy } from '@angular/core'
import { Router } from '@angular/router'

import { Observable } from 'rxjs/Observable'
import { combineLatest } from 'rxjs/observable/combineLatest'
import { map } from 'rxjs/operators'
import { filter } from 'rxjs/operators'
import { merge } from 'rxjs/observable/merge'
import { BehaviorSubject }    from 'rxjs/BehaviorSubject'
import {
   debounceTime, distinctUntilChanged, switchMap
 } from 'rxjs/operators'

import "rxjs/add/operator/takeWhile"

import { DeviceService } from '../api/services/device.service'
import { Device } from '../api/models/device'

import { NgxPaginationModule } from 'ngx-pagination'
import { PagingConf } from '../paging.config'

@Component({
  selector: 'app-device-list',
  templateUrl: './device-list.component.html',
  styleUrls: ['./device-list.component.css']
})
export class DeviceListComponent implements OnInit {

  devices$: Observable<Device[]>

  currentPage : number = 1
  item_count : number = 1 
  items_per_page : number = +PagingConf.item_count

  private searchTerm$ = new BehaviorSubject<string>("")
  private pageNumber$ = new BehaviorSubject<number>(1)

  constructor(public deviceService: DeviceService, private router: Router) { }

  search(term: string): void {
    this.searchTerm$.next(term)
  }

  refreshDevices(page:number) : void {
    this.pageNumber$.next(page)
  }


  ngOnInit() {
    this.devices$ = merge(

      combineLatest(
        this.searchTerm$.pipe(
          debounceTime(300), 
          distinctUntilChanged(),
        ),
        this.pageNumber$
      ).pipe(
        switchMap(data => {
          let term : string = data[0]
          let page : number = data[1]
          this.currentPage = page

          return this.deviceService.filterDeviceResponse( { 
            'terms':term, 
            'limit':this.items_per_page,
            'offset':(page-1)*this.items_per_page} 
          )
        }),

        map(response => {
          this.item_count = +response.headers.get("x-total-count")
          return response.body
        })
      ),
      this.pageNumber$.map( ignored => {
        // Clear page when changing page
        return []
      })
    )
  }

}
