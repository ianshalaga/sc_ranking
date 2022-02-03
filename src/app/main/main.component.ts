import { Component, OnInit } from '@angular/core';

import { PlayerData } from 'src/app/player-data'
import { RankingsService } from '../rankings.service';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {

  // PC
  rankingList_pl_ch_pc!: PlayerData[]
  rankingList_pl_pc!: PlayerData[]
  rankingList_ch_pc!: PlayerData[]

  // PS4
  rankingList_pl_ch_ps4!: PlayerData[]
  rankingList_pl_ps4!: PlayerData[]
  rankingList_ch_ps4!: PlayerData[]

  // PC_PS4
  rankingList_pl_ch_union!: PlayerData[]
  rankingList_pl_union!: PlayerData[]
  rankingList_ch_union!: PlayerData[]

  platform: string = ""
  rankingType: string = ""

  constructor(private rankingService: RankingsService) { }

  ngOnInit(): void {
    this.getPcPlCh();
    this.getPcPl();
    this.getPcCh();
    this.getPs4PlCh();
    this.getPs4Pl();
    this.getPs4Ch();
    this.getUnionPlCh();
    this.getUnionPl();
    this.getUnionCh();
  }

  getPcPlCh(): void {this.rankingService.getPcPlCh().subscribe(ranking => this.rankingList_pl_ch_pc = ranking)}
  getPcPl(): void {this.rankingService.getPcPl().subscribe(ranking => this.rankingList_pl_pc = ranking)}
  getPcCh(): void {this.rankingService.getPcCh().subscribe(ranking => this.rankingList_ch_pc = ranking)}
  getPs4PlCh(): void {this.rankingService.getPs4PlCh().subscribe(ranking => this.rankingList_pl_ch_ps4 = ranking)}
  getPs4Pl(): void {this.rankingService.getPs4Pl().subscribe(ranking => this.rankingList_pl_ps4 = ranking)}
  getPs4Ch(): void {this.rankingService.getPs4Ch().subscribe(ranking => this.rankingList_ch_ps4 = ranking)}
  getUnionPlCh(): void {this.rankingService.getUnionPlCh().subscribe(ranking => this.rankingList_pl_ch_union = ranking)}
  getUnionPl(): void {this.rankingService.getUnionPl().subscribe(ranking => this.rankingList_pl_union = ranking)}
  getUnionCh(): void {this.rankingService.getUnionCh().subscribe(ranking => this.rankingList_ch_union = ranking)}

  recievePlatform($platform: string) {
    this.platform = $platform
    // console.log(this.platform)
  }

  recieveRanking($ranking: string) {
    this.rankingType = $ranking
  }

  setButtonStyle(pltf: string): string {
    var Style: string = "btn btn-union btn-sm m-1"
    if (pltf == "PC")
      Style = "btn btn-pc btn-sm m-1"
    if (pltf == "PS4")
      Style = "btn btn-ps4 btn-sm m-1"
    return Style
  }

  setRankingContent(): PlayerData[] {
    var rankingList!: PlayerData[]
    if (this.platform == "PC" && this.rankingType == "PL_CH")
      rankingList = this.rankingList_pl_ch_pc
    if (this.platform == "PC" && this.rankingType == "PL")
      rankingList = this.rankingList_pl_pc
    if (this.platform == "PC" && this.rankingType == "CH")
      rankingList = this.rankingList_ch_pc
    if (this.platform == "PS4" && this.rankingType == "PL_CH")
      rankingList = this.rankingList_pl_ch_ps4
    if (this.platform == "PS4" && this.rankingType == "PL")
      rankingList = this.rankingList_pl_ps4
    if (this.platform == "PS4" && this.rankingType == "CH")
      rankingList = this.rankingList_ch_ps4
    if (this.platform == "PC_PS4" && this.rankingType == "PL_CH")
      rankingList = this.rankingList_pl_ch_union
    if (this.platform == "PC_PS4" && this.rankingType == "PL")
      rankingList = this.rankingList_pl_union
    if (this.platform == "PC_PS4" && this.rankingType == "CH")
      rankingList = this.rankingList_ch_union
    return rankingList
  }

  setTextPlatform(): string {
    var textPlatform!: string
    if (this.platform == "PC")
      textPlatform = "PC"
    if (this.platform == "PS4")
      textPlatform = "PS4"
    if (this.platform == "PC_PS4")
      textPlatform = "PC + PS4"

    return textPlatform
  }

  setTextRanking(): string {
    var textRanking!: string
    if (this.rankingType == "PL_CH")
      textRanking = "Player-Character"
    if (this.rankingType == "PL")
      textRanking = "Player"
    if (this.rankingType == "CH")
      textRanking = "Character"

    return textRanking
  }
}
