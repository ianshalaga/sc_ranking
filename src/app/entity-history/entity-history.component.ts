import { Component, OnInit } from '@angular/core';

import { BattleData } from '../player-data';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { RankingsService } from '../rankings.service';

@Component({
  selector: 'app-entity-history',
  templateUrl: './entity-history.component.html',
  styleUrls: ['./entity-history.component.css']
})
export class EntityHistoryComponent implements OnInit {

  battle!: BattleData[];
  platform!: string
  entity!: string

  constructor(
    private route: ActivatedRoute,
    private rankingsService: RankingsService,
    private location: Location
  ) {}

  ngOnInit(): void {
    this.getEntity();
  }

  getEntity(): void {
    this.platform = this.route.snapshot.paramMap.get('platform')!
    this.entity = this.route.snapshot.paramMap.get('entity')!
    this.rankingsService.getEntity(this.platform, this.entity).subscribe(ent => this.battle = ent);
  }

  getEntityClick(platform: string, entity: string): void {
    this.platform = platform
    this.entity = entity
    this.rankingsService.getEntity(this.platform, this.entity).subscribe(ent => this.battle = ent);
  }

  textPlatform(): string {
    let pltf!: string
    if (this.platform == 'PC')
      pltf = 'PC'
    if (this.platform == 'PS4')
      pltf = 'PS4'
    if (this.platform == 'PC_PS4')
      pltf = 'PC + PS4'
    return pltf
  }

  goBack(): void {
    this.location.back();
  }

}
