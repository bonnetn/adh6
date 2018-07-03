import { Component, OnInit, OnDestroy } from '@angular/core'
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms'
import { HttpResponse } from '@angular/common/http'
import { Router, ActivatedRoute, ParamMap } from '@angular/router'

import 'rxjs/add/operator/takeWhile'
import 'rxjs/add/operator/switchMap'
import { empty } from 'rxjs/observable/empty'
import { catchError, flatMap, first, finalize } from 'rxjs/operators';

import { DeviceService } from '../api/services/device.service'
import { Device } from '../api/models/device'
import { NotificationsService } from 'angular2-notifications/dist'

@Component({
  selector: 'app-device-new',
  templateUrl: './device-new.component.html',
  styleUrls: ['./device-new.component.css']
})

export class DeviceNewComponent implements OnInit, OnDestroy {
  
  disabled: boolean = false
  deviceForm: FormGroup

  constructor(
    public deviceService: DeviceService,
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private notif: NotificationsService,
  ) { 
  this.createForm()
  }

  createForm() {
    this.deviceForm = this.fb.group({
      username: ['', [Validators.required, Validators.minLength(8), Validators.maxLength(8)] ],
      mac: ['', [Validators.required, Validators.minLength(17), Validators.maxLength(17)] ],
      connectionType: ['', Validators.required ],
    })
  }
  
  onSubmit() {
    this.disabled = true
    const v = this.deviceForm.value
    const device: Device = {
      username: v.username,
      mac: v.mac,
      connectionType: v.connectionType
    }

    this.deviceService.getDeviceResponse(v.mac).first().pipe(
        flatMap( (response, index) => {
          // if there is a response then you should not create a new device
          this.notif.error("Device already exists in database.")
          return empty<HttpResponse<void>>()
        }),
        catchError( err => {
          return this.deviceService.putDeviceResponse( { "macAddress": v.mac, body: device }).first()
        }),
        finalize( () => {
          this.disabled = false
        }),
    ).subscribe( response => {
      this.router.navigate(["device/view", v.mac ])
    })

  }

  ngOnInit() {
  }
  
  ngOnDestroy() {
  }

}
