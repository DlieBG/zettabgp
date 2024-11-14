import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { HomeComponent } from './components/home/home.component';
import { MatTabsModule } from '@angular/material/tabs';
import { MrtLibraryComponent } from './components/mrt-library/mrt-library.component';
import { AnomalyExplorerComponent } from './components/anomaly-explorer/anomaly-explorer.component';
import { MrtScenarioComponent } from './components/mrt-library/mrt-scenario/mrt-scenario.component';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatCardModule } from '@angular/material/card';
import { RabbitmqComponent } from './components/rabbitmq/rabbitmq.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    MrtLibraryComponent,
    AnomalyExplorerComponent,
    MrtScenarioComponent,
    RabbitmqComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    MatToolbarModule,
    MatIconModule,
    MatButtonModule,
    MatTabsModule,
    MatProgressSpinnerModule,
    MatCardModule,
  ],
  providers: [
    provideAnimationsAsync(),
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
