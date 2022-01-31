import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { MainComponent } from './main/main.component';
import { EntityHistoryComponent } from './entity-history/entity-history.component';
import { PlatformComponent } from './platform/platform.component';

const routes: Routes = [
  { path: '', redirectTo: '/rankings', pathMatch: 'full' },
  { path: 'rankings', component: MainComponent },
  { path: 'history/:platform/:entity', component: EntityHistoryComponent },
  // { path: 'rankings/:platform', component: PlatformComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
