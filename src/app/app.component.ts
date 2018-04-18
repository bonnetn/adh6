import { Component, OnInit, OnDestroy } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy{
  titre: string = 'ADH6';
  public token: any;

  getToken() {
    return this.token
  }
  
  isAuthenticated() {
    return this.getToken()!=null
  }

  ngOnInit() {
  }

  ngOnDestroy() {
  }

}

