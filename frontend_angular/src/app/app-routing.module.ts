import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';

import {DashboardComponent} from './dashboard/dashboard.component';
import {MemberListComponent} from './member-list/member-list.component';
import {MemberCreateOrEditComponent} from './member-create-or-edit/member-create-or-edit.component';
import {MemberViewComponent} from './member-view/member-view.component';
import {RoomListComponent} from './room-list/room-list.component';
import {RoomDetailsComponent} from './room-details/room-details.component';
import {RoomEditComponent} from './room-edit/room-edit.component';
import {RoomNewComponent} from './room-new/room-new.component';
import {PortListComponent} from './port-list/port-list.component';
import {PortDetailsComponent} from './port-details/port-details.component';
import {PortNewComponent} from './port-new/port-new.component';
import {SwitchLocalComponent} from './switch-local/switch-local.component';
import {SwitchListComponent} from './switch-list/switch-list.component';
import {SwitchDetailsComponent} from './switch-details/switch-details.component';
import {SwitchEditComponent} from './switch-edit/switch-edit.component';
import {SwitchNewComponent} from './switch-new/switch-new.component';
import {DeviceListComponent} from './device-list/device-list.component';
import {MemberPasswordEditComponent} from './member-password-edit/member-password-edit.component';
import {CreateTemporaryAccountComponent} from './create-temporary-account/create-temporary-account.component';
import {TreasuryComponent} from "./treasury/treasury.component";
import {AccountCreateComponent} from "./account-create/account-create.component";

const routes: Routes = [
  {path: '', redirectTo: '/dashboard', pathMatch: 'full'},
  {path: 'dashboard', component: DashboardComponent},
  {
    path: 'member',
    children: [
      {path: 'search', component: MemberListComponent},
      {path: 'add', component: MemberCreateOrEditComponent},
      {path: 'view/:username', component: MemberViewComponent},
      {path: 'edit/:username', component: MemberCreateOrEditComponent},
      {path: 'password/:username', component: MemberPasswordEditComponent},
    ],
  },
  {
    path: 'room',
    children: [
      {path: '', redirectTo: 'search', pathMatch: 'full'},
      {path: 'search', component: RoomListComponent},
      {path: 'add', component: RoomNewComponent},
      {path: 'view/:roomNumber', component: RoomDetailsComponent},
      {path: 'edit/:roomNumber', component: RoomEditComponent},
    ],
  },
  {
    path: 'device',
    children: [
      {path: '', redirectTo: 'search', pathMatch: 'full'},
      {path: 'search', component: DeviceListComponent},
    ],
  },
  {path: 'switch_local', component: SwitchLocalComponent},
  {
    path: 'switch',
    children: [
      {path: '', redirectTo: 'search', pathMatch: 'full'},
      {path: 'search', component: SwitchListComponent},
      {path: 'view/:switchID', component: SwitchDetailsComponent},
      {path: 'edit/:switchID', component: SwitchEditComponent},
      {path: 'add', component: SwitchNewComponent},
      {path: 'view/:switchID/port/:portID', component: PortDetailsComponent},
      {path: 'add/:switchID/port', component: PortNewComponent},
    ],
  },
  {
    path: 'port',
    children: [
      {path: '', redirectTo: 'search', pathMatch: 'full'},
      {path: 'search', component: PortListComponent},
    ],
  },
  {
    path: 'naina',
    component: CreateTemporaryAccountComponent,
  },
  {
    path: 'treasury',
    children: [
    {path:'', component: TreasuryComponent},
    ]
  },
  {
    path: 'account',
    children: [
    {path: 'add', component: AccountCreateComponent},
    ]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
