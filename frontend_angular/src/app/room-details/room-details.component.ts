import {Component, OnDestroy, OnInit} from '@angular/core';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/operator/switchMap';
import 'rxjs/add/operator/takeWhile';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {ActivatedRoute, Router} from '@angular/router';
import {RoomService} from '../api/api/room.service';
import {PortService} from '../api/api/port.service';
import {Room} from '../api/model/room';
import {Port} from '../api/model/port';
import {Member} from '../api/model/member';
import {MemberService} from '../api/api/member.service';
import {NotificationsService} from 'angular2-notifications';

@Component({
  selector: 'app-room-details',
  templateUrl: './room-details.component.html',
  styleUrls: ['./room-details.component.css']
})
export class RoomDetailsComponent implements OnInit, OnDestroy {

  disabled = false;
  authenth = false;
  room$: Observable<Room>;
  ports$: Observable<Array<Port>>;
  members$: Observable<Array<Member>>;
  roomNumber: number;
  roomForm: FormGroup;
  EmmenagerForm: FormGroup;
  public isEmmenager = false;
  public isDemenager = false;
  public ref: string;
  private alive = true;
  private sub: any;

  constructor(
    private notif: NotificationsService,
    private router: Router,
    public roomService: RoomService,
    public portService: PortService,
    public memberService: MemberService,
    private fb: FormBuilder,
    private route: ActivatedRoute,
  ) {
    this.createForm();
  }

  createForm() {
    this.ngOnInit();
    this.roomForm = this.fb.group({
      roomNumberNew: [this.roomNumber, [Validators.min(1000), Validators.max(9999), Validators.required]],
    });
    this.EmmenagerForm = this.fb.group({
      username: ['', [Validators.minLength(7), Validators.maxLength(8), Validators.required]],
    });
  }

  auth() {
    this.authenth = !this.authenth;
  }

  onEmmenager() {
    this.isEmmenager = !this.isEmmenager;
  }

  onDemenager(username) {
    this.ref = username;
    this.isDemenager = !this.isDemenager;
  }

  refreshInfo() {
    this.room$ = this.roomService.roomRoomNumberGet(this.roomNumber);
    this.ports$ = this.portService.portGet(undefined, undefined, undefined, this.roomNumber);
    this.members$ = this.memberService.memberGet(undefined, undefined, undefined, this.roomNumber);
  }

  onSubmitComeInRoom() {
    const v = this.EmmenagerForm.value;
    this.memberService.memberUsernameGet(v.username)
      .takeWhile(() => this.alive)
      .subscribe((user) => {
        user['roomNumber'] = this.roomNumber;
        this.memberService.memberUsernamePut(user, v.username, 'response')
          .takeWhile(() => this.alive)
          .subscribe((response) => {
            this.refreshInfo();
            this.notif.success(response.status + ': Success');
            this.onEmmenager();
          });
      }, (user) => {
        this.notif.error('Member ' + v.username + ' does not exists');
      });
  }

  onSubmitMoveRoom(username) {
    const v = this.roomForm.value;
    const room: Room = {
      roomNumber: v.roomNumberNew
    };
    this.memberService.memberUsernameGet(username)
      .takeWhile(() => this.alive)
      .subscribe((user) => {
        user['roomNumber'] = v.roomNumberNew;
        this.memberService.memberUsernamePut(user, username, 'response')
          .takeWhile(() => this.alive)
          .subscribe((response) => {
            this.refreshInfo();
            this.onDemenager(username);
            this.router.navigate(['room', v.roomNumberNew]);
            this.notif.success(response.status + ': Success');
          });
      });
  }

  onRemoveFromRoom(username) {
    this.memberService.memberUsernameGet(username)
      .takeWhile(() => this.alive)
      .subscribe((user) => {
        delete user['roomNumber'];
        this.memberService.memberUsernamePut(user, username, 'response')

          .takeWhile(() => this.alive)
          .subscribe((response) => {
            this.refreshInfo();
            this.notif.success(response.status + ': Success');
          });
      });
  }

  onDelete() {
    const v = this.roomNumber;
    this.roomService.roomRoomNumberDelete(v, 'response')
      .takeWhile(() => this.alive)
      .subscribe((response) => {
        this.router.navigate(['room']);
        this.notif.success(response.status + ': Success');
      });
  }


  ngOnInit() {
    this.sub = this.route.params.subscribe(params => {
      this.roomNumber = +params['roomNumber'];
      this.refreshInfo();
    });
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }

}
