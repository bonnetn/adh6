import {Component, OnInit} from '@angular/core';
import {AppComponent} from '../app.component';
import {OAuthService} from 'angular-oauth2-oidc';
import {authConfig} from '../config/auth.config';


@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {

  public titre: string = this.appcomponent.titre;
  navBarStatus = false;

  constructor(private oauthService: OAuthService,
              private appcomponent: AppComponent) {
  }

  logout() {
    this.oauthService.logOut();
    window.location.href = authConfig.logoutUrl;
  }

  ngOnInit() {
  }

}
