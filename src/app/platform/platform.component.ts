import { Component, OnInit, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-platform',
  templateUrl: './platform.component.html',
  styleUrls: ['./platform.component.css']
})
export class PlatformComponent implements OnInit {

  @Output() selectedPlatform = new EventEmitter<string>();

  constructor() { }

  ngOnInit(): void {
  }

  sendPlatform(platformType: string) {
    this.selectedPlatform.emit(platformType)
  }

}
