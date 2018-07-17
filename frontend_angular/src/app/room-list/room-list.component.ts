import {Component, OnInit} from '@angular/core';

import {Observable} from 'rxjs/Observable';
import 'rxjs/add/operator/takeWhile';

import {RoomService} from '../api/api/room.service';
import {Room} from '../api/model/room';

import {BehaviorSubject} from 'rxjs/BehaviorSubject';
import {PagingConf} from '../paging.config';

import {debounceTime, distinctUntilChanged, switchMap} from 'rxjs/operators';

@Component({
  selector: 'app-rooms',
  templateUrl: './room-list.component.html',
  styleUrls: ['./room-list.component.css']
})

export class RoomListComponent implements OnInit {

  rooms$: Observable<Array<Room>>;

  page_number = 1;
  item_count = 1;
  items_per_page: number = +PagingConf.item_count;
  private searchTerms = new BehaviorSubject<string>('');

  constructor(public roomService: RoomService) {
  }

  search(term: string): void {
    this.searchTerms.next(term);
  }

  refreshRooms(page: number): void {
    this.rooms$ = this.searchTerms.pipe(
      // wait 300ms after each keystroke before considering the term
      debounceTime(300),

      // ignore new term if same as previous term
      distinctUntilChanged(),

      // switch to new search observable each time the term changes
      switchMap((term: string) => this.roomService.filterRoom(this.items_per_page, (page - 1) * this.items_per_page, term, 'response')),
      switchMap((response) => {
        this.item_count = +response.headers.get('x-total-count');
        this.page_number = page;
        return Observable.of(response.body);
      }),
    );
  }

  ngOnInit() {
    this.refreshRooms(1);
  }

}
