import { Component, OnInit, OnDestroy } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/switchMap';
import 'rxjs/add/operator/takeWhile';
import { HttpResponse } from '@angular/common/http';
import { AbstractControl, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { RoomService } from '../api/services/room.service';
import { PortService } from '../api/services/port.service';
import { Room } from '../api/models/room';
import { Port } from '../api/models/port';
import { User } from '../api/models/user';
import { UserService } from '../api/services/user.service';
import { NotificationsService } from 'angular2-notifications';

@Component({
  selector: 'app-room-details',
  templateUrl: './room-details.component.html',
  styleUrls: ['./room-details.component.css']
})
export class RoomDetailsComponent implements OnInit, OnDestroy {
  
  disabled: boolean = false;
  private alive: boolean = true;

  room$: Observable<Room>;
  ports$: Observable<Port[]>;
  members$: Observable<User[]>;
  roomNumber: number;
  private sub: any;

  constructor(
    private notif: NotificationsService,
    private router: Router,
    public roomService: RoomService, 
    public portService: PortService, 
    public userService: UserService, 
    private fb: FormBuilder,
    private route: ActivatedRoute,
  ) { }

  refreshInfo() {
    this.room$ = this.roomService.getRoom( this.roomNumber );
    this.ports$ = this.portService.filterPort( { 'roomNumber': this.roomNumber } );
    this.members$ = this.userService.filterUser( { 'roomNumber': this.roomNumber } );
  }


  onRemoveFromRoom(username) {
    this.userService.getUser(username)
      .takeWhile( () => this.alive )
      .subscribe( (user) => {
        delete user['roomNumber'];
        this.userService.putUserResponse( { 
                  "username": username,
                  "body": user,
                })

        .takeWhile( () => this.alive )
        .subscribe( (response) => {
          this.refreshInfo();
          this.notif.success(response.status + ": success")
        }, (response) => {
          this.notif.error(response.status + ": " + response.error);
        });
    });
  }

  onDelete() {
    const v = this.roomNumber;
    this.roomService.deleteRoomResponse( v )
      .takeWhile( () => this.alive )
      .subscribe( (response) => {
        this.router.navigate(["room"])
        this.notif.success(response.status + ": success")
      }, (response) => {
        this.notif.error(response.status + ": " + response.error);
      });
  }


  ngOnInit() {
    this.sub = this.route.params.subscribe( params => {
      this.roomNumber = +params["roomNumber"];
      this.refreshInfo();
    });
  }
  
  ngOnDestroy() {
    this.sub.unsubscribe();
  }

}
