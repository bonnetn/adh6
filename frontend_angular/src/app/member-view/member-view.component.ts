import {Component, OnDestroy, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {Observable} from 'rxjs/Observable';
import {BehaviorSubject} from 'rxjs/BehaviorSubject';
import {MemberService} from '../api/api/member.service';
import {DeviceService} from '../api/api/device.service';
import {Member} from '../api/model/member';
import {Device} from '../api/model/device';
import {ActivatedRoute, Router} from '@angular/router';
import {NotificationsService} from 'angular2-notifications';
import {catchError, finalize, first, flatMap, map, share, switchMap, tap} from 'rxjs/operators';
import {combineLatest} from 'rxjs';

@Component({
  selector: 'app-member-details',
  templateUrl: './member-view.component.html',
  styleUrls: ['./member-view.component.css']
})
export class MemberViewComponent implements OnInit, OnDestroy {

  submitDisabled = false;

  member$: Observable<Member>;
  all_devices$: Observable<Device[]>;
  public MAB: string;
  public MABdisabled: boolean;
  public cotisation = false;
  private refreshInfo$ = new BehaviorSubject<null>(null);
  private username$: Observable<string>;
  private commentForm: FormGroup;
  private deviceForm: FormGroup;

  constructor(
    public memberService: MemberService,
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
    if (v.connectionType === 'wired') {
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
    this.commentForm = this.fb.group({
      comment: [''],
    });
    this.deviceForm = this.fb.group({
      mac: ['01:23:45:76:89:AB', [Validators.required, Validators.minLength(17), Validators.maxLength(17)]],
      connectionType: ['wired', Validators.required],
    });
  }

  onSubmitComment() {
    this.submitDisabled = true;
    const newComment = this.commentForm.value.comment;

    this.member$.pipe(
      map(user => {
        user.comment = newComment;
        return user;
      }),
      flatMap(user => this.memberService.putMember(user.username, user)),
      flatMap(() => {
        this.refreshInfo();
        return this.member$;
      }),
      finalize(() => this.submitDisabled = false),
      first(),
    ).subscribe(() => {
    });

    // will trigger the refresh of member$ and thus the update of the comment
    this.refreshInfo();

  }

  onSubmitDevice() {
    // First we fetch the username of the current user...
    this.submitDisabled = true;
    this.updateDevice()
      .pipe(
        first(),
        // No matter what, submit will be re-enable (even if there is an error)
        finalize(() => this.submitDisabled = false),
      )
      .subscribe(() => {
      });

  }

  updateDevice();
  updateDevice(username: string);
  updateDevice(username: string, alreadyExists: boolean);
  updateDevice(username?: string, alreadyExists?: boolean) {

    if (username == undefined) {
      return this.username$
        .pipe(
          flatMap((username) => this.updateDevice(username))
        );
    }

    const v = this.deviceForm.value;
    if (alreadyExists === undefined) {
      return this.deviceService.getDevice(v.mac).pipe(
        map(() => true),
        catchError(() => Observable.of(false)),
        flatMap((exists) => this.updateDevice(username, exists)),
      );
    }

    const device: Device = {
      mac: v.mac,
      connectionType: v.connectionType,
      username: username
    };

    // Make an observable that will return True if the device already exists
    if (!alreadyExists) {
      // If the device does not then create it, and refresh the info
      return this.deviceService.putDevice(v.mac, device)
        .pipe(
          flatMap(() => {
            this.refreshInfo();
            return this.all_devices$;
          }),
          map(() => null)
        );
    } else {
      this.notif.error('Device already exists');
      return Observable.of(null);
    }
  }

  onDelete(mac: string) {
    this.deviceService.deleteDevice(mac)
      .pipe(
        first()
      )
      .subscribe(() => this.refreshInfo());
  }

  ngOnInit() {
    this.onMAB();

    // username of the owner of the profile
    this.username$ = this.route.params.pipe(
      map(params => params['username'])
    );

    // stream, which will emit the username every time the profile needs to be refreshed
    const refresh$ = combineLatest(this.username$, this.refreshInfo$)
      .pipe(
        map(([x]) => x)
      );

    this.member$ = refresh$.pipe(
      switchMap(username => this.memberService.getMember(username)),
      tap((user) => this.commentForm.setValue({comment: (user.comment === undefined) ? '' : user.comment,})),
      share(),
    );

    this.all_devices$ = refresh$.pipe(
      switchMap(username => this.deviceService.filterDevice(undefined, undefined, username)),
      share(),
    );

  }

  ngOnDestroy() {
  }

}
