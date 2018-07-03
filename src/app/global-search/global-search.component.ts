import { Component, OnInit } from '@angular/core';

import { Observable } from 'rxjs/Observable';
import { Subject } from 'rxjs/Subject';
import 'rxjs/add/operator/map'
import { scan } from 'rxjs/operators';
import 'rxjs/add/operator/concat'
import 'rxjs/add/operator/merge';
import 'rxjs/add/observable/of';
import { from } from 'rxjs/observable/from';

import { UserService } from '../api/services/user.service';
import { User } from '../api/models/user';

import { DeviceService } from '../api/services/device.service';
import { Device } from '../api/models/device';

import { RoomService } from '../api/services/room.service';
import { Room } from '../api/models/room';

import { SwitchService } from '../api/services/switch.service';
import { Switch } from '../api/models/switch';

import { PortService } from '../api/services/port.service';
import { Port } from '../api/models/port';

import { debounceTime, distinctUntilChanged, switchMap, mergeMap, map } from 'rxjs/operators';


export class SearchResult {
  objType: string;
  name: string;
  color: string = "grey";
  constructor( t:string, n:string ) {
    this.objType = t;
    this.name = n;
    if(t == "user") {
      this.color = "red";
    } else if(t == "device") {
      this.color = "blue";
    } else if(t == "room") {
      this.color = "green";
    } else if(t == "switch") {
      this.color = "orange";
    } else if(t == "port") {
      this.color = "purple";
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
    var debouncedSearchTerm$ = this.searchTerm$.pipe(
      debounceTime(300),
      distinctUntilChanged()
    )

    // This returns a stream of object matching to what the user has typed
    var result$ = debouncedSearchTerm$.pipe( 
      switchMap( (terms:string) => {

        if( terms.length < 2 ) {
          return Observable.of( [ ] );
        }

        let LIMIT = 20;
        let args = {'terms':terms, 'limit':LIMIT}

        let user$ = this.userService.filterUser(args).pipe(
          mergeMap((array) => from(array)),
          map( (obj) => new SearchResult( "user", obj.firstName + " " + obj.lastName )),
        )

        let device$ = this.deviceService.filterDevice(args).pipe(
          mergeMap((array) => from(array)),
          map( (obj) => new SearchResult( "device", obj.mac)),
        )

        let room$ = this.roomService.filterRoom(args).pipe(
          mergeMap((array) => from(array)),
          map( (obj) => new SearchResult( "room", obj.description)),
        )
        let switch$ = this.switchService.filterSwitch(args).pipe(
          mergeMap((array) => from(array)),
          map( (obj) => new SearchResult( "switch", obj.description)),
        )

        let port$ = this.portService.filterPort(args).pipe(
          mergeMap((array) => from(array)),
          map( (obj) => new SearchResult( "port", "Switch " + obj.switchID + " " + obj.portNumber)),
        )

        return user$.merge(device$).merge(room$).merge(switch$).merge(port$);

      }),
    );

    // This stream emits Arrays of results growing as the searchResults are
    // found. The Arrays are cleared everytime the user changes the text in the
    // textbox.
    this.searchResult$ = result$.map(x => [x]).merge(
        debouncedSearchTerm$.map(ignored => null)
      ).pipe(
        scan( (acc, value, index) => {
          if(!value) // if it is null then we clear the array
            return []
          return acc.concat(value[0]) // we keep adding elements
        }, [])
      )

  }

}
