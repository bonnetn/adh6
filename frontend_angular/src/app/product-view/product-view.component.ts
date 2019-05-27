import { Component, OnInit } from '@angular/core';
import {Observable} from 'rxjs';
import {ActivatedRoute} from '@angular/router';

import {Product} from '../api/model/product';
import {ProductService} from '../api/api/product.service';

import {SearchPage} from '../search-page';
import {BehaviorSubject} from 'rxjs';
import {PagingConf} from '../paging.config';

import {map} from 'rxjs/operators';


@Component({
  selector: 'app-product-view',
  templateUrl: './product-view.component.html',
  styleUrls: ['./product-view.component.css']
})

export class ProductViewComponent extends SearchPage implements OnInit {
  product$: Observable<Product>;
  productID: number;
  page_number = 1;
  item_count = 1;
  items_per_page: number = +PagingConf.item_count;
  private sub: any;
  private searchTerms = new BehaviorSubject<string>('');

  constructor(public productService: ProductService, private route: ActivatedRoute) {
    super();
  }

  search(term: string): void {
    this.searchTerms.next(term);
  }

    ngOnInit() {
    super.ngOnInit();
    this.sub = this.route.params.subscribe(params => {
      this.productID = +params['productID'];
    });

  }

}
