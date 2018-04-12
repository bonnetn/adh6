import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  constructor (
    public alert_type: string = "default";
    public alert_message_type: string = "";
    public alert_message_display: string  = "";
    public title: string = 'AboXII';
  )
  alert_type = "default" 
}

