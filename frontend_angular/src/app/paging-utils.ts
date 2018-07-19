import {combineLatest, Observable} from 'rxjs';
import {debounceTime, distinctUntilChanged, map, switchMap} from 'rxjs/operators';
import {merge} from 'rxjs/observable/merge';

export class PagingUtils {

  public static getSearchResult(term$: Observable<string>,
                                page$: Observable<number>,
                                f: (term: string, page: number) => Observable<any>): Observable<any> {

    // Stream of terms debounced
    const termsDebounced$ = term$
      .pipe(
        debounceTime(300),
        distinctUntilChanged(),
      );

    // Combine terms + page and fetch the result from backend
    const deviceResult$ = combineLatest(termsDebounced$, page$)
      .pipe(
        switchMap(data => f(data[0], data[1])),
      );

    // When a new page is requested, emit an empty result to clear the page
    return merge(
      deviceResult$,
      page$
        .pipe(
          map(() => null)
        )
    );
  }


}
