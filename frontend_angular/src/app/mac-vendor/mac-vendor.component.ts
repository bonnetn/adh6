import {Component, Input, OnDestroy, OnInit} from '@angular/core';
import {DeviceService} from '../api/api/device.service';
import {first, map} from 'rxjs/operators';
import {Utils} from '../utils';

@Component({
  selector: 'app-mac-vendor',
  templateUrl: './mac-vendor.component.html',
  styleUrls: ['./mac-vendor.component.css']
})
export class MacVendorComponent implements OnInit, OnDestroy {

  @Input() mac: string;

  private alive = true;
  private vendor = '';

  constructor(
    public deviceService: DeviceService
  ) {
  }

  ngOnInit() {
    this.deviceService.vendorGet(Utils.sanitizeMac(this.mac).substr(0, 8))
      .pipe(
        map((data) => data.vendorname),
        first(),
      )
      .subscribe((vendor) => {
        this.vendor = vendor;
      });
  }

  ngOnDestroy() {
    this.alive = false;
  }

}
