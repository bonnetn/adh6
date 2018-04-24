import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { AbstractControl, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { SwitchService } from '../api/services/switch.service';
import { Switch } from '../api/models/switch';

@Component({
  selector: 'app-switch-edit',
  templateUrl: './switch-edit.component.html',
  styleUrls: ['./switch-edit.component.css']
})
export class SwitchEditComponent implements OnInit {

  switches$: Observable<Switch[]>;
  switchForm: FormGroup;

  constructor(
    private fb: FormBuilder, 
    public switchService: SwitchService,
  ) { 
    this.createForm(); 
  }

  createForm() {
    this.switchForm = this.fb.group({
      ip: ['', [Validators.required, Validators.minLength(11), Validators.maxLength(15)]],
    });
  }

  ngOnInit() {
    this.switches$ = this.switchService.filterSwitch({});
  }

}
