import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule }   from '@angular/forms';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './/app-routing.module';
import { DashboardComponent } from './dashboard/dashboard.component';
import { SwitchLocalComponent } from './switch-local/switch-local.component';

import { MemberListComponent } from './member-list/member-list.component';
import { MemberDetailsComponent } from './member-details/member-details.component';

import { PatchingComponent } from './patching/patching.component';

import { ApiModule } from './api/api.module';
import { RoomListComponent } from './room-list/room-list.component';
import { RoomDetailsComponent } from './room-details/room-details.component';
import { RoomNewComponent } from './room-new/room-new.component';
import { PortListComponent } from './port-list/port-list.component';
import { PortDetailsComponent } from './port-details/port-details.component';
import { SwitchListComponent } from './switch-list/switch-list.component';
import { SwitchDetailsComponent } from './switch-details/switch-details.component';
import { DeviceListComponent } from './device-list/device-list.component';
import { DeviceDetailsComponent } from './device-details/device-details.component';
import { MemberFormComponent } from './member-form/member-form.component';
import { DeviceNewComponent } from './device-new/device-new.component';
import { DeviceEditComponent } from './device-edit/device-edit.component';
import { MemberEditComponent } from './member-edit/member-edit.component';
import { MacVendorComponent } from './mac-vendor/mac-vendor.component';
import { GlobalSearchComponent } from './global-search/global-search.component';
import { NavbarComponent } from './navbar/navbar.component';
import { SimpleNotificationsModule } from 'angular2-notifications';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';

@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    SwitchLocalComponent,
    MemberListComponent,
    MemberDetailsComponent,
    PatchingComponent,
    RoomListComponent,
    RoomDetailsComponent,
    RoomNewComponent,
    PortListComponent,
    PortDetailsComponent,
    SwitchListComponent,
    SwitchDetailsComponent,
    DeviceListComponent,
    DeviceDetailsComponent,
    MemberFormComponent,
    MemberEditComponent,
    DeviceNewComponent,
    DeviceEditComponent,
    MemberEditComponent,
    DeviceEditComponent,
    MacVendorComponent,
    GlobalSearchComponent,
    NavbarComponent,
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
      animate: "fade",
      showProgressBar: false,
    
    }),
    BrowserAnimationsModule,
  ],
  providers: [ AppComponent ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }
