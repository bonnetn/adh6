import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { HttpResponse } from '@angular/common/http';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';

import 'rxjs/add/operator/takeWhile';
import 'rxjs/add/operator/switchMap';

import { RoomService } from '../api/services/room.service';
import { Room } from '../api/models/room';
import { NotificationsService } from 'angular2-notifications';

@Component({
  selector: 'app-room-new',
  templateUrl: './room-new.component.html',
  styleUrls: ['./room-new.component.css']
})

export class RoomNewComponent implements OnInit, OnDestroy {
  
  // Disable the button to prevent multiple submit
  disabled: boolean = false;
  // Variable to destroy all subscriptions
  private alive: boolean = true;
  
  RoomForm: FormGroup;
  
  constructor(
    public roomService: RoomService,
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private notif: NotificationsService,
  ) { 
  this.createForm();
  }

  createForm() {
    this.RoomForm = this.fb.group({
      username: ['', [Validators.required, Validators.minLength(8), Validators.maxLength(8)] ],
      mac: ['', [Validators.required, Validators.minLength(17), Validators.maxLength(17)] ],
      connectionType: ['', Validators.required ],
    });
  }
 
  onSubmit() {
    this.disabled = true;
    const v = this.RoomForm.value;
    const room: Room = {
      roomNumber: v.roomNumber
    }
          
    this.roomService.putRoomResponse( { "roomNumber": v.roomNumber, body: room })
      .takeWhile( ()=> this.alive )
      .subscribe( (response) => {
        this.router.navigate(["device/view", v.mac ])
        this.notif.success(response.status + ": Success")
      }, (response) => {
        this.notif.error(response.status + ": " + response.error); 
      });
  
  }

  ngOnInit() {
  }
  
  ngOnDestroy() {
    this.alive=false;
  }

}
