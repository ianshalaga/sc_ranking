import { Component, OnInit } from '@angular/core';

import { PlayerStats, BattleData } from '../player-data';
import { ActivatedRoute } from '@angular/router';
// import { Location } from '@angular/common';
import { RankingsService } from '../rankings.service';

@Component({
  selector: 'app-entity-stats',
  templateUrl: './entity-stats.component.html',
  styleUrls: ['./entity-stats.component.css']
})
export class EntityStatsComponent implements OnInit {

  entity!: string

  PlayerStatsPC!: PlayerStats[]
  PlayerStatsPS4!: PlayerStats[]
  PlayerStatsPcPs4!: PlayerStats[]

  BattlesListPC!: BattleData[];
  BattlesListPS4!: BattleData[];
  BattlesListPcPs4!: BattleData[];

  constructor(
    private route: ActivatedRoute,
    private rankingsService: RankingsService,
    // private location: Location
  ) {}

  ngOnInit(): void {
    this.getPlayerStatsPC()
    this.getPlayerStatsPS4()
    this.getPlayerStatsPcPs4()
    this.getBattlesHistoryPC()
    this.getBattlesHistoryPS4()
    this.getBattlesHistoryPcPs4()
  }

  getPlayerStatsPC(): void {
    this.entity = this.route.snapshot.paramMap.get('entity')!
    this.rankingsService.getPlayerStatsPC(this.entity).subscribe(ent => this.PlayerStatsPC = ent);
  }

  getPlayerStatsPS4(): void {
    this.entity = this.route.snapshot.paramMap.get('entity')!
    this.rankingsService.getPlayerStatsPS4(this.entity).subscribe(ent => this.PlayerStatsPS4 = ent);
  }

  getPlayerStatsPcPs4(): void {
    this.entity = this.route.snapshot.paramMap.get('entity')!
    this.rankingsService.getPlayerStatsPcPs4(this.entity).subscribe(ent => this.PlayerStatsPcPs4 = ent);
  }

  getBattlesHistoryPC(): void {
    this.entity = this.route.snapshot.paramMap.get('entity')!
    this.rankingsService.getBattlesHistoryPC(this.entity).subscribe(ent => this.BattlesListPC = ent);
  }

  getBattlesHistoryPS4(): void {
    this.entity = this.route.snapshot.paramMap.get('entity')!
    this.rankingsService.getBattlesHistoryPS4(this.entity).subscribe(ent => this.BattlesListPS4 = ent);
  }

  getBattlesHistoryPcPs4(): void {
    this.entity = this.route.snapshot.paramMap.get('entity')!
    this.rankingsService.getBattlesHistoryPcPs4(this.entity).subscribe(ent => this.BattlesListPcPs4 = ent);
  }

  max(num1: number, num2: number): number {
    return Math.max(num1, num2)
  }

  getUpdateClick(entity: string): void {
    this.entity = entity
    this.rankingsService.getPlayerStatsPC(this.entity).subscribe(ent => this.PlayerStatsPC = ent);
    this.rankingsService.getPlayerStatsPS4(this.entity).subscribe(ent => this.PlayerStatsPS4 = ent);
    this.rankingsService.getPlayerStatsPcPs4(this.entity).subscribe(ent => this.PlayerStatsPcPs4 = ent);
    this.rankingsService.getBattlesHistoryPC(this.entity).subscribe(ent => this.BattlesListPC = ent);
    this.rankingsService.getBattlesHistoryPS4(this.entity).subscribe(ent => this.BattlesListPS4 = ent);
    this.rankingsService.getBattlesHistoryPcPs4(this.entity).subscribe(ent => this.BattlesListPcPs4 = ent);
  }
  
}
