import { Component, OnInit } from '@angular/core';

import { Observable } from 'rxjs/Observable';
import { Subject } from 'rxjs/Subject';
import 'rxjs/add/operator/map';
import { scan } from 'rxjs/operators';
import 'rxjs/add/operator/concat';
import 'rxjs/add/operator/merge';
import 'rxjs/add/observable/of';
import { from } from 'rxjs/observable/from';

import { UserService } from '../api/api/user.service';

import { DeviceService } from '../api/api/device.service';

import { RoomService } from '../api/api/room.service';

import { SwitchService } from '../api/api/switch.service';

import { PortService } from '../api/api/port.service';

import { debounceTime, distinctUntilChanged, switchMap, mergeMap, map } from 'rxjs/operators';
import {Port} from '../api';


export class SearchResult {
  objType: string;
  name: string;
  color = 'grey';
  constructor( t: string, n: string ) {
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
  }
}

@Component({
  selector: 'app-global-search',
  templateUrl: './global-search.component.html',
  styleUrls: ['./global-search.component.css']
})
export class GlobalSearchComponent implements OnInit {

  searchResult$: Observable<SearchResult[]>;
  private searchTerm$ = new Subject<string>();

  constructor(
    private userService: UserService,
    private deviceService: DeviceService,
    private roomService: RoomService,
    private switchService: SwitchService,
    private portService: PortService,
  ) { }

  search( terms: string ) {
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
      switchMap( (terms: string) => {

        if ( terms.length < 2 ) {
          return Observable.of( [ ] );
        }

        const LIMIT = 20;

        const user$ = this.userService.filterUser(LIMIT, undefined, terms).pipe(
          mergeMap((array) => from(array)),
          map( (obj) => new SearchResult( 'user', obj.firstName + ' ' + obj.lastName )),
        );

        const device$ = this.deviceService.filterDevice(LIMIT, undefined, undefined, terms).pipe(
          mergeMap((array) => from(array)),
          map( (obj) => new SearchResult( 'device', obj.mac)),
        );

        const room$ = this.roomService.filterRoom(LIMIT, undefined, terms).pipe(
          mergeMap((array) => from(array)),
          map( (obj) => new SearchResult( 'room', obj.description)),
        );
        const switch$ = this.switchService.filterSwitch(LIMIT, undefined, terms).pipe(
          mergeMap((array) => from(array)),
          map( (obj) => new SearchResult( 'switch', obj.description)),
        );

        const port$ = this.portService.filterPort(LIMIT, undefined, undefined, undefined, terms).pipe(
          mergeMap((array: Array<Port>) => from(array)),
          map( (obj: Port) => new SearchResult( 'port', 'Switch ' + obj.switchId + ' ' + obj.portNumber)),
        );

        return user$.concat(device$).concat(room$).concat(switch$).concat(port$);

      }),
    );

    // This stream emits Arrays of results growing as the searchResults are
    // found. The Arrays are cleared every time the user changes the text in the
    // text box.
    this.searchResult$ = result$.map(x => [x]).merge(
        debouncedSearchTerm$.map(ignored => null)
      ).pipe(
        scan( (acc, value) => {
          if (!value) {// if it is null then we clear the array
            return [];
          }
          return acc.concat(value[0]); // we keep adding elements
        }, [])
      );

  }

}