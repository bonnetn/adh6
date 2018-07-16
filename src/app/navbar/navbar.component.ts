import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AppComponent } from '../app.component';
import { OAuthService } from 'angular-oauth2-oidc';
import { authConfig } from '../auth.config';


@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {

  public titre: string = this.appcomponent.titre

  constructor(private oauthService: OAuthService,
    private appcomponent: AppComponent,
    private router: Router
  ) { }

  logout(){
    this.oauthService.logOut()
    window.location.href=authConfig.logoutUrl;
  }

  navBarStatus: boolean = false;

  ngOnInit() {
  }

}
