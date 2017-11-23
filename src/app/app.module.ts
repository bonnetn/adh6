import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';


import { AppComponent } from './app.component';
import { AppRoutingModule } from './/app-routing.module';
import { DashboardComponent } from './dashboard/dashboard.component';
import { SwitchLocalComponent } from './switch-local/switch-local.component';
import { MembersComponent } from './members/members.component';
import { RoomsComponent } from './rooms/rooms.component';
import { PortsComponent } from './ports/ports.component';
import { PatchingComponent } from './patching/patching.component';
import { MemberService } from './member.service';


@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    SwitchLocalComponent,
    MembersComponent,
    RoomsComponent,
    PortsComponent,
    PatchingComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [MemberService],
  bootstrap: [AppComponent]
})
export class AppModule { }
