import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {TemporaryAccountService} from '../api';
import {finalize, first, map, tap} from 'rxjs/operators';
import {authConfig} from '../config/auth.config';

@Component({
  selector: 'app-create-temporary-account',
  templateUrl: './create-temporary-account.component.html',
  styleUrls: ['./create-temporary-account.component.css']
})
export class CreateTemporaryAccountComponent implements OnInit {

  formGroup: FormGroup;
  disabled: boolean = false;
  access_token: string;
  url: string;

  constructor(
    private fb: FormBuilder,
    public tempAccService: TemporaryAccountService,
  ) {
  }

  ngOnInit() {
    this.createForm();
    this.access_token = '';
    this.url = authConfig.redirectUri;
  }

  createForm(): void {
    this.formGroup = this.fb.group({
      first_name: ['', [Validators.required]],
      last_name: ['', [Validators.required]],
    });
  }

  createNainA(): void {
    const v = this.formGroup.value;
    this.disabled = true;
    this.tempAccService.createTempAccount(
      {
        firstname: v.first_name,
        lastname: v.last_name
      })
      .pipe(
        finalize(() => this.disabled = false),
        tap((data) => {console.log(data)})
        map((data) => data.accessToken),
        first(),
      )
      .subscribe((token) => {
        this.access_token = token;
      });
  }
}
