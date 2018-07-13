import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Observable } from 'rxjs/Observable';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { UserService } from '../api/services/user.service';
import { DeviceService } from '../api/services/device.service';
import { User } from '../api/models/user';
import { Device } from '../api/models/device';
import { Router, ActivatedRoute } from '@angular/router';
import { NotificationsService } from 'angular2-notifications/dist';
import 'rxjs/add/operator/last';
import 'rxjs/add/operator/mergeMap';
import 'rxjs/add/operator/combineLatest';

@Component({
  selector: 'app-member-details',
  templateUrl: './member-details.component.html',
  styleUrls: ['./member-details.component.css']
})
export class MemberDetailsComponent implements OnInit, OnDestroy {

  submitDisabled = false;

  member$: Observable<User>;
  refreshInfo$ = new BehaviorSubject<null>(null);
  all_devices$: Observable<Device[]>;
  username: string;
  public MAB: string;
  public MABdisabled: boolean;
  public cotisation = false;
  private commentForm: FormGroup;
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

  refreshInfo() {
    this.refreshInfo$.next(null);
    return this.member$;
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
    this.submitDisabled = true;
    const newComment = this.commentForm.value.comment;

    this.member$
      .last()
      .map(user => {
        user.comment = newComment;
        return user;
      })
      .flatMap(user => this.userService.putUserResponse(
        {
          'username': user.username,
          'body': user,
        }))
      .first()
      .subscribe(() => {
        this.submitDisabled = false;
        this.refreshInfo();
      });

  }

  onSubmitDevice() {
    this.submitDisabled = true;

    const v = this.deviceForm.value;
    const device: Device = {
      mac: v.mac,
      connectionType: v.connectionType,
      username: this.username
    };

    // Make an observable that will return True if the device already exists
    const deviceExists$ = this.deviceService.getDeviceResponse(v.mac)
      .first()
      .map(() => true)
      .catch(() => Observable.of(false))
      .publish();

    // If the device already exists then notify the user
    deviceExists$
      .filter(exists => exists)
      .subscribe(() => {
        this.notif.error('Device already exists');
        this.submitDisabled = false;
      });

    // If the device does not then create it, and refresh the info
    deviceExists$
      .filter(exists => !exists)
      .flatMap(() => this.deviceService.putDeviceResponse( { 'macAddress': v.mac, body: device }))
      .first()
      .subscribe(() => {
        this.submitDisabled = false;
        this.refreshInfo();
      });

    // "Launch" the stream
    deviceExists$.connect();

  }

  onDelete(mac: string) {
    this.deviceService.deleteDevice(mac)
      .first()
      .subscribe(() => this.refreshInfo());
  }

  ngOnInit() {
    this.onMAB();
    const username$ = this.route.params
      .map(params => params['username'])
      .combineLatest(this.refreshInfo$)
      .map(([x]) => x);

    this.member$ = username$
      .switchMap(username => this.userService.getUser(username));

    this.all_devices$ = username$
      .switchMap(username => this.deviceService.filterDevice({'username': username}));

    // TODO: fill the comment form
    // subscribe( (user) => {
    //  this.commentForm.setValue( {
    //    comment: user.comment,
    //  });

  }

  ngOnDestroy() {
  }

}
