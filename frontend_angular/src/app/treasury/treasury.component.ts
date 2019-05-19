import {Component, OnInit} from '@angular/core';

import {Observable} from 'rxjs';

import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import {PagingConf} from '../paging.config';

import {AccountService} from '../api/api/account.service';
import {Account} from '../api/model/account';
import {PagingConf} from '../paging.config';

import {map} from 'rxjs/operators';
import {SearchPage} from '../search-page';

class AccountListResponse {
  accounts?: Array<Account>;
  page_number?: number;
  item_count?: number;
  item_per_page?: number;
}

@Component({
  selector: 'app-treasury',
  templateUrl: './treasury.component.html',
  styleUrls: ['./treasury.component.css']
})
export class TreasuryComponent extends SearchPage implements OnInit {
  result$: Observable<AccountListResponse>;

  showFundManagement = false;
  fundManagementForm: FormGroup;
  create = false;

  constructor(private fb: FormBuilder, public accountService: AccountService) {
    super();
    this.createForm();
  }

  createForm() {
    this.fundManagementForm = this.fb.group({
      toCashRegister: ['', [Validators.min(0)]],
      outOfCashRegister: ['', [Validators.min(0)]],
      toSafe: ['', [Validators.min(0)]],
      outOfSafe: ['', [Validators.min(0)]],
      labelOp: ['', []],
    });
  }

  ngOnInit() {
    super.ngOnInit();
    this.result$ = this.getSearchResult((terms, page) => this.fetchAccounts(terms, page));
  }

  onSubmit() {
    console.log("onSubmit() à compléter");;
  }

  toggleFundManagement() {
    this.showFundManagement = !this.showFundManagement;
  }

  private fetchAccounts(terms: string, page: number) {
    const n = +PagingConf.item_count;
    return this.accountService.accountGet(n, (page - 1) * n, terms, undefined, undefined, 'response')
      .pipe(
        // switch to new search observable each time the term changes
        map((response) => <AccountListResponse>{
          accounts: response.body,
          item_count: +response.headers.get('x-total-count'),
          page_number: page,
          item_per_page: n,
        }),
      );
  }


}
