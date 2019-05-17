import {Component, OnInit} from '@angular/core';
import {AbstractControl, FormBuilder, FormGroup, Validators} from '@angular/forms';
import {ActivatedRoute, Router} from '@angular/router';
import {NotificationsService} from 'angular2-notifications';
import {finalize, first, map, switchMap, tap} from 'rxjs/operators';
import {Observable} from 'rxjs';
import {MemberService} from '../api';

function passwordConfirming(c: AbstractControl): any {
  if (!c || !c.value) { return; }
  const pwd = c.value['password'];
  const cpwd = c.value['password_confirm'];

  if (!pwd || !cpwd) { return; }
  if (pwd !== cpwd) {
    return {invalid: true};
  }
}

@Component({
  selector: 'app-member-password-edit',
  templateUrl: './member-password-edit.component.html',
  styleUrls: ['./member-password-edit.component.css']
})
export class MemberPasswordEditComponent implements OnInit {

  disabled = false;
  memberPassword: FormGroup;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private notif: NotificationsService,
    private route: ActivatedRoute,
    private memberService: MemberService,
  ) {
  }

  ngOnInit() {
    this.createForm();
  }

  createForm(): void {
    this.memberPassword = this.fb.group({
      password: ['', [Validators.required, Validators.minLength(8)]],
      password_confirm: ['', [Validators.required, Validators.minLength(8)]],
    }, {
      validator: passwordConfirming
    });
  }


  changePassword(): void {
    this.getUsername()
      .pipe(
        first(),
        switchMap(username => this.updatePasswordOfUser(username)),
        finalize(() => this.disabled = false)
      )
      .subscribe((_) => {
      });
  }

  private updatePasswordOfUser(username: string) {
    return this.memberService.memberUsernamePasswordPut(
      {password: this.memberPassword.value.password},
      username,
      'response')
      .pipe(
        first(),
        tap((response) => {
          this.router.navigate(['member/view', username]);
          this.notif.success(response.status + ': Success');
        }),
      );

  }

  private getUsername(): Observable<string> {
    return this.route.paramMap.pipe(
      map(params => params.get('username')),
      first(),
    );
  }
}
