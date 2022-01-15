import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { HttpClientModule } from '@angular/common/http';

import { ImageEntityApiService } from './imageEntity/imageEntity-api.service';
import { ImageDisplayComponent } from './image-display/image-display.component';
import { NgxSliderModule } from '@angular-slider/ngx-slider';
import { MatIconModule} from '@angular/material/icon'

import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    AppComponent,
    ImageDisplayComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    NgxSliderModule,
    FormsModule,
    MatIconModule
  ],
  providers: [
    ImageEntityApiService
  ],
  bootstrap: [
    AppComponent
  ]
})
export class AppModule { }
