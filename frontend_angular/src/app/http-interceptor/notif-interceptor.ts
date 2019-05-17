import {Injectable} from '@angular/core';
import {NotificationsService} from 'angular2-notifications';
import {HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from '@angular/common/http';

import {Observable, throwError} from 'rxjs';
import {catchError} from 'rxjs/operators';
import {authConfig} from '../config/auth.config';

@Injectable()
export class NotifInterceptor implements HttpInterceptor {
  constructor(private notif: NotificationsService) {
  }

  intercept(req: HttpRequest<any>, next: HttpHandler):
    Observable<HttpEvent<any>> {
    const api_url = authConfig.redirectUri;
    // Check that the request is for the API server
    if (req.method !== 'GET' && req.url.substr(0, api_url.length) === api_url) {
      // if there is an error, notify
      return next.handle(req).pipe(
        catchError(response => {
          this.notif.error(response.status + ': ' + response.error);
          return throwError(response);
        }),
      );
    } else {
      return next.handle(req);
    }
  }
}
