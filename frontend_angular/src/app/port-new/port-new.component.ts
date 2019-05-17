import {ActivatedRoute, Router} from '@angular/router';
import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {NotificationsService} from 'angular2-notifications';
import {PortService} from '../api/api/port.service';
import {Port} from '../api/model/port';

@Component({
  selector: 'app-port-new',
  templateUrl: './port-new.component.html',
  styleUrls: ['./port-new.component.css']
})
export class PortNewComponent implements OnInit {

  portForm: FormGroup;
  switchID: number;
  private alive = true;
  private sub: any;

  constructor(
    private fb: FormBuilder,
    public portService: PortService,
    private router: Router,
    private notif: NotificationsService,
    private route: ActivatedRoute,
  ) {
    this.createForm();
  }

  createForm() {
    this.portForm = this.fb.group({
      id: ['', [Validators.required]],
      roomNumber: ['', [Validators.required]],
      portNumber: ['', [Validators.required]],

    });
  }

  onSubmit() {
    const v = this.portForm.value;
    const port: Port = {
      id: v.id,
      portNumber: v.portNumber,
      roomNumber: v.roomNumber,
      switchID: this.switchID
    };
    this.portService.portPost(port)
      .takeWhile(() => this.alive)
      .subscribe((res) => {
        this.router.navigate(['/switch/', this.switchID, 'details']);
        this.notif.success(res.status + ': Success');
      });
  }

  ngOnInit() {
    this.sub = this.route.params.subscribe(params => {
      this.switchID = +params['switchID'];
    });
  }

}
