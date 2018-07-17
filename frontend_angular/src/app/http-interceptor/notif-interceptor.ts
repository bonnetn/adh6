import { Injectable } from '@angular/core';
import { OAuthService } from 'angular-oauth2-oidc';
import { HttpResponse } from '@angular/common/http';
import { HttpEventType } from '@angular/common/http';
import { NotificationsService } from 'angular2-notifications';
import {
  HttpEvent, HttpInterceptor, HttpHandler, HttpRequest
} from '@angular/common/http';

import { Observable } from 'rxjs/Observable';
import {catchError} from 'rxjs/operators';

@Injectable()
export class NotifInterceptor implements HttpInterceptor {
  constructor(public oauthService : OAuthService, private notif: NotificationsService) {}

  intercept(req: HttpRequest<any>, next: HttpHandler):
    Observable<HttpEvent<any>> {
    let api_url = "https://adh6.minet.net/api";
    // Check that the request is for the API server
    if( req.method != "GET" && req.url.substr(0, api_url.length) == api_url) {
      // if there is an error, notify
      return next.handle(req).pipe(
        catchError(response => {
            this.notif.error(response.status + ": " + response.error);
            return Observable.throw(response)
          }),
      );
    } else {
      return next.handle(req);
    }
  }
}
