import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { NavBarComponent } from './nav-bar/nav-bar.component';
import { PlatformComponent } from './platform/platform.component';
import { RankingTypeComponent } from './ranking-type/ranking-type.component';
import { RankingContentComponent } from './ranking-content/ranking-content.component';
import { FooterComponent } from './footer/footer.component';
import { AppRoutingModule } from './app-routing.module';
import { MainComponent } from './main/main.component';
import { EntityHistoryComponent } from './entity-history/entity-history.component';

@NgModule({
  declarations: [
    AppComponent,
    NavBarComponent,
    PlatformComponent,
    RankingTypeComponent,
    RankingContentComponent,
    FooterComponent,
    MainComponent,
    EntityHistoryComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
