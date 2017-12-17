import { Component, OnInit, OnDestroy } from '@angular/core';

import { Observable } from 'rxjs/Observable';

import { SwitchService } from '../api/services/switch.service';
import { Switch } from '../api/models/switch';
import { PortSearchResult } from '../api/models/port-search-result';
import { PortService } from '../api/services/port.service';

import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-switch-details',
  templateUrl: './switch-details.component.html',
  styleUrls: ['./switch-details.component.css']
})
export class SwitchDetailsComponent implements OnInit, OnDestroy {

  switch$: Observable<Switch>;
  ports$: Observable<PortSearchResult[]>;
  switchID: number;
  private sub: any;

  constructor(public switchService: SwitchService, private route: ActivatedRoute, public portService: PortService) { }

  ngOnInit() {
    this.sub = this.route.params.subscribe( params => {
      this.switchID = +params["switchID"];
      this.switch$ = this.switchService.getSwitch(this.switchID);
      this.ports$ = this.portService.filterPort( { 'switchID': this.switchID } );
    });
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }

}
