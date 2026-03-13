import { Component, OnInit } from '@angular/core';
import { NotificationService, Toast } from '../../../services/notification.service';

@Component({
  selector: 'app-toast',
  template: `
    <div class="fixed bottom-6 right-6 z-[9999] flex flex-col gap-3">
      <div *ngFor="let toast of toasts"
        class="px-6 py-4 rounded-xl shadow-2xl text-sm font-bold tracking-wide animate-slide-in min-w-[280px] flex items-center justify-between"
        [ngClass]="{
          'bg-green-500 text-white': toast.type === 'success',
          'bg-red-500 text-white': toast.type === 'error',
          'bg-blue-500 text-white': toast.type === 'info',
          'bg-yellow-400 text-black': toast.type === 'warning'
        }">
        <span>{{ toast.message }}</span>
        <button (click)="dismiss(toast.id)" class="ml-4 opacity-70 hover:opacity-100 text-lg">&times;</button>
      </div>
    </div>
  `,
  styles: [`
    @keyframes slideIn {
      from { transform: translateX(100%); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }
    .animate-slide-in {
      animation: slideIn 0.3s ease-out;
    }
  `]
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