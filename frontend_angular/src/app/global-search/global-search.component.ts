import {Component, OnInit} from '@angular/core';

import {Observable} from 'rxjs/Observable';
import {Subject} from 'rxjs/Subject';
import 'rxjs/add/operator/map';
import {debounceTime, distinctUntilChanged, map, mergeMap, scan, switchMap} from 'rxjs/operators';
import 'rxjs/add/operator/concat';
import 'rxjs/add/operator/merge';
import 'rxjs/add/observable/of';
import {from} from 'rxjs/observable/from';

import {MemberService} from '../api/api/member.service';

import {DeviceService} from '../api/api/device.service';

import {RoomService} from '../api/api/room.service';

import {SwitchService} from '../api/api/switch.service';

import {PortService} from '../api/api/port.service';
import {Port} from '../api';
import {EMPTY} from 'rxjs';


export class SearchResult {
  objType: string;
  name: string;
  color = 'grey';
  link: Array<string>;

  constructor(t: string, n: string, link: Array<string>) {
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

        const user$ = this.memberService.filterMember(LIMIT, undefined, terms).pipe(
          mergeMap((array) => from(array)),
          map((obj) => new SearchResult('user', obj.firstName + ' ' + obj.lastName, ['/member/view', obj.username])),
        );

        const device$ = this.deviceService.filterDevice(LIMIT, undefined, undefined, terms).pipe(
          mergeMap((array) => from(array)),
          map((obj) => new SearchResult('device', obj.mac, ['/member/view/', obj.username])),
        );

        const room$ = this.roomService.filterRoom(LIMIT, undefined, terms).pipe(
          mergeMap((array) => from(array)),
          map((obj) => new SearchResult('room', obj.description, ['/room/view', obj.roomNumber.toString()])),
        );
        const switch$ = this.switchService.filterSwitch(LIMIT, undefined, terms).pipe(
          mergeMap((array) => from(array)),
          map((obj) => new SearchResult('switch', obj.description, ['/switch/view', obj.id.toString()])),
        );

        const port$ = this.portService.filterPort(LIMIT, undefined, undefined, undefined, terms).pipe(
          mergeMap((array: Array<Port>) => from(array)),
          map((obj: Port) =>
            new SearchResult(
              'port',
              `Switch ${obj.switchID} ${obj.portNumber}`,
              ['/switch/view', obj.switchID.toString(), 'port', obj.id.toString()]
            )),
        );

        return user$
          .concat(device$)
          .concat(room$)
          .concat(switch$)
          .concat(port$);

      }),
    );

    // This stream emits Arrays of results growing as the searchResults are
    // found. The Arrays are cleared every time the user changes the text in the
    // text box.
    this.searchResult$ = result$.map(x => [x]).merge(
      debouncedSearchTerm$.map(ignored => null)
    ).pipe(
      scan((acc, value) => {
        if (!value) {// if it is null then we clear the array
          return [];
        }
        return acc.concat(value[0]); // we keep adding elements
      }, [])
    );

  }

}
