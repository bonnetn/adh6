import { Component, OnInit, OnDestroy } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/switchMap';
import 'rxjs/add/operator/takeWhile';
import { HttpResponse } from '@angular/common/http';
import { AbstractControl, FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
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

  roomForm: FormGroup;
  EmmenagerForm: FormGroup;
  public isEmmenager: boolean = false;
  public isDemenager: boolean = false;
  public ref: string;

  constructor(
    private notif: NotificationsService,
    private router: Router,
    public roomService: RoomService, 
    public portService: PortService, 
    public userService: UserService, 
    private fb: FormBuilder,
    private route: ActivatedRoute,
  ) { 
  this.createForm();
  }

  createForm() {
    this.ngOnInit()
    this.roomForm = this.fb.group({
      roomNumberNew: [this.roomNumber, [Validators.min(1000), Validators.max(9999), Validators.required ]],
    });
    this.EmmenagerForm = this.fb.group({
      username: ['', [Validators.minLength(7), Validators.maxLength(8), Validators.required ]],
    });
  }

  onEmmenager() {
    this.isEmmenager = !this.isEmmenager
  }
 
  onDemenager(username) {
    this.ref = username
    this.isDemenager = !this.isDemenager
  }

  refreshInfo() {
    this.room$ = this.roomService.getRoom( this.roomNumber );
    this.ports$ = this.portService.filterPort( { 'roomNumber': this.roomNumber } );
    this.members$ = this.userService.filterUser( { 'roomNumber': this.roomNumber } );
  }
  
  onSubmitComeInRoom() {
    const v = this.EmmenagerForm.value;
    this.userService.getUser(v.username)
      .takeWhile( () => this.alive )
      .subscribe( (user) => {
        user["roomNumber"]=this.roomNumber
        this.userService.putUserResponse( { 
                  "username": v.username,
                  "body": user,
                })
        .takeWhile( () => this.alive )
        .subscribe( (response) => {
          this.refreshInfo();
          this.notif.success(response.status + ": success")
          this.onEmmenager()
        }, (response) => {
          this.notif.error(response.status + ": " + response.error);
        });
      }, (user) => {
          this.notif.error("User "+v.username+" does not exists");
      });
  }

  onSubmitMoveRoom(username) {
    const v = this.roomForm.value;
    const room: Room = {
      roomNumber: v.roomNumberNew
    }
    this.userService.getUser(username)
      .takeWhile( () => this.alive )
      .subscribe( (user) => {
        user["roomNumber"]=v.roomNumberNew
        this.userService.putUserResponse( { 
                  "username": username,
                  "body": user,
                })
        .takeWhile( () => this.alive )
        .subscribe( (response) => {
          this.refreshInfo();
          this.onDemenager(username)
          this.router.navigate(["room", v.roomNumberNew ])
          this.notif.success(response.status + ": success")
        }, (response) => {
          this.notif.error(response.status + ": " + response.error);
        });
    });
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
