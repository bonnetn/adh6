import {Component, OnDestroy, OnInit} from '@angular/core';
import {Observable} from 'rxjs/Observable';
import {PortService} from '../api/api/port.service';
import {Port} from '../api/model/port';
import {ActivatedRoute, Router} from '@angular/router';
import {NotificationsService} from 'angular2-notifications';

@Component({
  selector: 'app-port-details',
  templateUrl: './port-details.component.html',
  styleUrls: ['./port-details.component.css']
})
export class PortDetailsComponent implements OnInit, OnDestroy {

  port$: Observable<Port>;
  portID: number;
  switchID: number;

  vlans = [
    {'name': '1', 'value': '1'},
    {'name': 'dev: 103', 'value': '103'},
    {'name': 'prod: 102', 'value': '102'},
    {'name': '999', 'value': '999'}
  ];

  vlan: number;
  changeVlanVisible = false;
  selectedVlan = '1';

  portStatusString = 'N/A';
  portStatus: boolean;

  portAuthString = 'N/A';
  portAuth: boolean;

  private sub: any;

  constructor(
    public portService: PortService,
    private route: ActivatedRoute,
    private router: Router,
    private notif: NotificationsService,
  ) {
  }

  setStatus(state) {
    if (state) {
      this.portStatusString = 'OUI';
    } else {
      this.portStatusString = 'NON';
    }
    this.portStatus = state;
  }

  toggleStatus() {
    this.portService.portPortIdStatePut(!this.portStatus, this.portID)
      .subscribe((status) => {
        this.setStatus(status);
      });
  }

  setAuth(state) {
    if (state) {
      this.portAuthString = 'ACTIVE';
    } else {
      this.portAuthString = 'NON ACTIVE';
    }
    this.portAuth = state;
  }

  changeVlan(newVlan) {
    this.portService.portPortIdVlanPut(this.portID, newVlan)
      .subscribe((vlan) => {
        this.vlan = vlan;
      });
  }

  IfRoomExists(roomNumber) {
    if (roomNumber == null) {
      this.notif.error('This port is not assigned to a room');
    } else {
      this.router.navigate(['/room/view', roomNumber]);
    }
  }

  ngOnInit() {
    this.sub = this.route.params.subscribe(params => {
      this.switchID = +params['switchID'];
      this.portID = +params['portID'];
      this.port$ = this.portService.portPortIdGet(this.portID);
    });

    this.portService.stateGet(this.portID)
      .subscribe((status) => {
        this.setStatus(status);
      });
    this.portService.vlanGet(this.portID)
      .subscribe((vlan) => {
        this.vlan = vlan;
      });
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }

}
