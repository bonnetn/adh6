import {Router} from '@angular/router';
import {Component, OnInit} from '@angular/core';
import {Observable} from 'rxjs';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {NotificationsService} from 'angular2-notifications';
import {SwitchService} from '../api/api/switch.service';
import {ModelSwitch} from '../api/model/modelSwitch';
import {takeWhile} from 'rxjs/operators';

@Component({
  selector: 'app-switch-new',
  templateUrl: './switch-new.component.html',
  styleUrls: ['./switch-new.component.css']
})
export class SwitchNewComponent implements OnInit {

  switches$: Observable<Array<ModelSwitch>>;
  switchForm: FormGroup;
  disabled = false;
  private alive = true;

  constructor(
    private fb: FormBuilder,
    public switchService: SwitchService,
    private router: Router,
    private notif: NotificationsService,
  ) {
    this.createForm();
  }

  createForm() {
    this.switchForm = this.fb.group({
      ip: ['', [Validators.required, Validators.minLength(11), Validators.maxLength(15)]],
      description: ['', Validators.required],
      community: ['', Validators.required],
    });
  }

  onSubmit() {
    const v = this.switchForm.value;
    const varSwitch: ModelSwitch = {
      description: v.description,
      ip: v.ip,
      community: v.community,
    };

    this.switchService.switchPost(varSwitch)
      .pipe(takeWhile(() => this.alive))
      .subscribe((res) => {
        this.router.navigate(['/switch/search']);
        this.notif.success(res.status + ': Success');
      });
  }

  ngOnInit() {
    this.switches$ = this.switchService.switchGet();
  }

}
