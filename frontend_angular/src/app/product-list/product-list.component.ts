import { Component, OnInit } from '@angular/core';

import {Observable} from 'rxjs';

import {ProductService} from '../api/api/product.service';
import {PagingConf} from '../paging.config';
import {SearchPage} from '../search-page';
import {map} from 'rxjs/operators';
import {Product} from '../api';

export interface ProductListResult {
  products: Array<Product>;
  item_count?: number;
  current_page?: number;
  items_per_page?: number;
}

@Component({
  selector: 'app-product-list',
  templateUrl: './product-list.component.html',
  styleUrls: ['./product-list.component.css']
})
export class ProductListComponent extends SearchPage implements OnInit {
  result$: Observable<ProductListResult>;

  constructor(public productService: ProductService) {
    super();
  }

  ngOnInit() {
    super.ngOnInit();
    this.result$ = this.getSearchResult((terms, page) => this.fetchProducts(terms, page));
  }

  private fetchProducts(terms: string, page: number): Observable<ProductListResult> {
      const n = +PagingConf.item_count;
      return this.productService.productGet(n, (page - 1) * n, terms, undefined, 'response')
        .pipe(
          map((response) => {
            return <ProductListResult> {
              products: response.body,
              item_count: +response.headers.get('x-total-count'),
              current_page: page,
              items_per_page: n,
            };
          }),
        );
  }
}
