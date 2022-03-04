import csv
import json
import sqlite3
from sqlite3 import Error


def load_fights(fights_path):
    '''
    Input:
        * csv files with data of fights.
    Outputs:
        * Dictionary with the data from input.
        * Dictionary with battle indexes.
    '''
    fights_dict = dict() # Output

    # csv to list
    battles_list = list()
    with open(fights_path, encoding="utf8") as f:
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

    # Duels grouping
    duel = battles_list[1][idx_dict["duel"]]
    duel_fights_list = [battles_list[1]]
    duels_list = list()
    for battle in battles_list[2:]:
        if battle[idx_dict["duel"]] == duel:
            duel_fights_list.append(battle)
        else:
            duels_list.append(duel_fights_list)
            duel = battle[idx_dict["duel"]]
            duel_fights_list = [battle]
    duels_list.append(duel_fights_list)

    # Filling fights dict
    # PC
    fights_dict["PC"] = {
        "data": {
            "events": dict(),
            "players": dict(),
            "characters": dict()
        },
        "duels": list()
    }
    # PS4
    fights_dict["PS4"] = {
        "data": {
            "events": dict(),
            "players": dict(),
            "characters": dict()
        },
        "duels": list()
    }
    # PC + PS4
    fights_dict["union"] = {
        "data": {
            "events": dict(),
            "players": dict(),
            "characters": dict()
        },
        "duels": list()
    }
    # Events
    fights_dict["events"] = dict()

    for duel in duels_list:
        # Union
        fights_dict["union"]["duels"].append(duel)
        fights_dict["union"]["data"]["events"][duel[0][idx_dict["event"]]] = {
            "playlist": duel[0][idx_dict["playlist"]],
            "brackets": duel[0][idx_dict["brackets"]]
        }
        for fight in duel:
            # Player 1
            if fights_dict["union"]["data"]["players"].get(fight[idx_dict["player1"]]):
                fights_dict["union"]["data"]["players"][fight[idx_dict["player1"]]]["events"][fight[idx_dict["event"]]] = ""
                fights_dict["union"]["data"]["players"][fight[idx_dict["player1"]]]["characters"][fight[idx_dict["character1"]]] = ""
            else:
                fights_dict["union"]["data"]["players"][fight[idx_dict["player1"]]] = {
                    "events": dict(),
                    "characters": dict()
                }
            # Player 2
            if fights_dict["union"]["data"]["players"].get(fight[idx_dict["player2"]]):
                fights_dict["union"]["data"]["players"][fight[idx_dict["player2"]]]["events"][fight[idx_dict["event"]]] = ""
                fights_dict["union"]["data"]["players"][fight[idx_dict["player2"]]]["characters"][fight[idx_dict["character2"]]] = ""
            else:
                fights_dict["union"]["data"]["players"][fight[idx_dict["player2"]]] = {
                    "events": dict(),
                    "characters": dict()
                }
            # Character 1
            if fights_dict["union"]["data"]["characters"].get(fight[idx_dict["character1"]]):
                fights_dict["union"]["data"]["characters"][fight[idx_dict["character1"]]]["events"][fight[idx_dict["event"]]] = ""
                fights_dict["union"]["data"]["characters"][fight[idx_dict["character1"]]]["players"][fight[idx_dict["player1"]]] = ""
            else:
                fights_dict["union"]["data"]["characters"][fight[idx_dict["character1"]]] = {
                    "events": dict(),
                    "players": dict()
                }
            # Character 2
            if fights_dict["union"]["data"]["characters"].get(fight[idx_dict["character2"]]):
                fights_dict["union"]["data"]["characters"][fight[idx_dict["character2"]]]["events"][fight[idx_dict["event"]]] = ""
                fights_dict["union"]["data"]["characters"][fight[idx_dict["character2"]]]["players"][fight[idx_dict["player2"]]] = ""
            else:
                fights_dict["union"]["data"]["characters"][fight[idx_dict["character2"]]] = {
                    "events": dict(),
                    "players": dict()
                }

        # PC
        if duel[0][idx_dict["platform"]] == "PC":
            fights_dict["PC"]["duels"].append(duel)
            fights_dict["PC"]["data"]["events"][duel[0][idx_dict["event"]]] = {
                "playlist": duel[0][idx_dict["playlist"]],
                "brackets": duel[0][idx_dict["brackets"]]
            }
            for fight in duel:
                # Player 1
                if fights_dict["PC"]["data"]["players"].get(fight[idx_dict["player1"]]):
                    fights_dict["PC"]["data"]["players"][fight[idx_dict["player1"]]]["events"][fight[idx_dict["event"]]] = ""
                    fights_dict["PC"]["data"]["players"][fight[idx_dict["player1"]]]["characters"][fight[idx_dict["character1"]]] = ""
                else:
                    fights_dict["PC"]["data"]["players"][fight[idx_dict["player1"]]] = {
                        "events": dict(),
                        "characters": dict()
                    }
                # Player 2
                if fights_dict["PC"]["data"]["players"].get(fight[idx_dict["player2"]]):
                    fights_dict["PC"]["data"]["players"][fight[idx_dict["player2"]]]["events"][fight[idx_dict["event"]]] = ""
                    fights_dict["PC"]["data"]["players"][fight[idx_dict["player2"]]]["characters"][fight[idx_dict["character2"]]] = ""
                else:
                    fights_dict["PC"]["data"]["players"][fight[idx_dict["player2"]]] = {
                        "events": dict(),
                        "characters": dict()
                    }
                # Character 1
                if fights_dict["PC"]["data"]["characters"].get(fight[idx_dict["character1"]]):
                    fights_dict["PC"]["data"]["characters"][fight[idx_dict["character1"]]]["events"][fight[idx_dict["event"]]] = ""
                    fights_dict["PC"]["data"]["characters"][fight[idx_dict["character1"]]]["players"][fight[idx_dict["player1"]]] = ""
                else:
                    fights_dict["PC"]["data"]["characters"][fight[idx_dict["character1"]]] = {
                        "events": dict(),
                        "players": dict()
                    }
                # Character 2
                if fights_dict["PC"]["data"]["characters"].get(fight[idx_dict["character2"]]):
                    fights_dict["PC"]["data"]["characters"][fight[idx_dict["character2"]]]["events"][fight[idx_dict["event"]]] = ""
                    fights_dict["PC"]["data"]["characters"][fight[idx_dict["character2"]]]["players"][fight[idx_dict["player2"]]] = ""
                else:
                    fights_dict["PC"]["data"]["characters"][fight[idx_dict["character2"]]] = {
                        "events": dict(),
                        "players": dict()
                    }

        # PS4
        if duel[0][idx_dict["platform"]] == "PS4":
            fights_dict["PS4"]["duels"].append(duel)
            fights_dict["PS4"]["data"]["events"][duel[0][idx_dict["event"]]] = {
                "playlist": duel[0][idx_dict["playlist"]],
                "brackets": duel[0][idx_dict["brackets"]]
            }
            for fight in duel:
                # Player 1
                if fights_dict["PS4"]["data"]["players"].get(fight[idx_dict["player1"]]):
                    fights_dict["PS4"]["data"]["players"][fight[idx_dict["player1"]]]["events"][fight[idx_dict["event"]]] = ""
                    fights_dict["PS4"]["data"]["players"][fight[idx_dict["player1"]]]["characters"][fight[idx_dict["character1"]]] = ""
                else:
                    fights_dict["PS4"]["data"]["players"][fight[idx_dict["player1"]]] = {
                        "events": dict(),
                        "characters": dict()
                    }
                # Player 2
                if fights_dict["PS4"]["data"]["players"].get(fight[idx_dict["player2"]]):
                    fights_dict["PS4"]["data"]["players"][fight[idx_dict["player2"]]]["events"][fight[idx_dict["event"]]] = ""
                    fights_dict["PS4"]["data"]["players"][fight[idx_dict["player2"]]]["characters"][fight[idx_dict["character2"]]] = ""
                else:
                    fights_dict["PS4"]["data"]["players"][fight[idx_dict["player2"]]] = {
                        "events": dict(),
                        "characters": dict()
                    }
                # Character 1
                if fights_dict["PS4"]["data"]["characters"].get(fight[idx_dict["character1"]]):
                    fights_dict["PS4"]["data"]["characters"][fight[idx_dict["character1"]]]["events"][fight[idx_dict["event"]]] = ""
                    fights_dict["PS4"]["data"]["characters"][fight[idx_dict["character1"]]]["players"][fight[idx_dict["player1"]]] = ""
                else:
                    fights_dict["PS4"]["data"]["characters"][fight[idx_dict["character1"]]] = {
                        "events": dict(),
                        "players": dict()
                    }
                # Character 2
                if fights_dict["PS4"]["data"]["characters"].get(fight[idx_dict["character2"]]):
                    fights_dict["PS4"]["data"]["characters"][fight[idx_dict["character2"]]]["events"][fight[idx_dict["event"]]] = ""
                    fights_dict["PS4"]["data"]["characters"][fight[idx_dict["character2"]]]["players"][fight[idx_dict["player2"]]] = ""
                else:
                    fights_dict["PS4"]["data"]["characters"][fight[idx_dict["character2"]]] = {
                        "events": dict(),
                        "players": dict()
                    }

        # Events
        if fights_dict["events"].get(duel[0][idx_dict["event"]]):
            fights_dict["events"][duel[0][idx_dict["event"]]]["duels"].append(duel)
            fights_dict["events"][duel[0][idx_dict["event"]]]["data"]["playlist"] = duel[0][idx_dict["playlist"]]
            fights_dict["events"][duel[0][idx_dict["event"]]]["data"]["brackets"] = duel[0][idx_dict["brackets"]]
        else:
            fights_dict["events"][duel[0][idx_dict["event"]]] = {
                "data": dict(),
                "duels": [duel]
            }

    fights_dict["players"] = dict()
    players_set = set()
    characters_set = set()
    for battle in battles_list:
        players_set.add(battle[idx_dict["player1"]])
        players_set.add(battle[idx_dict["player2"]])
        characters_set.add(battle[idx_dict["character1"]])
        characters_set.add(battle[idx_dict["character2"]])
    

    return fights_dict, idx_dict


class point_system:
    def __init__(self,
                 pw, # perfect win
                 w, # win
                 d, # draw
                 pl, # perfect lose
                 lb, # lose blue
                 ly): # lose yellow
        self.pw = pw
        self.w = w
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
            self.p1_beating_factor = 0.1
        else:
            self.p1_beating_factor = self.p1_won_rounds / self.rounds_played
        if self.p2_won_rounds == 0:
            self.p2_beating_factor = 0.1
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

    def generate_battle_data(self, p1_win_rate, p2_win_rate, event, video):
        self.calculate_rounds_played()
        self.calculate_beating_factors()
        self.calculate_won_points(p1_win_rate, p2_win_rate)
        self.calculate_result()
        self.generate_history(event, video)


def battle_data_generator(battle, point_system_obj, player1_win_rate, player2_win_rate, extras):
    battle_data_obj = battle_data(p1_won_rounds=0,
                                  p2_won_rounds = 0,
                                  p1_raw_points = 0,
                                  p2_raw_points = 0,
                                  p1_won_points = 0,
                                  p2_won_points = 0,
                                  rounds_played = 0,
                                  p1_beating_factor = 0,
                                  p2_beating_factor = 0,
                                  p1_lvl_factor = 0,
                                  p2_lvl_factor = 0,
                                  p1_win = 0,
                                  p2_win = 0,
                                  draw = 0,
                                  p1_history = 0,
                                  p2_history = 0)
    for i in range(5):
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

    battle_data_obj.generate_battle_data(player1_win_rate, player2_win_rate, extras["event"], extras["video"])

    return battle_data_obj


class duel_data:
    def __init__(self,
                 p1_won_fights,
                 p2_won_fights,
                 fights_played,
                 p1_raw_points,
                 p2_raw_points,
                 p1_beating_factor,
                 p2_beating_factor,
                 p1_lvl_factor,
                 p2_lvl_factor,
                 p1_won_points,
                 p2_won_points,
                 p1_win,
                 p2_win,
                 draw,
                 p1_history,
                 p2_history,
                 duel_format):
        self.p1_won_fights = p1_won_fights
        self.p2_won_fights = p2_won_fights
        self.fights_played = fights_played
        self.p1_raw_points = p1_raw_points
        self.p2_raw_points = p2_raw_points
        self.p1_beating_factor = p1_beating_factor
        self.p2_beating_factor = p2_beating_factor
        self.p1_lvl_factor = p1_lvl_factor
        self.p2_lvl_factor = p2_lvl_factor
        self.p1_won_points = p1_won_points
        self.p2_won_points = p2_won_points
        self.p1_win = p1_win
        self.p2_win = p2_win
        self.draw = draw
        self.p1_history = p1_history
        self.p2_history = p2_history
        self.duel_format = duel_format
    
    def calculate_fights_played(self):
        self.fights_played = self.p1_won_fights + self.p2_won_fights

    def calculate_beating_factors(self):
        if self.p1_won_fights == 0:
            self.p1_beating_factor = (1/self.fights_played)/2
        else:
            self.p1_beating_factor = self.p1_won_fights / self.fights_played
        if self.p2_won_fights == 0:
            self.p2_beating_factor = (1/self.fights_played)/2
        else:
            self.p2_beating_factor = self.p2_won_fights / self.fights_played
    
    def calculate_lvl_factors(self, p1_win_rate, p2_win_rate):
        b = 1
        a = -(14269091/261469091)
        self.p1_lvl_factor = a*(p1_win_rate - p2_win_rate) + b
        self.p2_lvl_factor = a*(p2_win_rate - p1_win_rate) + b

    def calculate_won_points(self, p1_win_rate, p2_win_rate):
        self.calculate_lvl_factors(p1_win_rate, p2_win_rate)
        self.p1_won_points = self.p1_raw_points * self.p1_beating_factor * self.p1_lvl_factor
        self.p2_won_points = self.p2_raw_points * self.p2_beating_factor * self.p2_lvl_factor

    def calculate_result(self):
        if self.p1_won_fights > self.p2_won_fights:  # Player 1 won
            self.p1_win = True
            self.p2_win = False
            self.draw = False
            self.p1_history = {"result": "Victory"}
            self.p2_history = {"result": "Defeat"}
        elif self.p2_won_fights > self.p1_won_fights:  # Player 2 won
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

    def get_duel_format(self):
        self.duel_format = "FT" + str(max(self.p1_won_fights, self.p2_won_fights))

    def generate_history(self, event, video):
        self.p1_history["duel_format"] = self.duel_format
        self.p1_history["won_fights"] = self.p1_won_fights
        self.p1_history["played_fights"] = self.fights_played
        self.p1_history["raw_points"] = f"{'%.0f' % self.p1_raw_points}"
        self.p1_history["beating_factor"] = f"{'%.2f' % self.p1_beating_factor}"
        self.p1_history["lvl_factor"] = f"{'%.2f' % self.p1_lvl_factor}"
        self.p1_history["won_points"] = f"{'%.0f' % self.p1_won_points}"
        self.p1_history["event"] = event
        self.p1_history["video"] = video

        self.p2_history["duel_format"] = self.duel_format
        self.p2_history["won_fights"] = self.p2_won_fights
        self.p2_history["played_fights"] = self.fights_played
        self.p2_history["raw_points"] = f"{'%.0f' % self.p2_raw_points}"
        self.p2_history["beating_factor"] = f"{'%.2f' % self.p2_beating_factor}"
        self.p2_history["lvl_factor"] = f"{'%.2f' % self.p2_lvl_factor}"
        self.p2_history["won_points"] = f"{'%.0f' % self.p2_won_points}"
        self.p2_history["event"] = event
        self.p2_history["video"] = video

    def generate_duel_data(self, p1_win_rate, p2_win_rate, event, video):
        self.calculate_fights_played()
        self.calculate_beating_factors()
        self.calculate_won_points(p1_win_rate, p2_win_rate)
        self.calculate_result()
        self.get_duel_format()
        self.generate_history(event, video)


def duel_data_generator(ranking_dict, fights_list, point_system_obj, player1, player2, idx_dict, player):
    duel_data_obj = duel_data(
        p1_won_fights = 0,
        p2_won_fights = 0,
        fights_played = 0,
        p1_raw_points = 0,
        p2_raw_points = 0,
        p1_beating_factor = 0,
        p2_beating_factor = 0,
        p1_lvl_factor = 0,
        p2_lvl_factor = 0,
        p1_won_points = 0,
        p2_won_points = 0,
        p1_win = 0,
        p2_win = 0,
        draw = 0,
        p1_history = 0,
        p2_history = 0,
        duel_format = 0
    )
    for fight in fights_list:
        if fight[idx_dict["player1"]] != player1:
            player1 = fight[idx_dict["player2"]]
            player2 = fight[idx_dict["player1"]]
            battle = [
                fight[idx_dict["r1_p2"]],
                fight[idx_dict["r2_p2"]],
                fight[idx_dict["r3_p2"]],
                fight[idx_dict["r4_p2"]],
                fight[idx_dict["r5_p2"]],
                fight[idx_dict["r1_p1"]],
                fight[idx_dict["r2_p1"]],
                fight[idx_dict["r3_p1"]],
                fight[idx_dict["r4_p1"]],
                fight[idx_dict["r5_p1"]]
            ]
        else:
            battle = [
                fight[idx_dict["r1_p1"]],
                fight[idx_dict["r2_p1"]],
                fight[idx_dict["r3_p1"]],
                fight[idx_dict["r4_p1"]],
                fight[idx_dict["r5_p1"]],
                fight[idx_dict["r1_p2"]],
                fight[idx_dict["r2_p2"]],
                fight[idx_dict["r3_p2"]],
                fight[idx_dict["r4_p2"]],
                fight[idx_dict["r5_p2"]]
            ]
        extras = {
            "event": fight[idx_dict["event"]],
            "video": fight[idx_dict["media"]]
        }
        battle_data_obj = battle_data_generator(battle,
                                                point_system_obj,
                                                ranking_dict[player1].fights_win_rate,
                                                ranking_dict[player2].fights_win_rate,
                                                extras)

        if battle_data_obj.p1_win:
            ranking_dict[player1].won_battles += 1
            ranking_dict[player2].lost_battles += 1
            ranking_dict[player1].player_stats[player2].won_battles += 1
            ranking_dict[player2].player_stats[player1].lost_battles += 1
            duel_data_obj.p1_won_fights += 1
            

        if battle_data_obj.p2_win:
            ranking_dict[player1].lost_battles += 1
            ranking_dict[player2].won_battles += 1
            ranking_dict[player2].player_stats[player1].won_battles += 1
            ranking_dict[player1].player_stats[player2].lost_battles += 1
            duel_data_obj.p2_won_fights += 1
            

        if battle_data_obj.draw:
            ranking_dict[player1].draw_battles += 1
            ranking_dict[player2].draw_battles += 1
            ranking_dict[player1].player_stats[player2].draw_battles += 1
            ranking_dict[player2].player_stats[player1].draw_battles += 1

        ranking_dict[player1].played_battles += 1
        ranking_dict[player2].played_battles += 1
        ranking_dict[player1].calculate_win_rate_fights()
        ranking_dict[player2].calculate_win_rate_fights()
        ranking_dict[player1].calculate_wlr_fights()
        ranking_dict[player2].calculate_wlr_fights()
        # ranking_dict[player1].calculate_player_lvl(player)
        # ranking_dict[player2].calculate_player_lvl(player)
        ranking_dict[player1].add_to_history(battle_data_obj.p1_history, player2)
        ranking_dict[player2].add_to_history(battle_data_obj.p2_history, player1)

        ranking_dict[player1].player_stats[player2].played_battles += 1
        ranking_dict[player2].player_stats[player1].played_battles += 1
        ranking_dict[player1].player_stats[player2].calculate_win_rate()
        ranking_dict[player2].player_stats[player1].calculate_win_rate()

        duel_data_obj.p1_raw_points += battle_data_obj.p1_won_points
        duel_data_obj.p2_raw_points += battle_data_obj.p2_won_points

    duel_data_obj.generate_duel_data(ranking_dict[player1].duels_win_rate, ranking_dict[player2].duels_win_rate, extras["event"], extras["video"])

    return duel_data_obj 
  

class player_data:
    def __init__(self,
                 played_duels,
                 won_duels,
                 lost_duels,
                 duels_win_rate,
                 wlr_duels,
                 played_battles,
                 won_battles,
                 lost_battles,
                 draw_battles,
                 fights_win_rate,
                 wlr_fights,
                 points_earned,
                 player_level,
                 duels_history,
                 battles_history,
                 player_stats):
        # Duels
        self.played_duels = played_duels
        self.won_duels = won_duels
        self.lost_duels = lost_duels
        self.duels_win_rate = duels_win_rate
        self.wlr_duels = wlr_duels
        # Fights
        self.played_battles = played_battles
        self.won_battles = won_battles
        self.lost_battles = lost_battles
        self.draw_battles = draw_battles
        self.fights_win_rate = fights_win_rate
        self.wlr_fights = wlr_fights
        # Points
        self.points_earned = points_earned
        self.player_level = player_level
        # Histories
        self.duels_history = duels_history
        self.battles_history = battles_history
        self.player_stats = player_stats

    def calculate_win_rate_fights(self):
        self.fights_win_rate = self.won_battles / self.played_battles

    def calculate_win_rate_duels(self):
        self.duels_win_rate = self.won_duels / self.played_duels

    def calculate_wlr_fights(self):
        if self.lost_battles == 0:
            self.wlr_fights = self.won_battles + (self.draw_battles / 2)
        elif self.won_battles == 0:
            self.wlr_fights = (1 + (self.draw_battles / 2)) / self.lost_battles
        else:
            self.wlr_fights = (self.won_battles + (self.draw_battles / 2)) / self.lost_battles

    def calculate_wlr_duels(self):
        if self.lost_duels == 0:
            self.wlr_duels = self.won_duels
        elif self.won_duels == 0:
            self.wlr_duels = 1 / self.lost_duels
        else:
            self.wlr_duels = self.won_duels / self.lost_duels

    def calculate_player_lvl(self, player):
        if player:
            self.player_level = self.points_earned * self.wlr_duels * self.wlr_fights
        else:
            self.player_level = self.points_earned * self.wlr_fights

    def add_to_history(self, battle, rival):
        battle["rival"] = rival
        self.battles_history.append(battle)


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


def flatten_duels(duels_list):
    fights_list = list()
    for duel in duels_list:
        fights_list += duel
    return fights_list


def player_data_generator(ranking_dict, fight, entity1, entity2, point_system_obj, player):
    # Entity 1
    if entity1 not in ranking_dict:
        ranking_dict[entity1] = player_data(played_duels = 0,
                                            won_duels = 0,
                                            lost_duels = 0,
                                            duels_win_rate = 0,
                                            wlr_duels = 0,
                                            played_battles = 0,
                                            won_battles = 0,
                                            lost_battles = 0,
                                            draw_battles = 0,
                                            fights_win_rate = 0,
                                            wlr_fights = 0,
                                            points_earned = 0,
                                            player_level = 0,
                                            duels_history = 0,
                                            battles_history = [],
                                            player_stats = {entity2: player_stats(0, 0, 0, 0, 0)})
    elif entity2 not in ranking_dict[entity1].player_stats:
        ranking_dict[entity1].player_stats[entity2] = player_stats(0, 0, 0, 0, 0)

    # Entity 2
    if entity2 not in ranking_dict:
        ranking_dict[entity2] = player_data(played_duels = 0,
                                            won_duels = 0,
                                            lost_duels = 0,
                                            duels_win_rate = 0,
                                            wlr_duels = 0,
                                            played_battles = 0,
                                            won_battles = 0,
                                            lost_battles = 0,
                                            draw_battles = 0,
                                            fights_win_rate = 0,
                                            wlr_fights = 0,
                                            points_earned = 0,
                                            player_level = 0,
                                            duels_history = 0,
                                            battles_history = [],
                                            player_stats = {entity1: player_stats(0, 0, 0, 0, 0)})
    elif entity1 not in ranking_dict[entity2].player_stats:
        ranking_dict[entity2].player_stats[entity1] = player_stats(0, 0, 0, 0, 0)

    if player:
        duel_data_obj = duel_data_generator(ranking_dict, fight, point_system_obj, entity1, entity2, idx_dict, player)

        if duel_data_obj.p1_win:
            ranking_dict[entity1].won_duels += 1
            ranking_dict[entity2].lost_duels += 1

        if duel_data_obj.p2_win:
            ranking_dict[entity1].lost_duels += 1
            ranking_dict[entity2].won_duels += 1

        ranking_dict[entity1].played_duels += 1
        ranking_dict[entity2].played_duels += 1
        ranking_dict[entity1].calculate_win_rate_duels()
        ranking_dict[entity2].calculate_win_rate_duels()
        ranking_dict[entity1].calculate_wlr_duels()
        ranking_dict[entity2].calculate_wlr_duels()

        ranking_dict[entity1].points_earned += duel_data_obj.p1_won_points
        ranking_dict[entity2].points_earned += duel_data_obj.p2_won_points
        ranking_dict[entity1].calculate_player_lvl(player)
        ranking_dict[entity2].calculate_player_lvl(player)
    else:
        battle = [
            fight[idx_dict["r1_p1"]],
            fight[idx_dict["r2_p1"]],
            fight[idx_dict["r3_p1"]],
            fight[idx_dict["r4_p1"]],
            fight[idx_dict["r5_p1"]],
            fight[idx_dict["r1_p2"]],
            fight[idx_dict["r2_p2"]],
            fight[idx_dict["r3_p2"]],
            fight[idx_dict["r4_p2"]],
            fight[idx_dict["r5_p2"]]
        ]
        extras = {
            "event": fight[idx_dict["event"]],
            "video": fight[idx_dict["media"]]
        }
        battle_data_obj = battle_data_generator(battle,
                                                point_system_obj,
                                                ranking_dict[entity1].fights_win_rate,
                                                ranking_dict[entity2].fights_win_rate,
                                                extras)

        if battle_data_obj.p1_win:
            ranking_dict[entity1].won_battles += 1
            ranking_dict[entity2].lost_battles += 1
            ranking_dict[entity1].player_stats[entity2].won_battles += 1
            ranking_dict[entity2].player_stats[entity1].lost_battles += 1

        if battle_data_obj.p2_win:
            ranking_dict[entity1].lost_battles += 1
            ranking_dict[entity2].won_battles += 1
            ranking_dict[entity2].player_stats[entity1].won_battles += 1
            ranking_dict[entity1].player_stats[entity2].lost_battles += 1

        if battle_data_obj.draw:
            ranking_dict[entity1].draw_battles += 1
            ranking_dict[entity2].draw_battles += 1
            ranking_dict[entity1].player_stats[entity2].draw_battles += 1
            ranking_dict[entity2].player_stats[entity1].draw_battles += 1

        ranking_dict[entity1].points_earned += battle_data_obj.p1_won_points
        ranking_dict[entity2].points_earned += battle_data_obj.p2_won_points
        ranking_dict[entity1].played_battles += 1
        ranking_dict[entity2].played_battles += 1
        ranking_dict[entity1].calculate_win_rate_fights()
        ranking_dict[entity2].calculate_win_rate_fights()
        ranking_dict[entity1].calculate_wlr_fights()
        ranking_dict[entity2].calculate_wlr_fights()
        ranking_dict[entity1].calculate_player_lvl(player)
        ranking_dict[entity2].calculate_player_lvl(player)
        ranking_dict[entity1].add_to_history(battle_data_obj.p1_history, entity2)
        ranking_dict[entity2].add_to_history(battle_data_obj.p2_history, entity1)

        ranking_dict[entity1].player_stats[entity2].played_battles += 1
        ranking_dict[entity2].player_stats[entity1].played_battles += 1
        ranking_dict[entity1].player_stats[entity2].calculate_win_rate()
        ranking_dict[entity2].player_stats[entity1].calculate_win_rate()


def make_rankings_PlCh(duels_list, idx_dict, point_system_obj):
    ranking_plch = dict()
    fights_list = flatten_duels(duels_list)
    for fight in fights_list:
        pl_ch1 = fight[idx_dict["player1"]] + "-" + fight[idx_dict["character1"]]
        pl_ch2 = fight[idx_dict["player2"]] + "-" + fight[idx_dict["character2"]]
        player_data_generator(ranking_plch, fight, pl_ch1, pl_ch2, point_system_obj, False)

    result = dict(sorted(ranking_plch.items(), key=lambda item: item[1].player_level, reverse=True))
    for k, v in result.items():
        print(k, v.points_earned, v.wlr_fights, v.wlr_duels, v.player_level)
    return dict(sorted(ranking_plch.items(), key=lambda item: item[1].player_level, reverse=True))


def make_rankings_Pl(duels_list, idx_dict, point_system_obj):
    ranking_plch = dict()
    # fights_list = flatten_duels(duels_list)
    for duel in duels_list:
        player1 = duel[0][idx_dict["player1"]]
        player2 = duel[0][idx_dict["player2"]]
        # player1 = duel[idx_dict["player1"]]
        # player2 = duel[idx_dict["player2"]]
        player_data_generator(ranking_plch, duel, player1, player2, point_system_obj, True)

    result = dict(sorted(ranking_plch.items(), key=lambda item: item[1].player_level, reverse=True))
    for k, v in result.items():
        # print(k, v.points_earned, v.wlr_fights, v.wlr_duels, v.player_level, v.wlr_duels*v.wlr_fights, v.duels_win_rate, v.fights_win_rate)
        print(k, v.duels_win_rate, v.fights_win_rate)
        for pl, stat in v.player_stats.items():
            print("\t" ,pl, stat.win_rate)
    return dict(sorted(ranking_plch.items(), key=lambda item: item[1].player_level, reverse=True))


def make_rankings(fights_dict, idx_dict, point_system_obj):
    rankings_dict = {"PC": {},
                     "PS4": {},
                     "union": {}
    }

    rankings_dict["PC"]["PL+CH"] = make_rankings_PlCh(fights_dict["PC"], idx_dict, point_system_obj)
    rankings_dict["PC"]["PL"] = make_rankings_Pl(fights_dict["PC"], idx_dict, point_system_obj)
    # rankings_dict["PC"]["CH"] = make_rankings_Ch(fights_dict["PC"], idx_dict, point_system_obj)

    # rankings_dict["PS4"]["PL+CH"] = make_rankings_PlCh(fights_dict["PS4"], idx_dict, point_system_obj)
    # rankings_dict["PS4"]["PL"] = make_rankings_Pl(fights_dict["PS4"], idx_dict, point_system_obj)
    # rankings_dict["PS4"]["CH"] = make_rankings_Ch(fights_dict["PS4"], idx_dict, point_system_obj)

    # rankings_dict["union"]["PL+CH"] = make_rankings_PlCh(fights_dict["union"], idx_dict, point_system_obj)
    # rankings_dict["union"]["PL"] = make_rankings_Pl(fights_dict["union"], idx_dict, point_system_obj)
    # rankings_dict["union"]["CH"] = make_rankings_Ch(fights_dict["union"], idx_dict, point_system_obj)

    return rankings_dict


''' ----------------------------------------------------------------------------- '''

fights_path = "backend/SCMdb - SSLT.csv"
fights_dict, idx_dict = load_fights(fights_path)

point_system_obj = point_system(
    w = 240,
    pw = 240,
    d = 240,
    pl = 0,
    lb = 84,
    ly = 168
)

# make_rankings_PlCh(fights_dict["PC"], idx_dict, point_system_obj)
# make_rankings_Pl(fights_dict["events"]["SSLT 7"], idx_dict, point_system_obj)

json_path = "backend/json.json"
with open(json_path, "w", encoding="utf8") as f:
    json.dump(fights_dict, f)