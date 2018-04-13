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

  memberEdit: FormGroup;

  constructor(
    private router: Router,
    public roomService: RoomService, 
    public portService: PortService, 
    public userService: UserService, 
    private fb: FormBuilder,
    private route: ActivatedRoute,
  ) { this.createForm(); }

  createForm() {
    this.memberEdit = this.fb.group({
      firstName: ['', Validators.required ],
      lastName: ['', Validators.required ],
      username: ['', [Validators.required, Validators.minLength(7)] ],
      email: ['', [Validators.required, Validators.email] ],
      roomNumber: [0, [Validators.min(1000), Validators.max(9999), Validators.required ]],
    });

  }

  onKick() {
    this.disabled = true;
    const v = this.memberEdit.value;
    const user: User = {
      email: v.email,
      firstName: v.firstName,
      lastName: v.lastName,
      username: v.username,
      roomNumber: 7601
    }

    this.userService.putUserResponse( { "username": v.username, body: user } )
      .takeWhile( () => this.alive )
      .subscribe( (response : HttpResponse<void>) => {
        if(response.status == 204) {
          this.router.navigate(["member/view", user.username ])
        }
        else if (response.status == 400) {
          this.router.navigate(["member/view", user.username ])
        }
        else {
        }
      });

  }

  onDelete() {
    const v = this.roomNumber;
    this.roomService.deleteRoomResponse( v )
      .takeWhile( () => this.alive )
      .subscribe( (response : HttpResponse<void>) => {
        if( response.status == 204 ) {
          this.router.navigate(["room"])
        }
        else if (response.status == 404 ){
        }
        else {
        }
      });
  
  }


  ngOnInit() {
    this.sub = this.route.params.subscribe( params => {
      this.roomNumber = +params["roomNumber"];
      this.room$ = this.roomService.getRoom( this.roomNumber );
      this.ports$ = this.portService.filterPort( { 'roomNumber': this.roomNumber } );
      this.members$ = this.userService.filterUser( { 'roomNumber': this.roomNumber } );
    });
  }
  
  ngOnDestroy() {
    this.sub.unsubscribe();
  }

}
