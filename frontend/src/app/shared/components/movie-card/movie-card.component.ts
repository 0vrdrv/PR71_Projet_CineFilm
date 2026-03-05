import { Component, Input } from '@angular/core';
import { Movie } from '../../../models/movie.model'; // Ton modèle typé !

@Component({
  selector: 'app-movie-card',
  template: `
    <div 
      [routerLink]="['/films', movie.id]" 
      class="bg-figma-gray-card aspect-[2/3] rounded-xl shadow-sm overflow-hidden relative cursor-pointer hover:scale-105 transition-transform duration-300 group"
    >
      <img 
        *ngIf="movie.poster_path" 
        [src]="'https://image.tmdb.org/t/p/w500' + movie.poster_path" 
        [alt]="movie.title" 
        appBrokenImg
        class="w-full h-full object-cover"
      >
      
      <div *ngIf="!movie.poster_path" class="w-full h-full flex items-center justify-center bg-gray-700 text-center p-2">
          <span class="text-xs text-gray-400 font-bold">{{ movie.title }}</span>
      </div>

      <div class="absolute inset-0 bg-black/70 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col items-center justify-center p-4">
        <span class="text-white font-bold text-sm text-center mb-2">{{ movie.title }}</span>
        <span class="bg-figma-yellow text-black text-xs font-bold px-2 py-1 rounded">⭐ {{ movie.vote_average | number:'1.1-1' }}</span>
      </div>
    </div>
  `
})
export class MovieCardComponent {
  @Input() movie!: Movie; // Le composant attend un film en entrée
}