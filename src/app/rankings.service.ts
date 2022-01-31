import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

import { BattleData, PlayerData } from 'src/app/player-data'

// PC
import ranking_pl_ch_pc from 'src/assets/data/ranking_pl_ch_pc.json'
import ranking_pl_pc from 'src/assets/data/ranking_pl_pc.json'
import ranking_ch_pc from 'src/assets/data/ranking_ch_pc.json'

// PS4
import ranking_pl_ch_ps4 from 'src/assets/data/ranking_pl_ch_ps4.json'
import ranking_pl_ps4 from 'src/assets/data/ranking_pl_ps4.json'
import ranking_ch_ps4 from 'src/assets/data/ranking_ch_ps4.json'

// PC_PS4
import ranking_pl_ch_union from 'src/assets/data/ranking_pl_ch_union.json'
import ranking_pl_union from 'src/assets/data/ranking_pl_union.json'
import ranking_ch_union from 'src/assets/data/ranking_ch_union.json'

@Injectable({
  providedIn: 'root'
})
export class RankingsService {

  constructor() { }

  getPcPlCh(): Observable<PlayerData[]> { return of(ranking_pl_ch_pc) }
  getPcPl(): Observable<PlayerData[]> { return of(ranking_pl_pc) }
  getPcCh(): Observable<PlayerData[]> { return of(ranking_ch_pc) }
  getPs4PlCh(): Observable<PlayerData[]> { return of(ranking_pl_ch_ps4) }
  getPs4Pl(): Observable<PlayerData[]> { return of(ranking_pl_ps4) }
  getPs4Ch(): Observable<PlayerData[]> { return of(ranking_ch_ps4) }
  getUnionPlCh(): Observable<PlayerData[]> { return of(ranking_pl_ch_union) }
  getUnionPl(): Observable<PlayerData[]> { return of(ranking_pl_union) }
  getUnionCh(): Observable<PlayerData[]> { return of(ranking_ch_union) }

  getEntity(platform: string, entity: string): Observable<BattleData[]> {
    let battleData: BattleData[] = []
    const listPC = ranking_pl_ch_pc.concat(ranking_pl_pc.concat(ranking_ch_pc))
    const listPS4 = ranking_pl_ch_ps4.concat(ranking_pl_ps4.concat(ranking_ch_ps4))
    const listUnion = ranking_pl_ch_union.concat(ranking_pl_union.concat(ranking_ch_union))
    if (platform == "PC")
      battleData = listPC.find(ent => ent.player == entity)?.battles_history!
    if (platform == "PS4")
      battleData = listPS4.find(ent => ent.player == entity)?.battles_history!
    if (platform == "PC_PS4")
      battleData = listUnion.find(ent => ent.player == entity)?.battles_history!
    return of(battleData)
  }
}
