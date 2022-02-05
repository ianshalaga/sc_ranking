import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { MainComponent } from './main/main.component';
import { EntityStatsComponent } from './entity-stats/entity-stats.component';
import { EntitiesListsComponent } from './entities-lists/entities-lists.component';

const routes: Routes = [
  { path: '', redirectTo: '/rankings', pathMatch: 'full' },
  { path: 'rankings', component: MainComponent },
  { path: 'stats', component: EntitiesListsComponent },
  { path: 'stats/:entity', component: EntityStatsComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
