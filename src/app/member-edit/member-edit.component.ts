import { Component, OnInit, OnDestroy } from '@angular/core';
import { AbstractControl, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpResponse } from '@angular/common/http';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';

import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/switchMap';
import 'rxjs/add/operator/takeWhile';

import { UserService } from '../api/services/user.service';
import { User } from '../api/models/user';

import { AppComponent } from '../app.component'; 

@Component({
  selector: 'app-member-edit',
  templateUrl: './member-edit.component.html',
  styleUrls: ['./member-edit.component.css'],
})
export class MemberEditComponent implements OnInit, OnDestroy {

  // Disable the button to prevent multiple submit
  disabled: boolean = false;
  // Variable to destroy all subscriptions
  private alive: boolean = true;

  private member$: Observable<User>;

  memberEdit: FormGroup;

  constructor(
    private appcomponent: AppComponent,
    public userService: UserService, 
    private route: ActivatedRoute,
    private fb: FormBuilder, 
    private router: Router,
  ) {
    this.createForm();
  }

  createForm() {
    this.memberEdit = this.fb.group({
      firstName: ['', Validators.required ], 
      lastName: ['', Validators.required ], 
      username: ['', [Validators.required, Validators.minLength(7)] ], 
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

    var req = {
      "user" : user,
    };

    this.userService.putUserResponse( { "username": v.username, body: req } )
      .takeWhile( () => this.alive )
      .subscribe( (response : HttpResponse<void>) => {
        if( response.status == 204 || response.status == 201 ) {
          this.router.navigate(["member/view", user.username ])
        }
      });

  }

  onDelete() {
    const v = this.memberEdit.value;
    const user: User = {
      email: v.email,
      firstName: v.firstName,
      lastName: v.lastName,
      username: v.username,
      roomNumber: v.roomNumber
    }

    var req = {
      "user" : user,
    };

    this.userService.deleteUserResponse( v.username )
      .takeWhile( () => this.alive )
      .subscribe( (response : HttpResponse<void>) => {
        if( response.status == 204 ) {
          this.router.navigate(["member/search"])
          this.appcomponent.alert_type = "success"
          this.appcomponent.alert_message_type = "Succès"
          this.appcomponent.alert_message_display = "Chambre Supprimée"
        }
        else if (response.status == 404 ){
          alert("Error Delete User")
        }
        else {
          alert("Unknown Error")
        }
      });

  }

  ngOnInit() {
    this.route.paramMap
      .switchMap((params: ParamMap) => 
        this.userService.getUser( params.get("username") ))
      .takeWhile( () => this.alive )
      .subscribe( (member: User) => {
        this.memberEdit.patchValue(member);
      });
  }

  ngOnDestroy() {
    this.alive = false;
  }

}
