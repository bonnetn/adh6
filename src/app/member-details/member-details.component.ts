import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Observable } from 'rxjs/Observable';
// import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { UserService } from '../api/services/user.service';
import { DeviceService } from '../api/services/device.service';
import { User } from '../api/models/user';
import { Device } from '../api/models/device';
import { Router, ActivatedRoute } from '@angular/router';
import { NotificationsService } from 'angular2-notifications/dist';

@Component({
  selector: 'app-member-details',
  templateUrl: './member-details.component.html',
  styleUrls: ['./member-details.component.css']
})
export class MemberDetailsComponent implements OnInit, OnDestroy {

  disabled = false;
  private alive = true;

  member$: Observable<User>;
  // refreshInfo$ = new BehaviorSubject<null>(null);
  all_devices$: Observable<Device[]>;
  username: string;
  public MAB: string;
  public MABdisabled: boolean;
  public cotisation = false;
  private sub: any;
  private commentForm: FormGroup;
  private commentSubmitDisabled = false;
  private deviceForm: FormGroup;

  constructor(
    public userService: UserService,
    public deviceService: DeviceService,
    private route: ActivatedRoute,
    private router: Router,
    private fb: FormBuilder,
    private notif: NotificationsService,
  ) {
    this.createForm();
  }

  onMAB() {
    this.MABdisabled = false;
    const v = this.deviceForm.value;
    if ( v.connectionType === 'wired') {
      if (this.MAB === 'on') {
        this.MAB = 'off';
      } else {
        this.MAB = 'on';
      }
    } else {
      this.MAB = 'wifi';
      this.MABdisabled = true;
    }
  }

  onCotisation() {
    this.cotisation = !this.cotisation;
  }

  IfRoomExists(roomNumber) {
    if (roomNumber == null) {
      this.notif.error('This user is not assigned to a room');
    } else {
      this.router.navigate(['/room/view', roomNumber]);
    }
  }

  createForm() {
    this.commentForm = this.fb.group( {
      comment: [''],
    });
    this.deviceForm = this.fb.group({
      mac: ['01:23:45:76:89:AB', [Validators.required, Validators.minLength(17), Validators.maxLength(17)]],
      connectionType: ['wired', Validators.required ],
    });
  }

  onSubmitComment() {
    this.disabled = true;
    const newComment = this.commentForm.value.comment;
    this.commentSubmitDisabled = true;
    this.userService.getUser(this.username)
      .takeWhile( () => this.alive )
      .subscribe( (user) => {
        user.comment = newComment;
        this.userService.putUserResponse( {
                  'username': this.username,
                  'body': user,
                })
        .takeWhile( () => this.alive )
        .subscribe( (response) => {
          this.commentSubmitDisabled = false;
          this.refreshInfo();
          this.notif.success(response.status + ': Success');
        });
    });
    this.disabled = false;
  }

  onSubmitDevice() {
    this.disabled = true;
    const v = this.deviceForm.value;
    const device: Device = {
      mac: v.mac,
      connectionType: v.connectionType,
      username: this.username
    };
    this.deviceService.getDeviceResponse(v.mac)
      .takeWhile( () => this.alive )
      .subscribe( () => {
        this.notif.error('Device already exists');
      }, () => {
        this.deviceService.putDeviceResponse( { 'macAddress': v.mac, body: device })
          .takeWhile( () => this.alive )
          .subscribe( (response) => {
            this.refreshInfo();
            this.notif.success(response.status + ': Success');
          });
      });
    this.disabled = false;
  }

  onDelete(mac: string) {
    this.deviceService.deleteDevice(mac).subscribe( () => {
      this.refreshInfo();
    });
  }

  refreshInfo() {
    this.member$ = this.userService.getUser(this.username);

    this.member$
      .takeWhile( () => this.alive )
      .subscribe( (user) => {
      this.commentForm.setValue( {
        comment: user.comment,
      });
    });
    this.all_devices$ = this.deviceService.filterDevice( { 'username': this.username } );
  }

  ngOnInit() {
    this.onMAB();
    this.sub = this.route.params.subscribe(params => {
      this.username = params['username'];
      this.refreshInfo();
    });
  }
  ngOnDestroy() {
    this.sub.unsubscribe();
    this.alive = false;
  }

}
