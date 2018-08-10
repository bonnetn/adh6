import {BehaviorSubject, combineLatest, merge, Observable} from 'rxjs';
import {debounceTime, distinctUntilChanged, map, switchMap} from 'rxjs/operators';

export class SearchPage {
  private searchTerm$ = new BehaviorSubject<string>('');
  private pageNumber$ = new BehaviorSubject<number>(1);

  protected getSearchResult(f: (term: string, page: number) => Observable<any>): Observable<any> {

    // Stream of terms debounced
    const termsDebounced$ = this.searchTerm$
      .pipe(
        debounceTime(300),
        distinctUntilChanged(),
      );

    // Combine terms + page and fetch the result from backend
    const result$ = combineLatest(termsDebounced$, this.pageNumber$)
      .pipe(
        switchMap(data => f(data[0], data[1])),
      );

    // When a new page is requested, emit an empty result to clear the page
    return merge(
      result$,
      this.pageNumber$
        .pipe(
          map(() => null)
        )
    );
  }

  protected search(term: string): void {
    this.searchTerm$.next(term);
  }

  protected changePage(page: number): void {
    this.pageNumber$.next(page);
  }

  ngOnInit() {
    this.changePage(1);
  }


}
