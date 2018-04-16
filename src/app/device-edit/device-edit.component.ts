import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { HttpResponse } from '@angular/common/http';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/switchMap';
import 'rxjs/add/operator/takeWhile';
import { DeviceService } from '../api/services/device.service';
import { Device } from '../api/models/device';
import { NotificationsService } from 'angular2-notifications';

@Component({
  selector: 'app-device-edit',
  templateUrl: './device-edit.component.html',
  styleUrls: ['./device-edit.component.css']
})

export class DeviceEditComponent implements OnInit, OnDestroy {

  disabled: boolean = false;
  private alive: boolean = true;
  deviceForm: FormGroup;
  username: string;
  private sub: any;
  private device: Device;
  
  constructor(
    public deviceService: DeviceService,
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private notif: NotificationsService,
  ) { 
  this.createForm();
  }

  createForm() {
    this.deviceForm = this.fb.group({
      username: [ '', [Validators.required ] ],
      mac: ['AA:AA:AA:AA:AA:AA', [Validators.required, Validators.minLength(17), Validators.maxLength(17)] ],
      connectionType: ['', Validators.required ],
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
    }
          
    this.deviceService.putDeviceResponse( { "macAddress": mac, body: device })
      .takeWhile( ()=> this.alive )
      .subscribe( (response : HttpResponse<void>) => {
        this.notif.success(response.status + ": Success");
        this.router.navigate(["member/view", v.username ]);
      }, (response) => {
        this.notif.error(response.status + ": " + response.error);
      });
  }

  ngOnInit() {
    this.route.paramMap
    .switchMap((params: ParamMap) =>
      this.deviceService.getDevice(params.get('mac')))
        .takeWhile( () => this.alive )
        .subscribe( device => {
          this.device = device;
          this.deviceForm.patchValue(device);
        });
  }
  
  ngOnDestroy() {
    this.alive=false;
  }
}
