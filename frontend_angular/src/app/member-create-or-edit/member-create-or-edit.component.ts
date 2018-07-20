import {Component, OnDestroy, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {ActivatedRoute, ParamMap, Router} from '@angular/router';

import {UserService} from '../api/api/user.service';
import {User} from '../api/model/user';
import {NotificationsService} from 'angular2-notifications';
import {finalize, first, flatMap} from 'rxjs/operators';
import {EMPTY, Observable} from 'rxjs';
import {Utils} from '../utils';


@Component({
  selector: 'app-member-edit',
  templateUrl: './member-create-or-edit.component.html',
  styleUrls: ['./member-create-or-edit.component.css'],
})
export class MemberCreateOrEditComponent implements OnInit, OnDestroy {

  disabled = true;
  create = false;
  memberEdit: FormGroup;
  private originalUsername;

  constructor(
    public userService: UserService,
    private route: ActivatedRoute,
    private fb: FormBuilder,
    private router: Router,
    private notif: NotificationsService,
  ) {
    this.createForm();
  }

  createForm() {
    this.memberEdit = this.fb.group({
      firstName: ['', Validators.required],
      lastName: ['', Validators.required],
      username: ['', [Validators.required, Validators.minLength(7), Validators.maxLength(8)]],
      email: ['', [Validators.required, Validators.email]],
      roomNumber: [null, [Validators.min(1000), Validators.max(9999)]],
    });

  }

  editMember() {
    this.disabled = true;
    const v = this.memberEdit.value;
    let user: User = {
      email: v.email,
      firstName: v.firstName,
      lastName: v.lastName,
      username: v.username,
    };
    if (v.roomNumber) {
      user.roomNumber = v.roomNumber;
    }
    //
    Observable.of(this.create)
      .pipe(
        flatMap((create) => {
          const has404 = Utils.hasReturned404(this.userService.getUser(user.username));
          if (!create && this.originalUsername === user.username) {
            // Update and no change of the username, then OK
            return Observable.of(true);
          }
          // (Update and try to modify the username) OR (Create new user)
          // If there is already a user with that username, do not allow.
          return has404;
        }),
        flatMap((allowed) => {
          if (!allowed) {
            return EMPTY;
          }

          // If you create a user, then use the username from the form.
          // If you update a user, since the admin might have modified their username, you better use the original one (the one loaded at
          // initialization of the page).
          let username = user.username;
          if (!this.create) {
            username = this.originalUsername;
          }
          return this.userService.putUser(username, user, 'response')
            .pipe(
              first(),
              finalize(() => this.disabled = false),
            );
        })
      )
      .subscribe((response) => {
        this.router.navigate(['member/view', user.username]);
        this.notif.success(response.status + ': Success');
      });

  }

  deleteMember() {
    this.disabled = true;
    this.userService.deleteUser(this.originalUsername, 'response')
      .pipe(
        first(),
        finalize(() => this.disabled = false),
      )
      .subscribe((response) => {
        this.router.navigate(['member/search']);
        this.notif.success(response.status + ': Success');
      });
  }

  ngOnInit() {
    this.route.paramMap
      .pipe(
        flatMap((params: ParamMap) => {
          if (params.has('username')) {
            return Observable.of(params.get('username'));
          } else {
            // If username is not provided, we assume this is a create request
            this.disabled = false;
            this.create = true;
            return EMPTY;
          }
        }),
        flatMap((username) => this.userService.getUser(username)),
        first(),
      )
      .subscribe((member: User) => {
        this.originalUsername = member.username;
        this.memberEdit.patchValue(member);
        this.disabled = false;
      });
  }

  ngOnDestroy() {
  }

}
