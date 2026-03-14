import { Component } from '@angular/core';

@Component({
  selector: 'app-not-found',
  template: `
    <div class="text-center py-32">
      <h1 class="text-9xl font-black text-surface-200 dark:text-surface-800 mb-4">404</h1>
      <h2 class="text-2xl font-bold text-surface-900 dark:text-white mb-4">Page not found</h2>
      <p class="text-surface-500 mb-8 max-w-md mx-auto">You may have mistyped the address or the page may have moved.</p>
      <a routerLink="/"
        class="btn-primary !rounded-full inline-block cursor-pointer">
        Back to Home
      </a>
    </div>
  `,
  styleUrls: ['./not-found.component.scss']
})
export class NotFoundComponent {}
