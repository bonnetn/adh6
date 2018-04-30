import { Injectable } from '@angular/core';
import { OAuthService } from 'angular-oauth2-oidc';
import { ApiConfiguration } from 'app/api/api-configuration'
import { HttpResponse } from '@angular/common/http';
import { HttpEventType } from '@angular/common/http';
import { NotificationsService } from 'angular2-notifications/dist';
import {
  HttpEvent, HttpInterceptor, HttpHandler, HttpRequest
} from '@angular/common/http';

import { Observable } from 'rxjs/Observable';

@Injectable()
export class NotifInterceptor implements HttpInterceptor {
  constructor(public oauthService : OAuthService,
    private conf : ApiConfiguration, 
    private notif: NotificationsService) {}

  intercept(req: HttpRequest<any>, next: HttpHandler):
    Observable<HttpEvent<any>> {
    let api_url = this.conf.rootUrl
    // Check that the request is for the API server
    if( req.url.substr(0, api_url.length) == api_url ) {
      // if there is an error, notify
      return next.handle(req).catch(response => {
        this.notif.error(response.status + ": " + response.error);
        return Observable.throw(response)
      });
    } else {
      return next.handle(req);
    }
  }
}
