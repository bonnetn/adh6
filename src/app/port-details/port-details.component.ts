import { Component, OnInit, OnDestroy } from '@angular/core';

import { Observable } from 'rxjs/Observable';

import { PortService } from '../api/services/port.service';
import { Port } from '../api/models/port';

import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-port-details',
  templateUrl: './port-details.component.html',
  styleUrls: ['./port-details.component.css']
})
export class PortDetailsComponent implements OnInit, OnDestroy {
  
  port$: Observable<Port>;
  portID: number;
  switchID: number;
  private sub: any;

  constructor(public portService: PortService, private route: ActivatedRoute) { }

  ngOnInit() {
    this.sub = this.route.params.subscribe( params => {
      this.switchID = +params["switchID"];
      this.portID = +params["portID"];  
      this.port$ = this.portService.getPort( { 'switchID': this.switchID, 'portID': this.portID } );
    });
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }

}
