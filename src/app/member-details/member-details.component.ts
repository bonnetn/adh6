import { Component, OnInit, OnDestroy } from '@angular/core';

import { AbstractControl, FormBuilder, FormGroup, Validators } from '@angular/forms';

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
  all_devices$: Observable<Device[]>;
  wired_devices$: Observable<Device[]>;
  wireless_devices$: Observable<Device[]>;
  username: string;
  public cotisation: boolean = false;
  private sub: any;
  private alive: boolean = true;
  private commentForm: FormGroup;
  private commentSubmitDisabled: boolean = false;
  private deviceForm: FormGroup;

  constructor(
    public userService: UserService, 
    public deviceService: DeviceService, 
    private route: ActivatedRoute,
    private fb: FormBuilder,
  ) { 
    this.createForm();
  }

  onCotisation() {
    this.cotisation = !this.cotisation
  }

  createForm() {
    this.commentForm = this.fb.group( {
      comment: [''],
    });
    this.deviceForm = this.fb.group({
      mac: ['01:23:45:76:89:AB', [Validators.required, Validators.minLength(17), Validators.maxLength(17)]],
      connectionType: ['wired', Validators.required ],
    });
  }

  onSubmitComment() {
    // TODO: implement PATCH in API to simplify that method
    const newComment = this.commentForm.value.comment;
    this.commentSubmitDisabled = true;
    this.userService.getUser(this.username)
      .takeWhile( () => this.alive )
      .subscribe( (user) => {
        user.comment = newComment;
        const req = {
          "user":user,
        };
        this.userService.putUser( { 
          "username": this.username,
          "body": req,
        })
          .takeWhile( () => this.alive )
          .subscribe( () => {
            this.commentSubmitDisabled = false 
            this.refreshInfo();
          });
      });
  }
  
  onSubmitDevice() {
    const v = this.deviceForm.value;
    const device: Device = {
      mac: v.mac,
      connectionType: v.connectionType,
      username: this.username
    }
    this.deviceService.putDeviceResponse( { "macAddress": v.mac, body: device })
      .takeWhile( ()=> this.alive )
      .subscribe( ()=> { this.refreshInfo() });
  }

  onDelete(mac: string) {
    this.deviceService.deleteDevice(mac).subscribe( () => {
      this.refreshInfo();
    });
  }

  fetch_and_sort_devices() {
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
  }

  refreshInfo() {
    this.member$ = this.userService.getUser(this.username);
    //this.fetch_and_sort_devices();

    this.member$
      .takeWhile( () => this.alive )
      .subscribe( (user) => {
      this.commentForm.setValue( {
        comment: user.comment,
      });
    });
    this.all_devices$ = this.deviceService.filterDevice( { 'username': this.username } );
  }

  ngOnInit() {
    this.sub = this.route.params.subscribe(params => {
      this.username = params['username']; 
      this.refreshInfo();
    });
  }
  ngOnDestroy() {
    this.sub.unsubscribe();
    //this.subDevices.unsubscribe();
    this.alive = false;
  }

}
