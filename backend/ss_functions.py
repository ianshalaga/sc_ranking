import json
import csv



def load_csv_data(csv_data_path):
    '''
    Input:
        CSV file with data of fights.
    Outputs:
        Dictionary with the data from input.
        Dictionary with battle indexes.
    '''

    # csv to list
    battles_list = list()
    with open(csv_data_path, encoding="utf8") as f:
        csv_reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL)
        for battle in csv_reader:
            for e in range(len(battle)):
                if battle[e] == "0":
                    battle[e] = 0
            battles_list.append(battle)

    # indexes for csv headers
    idx_dict = dict() # Output
    for i in range(len(battles_list[0])):
        idx_dict[battles_list[0][i]] = i

    columns_dict = dict()
    for e in idx_dict.keys():
        columns_dict[e] = list()
    for battle in battles_list[1:]:
        for column in idx_dict.keys():
            columns_dict[column].append(battle[idx_dict[column]])
    for column, content in columns_dict.items():
        columns_dict[column] = list(set(content))

    duels_list = list()
    duel_number = 1
    duel = battles_list[1]
    duels_list.append(duel)
    for battle in battles_list[2:]:
        if battle[idx_dict["duel"]] == duel_number:
            continue
        else:
            duel_number = battle[idx_dict["duel"]]
            duels_list.append(battle)

    return columns_dict, battles_list[1:], idx_dict, duels_list


def calculate_battle_winner(battle, battle_idx_dict, win_conditions):
    '''
    Inputs:
        Battle list.
        Indexes for the battle list.
        Win conditions strings.
    Output:
        Battle winner.
    '''
    winner = ""
    p1_won_rounds = 0
    p2_won_rounds = 0
    for round in range(battle_idx_dict["r1_p1"], battle_idx_dict["r1_p1"]+5):
        if battle[round] in win_conditions:
            p1_won_rounds += 1
        if battle[round+5] in win_conditions:
            p2_won_rounds += 1
        if (battle[round] or battle[round+5]) == "D":
            p1_won_rounds += 1
            p2_won_rounds += 1
    if p1_won_rounds > p2_won_rounds: # Player 1 wins
        if battle[battle_idx_dict["p1_team"]] != "":
            winner = battle[battle_idx_dict["p1_team"]]
        else:
            winner = battle[battle_idx_dict["player1"]]
    if p1_won_rounds < p2_won_rounds: # Players 2 wins
        if battle[battle_idx_dict["p2_team"]] != "":
            winner = battle[battle_idx_dict["p2_team"]]
        else:
            winner = battle[battle_idx_dict["player2"]]
    if p1_won_rounds == p2_won_rounds: # Draw
        winner = 0
    return winner


def calculate_duel_winner(duel, battle_idx_dict, win_conditions):
    '''
    Inputs:
        Duel (List of battles).
        Indexes for the battle list.
        Win conditions strings.
    Outputs:
        Duel winner and loser.
    '''
    winner = ""
    loser = ""
    if duel[0][battle_idx_dict["p1_team"]] != "":
        p1 = duel[0][battle_idx_dict["p1_team"]]
        p2 = duel[0][battle_idx_dict["p2_team"]]
    else:
        p1 = duel[0][battle_idx_dict["player1"]]
        p2 = duel[0][battle_idx_dict["player2"]]
    p1_won_fights = 0
    p2_won_fights = 0
    for fight in duel:
        result = calculate_battle_winner(fight, battle_idx_dict, win_conditions)
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
    '''
    Inputs:
        List of duels from an event.
        Indexes for the battle list.
    Output:
        List of players in the event.
    '''
    players_set = set()
    for duel in event_duels:
        if duel[0][battle_idx_dict["p1_team"]] != "":
            players_set.add(duel[0][battle_idx_dict["p1_team"]])
            players_set.add(duel[0][battle_idx_dict["p2_team"]])
        else:
            players_set.add(duel[0][battle_idx_dict["player1"]])
            players_set.add(duel[0][battle_idx_dict["player2"]])
    players_list = list(players_set)
    players_list.sort()
    return players_list


def get_win_lose_ratio(wins, loses):
    '''
    Inputs:
        Duels wins.
        Duels loses.
    Output:
        Win-lose ratio for duels.
    '''
    wlr = 0
    if loses == 0:
        wlr = wins
    elif wins == 0:
        wlr = 0.5/loses
    elif loses == 1:
        wlr = wins*0.75
    else:
        wlr = wins / loses
    return wlr


def calculate_event_results(event_duels, battle_idx_dict, win_conditions):
    '''
    Inputs:
        List of duels from an event.
        Indexes for the battle list.
        Win conditions strings.
    Output:
        Event results list ordered from best to worst.
    '''
    players_list = get_event_players(event_duels, battle_idx_dict)
    players_dict = dict()

    for player in players_list:
        players_dict[player] = {
            "wlr": 0,
            "buchholz_wlr": 0,
            "rivals": list(),
            "wins": 0,
            "loses": 0
        }

    for duel in event_duels:
        winner, loser = calculate_duel_winner(duel, battle_idx_dict, win_conditions)
        players_dict[winner]["wins"] += 1
        players_dict[loser]["loses"] += 1
        players_dict[winner]["rivals"].append(loser)
        players_dict[loser]["rivals"].append(winner)
    
    for player, data in players_dict.items():
        players_dict[player]["wlr"] = get_win_lose_ratio(players_dict[player]["wins"], players_dict[player]["loses"])

    for player, data in players_dict.items():
        for rival in data["rivals"]:
            players_dict[player]["buchholz_wlr"] += players_dict[rival]["wlr"]

    dic = dict(sorted(players_dict.items(), key=lambda item: (item[1]["wlr"], item[1]["buchholz_wlr"]), reverse=True))
    
    results = list()
    for k, v in dic.items():
        # print(k, v, "\n")
        results.append(k)

    return results



''' TESTING '''

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
        ["Fire Red", "Groh", "wylde", "Nightmare", "1", "LB", "W", "LB", "W", "LB", "W", "LY", "W", "LB", "W", "https://youtu.be/rMA50_1354o", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"],
        ["Fire Red", "Taki", "wylde", "Nightmare", "1", "PL", "LB", "W", "W", "LB", "PW", "W", "LB", "LB", "W", "https://youtu.be/rMA50_1354o", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"]
    ],
    [
        ["Kovas", "Ivy", "Imano", "Haohmaru", "2", "W", "W", "W", 0, 0, "LB", "LY", "LB", 0, 0, "https://youtu.be/cr5BiU9rC24", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"],
        ["Imano", "Haohmaru", "Kovas", "Ivy", "2", "LB", "W", "W", "LY", "W", "W", "LB", "LB", "W", "LY", "https://youtu.be/cr5BiU9rC24", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"],
        ["Kovas", "Ivy", "Imano", "Haohmaru", "2", "W", "LB", "W", "W", 0, "LB", "W", "LB", "LB", 0, "https://youtu.be/cr5BiU9rC24", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"]
    ],
    [
        ["JaffarWolf", "Yoshimitsu", "Sigfrancis", "Yoshimitsu", "3", "W", "LB", "W", "W", 0, "LB", "W", "LB", "LY", 0, "https://youtu.be/xLtq7FRKzho", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"],
        ["Sigfrancis", "Siegfried", "JaffarWolf", "Yoshimitsu", "3", "LY", "W", "LY", "W", "W", "W", "LB", "W", "LB", "LY", "https://youtu.be/xLtq7FRKzho", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"],
        ["JaffarWolf", "Yoshimitsu", "Sigfrancis", "Siegfried", "3", "W", "W", "LY", "LY", "W", "LY", "LY", "W", "W", "LY", "https://youtu.be/xLtq7FRKzho", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"]
    ],
    [
        ["raynarrok", "Azwel", "wylde", "Nightmare", "4", "LB", "LY", "LY", 0, 0, "W", "W", "W", 0, 0, "https://youtu.be/9-P2rhzFXZc", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"],
        ["raynarrok", "Xianghua", "wylde", "Nightmare", "4", "LY", "W", "LY", "LB", 0, "W", "LB", "W", "W", 0, "https://youtu.be/9-P2rhzFXZc", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"]
    ],
    [
        ["Sigfrancis", "Hwang", "Imano", "Haohmaru", "5", "LB", "W", "W", "W", 0, "W", "LB", "LY", "LY", 0, "https://youtu.be/FFL-Zzs8Fdc", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"],
        ["Imano", "Haohmaru", "Sigfrancis", "Hwang", "5", "LB", "LB", "LB", 0, 0, "W", "W", "W", 0, 0, "https://youtu.be/FFL-Zzs8Fdc", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"]
    ],
    [
        ["JaffarWolf", "Yoshimitsu", "Kovas", "Ivy", "6", "W", "LY", "PW", "LB", "LY", "LY", "W", "PL", "W", "W", "https://youtu.be/kx2h-oxhJ0I", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"],
        ["JaffarWolf", "Yoshimitsu", "Kovas", "Ivy", "6", "LB", "LB", "PW", "W", "W", "W", "W", "PL", "LB", "LB", "https://youtu.be/kx2h-oxhJ0I", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"],
        ["Kovas", "Ivy", "JaffarWolf", "Yoshimitsu", "6", "W", "LY", "PL", "PW", "LB", "LB", "W", "PW", "PL", "W", "https://youtu.be/kx2h-oxhJ0I", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"]
    ],
    [
        ["Sigfrancis", "Zasalamel", "raynarrok", "Azwel", "7", "W", "PW", "W", 0, 0, "LY", "PL", "LB", 0, 0, "https://youtu.be/nJ8fM7o3vDo", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"],
        ["raynarrok", "Amy", "Sigfrancis", "Zasalamel", "7", "LB", "LB", "W", "W", "LY", "W", "W", "LB", "LB", "W", "https://youtu.be/nJ8fM7o3vDo", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"]
    ],
    [
        ["Fire Red", "Groh", "Kovas", "Ivy", "8", "LB", "LY", "LY", 0, 0, "W", "W", "W", 0, 0, "https://youtu.be/voTfqBWDXFQ", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"],
        ["Fire Red", "Taki", "Kovas", "Ivy", "8", "LB", "LY", "W", "LY", 0, "W", "W", "LY", "W", 0, "https://youtu.be/voTfqBWDXFQ", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"]
    ],
    [
        ["JaffarWolf", "Yoshimitsu", "wylde", "Nightmare", "9", "LY", "W", "PL", "LB", 0, "W", "LB", "PW", "W", 0, "https://youtu.be/NbBkX0ZMea8", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"],
        ["JaffarWolf", "Yoshimitsu", "wylde", "Nightmare", "9", "LB", "W", "LY", "LB", 0, "W", "LY", "W", "W", 0, "https://youtu.be/NbBkX0ZMea8", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"],
        ["JaffarWolf", "Yoshimitsu", "wylde", "Nightmare", "9", "LY", "W", "W", "W", 0, "W", "LY", "LB", "LB", 0, "https://youtu.be/NbBkX0ZMea8", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"],
        ["wylde", "Nightmare", "JaffarWolf", "Yoshimitsu", "9", "LB", "W", "W", "LB", "LB", "W", "LB", "LB", "W", "W", "https://youtu.be/NbBkX0ZMea8", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"],
        ["wylde", "Nightmare", "JaffarWolf", "Yoshimitsu", "9", "W", "LB", "LY", "W", "PL", "LY", "W", "W", "LB", "PW", "https://youtu.be/NbBkX0ZMea8", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"]
    ],
    [
        ["Sigfrancis", "Hwang", "Kovas", "Ivy", "10", "LB", "W", "W", "LY", "W", "W", "LB", "LY", "W", "LY", "https://youtu.be/Odxqu1bx0tU", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"],
        ["Kovas", "Ivy", "Sigfrancis", "Hwang", "10", "LB", "LY", "W", "W", "LB", "W", "W", "LY", "LB", "W", "https://youtu.be/Odxqu1bx0tU", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"]
    ],
    [
        ["Sigfrancis", "Siegfried", "wylde", "Nightmare", "11", "LB", "PL", "W", "W", "LB", "W", "PW", "LB", "LB", "W", "https://youtu.be/C8M_-WxAZE0", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"],
        ["Sigfrancis", "Siegfried", "wylde", "Nightmare", "11", "LB", "LY", "LB", 0, 0, "W", "W", "W", 0, 0, "https://youtu.be/C8M_-WxAZE0", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"],
        ["Sigfrancis", "Yoshimitsu", "wylde", "Nightmare", "11", "LY", "LB", "LB", 0, 0, "W", "W", "W", 0, 0, "https://youtu.be/C8M_-WxAZE0", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"]
    ],
    [
        ["JaffarWolf", "Yoshimitsu", "wylde", "Nightmare", "12", "LB", "LB", "W", "PL", 0, "W", "W", "LY", "PW", 0, "https://youtu.be/Pf-wvdCSEj8", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"],
        ["JaffarWolf", "Yoshimitsu", "wylde", "Nightmare", "12", "W", "LB", "LB", "LB", 0, "LY", "W", "W", "W", 0, "https://youtu.be/Pf-wvdCSEj8", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"],
        ["JaffarWolf", "Yoshimitsu", "wylde", "Nightmare", "12", "LB", "W", "LY", "W", "LB", "W", "LB", "W", "LY", "W", "https://youtu.be/Pf-wvdCSEj8", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"]
    ],
    [
        ["JaffarWolf", "Yoshimitsu", "wylde", "Nightmare", "13", "W", "LB", "LB", "LB", 0, "LY", "W", "W", "W", 0, "https://youtu.be/QvdLUsXOdrM", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"],
        ["JaffarWolf", "Yoshimitsu", "wylde", "Nightmare", "13", "LY", "LB", "LB", 0, 0, "W", "W", "W", 0, 0, "https://youtu.be/QvdLUsXOdrM", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"],
        ["JaffarWolf", "Yoshimitsu", "wylde", "Nightmare", "13", "LB", "W", "LY", "W", "LY", "W", "LY", "W", "LY", "W", "https://youtu.be/QvdLUsXOdrM", "SSLT 11", "https://www.youtube.com/embed/videoseries?list=PL90QAKwVH1t7qd1ccQTkclZDIKJHr6J5_", "https://challonge.com/es/n6aamya3", "PC"]
    ]
]

# total_duels = ""
# json_path = "backend/json.json"
# with open(json_path, "r", encoding="utf8") as f:
#     total_duels = json.load(f)

win_conditions = ["PW", "W", "WB", "WY"]

# print(calculate_event_results(event_duels, battle_idx_dict, win_conditions))

csv_data_path = "backend/SCMdb - SSLT.csv"
columns_dict, battles_list, idx_dict, duels_list = load_csv_data(csv_data_path)

# for k, v in columns_dict.items():
#     print(k, v)

# for e in duels_list:
#     print(e, "\n")