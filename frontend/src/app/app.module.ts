import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { HttpClientModule } from '@angular/common/http';

import { ImageEntityApiService } from './imageEntity/imageEntity-api.service';
import { ImageDisplayComponent } from './image-display/image-display.component';

@NgModule({
  declarations: [
    AppComponent,
    ImageDisplayComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [
    ImageEntityApiService
  ],
  bootstrap: [
    AppComponent
  ]
})
export class AppModule { }
