import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, ParamMap, Router } from '@angular/router';

import { AccountService } from "../api/api/account.service";
import { Account } from "../api/model/account";
import { NotificationsService } from 'angular2-notifications';
import { Observable } from "rxjs";
import { switchMap, takeWhile } from 'rxjs/operators';
import { AccountType } from '../api/model/accountType';
import { AccountTypeService } from "../api/api/accountType.service";
import { AccountPatchRequest } from '../api';

@Component({
  selector: 'app-account-edit',
  templateUrl: './account-edit.component.html',
  styleUrls: ['./account-edit.component.css']
})

export class AccountEditComponent implements OnInit, OnDestroy {
  disabled = false;
  editAccountForm: FormGroup;
  accountTypes$: Observable<Array<AccountType>>;

  private alive = true;
  private account: Account;

  constructor(
    private accountService: AccountService,
    private route: ActivatedRoute,
    private fb: FormBuilder,
    public accountTypeService: AccountTypeService,
    private router: Router,
    private notif: NotificationsService,
  ) {
    this.createForm();
  }

  createForm() {
    this.disabled = false;
    this.editAccountForm = this.fb.group({
      name: ['', [Validators.required]],
      type: ['', [Validators.required]],
      actif: ['', [Validators.required]]
    });
  }

  onSubmit() {
    this.disabled = true;
    const v = this.editAccountForm.value;

    console.log(v);

    const accountPatch: AccountPatchRequest = {
      name: v.name,
      actif: v.actif,
      type: parseInt(v.type),
    };

    this.accountService.accountAccountIdPatch(this.account.id, accountPatch, 'response')
      .pipe(takeWhile(() => this.alive))
      .subscribe((response) => {
        this.router.navigate(['/account/view', this.account.id]);
        this.notif.success(response.status + ': Success');
      });
    this.disabled = false;
  }


  ngOnInit() {
    this.accountTypes$ = this.accountTypeService.accountTypeGet();

    this.route.paramMap
      .pipe(
        switchMap((params: ParamMap) => this.accountService.accountAccountIdGet(params.get('accountID'))),
        takeWhile(() => this.alive),
      )
      .subscribe((data: Account) => {
        this.account = data;
        console.log(data);
        this.editAccountForm.patchValue(data);
      });
  }

  ngOnDestroy() {
    this.alive = false;
  }

}
