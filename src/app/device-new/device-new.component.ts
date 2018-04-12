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
  
  // Disable the button to prevent multiple submit
  disabled: boolean = false;
  // Variable to destroy all subscriptions
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
      mac: ['AA:AA:AA:AA:AA:AA', [Validators.required, Validators.minLength(17), Validators.maxLength(17)] ],
      connectionType: ['', Validators.required ],
    });
  }
 
  onSubmit() {
    this.disabled = true;
    const v = this.deviceForm.value;
    const user = this.route.snapshot.paramMap.get('username');
    const device: Device = {
      mac: v.mac,
      connectionType: v.connectionType,
      username: user
    }
          
    this.deviceService.putDeviceResponse( { "macAddress": v.mac, body: device })
      .takeWhile( ()=> this.alive )
      .subscribe( (response : HttpResponse<void>) => {
        this.router.navigate(["member/view", user ])
        this.notif.success(response.status + ": Success")
      }, (response) => {
        this.notif.error(response.status + ": " + response.error); 
      });
  
  }

  ngOnInit() {
  }
  
  ngOnDestroy() {
    this.alive=false;
  }

}
