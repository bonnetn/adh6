import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';

import { Observable } from 'rxjs/Observable';

import "rxjs/add/operator/takeWhile";

import { DeviceService } from '../api/services/device.service';
import { Device } from '../api/models/device';

@Component({
  selector: 'app-device-list',
  templateUrl: './device-list.component.html',
  styleUrls: ['./device-list.component.css']
})
export class DeviceListComponent implements OnInit {

  devices$: Observable<Device[]>;
  alive: boolean = true;

  constructor(public deviceService: DeviceService, private router: Router) { }
  
  onDelete( mac: string ) {
    this.deviceService.deleteDevice( mac )
      .takeWhile( () => this.alive )
      .subscribe( () => {
      this.refreshDevices();
    });
  }

  refreshDevices() {
    this.devices$ = this.deviceService.filterDevice( {} );
  }

  ngOnInit() {
    this.refreshDevices();
  }

  ngOnDestroy() {
    this.alive = false;
  }

}
