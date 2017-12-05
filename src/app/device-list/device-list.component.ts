import { Component, OnInit } from '@angular/core';

import { Observable } from 'rxjs/Observable';

import { DeviceService } from '../api/services/device.service';
import { Device } from '../api/models/device';

@Component({
  selector: 'app-device-list',
  templateUrl: './device-list.component.html',
  styleUrls: ['./device-list.component.css']
})
export class DeviceListComponent implements OnInit {

  devices$: Observable<Device[]>;

  constructor(public deviceService: DeviceService) { }

  ngOnInit() {
    this.devices$ = this.deviceService.filterDevice( {} );
  }

}
