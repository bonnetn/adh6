import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  alert_type: string = "default";
  alert_message_type: string = "";
  alert_message_display: string  = "";
  titre: string = 'ADH6';

  onReset() {
    this.alert_type = "default";
    this.alert_message_type = "";
    this.alert_message_display = "";
  }
}

