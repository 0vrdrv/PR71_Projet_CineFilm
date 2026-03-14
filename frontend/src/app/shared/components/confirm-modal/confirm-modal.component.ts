import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-confirm-modal',
  template: `
    <div *ngIf="isOpen" class="fixed inset-0 z-[9999] flex items-center justify-center">
      <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" (click)="onCancel()"></div>
      <div class="relative card max-w-md w-full mx-4 z-10 p-8 !shadow-xl">
        <h3 class="text-xl font-bold text-surface-900 dark:text-white mb-2">{{ title }}</h3>
        <p class="text-surface-500 mb-8">{{ message }}</p>
        <div class="flex gap-4">
          <button (click)="onConfirm()"
            class="flex-1 bg-accent-red hover:bg-red-700 text-white font-bold text-xs tracking-widest uppercase py-3 rounded-xl transition-colors">
            {{ confirmText }}
          </button>
          <button (click)="onCancel()"
            class="flex-1 btn-secondary">
            Cancel
          </button>
        </div>
      </div>
    </div>
  `
})
export class ConfirmModalComponent {
  @Input() isOpen: boolean = false;
  @Input() title: string = 'Confirm';
  @Input() message: string = 'Are you sure?';
  @Input() confirmText: string = 'Delete';
  @Output() confirmed = new EventEmitter<void>();
  @Output() cancelled = new EventEmitter<void>();

  onConfirm() {
    this.confirmed.emit();
  }

  onCancel() {
    this.cancelled.emit();
  }
}
