import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, ParamMap, Router } from '@angular/router';

import { ProductService } from "../api/api/product.service";
import { Product } from "../api/model/product";
import { NotificationsService } from 'angular2-notifications';
import { Observable } from "rxjs";
import { switchMap, takeWhile } from 'rxjs/operators';

import { ProductPatchRequest } from '../api';

@Component({
  selector: 'app-product-edit',
  templateUrl: './product-edit.component.html',
  styleUrls: ['./product-edit.component.css']
})
export class ProductEditComponent implements OnInit, OnDestroy  {
  disabled = false;
  editProductForm: FormGroup;

  private alive = true;
  private product: Product;

  constructor(
    private productService: ProductService,
    private route: ActivatedRoute,
    private fb: FormBuilder,
    private router: Router,
    private notif: NotificationsService,
    ) {
        this.createForm();
    }
  createForm() {
    this.disabled = false;
    this.editProductForm = this.fb.group({
      productName: ['', [Validators.required]],
      productSellingPrice: ['', [Validators.required]],
      productBuyingPrice: ['', [Validators.required]]
    });
  }

  onSubmit() {
    this.disabled = true;
    const v = this.editProductForm.value;

    console.log(v);

    const productPatch: ProductPatchRequest = {
      name: v.productName,
      buyingPrice: v.productBuyingPrice,
      sellingPrice: v.productSellingPrice,
    };

    this.productService.productProductIdPatch(this.product.id, productPatch, 'response')
      .pipe(takeWhile(() => this.alive))
      .subscribe((response) => {
        this.router.navigate(['/product/view']);
        this.notif.success(response.status + ': Success');
      });
    this.disabled = false;
  }

  ngOnInit() {
   this.route.paramMap
      .pipe(
        switchMap((params: ParamMap) => this.productService.productProductIdGet(params.get('productID'))),
        takeWhile(() => this.alive),
      )
      .subscribe((data: Product) => {
        this.product = data;
        console.log(data);
        this.editProductForm.patchValue(data);
      });
  }

  ngOnDestroy() {
    this.alive = false;
  }

}
