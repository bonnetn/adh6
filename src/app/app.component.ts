import { Component, OnInit, OnDestroy } from '@angular/core';
import { OAuthService } from 'angular-oauth2-oidc';
import { JwksValidationHandler } from 'angular-oauth2-oidc';
import { authConfig } from './auth.config';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy{
  titre: string = 'ADH6';
  public isTokenValid: boolean;

  constructor(private oauthService: OAuthService) {
    this.configureWithNewConfigApi();
  }

  private configureWithNewConfigApi() {
    this.oauthService.configure(authConfig);
    this.oauthService.tokenValidationHandler = new JwksValidationHandler();
    this.oauthService.loadDiscoveryDocumentAndTryLogin();
  }

  isAuthenticated() {
    console.log(this.oauthService.hasValidIdToken())
    if (this.oauthService.hasValidIdToken()) {
      this.isTokenValid = true;
    }
    else {
      this.isTokenValid = false;
    }
  }

  ngOnInit() {
    this.isAuthenticated();
  }

  ngOnDestroy() {
  }

}

