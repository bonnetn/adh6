import { Component, OnInit, OnDestroy } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { PortService } from '../api/services/port.service';
import { Port } from '../api/models/port';
import { Router, ActivatedRoute } from '@angular/router';
import { NotificationsService } from 'angular2-notifications';

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
  port_ouverture: string = "ouvert";
  portouvert: boolean = true;
  port_authenth: string = "authentifié";
  isportauthenth: boolean = false;

  constructor(
    public portService: PortService, 
    private route: ActivatedRoute,
    private router: Router,
    private notif: NotificationsService,
  ) { }

  ouverture() {
    this.portouvert = !this.portouvert
  }

  authenth() {
    this.isportauthenth = ! this.isportauthenth
  }

  IfRoomExists(roomNumber) {
    console.log(roomNumber)
    if (roomNumber == null) {
      this.notif.error("This port is not assigned to a room");
    }
    else {
      this.router.navigate(["/room/view", roomNumber])
    }
  }

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
