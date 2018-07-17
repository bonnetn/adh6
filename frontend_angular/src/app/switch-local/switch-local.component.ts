import { Component, OnInit, OnDestroy } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { SwitchService } from '../api/api/switch.service';
import { ModelSwitch } from '../api/model/modelSwitch';
import { Port } from '../api/model/port';
import { PortService } from '../api/api/port.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-switch-local',
  templateUrl: './switch-local.component.html',
  styleUrls: ['./switch-local.component.css']
})
export class SwitchLocalComponent implements OnInit, OnDestroy {

  switch$: Observable<ModelSwitch>;
  ports$: Observable<Array<Port>>;
  switchID = 8;

  constructor(public switchService: SwitchService, private route: ActivatedRoute, public portService: PortService) { }

  ngOnInit() {
    this.switchID = 8;
    this.switch$ = this.switchService.getSwitch(this.switchID);
    this.ports$ = this.portService.filterPort(undefined, undefined, this.switchID);
  }

  ngOnDestroy() {
  }

}