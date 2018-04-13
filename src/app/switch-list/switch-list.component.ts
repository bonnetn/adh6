import { Component, OnInit } from '@angular/core';

import { Observable } from 'rxjs/Observable';

import { SwitchService } from '../api/services/switch.service';
import { Switch } from '../api/models/switch';

@Component({
  selector: 'app-switch-list',
  templateUrl: './switch-list.component.html',
  styleUrls: ['./switch-list.component.css']
})
export class SwitchListComponent implements OnInit {

  switches$: Observable<Switch[]>;

  constructor(public switchService: SwitchService) { }

  ngOnInit() {
    this.switches$ = this.switchService.filterSwitch({});
  }

}
