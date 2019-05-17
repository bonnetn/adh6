import {Component, OnDestroy, OnInit} from '@angular/core';
import {Observable} from 'rxjs';
import {SwitchService} from '../api/api/switch.service';
import {ModelSwitch} from '../api/model/modelSwitch';
import {Port} from '../api/model/port';
import {PortService} from '../api/api/port.service';

@Component({
  selector: 'app-switch-local',
  templateUrl: './switch-local.component.html',
  styleUrls: ['./switch-local.component.css']
})
export class SwitchLocalComponent implements OnInit, OnDestroy {

  switch$: Observable<ModelSwitch>;
  ports$: Observable<Array<Port>>;
  switchID = 1;

  constructor(public switchService: SwitchService, public portService: PortService) {
  }

  ngOnInit() {
    this.switchID = 1;
    this.switch$ = this.switchService.switchSwitchIDGet(this.switchID);
    this.ports$ = this.portService.portGet(undefined, undefined, this.switchID);
  }

  ngOnDestroy() {
  }

}
