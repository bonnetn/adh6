import {Component, OnInit} from '@angular/core';

import {concat, EMPTY, from, merge, Observable, Subject} from 'rxjs';
import {debounceTime, distinctUntilChanged, map, mergeMap, scan, switchMap} from 'rxjs/operators';

import {MemberService} from '../api/api/member.service';

import {DeviceService} from '../api/api/device.service';

import {RoomService} from '../api/api/room.service';

import {SwitchService} from '../api/api/switch.service';

import {PortService} from '../api/api/port.service';
import {Port} from '../api';

class QueryParams {
  highlight: string;
}

export class SearchResult {
  objType: string;
  name: string;
  color = 'grey';
  link: Array<string>;
  queryParams: QueryParams;

  constructor(t: string, n: string, link: Array<string>, params?: QueryParams) {
    this.objType = t;
    this.name = n;
    if (t === 'user') {
      this.color = 'red';
    } else if (t === 'device') {
      this.color = 'blue';
    } else if (t === 'room') {
      this.color = 'green';
    } else if (t === 'switch') {
      this.color = 'orange';
    } else if (t === 'port') {
      this.color = 'purple';
    }
    this.link = link;
    this.queryParams = params;
  }
}

@Component({
  selector: 'app-global-search',
  templateUrl: './global-search.component.html',
  styleUrls: ['./global-search.component.css']
})
export class GlobalSearchComponent implements OnInit {

  searchResult$: Observable<Array<SearchResult>>;
  private searchTerm$ = new Subject<string>();

  constructor(
    private memberService: MemberService,
    private deviceService: DeviceService,
    private roomService: RoomService,
    private switchService: SwitchService,
    private portService: PortService,
  ) {
  }

  search(terms: string) {
    this.searchTerm$.next(terms);
  }

  ngOnInit() {

    // This is a stream of what the user types debounced
    const debouncedSearchTerm$ = this.searchTerm$.pipe(
      debounceTime(300),
      distinctUntilChanged()
    );

    // This returns a stream of object matching to what the user has typed
    const result$ = debouncedSearchTerm$.pipe(
      switchMap((terms: string) => {

        if (terms.length < 2) {
          return EMPTY;
        }


        const LIMIT = 20;

        const user$ = this.memberService.memberGet(LIMIT, undefined, terms).pipe(
          mergeMap((array) => from(array)),
          map((obj) => new SearchResult(
            'user',
            `${this.capitalizeFirstLetter(obj.firstName)} ${obj.lastName.toUpperCase()}`,
            ['/member/view', obj.username]
          )),
        );

        const device$ = this.deviceService.deviceGet(LIMIT, undefined, undefined, terms).pipe(
          mergeMap((array) => from(array)),
          map((obj) => new SearchResult(
            'device',
            obj.mac,
            ['/member/view/', obj.username],
            {'highlight': obj.mac}
          )),
        );

        const room$ = this.roomService.roomGet(LIMIT, undefined, terms).pipe(
          mergeMap((array) => from(array)),
          map((obj) => new SearchResult('room', obj.description, ['/room/view', obj.roomNumber.toString()])),
        );
        const switch$ = this.switchService.switchGet(LIMIT, undefined, terms).pipe(
          mergeMap((array) => from(array)),
          map((obj) => new SearchResult('switch', obj.description, ['/switch/view', obj.id.toString()])),
        );

        const port$ = this.portService.portGet(LIMIT, undefined, undefined, undefined, terms).pipe(
          mergeMap((array: Array<Port>) => from(array)),
          map((obj: Port) =>
            new SearchResult(
              'port',
              `Switch ${obj.switchID} ${obj.portNumber}`,
              ['/switch/view', obj.switchID.toString(), 'port', obj.id.toString()]
            )),
        );

        return concat(user$, device$, room$, switch$, port$);
      }),
    );

    // This stream emits Arrays of results growing as the searchResults are
    // found. The Arrays are cleared every time the user changes the text in the
    // text box.
    this.searchResult$ = merge(
      result$.pipe(map(x => [x])),
      debouncedSearchTerm$.pipe(map(ignored => null)),
    ).pipe(
      scan((acc, value) => {
        if (!value) {// if it is null then we clear the array
          return [];
        }
        return acc.concat(value[0]); // we keep adding elements
      }, []),
    );

  }

  private capitalizeFirstLetter(str: string) {
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
  }

}
