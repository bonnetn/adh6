import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, ActivatedRoute} from '@angular/router';

import 'rxjs/add/operator/takeWhile';
import 'rxjs/add/operator/switchMap';

import { RoomService } from '../api/api/room.service';
import { Room } from '../api/model/room';
import { NotificationsService } from 'angular2-notifications';

@Component({
  selector: 'app-room-new',
  templateUrl: './room-new.component.html',
  styleUrls: ['./room-new.component.css']
})

export class RoomNewComponent implements OnInit, OnDestroy {

  disabled = false;
  private alive = true;

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
    };

    this.roomService.getRoom(v.roomNumber, 'response')
      .takeWhile( () => this.alive )
      .subscribe( (response) => {
        this.notif.error('Room already exists');
      }, (response) => {
        this.roomService.putRoom(v.roomNumber, room)
          .takeWhile( () => this.alive )
          .subscribe( (response) => {
            this.router.navigate(['/room/view', v.roomNumber ]);
            this.notif.success(response.status + ': Success');
          });
      });
    this.disabled = false;
  }

  ngOnInit() {
  }

  ngOnDestroy() {
    this.alive = false;
  }

}
