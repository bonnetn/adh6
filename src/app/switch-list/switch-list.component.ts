import { Component, OnInit } from '@angular/core';

import { Observable } from 'rxjs/Observable';

import { SwitchService } from '../api/services/switch.service';
import { SwitchSearchResult } from '../api/models/switch-search-result';

@Component({
  selector: 'app-switch-list',
  templateUrl: './switch-list.component.html',
  styleUrls: ['./switch-list.component.css']
})
export class SwitchListComponent implements OnInit {

  switches$: Observable<SwitchSearchResult[]>;

  constructor(public switchService: SwitchService) { }

  ngOnInit() {
    this.switches$ = this.switchService.filterSwitch( );
  }

}
