import { Component, OnInit } from '@angular/core';
import { Observable, combineLatest } from "rxjs";
import {map, share, switchMap} from 'rxjs/operators';
import { AccountService } from "../api/api/account.service";
import { Account } from "../api/model/account";
import {ActivatedRoute, Router} from '@angular/router';

@Component({
  selector: 'app-account-view',
  templateUrl: './account-view.component.html',
  styleUrls: ['./account-view.component.css']
})
export class AccountViewComponent implements OnInit {
  account$: Observable<Account>;

  private id$: Observable<number>;

  constructor(
    private accountService: AccountService,
    private route: ActivatedRoute,
  ) { }

  ngOnInit() {
    // id of the account
    this.id$ = this.route.params.pipe(
      map(params => params['accountID'])
    );

    // stream, which will emit the account id every time the page needs to be refreshed
    const refresh$ = combineLatest([this.id$])
      .pipe(
        map(([x]) => x),
      );

    this.account$ = refresh$.pipe(
      switchMap(id => this.accountService.accountAccountIdGet(''+id)),
      share()
    );
  }

  goBack() {
    window.history.back();
  }
}
