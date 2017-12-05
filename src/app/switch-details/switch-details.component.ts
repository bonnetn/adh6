import { Component, OnInit, OnDestroy } from '@angular/core';

import { Observable } from 'rxjs/Observable';

import { SwitchService } from '../api/services/switch.service';
import { Switch } from '../api/models/switch';

import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-switch-details',
  templateUrl: './switch-details.component.html',
  styleUrls: ['./switch-details.component.css']
})
export class SwitchDetailsComponent implements OnInit, OnDestroy {

  switch$: Observable<Switch>;
  switchID: number;
  private sub: any;

  constructor(public switchService: SwitchService, private route: ActivatedRoute) { }

  ngOnInit() {
    this.sub = this.route.params.subscribe( params => {
      this.switchID = params['switchID'];
      this.switch$ = this.switchService.getSwitch(this.switchID);
    });
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }

}
