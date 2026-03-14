import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DarkModeService {
  private darkModeSubject = new BehaviorSubject<boolean>(this.getInitialMode());
  isDarkMode$ = this.darkModeSubject.asObservable();

  private getInitialMode(): boolean {
    return localStorage.getItem('darkMode') === 'true';
  }

  get currentMode(): boolean {
    return this.darkModeSubject.value;
  }

  toggle() {
    const newValue = !this.darkModeSubject.value;
    this.darkModeSubject.next(newValue);
    localStorage.setItem('darkMode', String(newValue));
  }
}
