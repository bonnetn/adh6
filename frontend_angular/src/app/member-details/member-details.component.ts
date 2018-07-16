import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Observable } from 'rxjs/Observable';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { UserService } from '../api/api/user.service';
import { DeviceService } from '../api/api/device.service';
import { User } from '../api/model/user';
import { Device } from '../api/model/device';
import { Router, ActivatedRoute } from '@angular/router';
import { NotificationsService } from 'angular2-notifications';
import 'rxjs/add/operator/last';
import 'rxjs/add/operator/mergeMap';
import 'rxjs/add/operator/combineLatest';
import 'rxjs/add/operator/finally';
import 'rxjs/add/operator/share';

@Component({
  selector: 'app-member-details',
  templateUrl: './member-details.component.html',
  styleUrls: ['./member-details.component.css']
})
export class MemberDetailsComponent implements OnInit, OnDestroy {

  submitDisabled = false;

  username$: Observable<string>;
  member$: Observable<User>;
  all_devices$: Observable<Device[]>;
  refreshInfo$ = new BehaviorSubject<null>(null);

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
      .map(user => {
        user.comment = newComment;
        return user;
      })
      .flatMap(user => this.userService.putUserResponse(
        {
          'username': user.username,
          'body': user,
        }))
      .flatMap(() => {
        this.refreshInfo();
        return this.member$;
      })
      .finally(() => this.submitDisabled = false)
      .first()
      .subscribe(() => {});

      // will trigger the refresh of member$ and thus the update of the comment
      this.refreshInfo();

  }

  onSubmitDevice() {
    // First we fetch the username of the current user...
    this.submitDisabled = true;
    this.updateDevice()
      .first()
      // No matter what, submit will be re-enable (even if there is an error)
      .finally(() => this.submitDisabled = false)
      .subscribe(() => {});

  }

  updateDevice();
  updateDevice(username: string);
  updateDevice(username: string, alreadyExists: boolean);
  updateDevice(username?: string, alreadyExists?: boolean) {

    if (username == undefined) {
      return this.username$
        .flatMap((username) => this.updateDevice(username));
    }

    const v = this.deviceForm.value;
    if (alreadyExists === undefined) {
      return this.deviceService.getDeviceResponse(v.mac)
        .map(() => true)
        .catch(() => Observable.of(false))
        .flatMap((exists) => this.updateDevice(username, exists));
    }

    const device: Device = {
      mac: v.mac,
      connectionType: v.connectionType,
      username: username
    };

    // Make an observable that will return True if the device already exists
    if (!alreadyExists) {
      // If the device does not then create it, and refresh the info
      return this.deviceService.putDeviceResponse({'macAddress': v.mac, body: device})
        .flatMap(() => {
          this.refreshInfo();
          return this.all_devices$;
        })
        .map(() => null);
    } else {
      this.notif.error('Device already exists');
      return Observable.of(null);
    }
  }

  onDelete(mac: string) {
    this.deviceService.deleteDevice(mac)
      .first()
      .subscribe(() => this.refreshInfo());
  }

  ngOnInit() {
    this.onMAB();

    // username of the owner of the profile
    this.username$ = this.route.params
      .map(params => params['username']);

    // stream, which will emit the username every time the profile needs to be refreshed
    const refresh$ = this.username$
      .combineLatest(this.refreshInfo$)
      .map(([x]) => x);

    this.member$ = refresh$
      .switchMap(username => this.userService.getUser(username))
      .do((user) => this.commentForm.setValue({ comment: (user.comment === undefined) ? '' : user.comment, }))
      .share();

    this.all_devices$ = refresh$
      .switchMap(username => this.deviceService.filterDevice({'username': username}))
      .share();

    // TODO: fill the comment form
    // subscribe( (user) => {
    //  this.commentForm.setValue( {
    //    comment: user.comment,
    //  });

  }

  ngOnDestroy() {
  }

}
