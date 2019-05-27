import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Product } from "../api/model/product";
import { ProductService } from '../api/api/product.service';
import { takeWhile } from 'rxjs/operators';
import { ActivatedRoute, Router } from '@angular/router';
import { NotificationsService } from 'angular2-notifications';
import {Observable} from 'rxjs';

@Component({
  selector: 'app-product-create',
  templateUrl: './product-create.component.html',
  styleUrls: ['./product-create.component.css']
})
export class ProductCreateComponent implements OnInit {

  disabled = false;
  productForm: FormGroup;

  private alive = true;

  constructor(
    private fb: FormBuilder,
    public productService: ProductService,
    private route: ActivatedRoute,
    private router: Router,
    private notif: NotificationsService,
    ) {
      this.createForm();
      }

  createForm() {
    this.productForm = this.fb.group({
      productName: ['', [Validators.required]],
      productSellingPrice: [0, [Validators.required]],
      productBuyingPrice: [0, [Validators.required]],
    });
  }

    onSubmit() {
    this.disabled = true;
    const v = this.productForm.value;

    const product: Product = {
      name: v.productName,
      sellingPrice: v.productSellingPrice,
      buyingPrice: v.productBuyingPrice
    };

    this.productService.productPost(product)
      .pipe(takeWhile(() => this.alive))
      .subscribe(res => {
        this.router.navigate(['/product/search']);
        this.notif.success(res.status + ': Success');
      });

    this.disabled = false;
  }
  ngOnInit() {
  }

}
