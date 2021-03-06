import {Component, OnDestroy, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {ActivatedRoute, Router} from '@angular/router';


import {RoomService} from '../api/api/room.service';
import {Room} from '../api/model/room';
import {NotificationsService} from 'angular2-notifications';
import {takeWhile} from 'rxjs/operators';

@Component({
  selector: 'app-room-new',
  templateUrl: './room-new.component.html',
  styleUrls: ['./room-new.component.css']
})

export class RoomNewComponent implements OnInit, OnDestroy {

  disabled = false;
  roomForm: FormGroup;
  private alive = true;

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
      roomNumber: ['', [Validators.min(1000), Validators.max(9999), Validators.required]],
      vlan: ['', [Validators.min(0), Validators.max(100), Validators.required]],
      description: ['', Validators.required],
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

    this.roomService.roomRoomNumberGet(v.roomNumber, 'response')
      .pipe(takeWhile(() => this.alive))
      .subscribe(() => {
        this.notif.error('Room already exists');
      }, () => {
        this.roomService.roomRoomNumberPut(v.roomNumber, room)
          .pipe(takeWhile(() => this.alive))
          .subscribe((res) => {
            this.router.navigate(['/room/view', v.roomNumber]);
            this.notif.success(res.status + ': Success');
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
