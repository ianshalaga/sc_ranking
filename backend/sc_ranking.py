import csv
import json



def load_csv_fights(csv_fights_path):
    battles_list = list()
    battles_pc_count = 0
    battles_ps4_count = 0
    battles_count = 0
    with open(csv_fights_path, encoding="utf8") as f:
        csv_reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL)
        for battle in csv_reader:
            if battle[-1] == "Media":
                continue
            for e in range(len(battle)):
                if battle[e] == "0":
                    battle[e] = 0
            battles_list.append(battle)
            battles_count += 1
            if battle[-2] == "PC":
                battles_pc_count += 1
            if battle[-2] == "PS4":
                battles_ps4_count += 1
        print(f"Combates en PC: {battles_pc_count}")
        print(f"Combates en PS4: {battles_ps4_count}")
        print(f"Combates totales: {battles_count}")
    return battles_list


class point_system:
    def __init__(self,
                 pw,
                 w,
                 d,
                 pl,
                 lb,
                 ly):
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

    def calculate_won_points(self):
        self.p1_won_points = self.p1_raw_points * self.p1_beating_factor
        self.p2_won_points = self.p2_raw_points * self.p2_beating_factor

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
        self.p1_history["won_points"] = f"{'%.0f' % self.p1_won_points}"
        self.p1_history["event"] = event
        self.p1_history["video"] = video

        self.p2_history["won_rounds"] = self.p2_won_rounds
        self.p2_history["played_rounds"] = self.rounds_played
        self.p2_history["raw_points"] = f"{'%.0f' % self.p2_raw_points}"
        self.p2_history["beating_factor"] = f"{'%.2f' % self.p2_beating_factor}"
        self.p2_history["won_points"] = f"{'%.0f' % self.p2_won_points}"
        self.p2_history["event"] = event
        self.p2_history["video"] = video


def battle_data_generator(battle, point_system_obj):
    battle_data_obj = battle_data(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    for i in range(5): # int(len(battle)/2)
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
    battle_data_obj.calculate_won_points()
    battle_data_obj.calculate_result()
    battle_data_obj.generate_history(battle[-3], battle[-1])

    return battle_data_obj


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
                 battles_history):
        self.played_battles = played_battles
        self.won_battles = won_battles
        self.lost_battles = lost_battles
        self.draw_battles = draw_battles
        self.points_earned = points_earned
        self.win_rate = win_rate
        self.player_level = player_level
        self.wlr = wlr  # Wins / Loss Ratio
        self.battles_history = battles_history

    def calculate_win_rate(self):
        self.win_rate = self.won_battles / self.played_battles

    def calculate_wlr(self):
        if self.lost_battles == 0:
            self.wlr = self.won_battles
        elif self.won_battles == 0:
            self.wlr = 1 / self.lost_battles
        else:
            self.wlr = self.won_battles / self.lost_battles

    def calculate_player_lvl(self):
        self.player_level = self.wlr * self.points_earned

    def add_to_history(self, battle, rival):
        battle["rival"] = rival
        self.battles_history.append(battle)


def player_data_generator(battle, point_system_obj, entity1, entity2, entities_dict):
    battle_list = battle[4:]
    battle_data_obj = battle_data_generator(battle_list, point_system_obj)

    if entity1 not in entities_dict:
        entities_dict[entity1] = player_data(0, 0, 0, 0, 0, 0, 0, 0, [])
    if entity2 not in entities_dict:
        entities_dict[entity2] = player_data(0, 0, 0, 0, 0, 0, 0, 0, [])

    if battle_data_obj.p1_win:
        entities_dict[entity1].won_battles += 1
        entities_dict[entity2].lost_battles += 1

    if battle_data_obj.p2_win:
        entities_dict[entity1].lost_battles += 1
        entities_dict[entity2].won_battles += 1

    # if battle_data_obj.draw:
    #     entities_dict[entity1].draw_battles += 1
    #     entities_dict[entity2].draw_battles += 1

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


def make_tier_lists(battles_list, point_system_obj, tier_list_type, platform):
    '''
    tier_list_type: "PL" or "CH" or "PL-CH"
    platform: "PC" or "PS4" or "union"
    '''
    entities_dict = dict()

    for battle in battles_list:
        player1 = battle[0]
        player2 = battle[2]
        character1 = battle[1]
        character2 = battle[3]
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

        if platform == "PC" and battle[-2] == "PC":
            player_data_generator(battle, point_system_obj, entity1, entity2, entities_dict)

        if platform == "PS4" and battle[-2] == "PS4":
            player_data_generator(battle, point_system_obj, entity1, entity2, entities_dict)

        if platform == "union":
            player_data_generator(battle, point_system_obj, entity1, entity2, entities_dict)

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


def player_data_obj_to_dict(player_data_obj):
    player_data_dict = {
        "played_battles": player_data_obj.played_battles,
        "won_battles": player_data_obj.won_battles,
        "lost_battles": player_data_obj.lost_battles,
        "draw_battles": player_data_obj.draw_battles,
        "win_rate": f"{'%.0f' % (player_data_obj.win_rate * 100)}" + " %",
        "points_earned": f"{'%.0f' % player_data_obj.points_earned}" ,
        "wlr": f"{'%.2f' % player_data_obj.wlr}",
        "player_level": f"{'%.0f' % player_data_obj.player_level}",
        "battles_history": player_data_obj.battles_history
    }
    return player_data_dict


def player_data_obj_to_dict_batch(entities_dict):
    for entity, player_data in entities_dict.items():
        entities_dict[entity] = player_data_obj_to_dict(player_data)
    return entities_dict


def ranking_dict_to_json(ranking_dict, json_path):
    json_list = list()
    converted_dict = player_data_obj_to_dict_batch(ranking_dict)
    for entity, player_data in converted_dict.items():
        converted_dict[entity]["player"] = entity
        json_list.append(converted_dict[entity])
    
    with open(json_path, "w", encoding="utf8") as f:
        json.dump(json_list, f)



''' Execution '''

fights_path = "backend/SCMdb - SSLT.csv"
fights_list = load_csv_fights(fights_path)

point_system_obj = point_system(240, 240, 240, 0, 84, 168)

type_pl_ch = "PL-CH"
type_pl = "PL"
type_ch = "CH"

entities_dict_pl_ch_pc = make_tier_lists(fights_list, point_system_obj, type_pl_ch, "PC")
entities_dict_pl_pc = make_tier_lists(fights_list, point_system_obj, type_pl, "PC")
entities_dict_ch_pc = make_tier_lists(fights_list, point_system_obj, type_ch, "PC")

entities_dict_pl_ch_ps4 = make_tier_lists(fights_list, point_system_obj, type_pl_ch, "PS4")
entities_dict_pl_ps4 = make_tier_lists(fights_list, point_system_obj, type_pl, "PS4")
entities_dict_ch_ps4 = make_tier_lists(fights_list, point_system_obj, type_ch, "PS4")

entities_dict_pl_ch_union = make_tier_lists(fights_list, point_system_obj, type_pl_ch, "union")
entities_dict_pl_union = make_tier_lists(fights_list, point_system_obj, type_pl, "union")
entities_dict_ch_union = make_tier_lists(fights_list, point_system_obj, type_ch, "union")

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