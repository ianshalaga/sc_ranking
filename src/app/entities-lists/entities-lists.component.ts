import { Component, OnInit } from '@angular/core';

import { RankingsService } from '../rankings.service';
import { EntitiesCount } from '../player-data';

@Component({
  selector: 'app-entities-lists',
  templateUrl: './entities-lists.component.html',
  styleUrls: ['./entities-lists.component.css']
})
export class EntitiesListsComponent implements OnInit {

  PlChList!: string[];
  PlList!: string[];
  ChList!: string[];
  EntitiesCounts!: EntitiesCount;

  constructor(private rankingService: RankingsService) { }

  ngOnInit(): void {
    this.getPlChList()
    this.getPlList()
    this.getChList()

    this.getEntitiesCount()
  }

  getPlChList(): void { this.rankingService.getPlChList().subscribe((entity) => this.PlChList = entity) }
  getPlList(): void { this.rankingService.getPlList().subscribe((entity) => this.PlList = entity) }
  getChList(): void { this.rankingService.getChList().subscribe((entity) => this.ChList = entity) }


  getEntitiesCount(): void {
    this.rankingService.getEntitiesCount().subscribe((count) => this.EntitiesCounts = count)
  }
}
