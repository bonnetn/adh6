import { Component, OnInit, OnDestroy } from '@angular/core';

import { Observable } from 'rxjs/Observable';

import { RoomService } from '../api/services/room.service';
import { PortService } from '../api/services/port.service';
import { Room } from '../api/models/room';
import { Port } from '../api/models/port';

import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-room-details',
  templateUrl: './room-details.component.html',
  styleUrls: ['./room-details.component.css']
})
export class RoomDetailsComponent implements OnInit, OnDestroy {

  room$: Observable<Room>;
  ports$: Observable<Port[]>;
  roomNumber: number;
  private sub: any;

  constructor(public roomService: RoomService, public portService: PortService, private route: ActivatedRoute) { }

  ngOnInit() {
    this.sub = this.route.params.subscribe( params => {
      this.roomNumber = +params["roomNumber"];
      this.room$ = this.roomService.getRoom( this.roomNumber );
      this.ports$ = this.portService.filterPort( { 'roomNumber': this.roomNumber } );
    });
  }
  
  ngOnDestroy() {
    this.sub.unsubscribe();
  }

}
