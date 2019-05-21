import {Component, OnDestroy, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {BehaviorSubject, of} from 'rxjs';
import {MemberService} from '../api/api/member.service';
import {DeviceService} from '../api/api/device.service';
import {Member} from '../api/model/member';
import {Device} from '../api/model/device';
import {ActivatedRoute, Router} from '@angular/router';
import {NotificationsService} from 'angular2-notifications';
import {catchError, finalize, first, flatMap, map, share, switchMap, tap} from 'rxjs/operators';
import {combineLatest, interval, Observable} from 'rxjs';
import {TemporaryAccountService} from '../api/api/temporaryAccount.service';
import {Utils} from '../utils';
import { PaymentMethod } from '../api/model/paymentMethod';
import { PaymentMethodService } from '../api/api/paymentMethod.service';

@Component({
  selector: 'app-member-details',
  templateUrl: './member-view.component.html',
  styleUrls: ['./member-view.component.css']
})

export class MemberViewComponent implements OnInit, OnDestroy {
  submitDisabled = false;
  date = new Date;

  member$: Observable<Member>;
  paymentMethods$: Observable<Array<PaymentMethod>>;
  all_devices$: Observable<Device[]>;
  log$: Observable<Array<string>>;
  macHighlighted$: Observable<string>;

  cotisation = false;
  private refreshInfoOrder$ = new BehaviorSubject<null>(null);
  private username$: Observable<string>;
  private commentForm: FormGroup;
  private deviceForm: FormGroup;
  private subscriptionForm: FormGroup;
  private selectedDevice: string;
  private options = {year: "numeric", month: "long", day: "numeric"};
  private amountToPay: number = 0;

  constructor(
    public memberService: MemberService,
    public deviceService: DeviceService,
    public paymentMethodService: PaymentMethodService,
    private route: ActivatedRoute,
    private router: Router,
    private fb: FormBuilder,
    private notif: NotificationsService,
    public tempAccService: TemporaryAccountService,
  ) {
    this.createForm();
  }

  ngOnInit() {
    // username of the owner of the profile
    this.username$ = this.route.params.pipe(
      map(params => params['username'])
    );

    this.macHighlighted$ = this.route.queryParams.pipe(
      map(params => params['highlight'])
    );

    // stream, which will emit the username every time the profile needs to be refreshed
    const refresh$ = combineLatest([this.username$, this.refreshInfoOrder$])
      .pipe(
        map(([x]) => x),
      );

    this.member$ = refresh$.pipe(
      switchMap(username => this.memberService.memberUsernameGet(username)),
      tap((user) => this.commentForm.setValue({comment: (user.comment === undefined) ? '' : user.comment})),
      share(),
    );

    this.all_devices$ = refresh$.pipe(
      switchMap(username => this.deviceService.deviceGet(undefined, undefined, username)),
      share(),
    );

    this.log$ = this.username$.pipe(
      switchMap((str) => {
        return interval(10 * 1000).pipe(
          switchMap(() => this.memberService.memberUsernameLogsGet(str))
        );
      }) // refresh every 10 secs
    );

    this.paymentMethods$ = this.paymentMethodService.paymentMethodGet();
  }

  ngOnDestroy() {
  }

  refreshInfo(): void {
    this.refreshInfoOrder$.next(null);
  }

  toggleCotisationMenu(): void {
    this.cotisation = !this.cotisation;
  }

  createForm(): void {
    this.commentForm = this.fb.group({
      comment: [''],
    });
    this.deviceForm = this.fb.group({
      mac: ['01-23-45-76-89-AB', [Validators.required, Validators.minLength(17), Validators.maxLength(17)]],
      connectionType: ['wired', Validators.required],
    });
    this.subscriptionForm = this.fb.group({
      renewal: ['0', [Validators.required]],
      checkCable3: [false],
      checkCable5: [false],
      checkAdapter: [false],
      paidBy: ['liq', [Validators.required]],
    })
  }

  submitComment(): void {
    this.submitDisabled = true;
    const newComment = this.commentForm.value.comment;

    this.member$.pipe(
      map(user => {
        user.comment = newComment;
        return user;
      }),
      flatMap(user => this.memberService.memberUsernamePut(user.username, user)),
      map(() => {
        this.refreshInfo();
        return null;
      }),
      finalize(() => this.submitDisabled = false),
      first(),
    ).subscribe(() => {
    });

    // will trigger the refresh of member$ and thus the update of the comment
    this.refreshInfo();
  }

  submitDevice(): void {
    // First we fetch the username of the current user...
    this.submitDisabled = true;
    this.addDevice()
      .pipe(
        first(),
        // No matter what, submit will be re-enable (even if there is an error)
        finalize(() => this.submitDisabled = false),
      )
      .subscribe(() => {
      });
  }

  submitSubscription(): void {
    // TODO
  }


  addDevice(username?: string, alreadyExists?: boolean) {
    if (username === undefined) {
      return this.username$
        .pipe(
          flatMap((usr) => this.addDevice(usr))
        );
    }

    const v = this.deviceForm.value;
    const mac = Utils.sanitizeMac(v.mac);
    if (alreadyExists === undefined) {
      return this.deviceService.deviceMacAddressGet(mac).pipe(
        map(() => true),
        catchError(() => of(false)),
        flatMap((exists) => this.addDevice(username, exists)),
      );
    }

    const device: Device = {
      mac: mac,
      connectionType: v.connectionType,
      username: username
    };

    // Make an observable that will return True if the device already exists
    if (!alreadyExists) {
      // If the device does not then create it, and refresh the info
      return this.deviceService.deviceMacAddressPut(mac, device)
        .pipe(
          flatMap(() => {
            this.refreshInfo();
            return this.all_devices$;
          }),
          map(() => null)
        );
    } else {
      this.notif.error('Device already exists');
      return of(null);
    }
  }

  deviceDelete(mac: string): void {
    this.submitDisabled = true;
    this.deviceService.deviceMacAddressDelete(mac)
      .pipe(
        first(),
        flatMap(() => {
          this.refreshInfo();
          return this.all_devices$;
        }),
        first(),
        finalize(() => this.submitDisabled = false)
      )
      .subscribe(() => {
      });
  }

  extractDateFromLog(log: string): Date {
    return new Date(log.split(' ')[0]);
  }

  extractMsgFromLog(log: string): string {
    return log.substr(log.indexOf(' ') + 1);
  }

  toggleDeviceDetails(device: Device): void {
    if (this.isDeviceOpened(device)) {
      this.selectedDevice = null;
    } else {
      this.selectedDevice = device.mac;
    }
  }

  isDeviceOpened(device: Device): boolean {
    return this.selectedDevice === device.mac;
  }

  formatDate(monthsToAdd: number) {
    this.date = new Date();
    this.date.setMonth(this.date.getMonth() + monthsToAdd);

    return this.date.toLocaleDateString("fr-FR", this.options);
  }

  private subscriptionPrices: number[] = [0, 9, 18, 27, 36, 45, 50]

  updateAmount() {
    this.amountToPay = 0;
    this.amountToPay = this.amountToPay + this.subscriptionPrices[this.subscriptionForm.value.renewal];

    if (this.subscriptionForm.value.checkCable3 == true) {
      this.amountToPay = this.amountToPay + 3;
    }
    if (this.subscriptionForm.value.checkCable5 == true) {
      this.amountToPay = this.amountToPay + 5;
    }
    if (this.subscriptionForm.value.checkAdapter === true) {
      this.amountToPay = this.amountToPay + 13;
    }
  }

}
