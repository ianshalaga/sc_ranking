export interface PlayerStats {
    rival: string,
    played_battles: number,
    won_battles: number,
    lost_battles: number,
    draw_battles: number,
    win_rate: string
}

export interface BattleData {
    rival: string
    result: string,
    won_rounds: number,
    played_rounds: number,
    raw_points: string,
    beating_factor: string,
    lvl_factor: string,
    won_points: string,
    event: string,
    video: string
}

export interface PlayerData {
    player: string,
    played_battles: number,
    won_battles: number,
    lost_battles: number,
    draw_battles: number,
    win_rate: string,
    points_earned: string,
    wlr: string,
    player_level: string,
    battles_history: BattleData[],
    player_stats: PlayerStats[]
}

export interface EntitiesCount {
    PlChPc: number,
    PlPc: number,
    ChPc: number,
    PlChPs4: number,
    PlPs4: number,
    ChPs4: number,
    PlChPcPs4: number,
    PlPcPs4: number,
    ChPcPs4: number,
}

export interface EventStats {
    event: string,
    platform: string,
    players: string[],
    characters: string[],
    playlist: string,
    result: string[]
}