import {Injectable} from '@angular/core';
import {OAuthService} from 'angular-oauth2-oidc';

import {HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from '@angular/common/http';

import {Observable} from 'rxjs';
import {authConfig} from '../config/auth.config';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(public oauthService: OAuthService) {
  }

  intercept(req: HttpRequest<any>, next: HttpHandler):
    Observable<HttpEvent<any>> {
    const api_url = authConfig.redirectUri;
    // Check that the request is for the API server
    if (req.url.substr(0, api_url.length) === api_url) {
      // if so, add the authentication header
      req = req.clone({
        setHeaders: {
          Authorization: this.oauthService.authorizationHeader()
        }
      });
    }
    return next.handle(req);
  }
}
