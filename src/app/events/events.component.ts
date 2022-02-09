import { Component, OnInit } from '@angular/core';

import { EventStats } from '../player-data';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

import event_stats from "src/assets/data/event_stats.json"

@Component({
  selector: 'app-events',
  templateUrl: './events.component.html',
  styleUrls: ['./events.component.css']
})
export class EventsComponent implements OnInit {

  EventStats: EventStats[] = event_stats
  iframeURLs: SafeResourceUrl[] = []

  constructor(private sanitizer: DomSanitizer) {
    for (let i = 0; i < this.EventStats.length; i++) {
      this.iframeURLs.push(this.sanitizer.bypassSecurityTrustResourceUrl(this.EventStats[i].playlist)) 
    }
  }

  ngOnInit(): void {
  }
}
