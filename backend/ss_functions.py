


def calculate_battle_winner(battle, battle_idx_dict):
    winner = ""
    p1_won_rounds = 0
    p2_won_rounds = 0
    for round in range(battle_idx_dict["r1_p1"], battle_idx_dict["r1_p1"]+5):
        if battle[round] == "W" or battle[round] == "PW":
            p1_won_rounds += 1
        if battle[round+5] == "W" or battle[round+5] == "PW":
            p2_won_rounds += 1
        if (battle[round] or battle[round+5]) == "D":
            p1_won_rounds += 1
            p2_won_rounds += 1
    if p1_won_rounds > p2_won_rounds: # Player 1 wins
        winner = battle[battle_idx_dict["player1"]]
    if p1_won_rounds < p2_won_rounds: # Players 2 wins
        winner = battle[battle_idx_dict["player2"]]
    if p1_won_rounds == p2_won_rounds: # Draw
        winner = 0
    return winner


def calculate_duel_winner(duel, battle_idx_dict):
    winner = ""
    loser = ""
    p1 = duel[0][battle_idx_dict["player1"]]
    p2 = duel[0][battle_idx_dict["player2"]]
    p1_won_fights = 0
    p2_won_fights = 0
    for fight in duel:
        result = calculate_battle_winner(fight, battle_idx_dict)
        if result == p1:
            p1_won_fights += 1
        if result == p2:
            p2_won_fights += 1
        if result == 0:
            continue
    if p1_won_fights > p2_won_fights: # Player 1 wins
        winner = p1
        loser = p2
    if p1_won_fights < p2_won_fights: # Players 2 wins
        winner = p2
        loser = p1
    return winner, loser


def get_event_players(event_duels, battle_idx_dict):
    players_set = set()
    for duel in event_duels:
        players_set.add(duel[0][battle_idx_dict["player1"]])
        players_set.add(duel[0][battle_idx_dict["player2"]])
    players_list = list(players_set)
    players_list.sort()
    return players_list


def get_win_lose_ratio(wins, loses):
    wlr = 0
    if loses == 0:
        wlr = wins
    else:
        wlr = wins / loses
    return wlr


def calculate_event_results(event_duels, battle_idx_dict):
    players_list = get_event_players(event_duels, battle_idx_dict)
    players_dict = dict()

    for player in players_list:
        players_dict[player] = {
            "wlr": 0,
            "buchholz_wins": 0,
            "buchholz_wlr": 0,
            "rivals": set(),
            "wins": 0,
            "loses": 0
        }

    for duel in event_duels:
        winner, loser = calculate_duel_winner(duel, battle_idx_dict)
        players_dict[winner]["wins"] += 1
        players_dict[loser]["loses"] += 1
        players_dict[winner]["rivals"].add(loser)
        players_dict[loser]["rivals"].add(winner)
    
    for player, data in players_dict.items():
        players_dict[player]["wlr"] = get_win_lose_ratio(players_dict[player]["wins"], players_dict[player]["loses"])

    for player, data in players_dict.items():
        for rival in data["rivals"]:
            players_dict[player]["buchholz_wins"] += players_dict[rival]["wins"]
            players_dict[player]["buchholz_wlr"] += players_dict[rival]["wlr"]

    dic = dict(sorted(players_dict.items(), key=lambda item: (item[1]["wlr"], item[1]["buchholz_wins"], item[1]["buchholz_wlr"]), reverse=True))

    for k, v in dic.items():
        print(k, v, "\n")


battle_idx_dict = {
    "player1": 0,
    "character1": 1,
    "player2": 2,
    "character2": 3,
    "duel": 4,
    "r1_p1": 5,
    "r2_p1": 6,
    "r3_p1": 7,
    "r4_p1": 8,
    "r5_p1": 9,
    "r1_p2": 10,
    "r2_p2": 11,
    "r3_p2": 12,
    "r4_p2": 13,
    "r5_p2": 14,
    "video": 15,
    "event": 16,
    "playlist": 17,
    "brackets": 18,
    "platform": 19
}

battle = ['Fire Red', 'Taki', 'Camus', 'Kilik', '12', 'LB', 'LY', 'LY', 0, 0, 'W', 'W', 'W', 0, 0, 'https://youtu.be/6Ov08Pl2-eY', 'SSLT 9', 'https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t5nA6XGgwlhS_2XrL8XvdYq', 'https://challonge.com/es/2ja9lhxa', 'PC']

duel = [
        ["Gontranno", "Astaroth", "Sebas", "Yoshimitsu", "11", "LB", "LY", "W", "W", "PW", "W", "W", "LY", "LB", "PL", "https://youtu.be/pVeVUHu0y3Y", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"],
        ["Sebas", "Yoshimitsu", "Gontranno", "Astaroth", "11", "W", "W", "LB", "W", 0, "LB", "LB", "W", "LY", 0, "https://youtu.be/pVeVUHu0y3Y", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"],
        ["Gontranno", "Astaroth", "Sebas", "Yoshimitsu", "11", "W", "W", "LY", "PW", 0, "LY", "LY", "W", "PL", 0, "https://youtu.be/pVeVUHu0y3Y", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"]
    ]

event_duels = [
    [
        ["Junixart", "Talim", "Mastodon", "Talim", "1", "W", "W", "W", 0, 0, "LB", "LB", "LB", 0, 0, "https://youtu.be/ak9W5B2P4Jk", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"],
        ["Mastodon", "Talim", "Junixart", "Talim", "1", "W", "LY", "LY", "LY", 0, "LY", "W", "W", "W", 0, "https://youtu.be/ak9W5B2P4Jk", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"]
    ],
    [
        ["Ozkuervo", "Maxi", "Gontranno", "Tira", "2", "W", "LB", "LB", "LB", 0, "LY", "W", "W", "W", 0, "https://youtu.be/uzQB44CUvVU", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"],
        ["Ozkuervo", "Maxi", "Gontranno", "Tira", "2", "LB", "LB", "LB", 0, 0, "W", "W", "W", 0, 0, "https://youtu.be/uzQB44CUvVU", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"]
    ],
    [
        ["Sigfrancis", "Hwang", "Sebas", "Yoshimitsu", "3", "W", "W", "W", 0, 0, "LY", "LY", "LY", 0, 0, "https://youtu.be/oNOlPtE1l4c", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"],
        ["Sebas", "Yoshimitsu", "Sigfrancis", "Hwang", "3", "LB", "W", "W", "W", 0, "W", "LB", "LB", "LB", 0, "https://youtu.be/oNOlPtE1l4c", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"],
        ["Sigfrancis", "Xianghua", "Sebas", "Yoshimitsu", "3", "LB", "W", "LB", "LY", 0, "W", "LB", "W", "W", 0, "https://youtu.be/oNOlPtE1l4c", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"]
    ],
    [
        ["DaiaNerdKilik", "Kilik", "Nightwing", "Maxi", "4", "W", "W", "LY", "W", 0, "LY", "LB", "W", "LY", 0, "https://youtu.be/mYn2LmZ_LR4", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"],
        ["Nightwing", "Maxi", "DaiaNerdKilik", "Kilik", "4", "LB", "W", "LB", "LY", 0, "W", "LB", "W", "W", 0, "https://youtu.be/mYn2LmZ_LR4", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"]
    ],
    [
        ["Ozkuervo", "Maxi", "Mastodon", "Seong Mi-na", "5", "LB", "LB", "LB", 0, 0, "W", "W", "W", 0, 0, "https://youtu.be/Syy-a_12a6M", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"],
        ["Ozkuervo", "Maxi", "Mastodon", "Seong Mi-na", "5", "W", "LB", "LY", "W", "LY", "LB", "W", "W", "LY", "W", "https://youtu.be/Syy-a_12a6M", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"]
    ],
    [
        ["Sigfrancis", "Xianghua", "Nightwing", "Maxi", "6", "PL", "LB", "W", "W", "W", "PW", "W", "LB", "LB", "LB", "https://youtu.be/MaQ1XYpghkE", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"],
        ["Nightwing", "Maxi", "Sigfrancis", "Xianghua", "6", "PL", "LY", "W", "W", "W", "PW", "W", "LB", "LB", "LB", "https://youtu.be/MaQ1XYpghkE", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"],
        ["Sigfrancis", "Hwang", "Nightwing", "Maxi", "6", "W", "PL", "W", "W", 0, "LB", "PW", "LB", "LB", 0, "https://youtu.be/MaQ1XYpghkE", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"]
    ],
    [
        ["Gontranno", "Astaroth", "Junixart", "Talim", "7", "LB", "LB", "W", "LB", 0, "W", "W", "LB", "W", 0, "https://youtu.be/RlhghCiJQUA", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"],
        ["Gontranno", "Tira", "Junixart", "Talim", "7", "PL", "LY", "LY", 0, 0, "PW", "W", "W", 0, 0, "https://youtu.be/RlhghCiJQUA", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"]
    ],
    [
        ["DaiaNerdKilik", "Kilik", "Sebas", "Yoshimitsu", "8", "W", "LB", "W", "PL", "W", "LB", "W", "LB", "PW", "LB", "https://youtu.be/_urBSSl9SLM", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"],
        ["Sebas", "Yoshimitsu", "DaiaNerdKilik", "Kilik", "8", "W", "W", "W", 0, 0, "LB", "LB", "LB", 0, 0, "https://youtu.be/_urBSSl9SLM", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"],
        ["DaiaNerdKilik", "Kilik", "Sebas", "Yoshimitsu", "8", "W", "W", "W", 0, 0, "LY", "LB", "LY", 0, 0, "https://youtu.be/_urBSSl9SLM", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"]
    ],
    [
        ["Gontranno", "Astaroth", "Sigfrancis", "Xianghua", "9", "W", "W", "W", 0, 0, "LB", "LY", "LB", 0, 0, "https://youtu.be/BTKQ9FQi5Ns", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"],
        ["Sigfrancis", "Hwang", "Gontranno", "Astaroth", "9", "W", "LY", "W", "LB", "LB", "LY", "W", "LB", "W", "W", "https://youtu.be/BTKQ9FQi5Ns", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"]
    ],
    [
        ["Sebas", "Yoshimitsu", "Mastodon", "Talim", "10", "W", "PL", "W", "LY", "LB", "LB", "PW", "LB", "W", "W", "https://youtu.be/TEGV1S7tsgc", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"],
        ["Sebas", "Yoshimitsu", "Mastodon", "Talim", "10", "W", "W", "LY", "LB", "W", "LB", "LY", "W", "W", "LB", "https://youtu.be/TEGV1S7tsgc", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"],
        ["Mastodon", "Talim", "Sebas", "Yoshimitsu", "10", "LY", "LY", "LB", 0, 0, "W", "W", "W", 0, 0, "https://youtu.be/TEGV1S7tsgc", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"]
    ],
    [
        ["Gontranno", "Astaroth", "Sebas", "Yoshimitsu", "11", "LB", "LY", "W", "W", "PW", "W", "W", "LY", "LB", "PL", "https://youtu.be/pVeVUHu0y3Y", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"],
        ["Sebas", "Yoshimitsu", "Gontranno", "Astaroth", "11", "W", "W", "LB", "W", 0, "LB", "LB", "W", "LY", 0, "https://youtu.be/pVeVUHu0y3Y", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"],
        ["Gontranno", "Astaroth", "Sebas", "Yoshimitsu", "11", "W", "W", "LY", "PW", 0, "LY", "LY", "W", "PL", 0, "https://youtu.be/pVeVUHu0y3Y", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"]
    ],
    [
        ["Junixart", "Talim", "DaiaNerdKilik", "Kilik", "12", "W", "W", "LB", "W", 0, "LB", "LB", "W", "LY", 0, "https://youtu.be/pbXtjMq-E7E", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"],
        ["DaiaNerdKilik", "Kilik", "Junixart", "Talim", "12", "LY", "W", "W", "LY", "W", "W", "LB", "LB", "W", "LB", "https://youtu.be/pbXtjMq-E7E", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"],
        ["Junixart", "Talim", "DaiaNerdKilik", "Kilik", "12", "W", "LY", "W", "LY", "W", "LB", "W", "LB", "W", "LB", "https://youtu.be/pbXtjMq-E7E", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"],
        ["DaiaNerdKilik", "Kilik", "Junixart", "Talim", "12", "LB", "LY", "LY", 0, 0, "W", "W", "W", 0, 0, "https://youtu.be/pbXtjMq-E7E", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"]
    ],
    [
        ["Gontranno", "Astaroth", "DaiaNerdKilik", "Kilik", "13", "W", "W", "W", 0, 0, "LB", "LB", "LB", 0, 0, "https://youtu.be/u8xopJvZLBU", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"],
        ["DaiaNerdKilik", "Kilik", "Gontranno", "Astaroth", "13", "W", "LY", "LY", "W", "LY", "LB", "W", "W", "LY", "W", "https://youtu.be/u8xopJvZLBU", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"],
        ["DaiaNerdKilik", "Kilik", "Gontranno", "Astaroth", "13", "LB", "PL", "LB", 0, 0, "W", "PW", "W", 0, 0, "https://youtu.be/u8xopJvZLBU", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"]
    ],
    [
        ["Junixart", "Seong Mi-na", "Gontranno", "Astaroth", "14", "W", "W", "W", 0, 0, "LB", "LB", "LB", 0, 0, "https://youtu.be/jFrDUvN7g_o", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"],
        ["Gontranno", "Astaroth", "Junixart", "Seong Mi-na", "14", "LY", "LY", "W", "W", "W", "W", "W", "LY", "LB", "LY", "https://youtu.be/jFrDUvN7g_o", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"],
        ["Junixart", "Seong Mi-na", "Gontranno", "Astaroth", "14", "W", "PL", "W", "LB", "W", "LY", "PW", "LY", "W", "LB", "https://youtu.be/jFrDUvN7g_o", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"],
        ["Gontranno", "Astaroth", "Junixart", "Seong Mi-na", "14", "W", "W", "PL", "W", 0, "LB", "LB", "PW", "LB", 0, "https://youtu.be/jFrDUvN7g_o", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"],
        ["Junixart", "Seong Mi-na", "Gontranno", "Astaroth", "14", "LY", "W", "W", "W", 0, "W", "LB", "LY", "LB", 0, "https://youtu.be/jFrDUvN7g_o", "SSLT 8", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t70_LzcNxUNjh4fZFv49uRr", "https://challonge.com/aycj9qg6", "PS4"]
    ]
]

# print(calculate_battle_winner(battle, battle_idx_dict))

# print(calculate_duel_winner(duel, battle_idx_dict))

calculate_event_results(event_duels, battle_idx_dict)