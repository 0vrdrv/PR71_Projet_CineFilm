import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { DurationPipe } from './pipes/duration.pipe';
import { BrokenImgDirective } from './directives/broken-img.directive';
import { MovieCardComponent } from './components/movie-card/movie-card.component';

@NgModule({
  declarations: [
    DurationPipe,
    BrokenImgDirective,
    MovieCardComponent
  ],
  imports: [
    CommonModule,
    RouterModule 
  ],
  exports: [
    DurationPipe,
    BrokenImgDirective,
    MovieCardComponent,
    CommonModule
  ]
})
export class SharedModule { }