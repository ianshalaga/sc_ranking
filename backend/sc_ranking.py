import csv
import json
import ss_functions
import math
import numpy as np


def load_csv_fights(csv_fights_path):
    '''
    Input: csv file with battles extracted from Google Sheets.
    Output: List of battles where each battle is a list too.
    '''
    battles_list = list()
    battles_pc_count = 0
    battles_ps4_count = 0
    battles_count = 0
    idx_dict = dict() # Output
    with open(csv_fights_path, encoding="utf8") as f:
        csv_reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL)
        for battle in csv_reader:
            for i in range(len(battle)):
                idx_dict[battle[i]] = i
            break
        for battle in csv_reader:
            # if battle[-1] == "platform": # Avoids header row
            if battle[idx_dict["platform"]] == "platform": # Avoids header row
                continue
            if battle[idx_dict["season"]] != "S2":
                continue
            for e in range(len(battle)):
                if battle[e] == "0":
                    battle[e] = 0
            battles_list.append(battle)
            battles_count += 1
            # if battle[-1] == "PC":
            if battle[idx_dict["platform"]] == "PC":
                battles_pc_count += 1
            # if battle[-1] == "PS4":
            if battle[idx_dict["platform"]] == "PS4":
                battles_ps4_count += 1
        print(f"Combates en PC: {battles_pc_count}")
        print(f"Combates en PS4: {battles_ps4_count}")
        print(f"Combates totales: {battles_count}")

    return battles_list, idx_dict


class point_system:
    def __init__(self,
                 pw,
                 w,
                 wb,
                 wy,
                 d,
                 pl,
                 lb,
                 ly):
        self.pw = pw
        self.w = w
        self.wb = wb
        self.wy = wy
        self.d = d
        self.pl = pl
        self.lb = lb
        self.ly = ly


class battle_data:
    def __init__(self,
                 p1_won_rounds,
                 p2_won_rounds,
                 p1_raw_points,
                 p2_raw_points,
                 p1_won_points,
                 p2_won_points,
                 rounds_played,
                 p1_beating_factor,
                 p2_beating_factor,
                 p1_lvl_factor,
                 p2_lvl_factor,
                 p1_win,
                 p2_win,
                 draw,
                 p1_history,
                 p2_history):

        self.p1_won_rounds = p1_won_rounds
        self.p2_won_rounds = p2_won_rounds
        self.p1_raw_points = p1_raw_points
        self.p2_raw_points = p2_raw_points
        self.p1_won_points = p1_won_points
        self.p2_won_points = p2_won_points
        self.rounds_played = rounds_played
        self.p1_beating_factor = p1_beating_factor
        self.p2_beating_factor = p2_beating_factor
        self.p1_lvl_factor = p1_lvl_factor
        self.p2_lvl_factor = p2_lvl_factor
        self.p1_win = p1_win
        self.p2_win = p2_win
        self.draw = draw
        self.p1_history = p1_history
        self.p2_history = p2_history

    def calculate_rounds_played(self):
        self.rounds_played = self.p1_won_rounds + self.p2_won_rounds

    def calculate_beating_factors(self):
        if self.p1_won_rounds == 0:
            # self.p1_beating_factor = 0.1
            self.p1_beating_factor = (1/self.rounds_played)/2
        else:
            self.p1_beating_factor = self.p1_won_rounds / self.rounds_played
        if self.p2_won_rounds == 0:
            # self.p2_beating_factor = 0.1
            self.p2_beating_factor = (1/self.rounds_played)/2
        else:
            self.p2_beating_factor = self.p2_won_rounds / self.rounds_played
    
    def calculate_lvl_factors(self, p1_win_rate, p2_win_rate):
        b = 1
        a = -(25/132)
        self.p1_lvl_factor = a*(p1_win_rate - p2_win_rate) + b
        self.p2_lvl_factor = a*(p2_win_rate - p1_win_rate) + b

    def calculate_won_points(self, p1_win_rate, p2_win_rate):
        self.calculate_lvl_factors(p1_win_rate, p2_win_rate)
        self.p1_won_points = self.p1_raw_points * self.p1_beating_factor * self.p1_lvl_factor
        self.p2_won_points = self.p2_raw_points * self.p2_beating_factor * self.p2_lvl_factor

    def calculate_result(self):
        if self.p1_won_rounds > self.p2_won_rounds:  # Player 1 won
            self.p1_win = True
            self.p2_win = False
            self.draw = False
            self.p1_history = {"result": "Victory"}
            self.p2_history = {"result": "Defeat"}
        elif self.p2_won_rounds > self.p1_won_rounds:  # Player 2 won
            self.p1_win = False
            self.p2_win = True
            self.draw = False
            self.p1_history = {"result": "Defeat"}
            self.p2_history = {"result": "Victory"}
        else:  # It was a draw
            self.p1_win = False
            self.p2_win = False
            self.draw = True
            self.p1_history = {"result": "Draw"}
            self.p2_history = {"result": "Draw"}

    def generate_history(self, event, video):
        self.p1_history["won_rounds"] = self.p1_won_rounds
        self.p1_history["played_rounds"] = self.rounds_played
        self.p1_history["raw_points"] = f"{'%.0f' % self.p1_raw_points}"
        self.p1_history["beating_factor"] = f"{'%.2f' % self.p1_beating_factor}"
        self.p1_history["lvl_factor"] = f"{'%.2f' % self.p1_lvl_factor}"
        self.p1_history["won_points"] = f"{'%.0f' % self.p1_won_points}"
        self.p1_history["event"] = event
        self.p1_history["video"] = video

        self.p2_history["won_rounds"] = self.p2_won_rounds
        self.p2_history["played_rounds"] = self.rounds_played
        self.p2_history["raw_points"] = f"{'%.0f' % self.p2_raw_points}"
        self.p2_history["beating_factor"] = f"{'%.2f' % self.p2_beating_factor}"
        self.p2_history["lvl_factor"] = f"{'%.2f' % self.p2_lvl_factor}"
        self.p2_history["won_points"] = f"{'%.0f' % self.p2_won_points}"
        self.p2_history["event"] = event
        self.p2_history["video"] = video
    

def battle_data_generator(battle, point_system_obj, player1_win_rate, player2_win_rate, idx_dict):
    battle_data_obj = battle_data(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    for i in range(5, 10): # int(len(battle)/2)
        # Player 1
        if battle[i] == "W":
            battle_data_obj.p1_won_rounds += 1
            battle_data_obj.p1_raw_points += point_system_obj.w
        if battle[i] == "PW":
            battle_data_obj.p1_won_rounds += 1
            battle_data_obj.p1_raw_points += point_system_obj.pw
        if battle[i] == "D":
            battle_data_obj.p1_won_rounds += 1
            battle_data_obj.p1_raw_points += point_system_obj.d
        if battle[i] == "LY":
            battle_data_obj.p1_raw_points += point_system_obj.ly
        if battle[i] == "LB":
            battle_data_obj.p1_raw_points += point_system_obj.lb
        # Player 2
        if battle[i+5] == "W":
            battle_data_obj.p2_won_rounds += 1
            battle_data_obj.p2_raw_points += point_system_obj.w
        if battle[i+5] == "PW":
            battle_data_obj.p2_won_rounds += 1
            battle_data_obj.p2_raw_points += point_system_obj.pw
        if battle[i+5] == "D":
            battle_data_obj.p2_won_rounds += 1
            battle_data_obj.p2_raw_points += point_system_obj.d
        if battle[i+5] == "LY":
            battle_data_obj.p2_raw_points += point_system_obj.ly
        if battle[i+5] == "LB":
            battle_data_obj.p2_raw_points += point_system_obj.lb

    battle_data_obj.calculate_rounds_played()
    battle_data_obj.calculate_beating_factors()
    battle_data_obj.calculate_won_points(player1_win_rate, player2_win_rate)
    battle_data_obj.calculate_result()
    battle_data_obj.generate_history(battle[idx_dict["event"]], battle[idx_dict["video"]])

    return battle_data_obj


class player_stats:
    def __init__(self,
                 played_battles,
                 won_battles,
                 lost_battles,
                 draw_battles,
                 win_rate):
        self.played_battles = played_battles
        self.won_battles = won_battles
        self.lost_battles = lost_battles
        self.draw_battles = draw_battles
        self.win_rate = win_rate

    def calculate_win_rate(self):
        self.win_rate = self.won_battles / self.played_battles
    
        
class player_data:
    def __init__(self,
                 played_battles,
                 won_battles,
                 lost_battles,
                 draw_battles,
                 points_earned,
                 win_rate,
                 player_level,
                 wlr,
                 battles_history,
                 player_stats):
        self.played_battles = played_battles
        self.won_battles = won_battles
        self.lost_battles = lost_battles
        self.draw_battles = draw_battles
        self.points_earned = points_earned
        self.win_rate = win_rate
        self.player_level = player_level
        self.wlr = wlr  # Wins / Losses Ratio
        self.battles_history = battles_history
        self.player_stats = player_stats

    def calculate_win_rate(self):
        self.win_rate = self.won_battles / self.played_battles

    def calculate_wlr(self):
        if self.lost_battles == 0: # If there is no losses
            self.wlr = self.won_battles + (self.draw_battles / 2)
        elif self.won_battles + self.draw_battles == 0:
            # self.wlr = (1 + (self.draw_battles / 2)) / self.lost_battles
            # self.wlr = 1 / self.lost_battles
            self.wlr = 0.5 / self.lost_battles
        elif self.lost_battles == 1:
            self.wlr = (self.won_battles + (self.draw_battles / 2)) * 3/4
        else:
            self.wlr = (self.won_battles + (self.draw_battles / 2)) / self.lost_battles
        # self.wlr = math.sqrt(self.wlr)
        # self.wlr = -(1/self.wlr)+10
        self.wlr = np.arctan(self.wlr)

    def calculate_player_lvl(self):
        self.player_level = self.wlr * self.points_earned

    def add_to_history(self, battle, rival):
        battle["rival"] = rival
        self.battles_history.append(battle)


def player_data_generator(battle, point_system_obj, entity1, entity2, entities_dict, idx_dict):
    if entity1 not in entities_dict:
        entities_dict[entity1] = player_data(0, 0, 0, 0, 0, 0, 0, 0, [], {entity2: player_stats(0, 0, 0, 0, 0)})
    elif entity2 not in entities_dict[entity1].player_stats:
        entities_dict[entity1].player_stats[entity2] = player_stats(0, 0, 0, 0, 0)

    if entity2 not in entities_dict:
        entities_dict[entity2] = player_data(0, 0, 0, 0, 0, 0, 0, 0, [], {entity1: player_stats(0, 0, 0, 0, 0)})
    elif entity1 not in entities_dict[entity2].player_stats:
        entities_dict[entity2].player_stats[entity1] = player_stats(0, 0, 0, 0, 0)

    # battle_list = battle[5:]
    # battle_data_obj = battle_data_generator(battle_list, point_system_obj, entities_dict[entity1].win_rate, entities_dict[entity2].win_rate, idx_dict)
    battle_data_obj = battle_data_generator(battle, point_system_obj, entities_dict[entity1].win_rate, entities_dict[entity2].win_rate, idx_dict)

    if battle_data_obj.p1_win:
        entities_dict[entity1].won_battles += 1
        entities_dict[entity2].lost_battles += 1
        entities_dict[entity1].player_stats[entity2].won_battles += 1
        entities_dict[entity2].player_stats[entity1].lost_battles += 1

    if battle_data_obj.p2_win:
        entities_dict[entity1].lost_battles += 1
        entities_dict[entity2].won_battles += 1
        entities_dict[entity2].player_stats[entity1].won_battles += 1
        entities_dict[entity1].player_stats[entity2].lost_battles += 1

    if battle_data_obj.draw:
        entities_dict[entity1].draw_battles += 1
        entities_dict[entity2].draw_battles += 1
        entities_dict[entity1].player_stats[entity2].draw_battles += 1
        entities_dict[entity2].player_stats[entity1].draw_battles += 1

    entities_dict[entity1].points_earned += battle_data_obj.p1_won_points
    entities_dict[entity2].points_earned += battle_data_obj.p2_won_points
    entities_dict[entity1].played_battles += 1
    entities_dict[entity2].played_battles += 1
    entities_dict[entity1].calculate_win_rate()
    entities_dict[entity2].calculate_win_rate()
    entities_dict[entity1].calculate_wlr()
    entities_dict[entity2].calculate_wlr()
    entities_dict[entity1].calculate_player_lvl()
    entities_dict[entity2].calculate_player_lvl()
    entities_dict[entity1].add_to_history(battle_data_obj.p1_history, entity2)
    entities_dict[entity2].add_to_history(battle_data_obj.p2_history, entity1)

    entities_dict[entity1].player_stats[entity2].played_battles += 1
    entities_dict[entity2].player_stats[entity1].played_battles += 1
    entities_dict[entity1].player_stats[entity2].calculate_win_rate()
    entities_dict[entity2].player_stats[entity1].calculate_win_rate()


def make_tier_lists(battles_list, point_system_obj, tier_list_type, platform, idx_dict):
    '''
    tier_list_type: "PL" or "CH" or "PL-CH"
    platform: "PC" or "PS4" or "union"
    '''
    entities_dict = dict()

    for battle in battles_list:
        player1 = battle[idx_dict["player1"]]
        player2 = battle[idx_dict["player2"]]
        character1 = battle[idx_dict["character1"]]
        character2 = battle[idx_dict["character2"]]
        player_character1 = player1 + "-" + character1
        player_character2 = player2 + "-" + character2

        if tier_list_type == "PL-CH":  # Players - Characters
            entity1 = player_character1
            entity2 = player_character2
        if tier_list_type == "PL":  # Players
            entity1 = player1
            entity2 = player2
        if tier_list_type == "CH":  # Characters
            entity1 = character1
            entity2 = character2

        if platform == "PC" and battle[idx_dict["platform"]] == "PC":
            player_data_generator(battle, point_system_obj, entity1, entity2, entities_dict, idx_dict)

        if platform == "PS4" and battle[idx_dict["platform"]] == "PS4":
            player_data_generator(battle, point_system_obj, entity1, entity2, entities_dict, idx_dict)

        if platform == "union":
            player_data_generator(battle, point_system_obj, entity1, entity2, entities_dict, idx_dict)

    return dict(sorted(entities_dict.items(), key=lambda item: item[1].player_level, reverse=True))


def print_results(ranking_dict):
    for k, v in ranking_dict.items():
        print(k,
              v.played_battles,
              v.won_battles,
              v.lost_battles,
              v.draw_battles,
              v.win_rate,
              v.points_earned,
              v.wlr,
              v.player_level)
        for e in v.battles_history:
            print(
                "Rival: {}".format(e["rival"]),
                "Result: {}".format(e["result"]),
                "Won rounds: {}/{}".format(e["won_rounds"], e["played_rounds"]),
                "Beating factor: {}".format(e["beating_factor"]),
                "Points earned: {}/{}".format(e["won_points"], e["raw_points"]),
                "Event: {}".format(e["event"])
            )


def player_stats_obj_to_dict(rival, player_stats_obj):
    player_stats_dict = {
        "rival": rival,
        "played_battles": player_stats_obj.played_battles,
        "won_battles": player_stats_obj.won_battles,
        "lost_battles": player_stats_obj.lost_battles,
        "draw_battles": player_stats_obj.draw_battles,
        "win_rate": f"{'%.0f' % (player_stats_obj.win_rate * 100)}" + " %",
    }
    return player_stats_dict


def player_stats_obj_to_dict_batch(player_stats_dict):
    player_stats_list = list()
    for rival, player_stats_obj in player_stats_dict.items():
        player_stats_list.append(player_stats_obj_to_dict(rival, player_stats_obj))
    return player_stats_list


def player_data_obj_to_dict(player_data_obj):
    player_data_dict = {
        "played_battles": player_data_obj.played_battles,
        "won_battles": player_data_obj.won_battles,
        "lost_battles": player_data_obj.lost_battles,
        "draw_battles": player_data_obj.draw_battles,
        "win_rate": f"{'%.2f' % (player_data_obj.win_rate * 100)}" + " %",
        "points_earned": f"{'%.0f' % player_data_obj.points_earned}" ,
        "wlr": f"{'%.2f' % player_data_obj.wlr}",
        "player_level": f"{'%.0f' % player_data_obj.player_level}",
        "battles_history": player_data_obj.battles_history,
        "player_stats": player_stats_obj_to_dict_batch(player_data_obj.player_stats)
    }
    return player_data_dict


def player_data_obj_to_dict_batch(entities_dict):
    for entity, player_data in entities_dict.items():
        entities_dict[entity] = player_data_obj_to_dict(player_data)
    return entities_dict


def ranking_dict_to_json(ranking_dict, json_path):
    json_list = list()
    converted_dict = player_data_obj_to_dict_batch(ranking_dict)
    for entity in converted_dict.keys():
        converted_dict[entity]["player"] = entity
        json_list.append(converted_dict[entity])
    
    with open(json_path, "w", encoding="utf8") as f:
        json.dump(json_list, f)


def flatten_last(players_list):
    players_list.reverse()
    flatten_list = list()
    for player in players_list:
        if player not in flatten_list:
            flatten_list.append(player)
    return flatten_list


def normalize_string_length(strings_list):
    normalized_list = list()
    max_length = 0
    for string in strings_list:
        if len(string) > max_length:
            max_length = len(string)
    max_length += 1
    for string in strings_list:
        normalized_list.append(string.ljust(max_length))
    return normalized_list


def duel_grouping(battles_list, idx_dict):
    duels_grouped = list()
    duel = battles_list[0][idx_dict["duel"]]
    duels_list = list()
    for battle in battles_list:
        if battle[idx_dict["duel"]] == duel:
            duels_list.append(battle)
        else:
            duels_grouped.append(duels_list)
            duels_list = [battle]
            duel = battle[idx_dict["duel"]]
    duels_grouped.append(duels_list)

    return duels_grouped


def event_grouping(battles_list, idx_dict):
    events_grouped = list()
    event = battles_list[0][idx_dict["event"]]
    event_list = list()
    for battle in battles_list:
        if battle[idx_dict["event"]] == event:
            event_list.append(battle)
        else:
            events_grouped.append(duel_grouping(event_list, idx_dict))
            event_list = [battle]
            event = battle[idx_dict["event"]]
    events_grouped.append(duel_grouping(event_list, idx_dict))
    return events_grouped


def get_event_characters(event_duels, battle_idx_dict):
    '''
    List of players in te event.
    '''
    characters_set = set()
    for duel in event_duels:
        characters_set.add(duel[0][battle_idx_dict["character1"]])
        characters_set.add(duel[0][battle_idx_dict["character2"]])
    characters_list = list(characters_set)
    characters_list.sort()
    return characters_list


events_type_dic = {
    "SSLT": "Seyfer Studios Lightning Tournament",
    "SSLTT": "Seyfer Studios Lightning Team Tournament",
    "SSLTSE": "Seyfer Studios Lightning Tournament Special Edition",
    "SSLL": "Seyfer Studios Lightning League"
}


def league_results(battles_list, point_system_obj, tier_list_type, platform, idx_dict):
    '''
    tier_list_type: "PL" or "CH" or "PL-CH"
    platform: "PC" or "PS4" or "union"
    '''
    entities_dict = dict()

    for battle in battles_list:
        player1 = battle[idx_dict["player1"]]
        player2 = battle[idx_dict["player2"]]
        character1 = battle[idx_dict["character1"]]
        character2 = battle[idx_dict["character2"]]
        player_character1 = player1 + "-" + character1
        player_character2 = player2 + "-" + character2

        if tier_list_type == "PL-CH":  # Players - Characters
            entity1 = player_character1
            entity2 = player_character2
        if tier_list_type == "PL":  # Players
            entity1 = player1
            entity2 = player2
        if tier_list_type == "CH":  # Characters
            entity1 = character1
            entity2 = character2

        if platform == "PC" and battle[idx_dict["platform"]] == "PC":
            player_data_generator(battle, point_system_obj, entity1, entity2, entities_dict, idx_dict)

        if platform == "PS4" and battle[idx_dict["platform"]] == "PS4":
            player_data_generator(battle, point_system_obj, entity1, entity2, entities_dict, idx_dict)

        if platform == "union":
            player_data_generator(battle, point_system_obj, entity1, entity2, entities_dict, idx_dict)

    dic = dict(sorted(entities_dict.items(), key=lambda item: item[1].player_level, reverse=True))

    results = list()
    for k, _ in dic.items():
        results.append(k)
    return results


def event_stats_generator(battles_list, json_path, idx_dict):
    events_stats_list = list()
    events_grouped = event_grouping(battles_list, idx_dict)
    events_grouped.reverse()
    for event_duels in events_grouped:
        if event_duels[0][0][idx_dict["event"]].split(" ")[0] != "SSLL": # If is a league
            events_stats_list.append({
                    "event": events_type_dic[event_duels[0][0][idx_dict["event"]].split(" ")[0]] + " " + event_duels[0][0][idx_dict["event"]].split(" ")[1],
                    "platform": event_duels[0][0][idx_dict["platform"]],
                    "players": ss_functions.calculate_event_results(event_duels, idx_dict, ss_functions.win_conditions),
                    "characters": get_event_characters(event_duels, idx_dict),
                    "playlist": event_duels[0][0][idx_dict["playlist"]],
                    "result": ss_functions.calculate_event_results(event_duels, idx_dict, ss_functions.win_conditions)
            })
        else: # If is not a league
            events_stats_list.append({
                    "event": events_type_dic[event_duels[0][0][idx_dict["event"]].split(" ")[0]] + " " + event_duels[0][0][idx_dict["event"]].split(" ")[1],
                    "platform": event_duels[0][0][idx_dict["platform"]],
                    "players": league_results(ss_functions.duels_list_to_battles_list(event_duels),
                                              point_system_obj,
                                              "PL",
                                              event_duels[0][0][idx_dict["platform"]],
                                              idx_dict),
                    "characters": get_event_characters(event_duels, idx_dict),
                    "playlist": event_duels[0][0][idx_dict["playlist"]],
                    "result": league_results(ss_functions.duels_list_to_battles_list(event_duels),
                                             point_system_obj,
                                             "PL",
                                             event_duels[0][0][idx_dict["platform"]],
                                             idx_dict)
            })

    with open(json_path, "w", encoding="utf8") as f:
        json.dump(events_stats_list, f)



''' Execution '''

fights_path = "backend/SCMdb - SSLT.csv"
fights_list, idx_dict = load_csv_fights(fights_path)

point_system_obj = point_system(240, 240, 84, 168, 240, 0, 84, 168)

type_pl_ch = "PL-CH"
type_pl = "PL"
type_ch = "CH"

entities_dict_pl_ch_pc = make_tier_lists(fights_list, point_system_obj, type_pl_ch, "PC", idx_dict)
entities_dict_pl_pc = make_tier_lists(fights_list, point_system_obj, type_pl, "PC", idx_dict)
entities_dict_ch_pc = make_tier_lists(fights_list, point_system_obj, type_ch, "PC", idx_dict)

entities_dict_pl_ch_ps4 = make_tier_lists(fights_list, point_system_obj, type_pl_ch, "PS4", idx_dict)
entities_dict_pl_ps4 = make_tier_lists(fights_list, point_system_obj, type_pl, "PS4", idx_dict)
entities_dict_ch_ps4 = make_tier_lists(fights_list, point_system_obj, type_ch, "PS4", idx_dict)

entities_dict_pl_ch_union = make_tier_lists(fights_list, point_system_obj, type_pl_ch, "union", idx_dict)
entities_dict_pl_union = make_tier_lists(fights_list, point_system_obj, type_pl, "union", idx_dict)
entities_dict_ch_union = make_tier_lists(fights_list, point_system_obj, type_ch, "union", idx_dict)

# print_results(entities_dict_pl_ch_union)

json_pl_ch_pc_path = "src/assets/data/ranking_pl_ch_pc.json"
json_pl_pc_path = "src/assets/data/ranking_pl_pc.json"
json_ch_pc_path = "src/assets/data/ranking_ch_pc.json"

json_pl_ch_ps4_path = "src/assets/data/ranking_pl_ch_ps4.json"
json_pl_ps4_path = "src/assets/data/ranking_pl_ps4.json"
json_ch_ps4_path = "src/assets/data/ranking_ch_ps4.json"

json_pl_ch_union_path = "src/assets/data/ranking_pl_ch_union.json"
json_pl_union_path = "src/assets/data/ranking_pl_union.json"
json_ch_union_path = "src/assets/data/ranking_ch_union.json"

ranking_dict_to_json(entities_dict_pl_ch_pc, json_pl_ch_pc_path)
ranking_dict_to_json(entities_dict_pl_pc, json_pl_pc_path)
ranking_dict_to_json(entities_dict_ch_pc, json_ch_pc_path)

ranking_dict_to_json(entities_dict_pl_ch_ps4, json_pl_ch_ps4_path)
ranking_dict_to_json(entities_dict_pl_ps4, json_pl_ps4_path)
ranking_dict_to_json(entities_dict_ch_ps4, json_ch_ps4_path)

ranking_dict_to_json(entities_dict_pl_ch_union, json_pl_ch_union_path)
ranking_dict_to_json(entities_dict_pl_union, json_pl_union_path)
ranking_dict_to_json(entities_dict_ch_union, json_ch_union_path)

json_event_stats_path = "src/assets/data/event_stats.json"
event_stats_generator(fights_list, json_event_stats_path, idx_dict)

# events_grouped = event_grouping(fights_list, idx_dict)

# print(len(events_grouped))

# for e in events_grouped[10]:
#     print("\n")
#     for i in e:
#         print(i)

# for e in events_grouped:
#     print(e)