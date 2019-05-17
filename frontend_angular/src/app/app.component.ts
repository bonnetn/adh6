import {Component, OnDestroy, OnInit} from '@angular/core';
import {JwksValidationHandler, OAuthService} from 'angular-oauth2-oidc';
import {authConfig} from './config/auth.config';
import {NAINA_FIELD, NAINA_PREFIX} from './config/naina.config';
import {ActivatedRoute} from '@angular/router';
import {filter, first, map} from 'rxjs/operators';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {
  titre = 'ADH6';

  constructor(
    private oauthService: OAuthService,
    private route: ActivatedRoute,
  ) {
    this.configureWithNewConfigApi();
  }

  isAuthenticated() {
    return this.oauthService.hasValidAccessToken();
  }

  ngOnInit() {
    this.isAuthenticated();
    this.route.fragment
      .pipe(
        filter((fragment) => fragment != null && fragment.startsWith(NAINA_FIELD + NAINA_PREFIX)),
        map((fragment) => fragment.substring(NAINA_FIELD.length)),
        first(),
      )
      .subscribe((token) => {
        if (this.isAuthenticated()) {
          alert('Vous êtes déjà authentifié.');
          return;
        }
        sessionStorage.setItem('access_token', token);
        sessionStorage.setItem('granted_scopes', '["profile"]');
        sessionStorage.setItem('access_token_stored_at', '' + Date.now());

        // const pathWithoutHash = this.location.path(false);
        // this.location.replaceState(pathWithoutHash);
      });
  }

  ngOnDestroy() {
  }

  private configureWithNewConfigApi() {
    this.oauthService.configure(authConfig);
    this.oauthService.tokenValidationHandler = new JwksValidationHandler();
    this.oauthService.tryLogin();
  }

}

