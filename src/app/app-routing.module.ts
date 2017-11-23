import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { DashboardComponent } from './dashboard/dashboard.component';
import { MembersComponent } from './members/members.component';
import { RoomsComponent } from './rooms/rooms.component';
import { PortsComponent } from './ports/ports.component';
import { PatchingComponent } from './patching/patching.component';
import { SwitchLocalComponent } from './switch-local/switch-local.component';

const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { 
    path: 'members', 
    component: MembersComponent,
/*
    children: [
      { path: '', redirectTo: 'list' },
      { path: 'list', component: MembersListComponent },
      { path: 'edit/:memberId', component: MembersListComponent },
      { path: 'show/:memberId', component: MembersShowComponent },
      { path: 'add/', component: MembersAddComponent },
    ]
*/
  },
  { path: 'rooms', component: RoomsComponent },
  { path: 'ports', component: PortsComponent },
  { path: 'patching', component: PatchingComponent },
  { path: 'switch_local', component: SwitchLocalComponent },

];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule { }
