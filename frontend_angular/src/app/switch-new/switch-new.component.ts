import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { SwitchService } from '../api/api/switch.service';
import { ModelSwitch } from '../api/model/modelSwitch';

@Component({
  selector: 'app-switch-new',
  templateUrl: './switch-new.component.html',
  styleUrls: ['./switch-new.component.css']
})
export class SwitchNewComponent implements OnInit {

  switches$: Observable<Array<ModelSwitch>>;
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
    this.switches$ = this.switchService.filterSwitch();
  }

}
