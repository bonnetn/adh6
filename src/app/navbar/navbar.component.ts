import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AppComponent } from '../app.component';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {

  constructor(
    private appcomponent: AppComponent,
    private router: Router
  ) { }

  logout(){
    this.appcomponent.token=null
    this.router.navigate(["dashboard"])
  }

  navBarStatus: boolean = false;

  ngOnInit() {
  }

}
