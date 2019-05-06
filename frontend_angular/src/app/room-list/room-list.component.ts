import {Component, OnInit} from '@angular/core';

import {Observable} from 'rxjs/Observable';
import 'rxjs/add/operator/takeWhile';

import {RoomService} from '../api/api/room.service';
import {Room} from '../api/model/room';
import {PagingConf} from '../paging.config';

import {map} from 'rxjs/operators';
import {SearchPage} from '../search-page';

export interface RoomListResult {
  room?: Array<Room>;
  item_count?: number;
  current_page?: number;
  items_per_page?: number;
}

@Component({
  selector: 'app-rooms',
  templateUrl: './room-list.component.html',
  styleUrls: ['./room-list.component.css']
})

export class RoomListComponent extends SearchPage implements OnInit {

  result$: Observable<RoomListResult>;

  constructor(public roomService: RoomService) {
    super();
  }

  ngOnInit() {
    super.ngOnInit();
    this.result$ = this.getSearchResult((terms, page) => this.fetchRoom(terms, page));
  }

  private fetchRoom(terms: string, page: number) {
    const n = +PagingConf.item_count;
    return this.roomService.roomGet(n, (page - 1) * n, terms, 'response')
      .pipe(
        map((response) => <RoomListResult>{
          room: response.body,
          item_count: +response.headers.get('x-total-count'),
          current_page: page,
          items_per_page: n,
        })
      );
  }

}
