import { Component, OnInit, OnDestroy } from '@angular/core';

import { Observable } from 'rxjs/Observable';

import { DeviceService } from '../api/services/device.service';
import { Device } from '../api/models/device';

import { Router, ActivatedRoute } from '@angular/router';


@Component({
  selector: 'app-device-details',
  templateUrl: './device-details.component.html',
  styleUrls: ['./device-details.component.css']
})
export class DeviceDetailsComponent implements OnInit, OnDestroy {

  device$: Observable<Device>;
  mac: string;
  private sub: any;
  constructor( 
    public deviceService: DeviceService, 
    private route: ActivatedRoute,
    private router: Router) { }

  onDelete( mac: string ) {
    this.deviceService.deleteDevice( mac ).subscribe( () => {
      this.router.navigate(["device/search"]);
    });
  }

  ngOnInit() {
    this.sub = this.route.params.subscribe( params => {
      this.mac = params["mac"];
      this.device$ = this.deviceService.getDevice( this.mac );
    });
  }
  ngOnDestroy() {
    this.sub.unsubscribe();
  }

}
