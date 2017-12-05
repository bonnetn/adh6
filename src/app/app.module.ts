import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';


import { AppComponent } from './app.component';
import { AppRoutingModule } from './/app-routing.module';
import { DashboardComponent } from './dashboard/dashboard.component';
import { SwitchLocalComponent } from './switch-local/switch-local.component';

import { MemberListComponent } from './member-list/member-list.component';
import { MemberDetailsComponent } from './member-details/member-details.component';

import { RoomsComponent } from './rooms/rooms.component';
import { PortsComponent } from './ports/ports.component';
import { PatchingComponent } from './patching/patching.component';

import { ApiModule } from './api/api.module';

@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    SwitchLocalComponent,
    MemberListComponent,
    MemberDetailsComponent,
    RoomsComponent,
    PortsComponent,
    PatchingComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ApiModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
