import { Injectable } from '@angular/core';
import { OAuthService } from 'angular-oauth2-oidc';

import {
  HttpEvent, HttpInterceptor, HttpHandler, HttpRequest
} from '@angular/common/http';

import { Observable } from 'rxjs/Observable';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(public oauthService : OAuthService) {}

  intercept(req: HttpRequest<any>, next: HttpHandler):
    Observable<HttpEvent<any>> {
    let api_url = "https://adh6.minet.net/api";
    // Check that the request is for the API server
    if( req.url.substr(0, api_url.length) == api_url ) {
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
