import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

import {Observable} from 'rxjs';

import {TransactionService} from '../api/api/transaction.service';
import {Transaction} from '../api/model/transaction';
import {PagingConf} from '../paging.config';

import {map} from 'rxjs/operators';
import {SearchPage} from '../search-page';

export interface TransactionListResult {
  transactions?: Array<Transaction>;
  item_count?: number;
  current_page?: number;
  items_per_page?: number;
}

@Component({
  selector: 'app-transaction-new',
  templateUrl: './transaction-new.component.html',
  styleUrls: ['./transaction-new.component.css']
})
export class TransactionNewComponent extends SearchPage implements OnInit {
  transactionDetails: FormGroup;

  result$: Observable<TransactionListResult>;

  constructor(private fb: FormBuilder,
  public transactionService: TransactionService) {
    super();
    this.createForm();
  }

  createForm() {
    this.transactionDetails = this.fb.group({});
  }

  ngOnInit() {
    super.ngOnInit();
    this.result$ = this.getSearchResult((terms, page) => this.fetchTransaction(terms, page));
  }

  private fetchTransaction(terms: string, page: number): Observable<TransactionListResult> {
    const n = +PagingConf.item_count;
    return this.transactionService.transactionGet(n, (page - 1) * n, terms, undefined, 'response')
      .pipe(
        map((response) => {
          return <TransactionListResult>{
            transactions: response.body,
            item_count: +response.headers.get('x-total-count'),
            current_page: page,
            items_per_page: n,
          };
        }),
      );

  }

  onSubmit() {
  }
}
