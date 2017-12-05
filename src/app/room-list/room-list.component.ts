import { Component, OnInit } from '@angular/core';

import { Observable } from 'rxjs/Observable';

import { RoomService } from '../api/services/room.service';
import { Room } from '../api/models/room';

@Component({
  selector: 'app-rooms',
  templateUrl: './room-list.component.html',
  styleUrls: ['./room-list.component.css']
})

export class RoomListComponent implements OnInit {

  rooms$: Observable<Room[]>;

  constructor(public roomService: RoomService) { }

  ngOnInit() {
    this.rooms$ = this.roomService.filterRoom() ;
  }

}
