import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import {PagingConf} from '../paging.config';

@Component({
  selector: 'app-treasury',
  templateUrl: './treasury.component.html',
  styleUrls: ['./treasury.component.css']
})
export class TreasuryComponent implements OnInit {
  showFundManagement = false;
  fundManagementForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.createForm();
  }

  createForm() {
    this.fundManagementForm = this.fb.group({
      toCashRegister: ['', [Validators.min(0)]],
      outOfCashRegister: ['', [Validators.min(0)]],
      toSafe: ['', [Validators.min(0)]],
      outOfSafe: ['', [Validators.min(0)]],
      labelOp: ['', []],
    });
  }

  ngOnInit() {
  }

  onSubmit() {
    console.log("onSubmit() à compléter");;
  }

  toggleFundManagement() {
    this.showFundManagement = !this.showFundManagement;
  }

}
