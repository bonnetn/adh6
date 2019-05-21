import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Account } from "../api/model/account";
import { AccountService } from '../api/api/account.service';
import { takeWhile } from 'rxjs/operators';
import { ActivatedRoute, Router } from '@angular/router';
import { NotificationsService } from 'angular2-notifications';


@Component({
  selector: 'app-account-create',
  templateUrl: './account-create.component.html',
  styleUrls: ['./account-create.component.css']
})

export class AccountCreateComponent implements OnInit, OnDestroy {

  disabled = false;
  accountForm: FormGroup;
  private alive = true;

  constructor(
    private fb: FormBuilder,
    public accountService: AccountService,
    private route: ActivatedRoute,
    private router: Router,
    private notif: NotificationsService,
  ) {
    this.createForm();
  }

  createForm() {
    this.accountForm = this.fb.group({
      accountName: ['', [Validators.required]],
      accountType: ['0', [Validators.required]],
    });
  }

  onSubmit() {
    this.disabled = true;
    const v = this.accountForm.value;

    const account: Account = {
      actif: true,
      name: v.accountName,
      type: v.accountType
    };

    console.log(account);

    this.accountService.accountPost(account)
      .pipe(takeWhile(() => this.alive))
      .subscribe((res) => {
        this.router.navigate(['/treasury']);
        this.notif.success(res.status + ': Success');
      });

    this.disabled = false;
  }

  ngOnInit() {
  }

  ngOnDestroy() {
    this.alive = false;
  }

}
