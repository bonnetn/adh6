import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { HttpResponse } from '@angular/common/http';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';

import 'rxjs/add/operator/takeWhile';
import 'rxjs/add/operator/switchMap';

import { DeviceService } from '../api/services/device.service';
import { Device } from '../api/models/device';

@Component({
  selector: 'app-device-form',
  templateUrl: './device-form.component.html',
  styleUrls: ['./device-form.component.css']
})

export class DeviceFormComponent implements OnInit, OnDestroy {
  
  // Disable the button to prevent multiple submit
  private disabled: boolean = false;
  // Variable to destroy all subscriptions
  private alive: boolean = true;
  
  deviceForm: FormGroup;
  
  constructor(
    public deviceService: DeviceService,
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
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
        if( response.status == 204 || response.status == 201 ) {
          this.router.navigate(["member/view", user ])
        }
      });
  
  }

  ngOnInit() {
  }
  
  ngOnDestroy() {
    this.alive=false;
  }

}
