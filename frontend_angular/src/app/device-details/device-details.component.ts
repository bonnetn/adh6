import {Component, OnDestroy, OnInit} from '@angular/core';

import {Observable} from 'rxjs/Observable';
import {first, switchMap} from 'rxjs/operators';

import {DeviceService} from '../api/api/device.service';
import {Device} from '../api/model/device';

import {ActivatedRoute, Router} from '@angular/router';


@Component({
  selector: 'app-device-details',
  templateUrl: './device-details.component.html',
  styleUrls: ['./device-details.component.css']
})
export class DeviceDetailsComponent implements OnInit, OnDestroy {

  device$: Observable<Device>;

  constructor(
    public deviceService: DeviceService,
    private route: ActivatedRoute,
    private router: Router) {
  }

  onDelete(mac: string) {
    this.deviceService.deleteDevice(mac)
      .pipe(first())
      .subscribe(() => {
        this.router.navigate(['device/search']);
      });
  }

  ngOnInit() {
    this.device$ = this.route.params.pipe(
      switchMap(params =>
        this.deviceService.getDevice(params['mac'])
      ),
    );
  }

  ngOnDestroy() {
  }

}
