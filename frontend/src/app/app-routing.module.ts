import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ImageDisplayComponent } from './image-display/image-display.component';

const routes: Routes = [
  { path: '**', component: ImageDisplayComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
