import { Injectable } from '@angular/core';
import { OAuthService } from 'angular-oauth2-oidc';
import { ApiConfiguration } from 'app/api/api-configuration'

import {
  HttpEvent, HttpInterceptor, HttpHandler, HttpRequest
} from '@angular/common/http';

import { Observable } from 'rxjs/Observable';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(public oauthService : OAuthService,
              private conf : ApiConfiguration) {}

  intercept(req: HttpRequest<any>, next: HttpHandler):
    Observable<HttpEvent<any>> {
    let api_url = this.conf.rootUrl
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
