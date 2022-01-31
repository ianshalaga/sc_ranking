export interface BattleData {
    rival: String
    result: String,
    won_rounds: Number,
    played_rounds: Number,
    raw_points: String,
    beating_factor: String,
    won_points: String,
    event: String,
    video: String
}

export interface PlayerData {
    player: String,
    played_battles: Number,
    won_battles: Number,
    lost_battles: Number,
    draw_battles: Number,
    win_rate: String,
    points_earned: String,
    wlr: String,
    player_level: String,
    battles_history: BattleData[]
}