import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {TemporaryAccountService} from '../api';
import {filter, finalize, first, map} from 'rxjs/operators';
import {authConfig} from '../config/auth.config';
import {NotificationsService} from 'angular2-notifications';

@Component({
  selector: 'app-create-temporary-account',
  templateUrl: './create-temporary-account.component.html',
  styleUrls: ['./create-temporary-account.component.css']
})
export class CreateTemporaryAccountComponent implements OnInit {

  formGroup: FormGroup;
  disabled = false;
  access_token: string;
  url: string;

  constructor(
    private fb: FormBuilder,
    public tempAccService: TemporaryAccountService,
    private notif: NotificationsService,
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
        map((data) => data.accessToken),
        first(),
      )
      .subscribe((token) => {
        this.access_token = token;
      });
  }

  copyLink(inputElement) {
    inputElement.select();
    document.execCommand('copy');
    inputElement.setSelectionRange(0, 0);
    this.notif.success('Copied to clipboard!');
  }

  revokeTokens() {
    if (!window.confirm('Voulez-vous vraiment révoquer tous les comptes NainA actifs ?')) {
      return;
    }
    this.disabled = true;
    this.tempAccService.revokeTempAccount('response')
      .pipe(
        finalize(() => this.disabled = false)
        first(),
        map((response) => response.status),
        filter((status) => status === 204)
      )
      .subscribe((status) => {
        this.notif.success('Revoked all tokens!');
      });
  }
}
