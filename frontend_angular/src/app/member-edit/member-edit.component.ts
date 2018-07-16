import { Component, OnInit, OnDestroy } from '@angular/core';
import { AbstractControl, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpResponse, HttpErrorResponse } from '@angular/common/http';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';

import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/switchMap';
import 'rxjs/add/operator/takeWhile';

import { UserService } from '../api/services/user.service';
import { User } from '../api/models/user';
import { NotificationsService } from 'angular2-notifications/dist';


@Component({
  selector: 'app-member-edit',
  templateUrl: './member-edit.component.html',
  styleUrls: ['./member-edit.component.css'],
})
export class MemberEditComponent implements OnInit, OnDestroy {

  disabled: boolean = false;
  private alive: boolean = true;
  private originalUsername;

  private member$: Observable<User>;

  memberEdit: FormGroup;

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
      firstName: ['', Validators.required ], 
      lastName: ['', Validators.required ], 
      username: ['', [Validators.required, Validators.minLength(7), Validators.maxLength(8)] ],
      email: ['', [Validators.required, Validators.email] ], 
      roomNumber: [0, [Validators.min(1000), Validators.max(9999), Validators.required ]],
    });

  }

  onSubmit() {
    this.disabled = true;
    const v = this.memberEdit.value;
    const user: User = {
      email: v.email,
      firstName: v.firstName,
      lastName: v.lastName,
      username: v.username,
      roomNumber: v.roomNumber
    }
    this.userService.putUserResponse( { 
              "username": this.originalUsername,
              "body": user,
            })
      .takeWhile( () => this.alive )
      .subscribe( (response) => {
        this.router.navigate(["member/view", user.username ])
        this.notif.success(response.status + ": Success")
      });

  }

  onDelete() {
    this.userService.deleteUserResponse( this.originalUsername )
      .takeWhile( () => this.alive )
      .subscribe( (response) => {
        this.router.navigate(["member/search"])
        this.notif.success(response.status + ": Success")
      });
  }

  ngOnInit() {
    this.route.paramMap
      .switchMap((params: ParamMap) => 
        this.userService.getUser( params.get("username") ))
      .takeWhile( () => this.alive )
      .subscribe( (member: User) => {
        this.originalUsername = member.username;
        this.memberEdit.patchValue(member);
      });
  }

  ngOnDestroy() {
    this.alive = false;
  }

}
