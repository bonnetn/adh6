import { Component, OnInit } from '@angular/core';

import { Observable } from 'rxjs/Observable';
import { Subject } from 'rxjs/Subject';
import 'rxjs/add/operator/map'
import 'rxjs/add/operator/concat'
import 'rxjs/add/operator/merge';
import 'rxjs/add/observable/of';


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

import { debounceTime, distinctUntilChanged, switchMap, flatMap, map } from 'rxjs/operators';


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

  searchResults: SearchResult[] = [];
  searchResult$: Observable<SearchResult[]>;
  private searchTerms = new Subject<string>();

  constructor(
    private userService: UserService,
    private deviceService: DeviceService,
    private roomService: RoomService,
    private switchService: SwitchService,
    private portService: PortService,
  ) { }

  search( terms: string ) {
    this.searchTerms.next(terms);
  }


  ngOnInit() {
    this.searchResult$ = this.searchTerms.pipe( 
      debounceTime(300),
      distinctUntilChanged(),
      switchMap( (terms:string) => {

        let LIMIT = 5;

        let user$ = this.userService.filterUser( {'terms':terms, 'limit':LIMIT} )
          .map( (values) => {
            let res = [];
            values.forEach( (obj) => {
              res.push( new SearchResult( "user", obj.firstName + " " + obj.lastName ) );
            });

            return res;
          });
        let device$ = this.deviceService.filterDevice( {'terms':terms, 'limit':LIMIT} )
          .map( (values) => {
            let res = [];
            values.forEach( (obj) => {
              res.push( new SearchResult( "device", obj.mac ) );
            });

            return res;
          });
        let room$ = this.roomService.filterRoom( {'terms':terms, 'limit':LIMIT} )
          .map( (values) => {
            let res = [];
            values.forEach( (obj) => {
              res.push( new SearchResult( "room", obj.description ) );
            });

            return res;
          });
        let switch$ = this.switchService.filterSwitch( {'terms':terms, 'limit':LIMIT} )
          .map( (values) => {
            let res = [];
            values.forEach( (obj) => {
              res.push( new SearchResult( "switch", obj.switch.description ) );
            });

            return res;
          });
        
        let port$ = this.portService.filterPort( {'terms':terms, 'limit':LIMIT} )
          .map( (values) => {
            let res = [];
            values.forEach( (obj) => {
              res.push( new SearchResult( "port", "Switch " + obj.port.switchID + " " + obj.port.portNumber ) );
            });

            return res;
          });
        


        this.searchResults = [];
        return user$.merge(device$).merge(room$).merge(switch$).merge(port$);

      }),
      map( (value : SearchResult[]) => {
        this.searchResults = this.searchResults.concat( value );
        return this.searchResults;
      })
    );
  }

}
