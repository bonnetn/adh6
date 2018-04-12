import { Component, OnInit, OnDestroy } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/switchMap';
import 'rxjs/add/operator/takeWhile';
import { HttpResponse } from '@angular/common/http';
import { AbstractControl, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { RoomService } from '../api/services/room.service';
import { PortService } from '../api/services/port.service';
import { Room } from '../api/models/room';
import { PortSearchResult } from '../api/models/port-search-result';
import { User } from '../api/models/user';
import { UserService } from '../api/services/user.service';
import { AppComponent } from '../app.component';

@Component({
  selector: 'app-room-details',
  templateUrl: './room-details.component.html',
  styleUrls: ['./room-details.component.css']
})
export class RoomDetailsComponent implements OnInit, OnDestroy {
  
  disabled: boolean = false;
  private alive: boolean = true;

  room$: Observable<Room>;
  ports$: Observable<PortSearchResult[]>;
  members$: Observable<User[]>;
  roomNumber: number;
  private sub: any;

  memberEdit: FormGroup;

  constructor(
    private appcomponent: AppComponent,
    private router: Router,
    public roomService: RoomService, 
    public portService: PortService, 
    public userService: UserService, 
    private fb: FormBuilder,
    private route: ActivatedRoute,
  ) { this.createForm(); }

  createForm() {
    this.memberEdit = this.fb.group({
      firstName: ['', Validators.required ],
      lastName: ['', Validators.required ],
      username: ['', [Validators.required, Validators.minLength(7)] ],
      email: ['', [Validators.required, Validators.email] ],
      roomNumber: [0, [Validators.min(1000), Validators.max(9999), Validators.required ]],
    });

  }

  onKick() {
    this.disabled = true;
    const v = this.memberEdit.value;
    const user: User = {
      email: v.email,
      firstName: v.firstName,
      lastName: v.lastName,
      username: v.username,
      roomNumber: null
    }

    var req = {
      "user" : user,
    };

    this.userService.putUserResponse( { "username": v.username, body: req } )
      .takeWhile( () => this.alive )
      .subscribe( (response : HttpResponse<void>) => {
        if(response.status == 204) {
          this.router.navigate(["member/view", user.username ])
          this.appcomponent.alert_type = "info"
          this.appcomponent.alert_message_type = "Succès"
          this.appcomponent.alert_message_display = v.firstName+" "+v.lastName+" a bien été supprimé de la chambre "+String(v.RoomNumber)
        }
        else if (response.status == 400) {
          this.router.navigate(["member/view", user.username ])
          this.appcomponent.alert_type = "warning"
          this.appcomponent.alert_message_type = "Attention"
          this.appcomponent.alert_message_display = "Informations invalides"
        }
        else {
          this.appcomponent.alert_type = "danger"
          this.appcomponent.alert_message_type = "Danger "
          this.appcomponent.alert_message_display = "Erreur Inconnue"
        }
      });

  }

  onDelete() {
    const v = this.roomNumber;
    this.roomService.deleteRoomResponse( v )
      .takeWhile( () => this.alive )
      .subscribe( (response : HttpResponse<void>) => {
        if( response.status == 204 ) {
          this.router.navigate(["room"])
          this.appcomponent.alert_type = "success"
          this.appcomponent.alert_message_type = "Succès"
          this.appcomponent.alert_message_display = "Chambre Supprimée"
        }
        else if (response.status == 404 ){
          this.appcomponent.alert_type = "warning"
          this.appcomponent.alert_message_type = "Attention"
          this.appcomponent.alert_message_display = "Chambre Inconnue"
        }
        else {
          this.appcomponent.alert_type = "danger"
          this.appcomponent.alert_message_type = "Danger"
          this.appcomponent.alert_message_display = "Erreur Inconnue"
        }
      });
  
  }


  ngOnInit() {
    this.sub = this.route.params.subscribe( params => {
      this.roomNumber = +params["roomNumber"];
      this.room$ = this.roomService.getRoom( this.roomNumber );
      this.ports$ = this.portService.filterPort( { 'roomNumber': this.roomNumber } );
      this.members$ = this.userService.filterUser( { 'roomNumber': this.roomNumber } );
    });
  }
  
  ngOnDestroy() {
    this.sub.unsubscribe();
  }

}
