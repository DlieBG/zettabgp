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
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MessageReplayComponent } from './components/anomaly-explorer/message-replay/message-replay.component';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    MrtLibraryComponent,
    AnomalyExplorerComponent,
    MrtScenarioComponent,
    RabbitmqComponent,
    MessageReplayComponent
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
    MatProgressBarModule,
    MatCheckboxModule,
    MatFormFieldModule,
    MatInputModule,
  ],
  providers: [
    provideAnimationsAsync(),
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
