import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { DashboardComponent } from './dashboard/dashboard.component';
import { MemberListComponent } from './member-list/member-list.component';
import { MemberFormComponent } from './member-form/member-form.component';
import { MemberEditComponent } from './member-edit/member-edit.component';
import { MemberDetailsComponent } from './member-details/member-details.component';
import { RoomListComponent } from './room-list/room-list.component';
import { RoomDetailsComponent } from './room-details/room-details.component';
import { PortListComponent } from './port-list/port-list.component';
import { PortDetailsComponent } from './port-details/port-details.component';
import { PatchingComponent } from './patching/patching.component';
import { SwitchLocalComponent } from './switch-local/switch-local.component';
import { SwitchListComponent } from './switch-list/switch-list.component';
import { SwitchDetailsComponent } from './switch-details/switch-details.component';
import { DeviceListComponent } from './device-list/device-list.component';
import { DeviceFormComponent } from './device-form/device-form.component';
import { DeviceDetailsComponent } from './device-details/device-details.component';

const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { 
    path: 'member', 
    children: [
      { path: 'search', component: MemberListComponent },
      { path: 'view/:username', component: MemberDetailsComponent },
      { path: 'add', component: MemberFormComponent },
      { path: 'view/:username/newdevice', component: DeviceFormComponent },
      { path: 'edit/:username', component: MemberEditComponent },
    ]
  },
  { path: 'room', component: RoomListComponent },
  { path: 'room/:roomNumber', component: RoomDetailsComponent },
  { path: 'port', component: PortListComponent },
  { 
    path: 'device', 
    children: [
      { path: 'search', component: DeviceListComponent },
      { path: ':mac', component: DeviceDetailsComponent },
    ],
  },
  { path: 'patching', component: PatchingComponent },
  { path: 'switch_local', component: SwitchLocalComponent },
  { path: 'switch', component: SwitchListComponent },
  { 
    path: 'switch/:switchID',
    children: [
      { path: 'port/:portID', component: PortDetailsComponent },
      { path: '', component: SwitchDetailsComponent },
    ],
  }

];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule { }
