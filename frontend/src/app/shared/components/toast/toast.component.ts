import { Component, OnInit } from '@angular/core';
import { trigger, transition, style, animate } from '@angular/animations';
import { NotificationService, Toast } from '../../../services/notification.service';

@Component({
  selector: 'app-toast',
  template: `
    <div class="fixed bottom-6 right-6 z-[9999] flex flex-col gap-3">
      <div *ngFor="let toast of toasts" @toastAnimation
        class="px-6 py-4 rounded-xl shadow-xl text-sm font-semibold tracking-wide min-w-[280px] flex items-center justify-between toast-enter"
        [ngClass]="{
          'bg-accent-green text-white': toast.type === 'success',
          'bg-accent-red text-white': toast.type === 'error',
          'bg-accent-blue text-white': toast.type === 'info',
          'bg-brand-500 text-surface-900': toast.type === 'warning'
        }">
        <span>{{ toast.message }}</span>
        <button (click)="dismiss(toast.id)" class="ml-4 opacity-70 hover:opacity-100 text-lg">&times;</button>
      </div>
    </div>
  `,
  animations: [
    trigger('toastAnimation', [
      transition(':enter', [
        style({ transform: 'translateX(100%)', opacity: 0 }),
        animate('300ms ease-out', style({ transform: 'translateX(0)', opacity: 1 }))
      ]),
      transition(':leave', [
        animate('200ms ease-in', style({ transform: 'translateX(100%)', opacity: 0 }))
      ])
    ])
  ]
})
export class ToastComponent implements OnInit {
  toasts: Toast[] = [];

  constructor(private notificationService: NotificationService) {}

  ngOnInit() {
    this.notificationService.toasts$.subscribe(toasts => this.toasts = toasts);
  }

  dismiss(id: number) {
    this.notificationService.removeToast(id);
  }
}
