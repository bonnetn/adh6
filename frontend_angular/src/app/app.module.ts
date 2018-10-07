import {BrowserModule} from '@angular/platform-browser';
import {LOCALE_ID, NgModule} from '@angular/core';
import {ReactiveFormsModule} from '@angular/forms';
import {AppComponent} from './app.component';
import {AppRoutingModule} from './/app-routing.module';
import {DashboardComponent} from './dashboard/dashboard.component';
import {SwitchLocalComponent} from './switch-local/switch-local.component';
import {MemberListComponent} from './member-list/member-list.component';
import {MemberViewComponent} from './member-view/member-view.component';
import {ApiModule} from './api/api.module';
import {RoomListComponent} from './room-list/room-list.component';
import {RoomDetailsComponent} from './room-details/room-details.component';
import {RoomEditComponent} from './room-edit/room-edit.component';
import {RoomNewComponent} from './room-new/room-new.component';
import {PortListComponent} from './port-list/port-list.component';
import {PortDetailsComponent} from './port-details/port-details.component';
import {PortEditComponent} from './port-edit/port-edit.component';
import {PortNewComponent} from './port-new/port-new.component';
import {SwitchListComponent} from './switch-list/switch-list.component';
import {SwitchDetailsComponent} from './switch-details/switch-details.component';
import {SwitchEditComponent} from './switch-edit/switch-edit.component';
import {SwitchNewComponent} from './switch-new/switch-new.component';
import {DeviceListComponent} from './device-list/device-list.component';
import {MemberCreateOrEditComponent} from './member-create-or-edit/member-create-or-edit.component';
import {MacVendorComponent} from './mac-vendor/mac-vendor.component';
import {GlobalSearchComponent} from './global-search/global-search.component';
import {NavbarComponent} from './navbar/navbar.component';
import {NotificationAnimationType, SimpleNotificationsModule} from 'angular2-notifications';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {OAuthModule} from 'angular-oauth2-oidc';
import {LoginComponent} from './login/login.component';
import {NgxPaginationModule} from 'ngx-pagination';
import {HTTP_INTERCEPTORS} from '@angular/common/http';
import {AuthInterceptor} from './http-interceptor/auth-interceptor';
import {NotifInterceptor} from './http-interceptor/notif-interceptor';
import { MemberPasswordEditComponent } from './member-password-edit/member-password-edit.component';


@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    SwitchLocalComponent,
    MemberListComponent,
    MemberViewComponent,
    RoomListComponent,
    RoomDetailsComponent,
    RoomEditComponent,
    RoomNewComponent,
    PortListComponent,
    PortDetailsComponent,
    PortEditComponent,
    PortNewComponent,
    SwitchListComponent,
    SwitchDetailsComponent,
    SwitchEditComponent,
    SwitchNewComponent,
    DeviceListComponent,
    MemberCreateOrEditComponent,
    MemberCreateOrEditComponent,
    MacVendorComponent,
    GlobalSearchComponent,
    NavbarComponent,
    LoginComponent,
    MemberPasswordEditComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ApiModule,
    ReactiveFormsModule,
    SimpleNotificationsModule.forRoot({
      timeOut: 3000,
      clickToClose: false,
      clickIconToClose: true,
      animate: NotificationAnimationType.Fade,
      showProgressBar: false,
    }),
    BrowserAnimationsModule,
    OAuthModule.forRoot(),
    NgxPaginationModule,
  ],
  providers: [
    AppComponent,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: NotifInterceptor,
      multi: true
    },
    {provide: LOCALE_ID, useValue: 'en-US'},
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
