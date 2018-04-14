import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { DashboardComponent } from './dashboard/dashboard.component';
import { MemberListComponent } from './member-list/member-list.component';
import { MemberFormComponent } from './member-form/member-form.component';
import { MemberEditComponent } from './member-edit/member-edit.component';
import { MemberDetailsComponent } from './member-details/member-details.component';
import { RoomListComponent } from './room-list/room-list.component';
import { RoomDetailsComponent } from './room-details/room-details.component';
import { RoomNewComponent } from './room-new/room-new.component';
import { PortListComponent } from './port-list/port-list.component';
import { PortDetailsComponent } from './port-details/port-details.component';
import { PatchingComponent } from './patching/patching.component';
import { SwitchLocalComponent } from './switch-local/switch-local.component';
import { SwitchListComponent } from './switch-list/switch-list.component';
import { SwitchDetailsComponent } from './switch-details/switch-details.component';
import { DeviceListComponent } from './device-list/device-list.component';
import { DeviceNewComponent } from './device-new/device-new.component';
import { DeviceDetailsComponent } from './device-details/device-details.component';
import { DeviceEditComponent } from './device-edit/device-edit.component';

const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { 
    path: 'member', 
    children: [
      { path: 'search', component: MemberListComponent },
      { path: 'view/:username', component: MemberDetailsComponent },
      { path: 'edit/:username', component: MemberEditComponent },
      { path: 'add', component: MemberFormComponent },
      { path: 'view/:username/newdevice', component: DeviceNewComponent },
      { path: 'view/:username/editdevice/:mac', component: DeviceEditComponent },
      { path: 'edit/:username', component: MemberEditComponent },
    ]
  },
  { path: 'room', component: RoomListComponent },
  { path: 'room/:roomNumber', component: RoomDetailsComponent },
  { path: 'add', component: RoomNewComponent },
  { path: 'port', component: PortListComponent },
  { 
    path: 'device', 
    children: [
      { path: 'search', component: DeviceListComponent },
      { path: 'add', component: DeviceNewComponent },
      { path: 'view/:mac', component: DeviceDetailsComponent },
      { path: 'edit/:mac', component: DeviceEditComponent },
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
