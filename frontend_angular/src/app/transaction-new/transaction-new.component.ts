import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

import {concat, EMPTY, from, merge, Observable, Subject} from 'rxjs';
import {debounceTime, distinctUntilChanged, map, mergeMap, scan, switchMap} from 'rxjs/operators';

import {TransactionService} from '../api/api/transaction.service';
import {Transaction} from '../api/model/transaction';
import {PagingConf} from '../paging.config';

import {SearchPage} from '../search-page';

import { PaymentMethod } from '../api/model/paymentMethod';
import { Account } from '../api/model/account';
import { AccountService } from '../api/api/account.service';
import { PaymentMethodService } from '../api/api/paymentMethod.service';

export interface TransactionListResult {
  transactions?: Array<Transaction>;
  item_count?: number;
  current_page?: number;
  items_per_page?: number;
}

class QueryParams {
  highlight: string;
}

export class SearchResult {
  objType: string;
  name: string;
  color = 'grey';
  link: Array<string>;
  queryParams: QueryParams;

  constructor(t: string, n: string, link: Array<string>, params?: QueryParams) {
    this.objType = t;
    this.name = n;
    this.color = 'red';
    this.link = link;
    this.queryParams = params;
  }
}

@Component({
  selector: 'app-transaction-new',
  templateUrl: './transaction-new.component.html',
  styleUrls: ['./transaction-new.component.css']
})
export class TransactionNewComponent extends SearchPage implements OnInit {
  transactionDetails: FormGroup;

  paymentMethods$: Observable<Array<PaymentMethod>>;
  result$: Observable<TransactionListResult>;

  srcSearchResult$: Observable<Array<SearchResult>>;
  dstSearchResult$: Observable<Array<SearchResult>>;
  private srcSearchTerm$ = new Subject<string>();
  private dstSearchTerm$ = new Subject<string>();

  constructor(private fb: FormBuilder,
  public transactionService: TransactionService,
  public paymentMethodService: PaymentMethodService,
  private accountService: AccountService) {
    super();
    this.createForm();
  }

  srcSearch(terms: string) {
    this.srcSearchTerm$.next(terms);
  }
  dstSearch(terms: string) {
    this.dstSearchTerm$.next(terms);
  }

  createForm() {
    this.transactionDetails = this.fb.group({});
  }

  ngOnInit() {
    super.ngOnInit();
    this.result$ = this.getSearchResult((terms, page) => this.fetchTransaction(terms, page));
    this.paymentMethods$ = this.paymentMethodService.paymentMethodGet();

    this.srcSearchResult$ = this.srcSearchTerm$.pipe(
      debounceTime(300),
      distinctUntilChanged()
    ).pipe(
      switchMap((terms: string) => {
        return this.accountService.accountGet(20, 0, terms).pipe(
          mergeMap((array) => from(array)),
          map((obj) => new SearchResult(
            'account',
            obj.name,
            ['/account/view', ''+obj.id]
          )),
        );
      }),
    ).pipe(map(x => [x]));

    this.dstSearchResult$ = this.dstSearchTerm$.pipe(
      debounceTime(300),
      distinctUntilChanged()
    ).pipe(
      switchMap((terms: string) => {
        return this.accountService.accountGet(20, 0, terms).pipe(
          mergeMap((array) => from(array)),
          map((obj) => new SearchResult(
            'account',
            obj.name,
            ['/account/view', ''+obj.id]
          )),
        );
      }),
    ).pipe(map(x => [x]));
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
