import {EMPTY, Observable} from 'rxjs';
import {catchError, first, isEmpty} from 'rxjs/operators';
import {HttpErrorResponse} from '@angular/common/http';

export class Utils {

  public static hasReturned404(s: Observable<any>): Observable<boolean> {
    return s
      .pipe(
        first(),
        catchError((err: HttpErrorResponse) => {
          if (err.status === 404) {
            return EMPTY;
          }
          return Observable.of(false);
        }),
        isEmpty(),
      );
  }

  public static sanitizeMac(mac: string) {
    return mac.toLowerCase().replace(/[^a-f0-9]+/g, '-');
  }

}
