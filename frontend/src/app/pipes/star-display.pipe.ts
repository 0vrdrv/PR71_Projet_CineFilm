import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'starDisplay' })
export class StarDisplayPipe implements PipeTransform {
  transform(rating: number): string {
    const full = Math.floor(rating);
    const half = rating % 1 >= 0.5 ? '½' : '';
    return '★'.repeat(full) + half;
  }
}