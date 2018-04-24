import { Component, OnInit, OnDestroy } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { SwitchService } from '../api/services/switch.service';
import { Switch } from '../api/models/switch';
import { Port } from '../api/models/port';
import { PortService } from '../api/services/port.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-switch-local',
  templateUrl: './switch-local.component.html',
  styleUrls: ['./switch-local.component.css']
})
export class SwitchLocalComponent implements OnInit, OnDestroy {

  switch$: Observable<Switch>;
  ports$: Observable<Port[]>;
  switchID: number = 8;

  constructor(public switchService: SwitchService, private route: ActivatedRoute, public portService: PortService) { }

  ngOnInit() {
    this.switchID = 8;
    this.switch$ = this.switchService.getSwitch(this.switchID);
    this.ports$ = this.portService.filterPort( { 'switchID': this.switchID } );
  }

  ngOnDestroy() {
  }

}
