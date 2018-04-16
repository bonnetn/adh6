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
  
  disabled: boolean = false;
  private alive: boolean = true;
  
  roomForm: FormGroup;
  
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
    this.roomForm = this.fb.group({
      roomNumber: ['', [Validators.min(1000), Validators.max(9999), Validators.required ]],
      vlan: ['', [Validators.min(0), Validators.max(100), Validators.required ]],
      description: ['', Validators.required ],
    });
  }
 
  onSubmit() {
    this.disabled = true;
    const v = this.roomForm.value;
    const room: Room = {
      roomNumber: v.roomNumber,
      vlan: v.vlan,
      description: v.description
    }
          
    this.roomService.getRoomResponse(v.roomNumber)
      .takeWhile( ()=> this.alive )
      .subscribe( (response) => {
        this.notif.error("Room already exists"); 
      }, (response) => {
        this.roomService.putRoomResponse( { "roomNumber": v.roomNumber, body: room })
          .takeWhile( ()=> this.alive )
          .subscribe( (response) => {
            this.router.navigate(["room/", v.roomNumber ])
            this.notif.success(response.status + ": Success")
          }, (response) => {
            this.notif.error(response.status + ": " + response.error); 
          });
      });
    this.disabled = false;
  }

  ngOnInit() {
  }
  
  ngOnDestroy() {
    this.alive=false;
  }

}
