import { Directive, ElementRef, HostListener, Input } from '@angular/core';

@Directive({
  selector: 'img[appBrokenImg]',
})
export class BrokenImgDirective {
  @Input() appBrokenImg: string = '/frontend/src/assets/placeholder.png';
  constructor(private el: ElementRef) {}

  @HostListener('error') onError() {
    this.el.nativeElement.src = this.appBrokenImg;
    this.el.nativeElement.classList.add('image-missing');
  }
}
