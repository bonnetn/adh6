import {Component, OnDestroy, OnInit} from '@angular/core';
import {OAuthService} from 'angular-oauth2-oidc';
import {AppComponent} from '../app.component';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit, OnDestroy {

  public titre: string = this.appcomponent.titre;

  constructor(private oauthService: OAuthService,
              private appcomponent: AppComponent
  ) {
  }

  public login() {
    this.oauthService.initImplicitFlow();
  }

  public logoff() {
    this.oauthService.logOut();
  }

  ngOnInit() {
  }

  ngOnDestroy() {
  }

}

