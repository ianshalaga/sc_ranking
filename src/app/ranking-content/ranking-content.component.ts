import { Component, OnInit, Input } from '@angular/core';
import { PlayerData } from 'src/app/player-data';

@Component({
  selector: 'app-ranking-content',
  templateUrl: './ranking-content.component.html',
  styleUrls: ['./ranking-content.component.css']
})
export class RankingContentComponent implements OnInit {

  @Input() rankingList!: PlayerData[]
  @Input() platform!: string

  constructor() { }

  ngOnInit(): void {
  }

}
