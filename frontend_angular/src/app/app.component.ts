import {Component, OnDestroy, OnInit} from '@angular/core';
import {JwksValidationHandler, OAuthService} from 'angular-oauth2-oidc';
import {authConfig} from './auth.config';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {
  titre = 'ADH6';

  constructor(private oauthService: OAuthService) {
    this.configureWithNewConfigApi();
  }

  isAuthenticated() {
    return this.oauthService.hasValidAccessToken();
  }

  ngOnInit() {
    this.isAuthenticated();
  }

  ngOnDestroy() {
  }

  private configureWithNewConfigApi() {
    this.oauthService.configure(authConfig);
    this.oauthService.tokenValidationHandler = new JwksValidationHandler();
    this.oauthService.tryLogin();
  }

}

