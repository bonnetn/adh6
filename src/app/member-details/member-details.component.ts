import { Component, OnInit, OnDestroy } from '@angular/core';

import { Observable } from 'rxjs/Observable';
import { of }         from 'rxjs/observable/of';

import { UserService } from '../api/services/user.service';
import { DeviceService } from '../api/services/device.service';
import { User } from '../api/models/user';
import { Device } from '../api/models/device';

import { ActivatedRoute } from '@angular/router';


@Component({
  selector: 'app-member-details',
  templateUrl: './member-details.component.html',
  styleUrls: ['./member-details.component.css']
})
export class MemberDetailsComponent implements OnInit, OnDestroy {

  member$: Observable<User>;
  subDevices: any;
  wired_devices$: Observable<Device[]>;
  wireless_devices$: Observable<Device[]>;
  username: string;
  private sub: any;

  constructor(public userService: UserService, public deviceService: DeviceService, private route: ActivatedRoute) { }

  ngOnInit() {
    
    this.sub = this.route.params.subscribe(params => {
      this.username = params['username']; 
      this.member$ = this.userService.getUser(this.username);
      
      // Get all devices of a user and split them into two observables.
      // One for wireless devices and one for wired
      this.subDevices = this.deviceService.filterDevice( { 'username': this.username } ).subscribe( (devices: Device[]) => {
        var w = [];
        var wl = [];
        devices.forEach(function(device) {
          if(device.connectionType == "wired") {
            w.push( device );
          } else { 
            wl.push( device );
          }
        });
        this.wired_devices$ = of( w );
        this.wireless_devices$ = of( wl );
      });
    });
  }
  ngOnDestroy() {
    this.sub.unsubscribe();
    this.subDevices.unsubscribe();
  }

}
