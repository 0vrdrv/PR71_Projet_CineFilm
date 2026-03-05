import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'duration'
})
export class DurationPipe implements PipeTransform {
  transform(value: number | undefined): string {
    if (!value) return 'N/A';
    
    const hours = Math.floor(value / 60);
    const minutes = value % 60;
    
    if (hours === 0) return `${minutes}min`;
    return `${hours}h ${minutes}min`;
  }
}