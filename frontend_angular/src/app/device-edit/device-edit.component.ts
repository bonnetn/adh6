import {Component, OnDestroy, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {HttpResponse} from '@angular/common/http';
import {ActivatedRoute, ParamMap, Router} from '@angular/router';
import {DeviceService} from '../api/api/device.service';
import {Device} from '../api/model/device';
import {NotificationsService} from 'angular2-notifications';
import {first, switchMap} from 'rxjs/operators';

@Component({
  selector: 'app-device-edit',
  templateUrl: './device-edit.component.html',
  styleUrls: ['./device-edit.component.css']
})

export class DeviceEditComponent implements OnInit, OnDestroy {

  disabled = false;
  deviceForm: FormGroup;
  private device: Device;

  constructor(
    public deviceService: DeviceService,
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private notificationService: NotificationsService,
  ) {
    this.createForm();
  }

  createForm() {
    this.deviceForm = this.fb.group({
      username: ['', [Validators.required]],
      mac: ['AA:AA:AA:AA:AA:AA', [Validators.required, Validators.minLength(17), Validators.maxLength(17)]],
      connectionType: ['', Validators.required],
    });
  }

  onSubmit() {
    this.disabled = true;
    const v = this.deviceForm.value;
    const mac = this.device.mac;
    const device: Device = {
      mac: v.mac,
      connectionType: v.connectionType,
      username: v.username
    };

    this.deviceService.putDevice(mac, device, 'response')
      .pipe(first())
      .subscribe((response: HttpResponse<void>) => {
        this.notificationService.success(response.status + ': Success');
        this.router.navigate(['member/view', v.username]);
      });
  }

  ngOnInit() {
    this.route.paramMap
      .pipe(
        switchMap((params: ParamMap) => this.deviceService.getDevice(params.get('mac'))),
        first(),
      )
      .subscribe(device => {
        this.device = device;
        this.deviceForm.patchValue(device);
      });
  }

  ngOnDestroy() {
  }
}
