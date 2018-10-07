import {Component, OnInit} from '@angular/core';
import {AbstractControl, FormBuilder, FormGroup, Validators} from '@angular/forms';

function passwordConfirming(c: AbstractControl): any {
  if (!c || !c.value) return;
  const pwd = c.value['password'];
  const cpwd = c.value['password_confirm'];

  if (!pwd || !cpwd) return;
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
    alert('!');
  }
}
