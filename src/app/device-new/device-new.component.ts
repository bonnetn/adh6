import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { HttpResponse } from '@angular/common/http';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';

import 'rxjs/add/operator/takeWhile';
import 'rxjs/add/operator/switchMap';

import { DeviceService } from '../api/services/device.service';
import { Device } from '../api/models/device';
import { NotificationsService } from 'angular2-notifications';

@Component({
  selector: 'app-device-new',
  templateUrl: './device-new.component.html',
  styleUrls: ['./device-new.component.css']
})

export class DeviceNewComponent implements OnInit, OnDestroy {
  
  disabled: boolean = false;
  private alive: boolean = true;

  deviceForm: FormGroup;

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
      username: ['', [Validators.required, Validators.minLength(8), Validators.maxLength(8)] ],
      mac: ['', [Validators.required, Validators.minLength(17), Validators.maxLength(17)] ],
      connectionType: ['', Validators.required ],
    });
  }
 
  onSubmit() {
    this.disabled = true;
    const v = this.deviceForm.value;
    const device: Device = {
      connectionType: v.connectionType,
      mac: v.mac,
      username: v.username
    }
          
    this.deviceService.putDeviceResponse( { "macAddress": v.mac, body: device })
      .takeWhile( ()=> this.alive )
      .subscribe( (response) => {
        this.router.navigate(["device/view", v.mac ])
        this.notif.success(response.status + ": Success")
      }, (response) => {
        this.notif.error(response.status + ": " + response.error); 
      });
    this.disabled = false;
  
  }

  ngOnInit() {
  }
  
  ngOnDestroy() {
    this.alive=false;
  }

}
