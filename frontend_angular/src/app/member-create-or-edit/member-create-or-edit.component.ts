import {Component, OnDestroy, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {ActivatedRoute, ParamMap, Router} from '@angular/router';

import {MemberService} from '../api/api/member.service';
import {Member} from '../api/model/member';
import {NotificationsService} from 'angular2-notifications';
import {finalize, first, flatMap} from 'rxjs/operators';
import {EMPTY, Observable} from 'rxjs';
import {Utils} from '../utils';
import {MemberPatchRequest} from '../api';


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
    public memberService: MemberService,
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
    /*
    FLOW:
                +-------------+ update username  +-------------+ is allowed to +--------------------+
                |             | or create member |             |   put member  |                    |
    editMember-->  A) create  +------------------>  B) has404  +--------+------>  C) PATCH request  |
                |             |                  |             |        ^      |                    |
                +------+------+                  +-------------+        |      +--------------------+
                       |                                                |
                       +--------------------(true)----------------------+
                          regular update (does not update username)

     A) create value is transformed into an observable
        create = True means the form is for creation of a member
        create = False is to update a member
     B) has404 checks that a member with that username does not exist already.
     */


    this.disabled = true;
    const v = this.memberEdit.value;

    // If you create a user, then use the username from the form.
    // If you update a user, since the admin might have modified their username, you better use the original one (the one loaded at
    // initialization of the page).
    let requestUsername = v.username;
    if (!this.create) {
      requestUsername = this.originalUsername;
    }

    Observable.of(this.create)
      .pipe(
        flatMap((create) => {
          if (create) {
            // We don't want to override with PUT so we check if the member exist.
            return Utils.hasReturned404(this.memberService.getMember(v.username));
          }
          // If we try to modify, OK.
          return Observable.of(true);
        }),
        flatMap((canCreate) => {
          if (!canCreate) {
            return EMPTY;
          }
          return Observable.of(null);
        }),
        flatMap(() => {
          if (!this.create) {
            const req: MemberPatchRequest = {
              email: v.email,
              firstName: v.firstName,
              lastName: v.lastName,
              username: v.username,
            };
            if (v.roomNumber) {
              req.roomNumber = v.roomNumber;
            }
            return this.memberService.patchMember(requestUsername, req, 'response');
          } else {
            const req: Member = {
              email: v.email,
              firstName: v.firstName,
              lastName: v.lastName,
              username: v.username,
              roomNumber: (v.roomNumber == null ? 0 : v.roomNumber),
            };
            return this.memberService.putMember(requestUsername, req, 'response');
          }
        }),
        first(),
        finalize(() => this.disabled = false),
      )
      .subscribe((response) => {
        if (this.create) {
          this.router.navigate(['member/password', v.username]);
        } else {
          this.router.navigate(['member/view', v.username]);
        }
        this.notif.success(response.status + ': Success');
      });

  }

  deleteMember() {
    this.disabled = true;
    this.memberService.deleteMember(this.originalUsername, 'response')
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
        flatMap((username) => this.memberService.getMember(username)),
        first(),
      )
      .subscribe((member: Member) => {
        this.originalUsername = member.username;
        this.memberEdit.patchValue(member);
        this.disabled = false;
      });
  }

  ngOnDestroy() {
  }

}
