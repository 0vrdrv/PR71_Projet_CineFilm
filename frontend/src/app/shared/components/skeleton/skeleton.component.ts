import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-skeleton',
  template: `
    <div class="animate-pulse">
      <div *ngIf="type === 'card'" class="bg-surface-200 dark:bg-surface-800 aspect-[2/3] rounded-xl"></div>
      <div *ngIf="type === 'text'" class="h-4 bg-surface-200 dark:bg-surface-800 rounded w-3/4 mb-2"></div>
      <div *ngIf="type === 'title'" class="h-8 bg-surface-200 dark:bg-surface-800 rounded w-1/2 mb-4"></div>
      <div *ngIf="type === 'avatar'" class="w-16 h-16 bg-surface-200 dark:bg-surface-800 rounded-full"></div>
    </div>
  `,
  styles: [`
    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.5; }
    }
    .animate-pulse { animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }
  `]
})
export class SkeletonComponent {
  @Input() type: 'card' | 'text' | 'title' | 'avatar' = 'text';
}
