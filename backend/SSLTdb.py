import sqlite3
from sqlite3 import Error
from termcolor import colored
import ss_functions as ssf


code_names_dict = {
    "Soul Calibur VI": "SCVI",
    "PC": "Personal Computer",
    "PS4": "PlayStation 4",
    "SAS": "South America South",
    "SSLT": "Seyfer Studios Lightning Tournament",
    "SSLTT": "Seyfer Studios Lightning Team Tournament",
    "SSLTSE": "Seyfer Studios Lightning Tournament Special Edition",
    "SSLL": "Seyfer Studios Lightning League",
    "FT2": "First to 2",
    "FT3": "First to 3",
    "First to 2": "BO3",
    "First to 3": "BO5",
    "BO3": "Best of 3",
    "BO5": "Best of 5",
}

players_dict = {
    "DonMarlboro": "https://www.youtube.com/playlist?list=PL90QAKwVH1t4WgGCJqRtV4uHlajcSHAip",
    "Karol": "https://www.youtube.com/playlist?list=PL90QAKwVH1t4_84l7sweKXqbAxBUCD6Wb",
    "Sigfrancis": "https://www.youtube.com/playlist?list=PL90QAKwVH1t6fRaOJPS84khrnPhlKodB7",
    "Camus": "https://www.youtube.com/playlist?list=PL90QAKwVH1t5F3cOnsi0LEWya5FztxGTw",
    "Junixart": "https://www.youtube.com/playlist?list=PL90QAKwVH1t6cPJEfOvbZ4ewYT0xfyzeR",
    "zen-x": "https://www.youtube.com/playlist?list=PL90QAKwVH1t5iVwDcfNHJ30ORntTWE_Mt",
    "Eche": "https://www.youtube.com/playlist?list=PL90QAKwVH1t5EMa0pEOZbWuhnhCP1ZAWq",
    "Gontranno": "https://www.youtube.com/playlist?list=PL90QAKwVH1t78dk4jj6x51dJa_oEFQJJu",
    "raynarrok": "https://www.youtube.com/playlist?list=PL90QAKwVH1t4yWgUWujRmh_CpXPv6ovG1",
    "Maxxus": "https://www.youtube.com/playlist?list=PL90QAKwVH1t62PK83JBPXNCFDweBQJX5U",
    "E1000": "https://www.youtube.com/playlist?list=PL90QAKwVH1t5OrZV2eQgXC2S2OslYIoNK",
    "Lang": "https://www.youtube.com/playlist?list=PL90QAKwVH1t7oeQGl1kXJfLod9wwji8NQ",
    "Mastodon": "https://www.youtube.com/playlist?list=PL90QAKwVH1t5WtjO5OrpAs9VeRC3LPCyj",
    "Sebas": "https://www.youtube.com/playlist?list=PL90QAKwVH1t5cCPrXbS3vyIIHSP5ssLzE",
    "wylde": "https://www.youtube.com/playlist?list=PL90QAKwVH1t6EGhT85l7I_dyhcr8kScjl",
    "Kyorage": "https://www.youtube.com/playlist?list=PL90QAKwVH1t4wszcCcv3sVPWv5kGHOW5y",
    "Nightwing": "https://www.youtube.com/playlist?list=PL90QAKwVH1t7BZE16Lds-STFuexFYS4sI",
    "Estebangris": "https://www.youtube.com/playlist?list=PL90QAKwVH1t7dhJeajYfB2WQ_k0U0SLks",
    "Edu Bushi": "https://www.youtube.com/playlist?list=PL90QAKwVH1t52khCu1KxcwoCMzKrZ_WiB",
    "Kovas": "https://www.youtube.com/playlist?list=PL90QAKwVH1t76kUbMnqm_sM49OtCkwUML",
    "Fire Red": "https://www.youtube.com/playlist?list=PL90QAKwVH1t5Ww1-2kqO5AeMJfuNBvzsb",
    "Ozkuervo": "https://www.youtube.com/playlist?list=PL90QAKwVH1t4SnxBgafpkevWUxByL_Gpn",
    "JaffarWolf": "https://www.youtube.com/playlist?list=PL90QAKwVH1t6OazJzpkop7W6u9v4Q4cgH",
    "Leospirandio": "https://www.youtube.com/playlist?list=PL90QAKwVH1t76HmAfTwU9dxQp28Uv2bPX",
    "Ubitreides": "https://www.youtube.com/playlist?list=PL90QAKwVH1t67SU9-Br4O5a9teuu4cZvL",
    "Marv": "https://www.youtube.com/playlist?list=PL90QAKwVH1t7tqJ9tdKQ377j_PGNwTKb9",
    "Sagadalius": "https://www.youtube.com/playlist?list=PL90QAKwVH1t7SI0paoelLW60ka4fEO175",
    "DaiaNerdKilik": "https://www.youtube.com/playlist?list=PL90QAKwVH1t4bfFKuZL3w81ItKwXYRUfc",
    "Imano": "https://www.youtube.com/playlist?list=PL90QAKwVH1t4UX4ymnzNRvVFsY5iZT6qu",
    "Beowulf": "https://www.youtube.com/playlist?list=PL90QAKwVH1t6libDfzT5ZgnCKty20jPki",
    "Estaries": "https://www.youtube.com/playlist?list=PL90QAKwVH1t5vdm87xTohCp1mYcr0RXBb",
}

characters_dict = {
    "Taki": "https://www.youtube.com/playlist?list=PL90QAKwVH1t7W3yhPMKyU9uje26G1ZnBu",
    "Talim": "https://www.youtube.com/playlist?list=PL90QAKwVH1t7R1-ibZfefU2wUDRAIa3G2",
    "Setsuka": "https://www.youtube.com/playlist?list=PL90QAKwVH1t6GsZ9sHFdkhLJ4MdSEOrwF",
    "Hilde": "https://www.youtube.com/playlist?list=PL90QAKwVH1t5CnUs7a5OfQAQsL_VQdAF4",
    "2B": "https://www.youtube.com/playlist?list=PL90QAKwVH1t60fEU20FYYg20Tp1Y5FBGQ",
    "Azwel": "https://www.youtube.com/playlist?list=PL90QAKwVH1t6q-TlxlQSVO-F1WLcSLT03",
    "Geralt": "https://www.youtube.com/playlist?list=PL90QAKwVH1t78v9zPaxD-M2WS5W8Shdf9",
    "Groh": "https://www.youtube.com/playlist?list=PL90QAKwVH1t75-dwernEnAEWlSX73fzex",
    "Haohmaru": "https://www.youtube.com/playlist?list=PL90QAKwVH1t4IvEvmhRHEfz-xEzMaoLiR",
    "Zasalamel": "https://www.youtube.com/playlist?list=PL90QAKwVH1t6a2rA51DIX72J95BqTnsbh",
    "Tira": "https://www.youtube.com/playlist?list=PL90QAKwVH1t4dqovymm_ftxh69-vXOG0e",
    "Amy": "https://www.youtube.com/playlist?list=PL90QAKwVH1t7QvwDN2c4jbLq0hhqVlOFq",
    "Cassandra": "https://www.youtube.com/playlist?list=PL90QAKwVH1t5anV4BL93UxrqYBAGNOgI2",
    "Hwang": "https://www.youtube.com/playlist?list=PL90QAKwVH1t5Y9hflTAH8dVYLeOr10jHR",
    "Raphael": "https://www.youtube.com/playlist?list=PL90QAKwVH1t4vGjaOfK800WFGyx6EbCG1",
    "Xianghua": "https://www.youtube.com/playlist?list=PL90QAKwVH1t6LjfBNjGih8rH6pGcW1rg-",
    "Astaroth": "https://www.youtube.com/playlist?list=PL90QAKwVH1t4YdujqkS3PCw8HoaqC7p40",
    "Ivy": "https://www.youtube.com/playlist?list=PL90QAKwVH1t6jL0gEFDhFF8ypHtpU3ZQJ",
    "Kilik": "https://www.youtube.com/playlist?list=PL90QAKwVH1t4lDq3Ko9-yw4ipOzALlRf5",
    "Maxi": "https://www.youtube.com/playlist?list=PL90QAKwVH1t5HBO3pV8il2FFtRNcHLGEg",
    "Seong Mi-na": "https://www.youtube.com/playlist?list=PL90QAKwVH1t6faZQFTW_-d883_az5An5g",
    "Sophitia": "https://www.youtube.com/playlist?list=PL90QAKwVH1t7_Yf0QJUfGVpErfaQ7u_bV",
    "Yoshimitsu": "https://www.youtube.com/playlist?list=PL90QAKwVH1t7mTyKaL4pb_hzKvI6WHLgw",
    "Cervantes": "https://www.youtube.com/playlist?list=PL90QAKwVH1t7q1b8iijnrYmaYuI27Gfyo",
    "Mitsurugi": "https://www.youtube.com/playlist?list=PL90QAKwVH1t64CN2gW3GZYr6OiKOGRsWQ",
    "Nightmare": "https://www.youtube.com/playlist?list=PL90QAKwVH1t5lPgdyLfAac9Msc77gqGjZ",
    "Siegfried": "https://www.youtube.com/playlist?list=PL90QAKwVH1t49YI80I9PtNerAjAklbWXf",
    "Voldo": "https://www.youtube.com/playlist?list=PL90QAKwVH1t4JEKK40NPSAIXIO8Bh5Mu-",
}


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(colored(f"Conexión establecida. SQLite version {sqlite3.version}", "green"))
    except Error as e:
        print(colored(e, "red"))

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(colored(e, "red"))


def data_insertion(conn, columns_dict, battles_list, idx_dict, duels_list):
    cur = conn.cursor()

    table = "game"
    for e in columns_dict[table]:
        sql = f"SELECT name FROM {table} WHERE name = '{e}'"
        cur.execute(sql)
        query = cur.fetchall()
        if query == []:
            sql = f"INSERT INTO {table}(name, code_name) VALUES(?,?)"
            cur.execute(sql, (e, code_names_dict[e]))
            conn.commit()

    table = "platform"
    for e in columns_dict[table]:
        sql = f"SELECT code_name FROM {table} WHERE code_name = '{e}'"
        cur.execute(sql)
        query = cur.fetchall()
        if query == []:
            sql = f"INSERT INTO {table}(name, code_name) VALUES(?,?)"
            cur.execute(sql, (code_names_dict[e], e))
            conn.commit()

    table = "region"
    for e in columns_dict[table]:
        sql = f"SELECT code_name FROM {table} WHERE code_name = '{e}'"
        cur.execute(sql)
        query = cur.fetchall()
        if query == []:
            sql = f"INSERT INTO {table}(name, code_name) VALUES(?,?)"
            cur.execute(sql, (code_names_dict[e], e))
            conn.commit()

    table = "region"
    for e in columns_dict[table]:
        sql = f"SELECT code_name FROM {table} WHERE code_name = '{e}'"
        cur.execute(sql)
        query = cur.fetchall()
        if query == []:
            sql = f"INSERT INTO {table}(name, code_name) VALUES(?,?)"
            cur.execute(sql, (code_names_dict[e], e))
            conn.commit()

    table = "event_type"
    for e in columns_dict["event"]:
        event = e.split(" ")[0]
        sql = f"SELECT code_name FROM {table} WHERE code_name = '{event}'"
        cur.execute(sql)
        query = cur.fetchall()
        if query == []:
            sql = f"INSERT INTO {table}(name, code_name) VALUES(?,?)"
            cur.execute(sql, (code_names_dict[event], event))
            conn.commit()

    table = "duel_type"
    for e in columns_dict[table]:
        sql = f"SELECT code_name FROM {table} WHERE code_name = '{e}'"
        cur.execute(sql)
        query = cur.fetchall()
        if query == []:
            sql = f"INSERT INTO {table}(name, code_name, name_synonymous, code_name_synonymous) VALUES(?,?,?,?)"
            cur.execute(sql, (code_names_dict[e], e, code_names_dict[code_names_dict[code_names_dict[e]]], code_names_dict[code_names_dict[e]]))
            conn.commit()

    table = "player"
    for e in columns_dict["player1"]:
        sql = f"SELECT name FROM {table} WHERE name = '{e}'"
        cur.execute(sql)
        query = cur.fetchall()
        if query == []:
            sql = f"INSERT INTO {table}(name, playlist) VALUES(?,?)"
            if players_dict.get(e) is not None:
                cur.execute(sql, (e, players_dict[e]))
                conn.commit()
            else:
                cur.execute(sql, (e, "NULL"))
                conn.commit()
        else:
            sql = f"UPDATE {table} SET playlist = ? WHERE name = ?"
            if players_dict.get(e) is not None:
                cur.execute(sql, (players_dict[e], e))
                conn.commit()
    for e in columns_dict["player2"]:
        sql = f"SELECT name FROM {table} WHERE name = '{e}'"
        cur.execute(sql)
        query = cur.fetchall()
        if query == []:
            sql = f"INSERT INTO {table}(name, playlist) VALUES(?,?)"
            if players_dict.get(e) is not None:
                cur.execute(sql, (e, players_dict[e]))
                conn.commit()
            else:
                cur.execute(sql, (e, "NULL"))
                conn.commit()
        else:
            sql = f"UPDATE {table} SET playlist = ? WHERE name = ?"
            if players_dict.get(e) is not None:
                cur.execute(sql, (players_dict[e], e))
                conn.commit()

    table = "character"
    for e in columns_dict["character1"]:
        sql = f"SELECT name FROM {table} WHERE name = '{e}'"
        cur.execute(sql)
        query = cur.fetchall()
        if query == []:
            sql = f"INSERT INTO {table}(name, playlist) VALUES(?,?)"
            if characters_dict.get(e) is not None:
                cur.execute(sql, (e, characters_dict[e]))
                conn.commit()
            else:
                cur.execute(sql, (e, "NULL"))
                conn.commit()
        else:
            sql = f"UPDATE {table} SET playlist = ? WHERE name = ?"
            if characters_dict.get(e) is not None:
                cur.execute(sql, (characters_dict[e], e))
                conn.commit()
    for e in columns_dict["character2"]:
        sql = f"SELECT name FROM {table} WHERE name = '{e}'"
        cur.execute(sql)
        query = cur.fetchall()
        if query == []:
            sql = f"INSERT INTO {table}(name, playlist) VALUES(?,?)"
            if characters_dict.get(e) is not None:
                cur.execute(sql, (e, characters_dict[e]))
                conn.commit()
            else:
                cur.execute(sql, (e, "NULL"))
                conn.commit()
        else:
            sql = f"UPDATE {table} SET playlist = ? WHERE name = ?"
            if characters_dict.get(e) is not None:
                cur.execute(sql, (characters_dict[e], e))
                conn.commit()

    # 2
    table = "game_version_platform"
    for i in range(len(battles_list)):
        game = battles_list[i][idx_dict["game"]]
        platform = battles_list[i][idx_dict["platform"]]
        version = battles_list[i][idx_dict["version"]]
        sql = f"SELECT id FROM game WHERE name = '{game}'"
        cur.execute(sql)
        query = cur.fetchall()
        game_id = query[0][0]
        sql = f"SELECT id FROM platform WHERE code_name = '{platform}'"
        cur.execute(sql)
        query = cur.fetchall()
        platform_id = query[0][0]
        sql = f"SELECT id FROM {table} WHERE version = '{version}' AND game_id = {game_id} AND platform_id = {platform_id}"
        cur.execute(sql)
        query = cur.fetchall()
        if query == []:
            sql = f"INSERT INTO {table}(version, game_id, platform_id) VALUES(?,?,?)"
            cur.execute(sql, (version, game_id, platform_id))
            conn.commit()

    # 3
    table = "event"
    for i in range(len(battles_list)):
        game = battles_list[i][idx_dict["game"]]
        platform = battles_list[i][idx_dict["platform"]]
        version = battles_list[i][idx_dict["version"]]
        event_code_name = battles_list[i][idx_dict["event"]]
        region = battles_list[i][idx_dict["region"]]
        event_type = battles_list[i][idx_dict["event"]].split(" ")[0]
        event_number = battles_list[i][idx_dict["event"]].split(" ")[1]
        playlist = battles_list[i][idx_dict["playlist"]]
        brackets = battles_list[i][idx_dict["brackets"]]
        sql = f"SELECT id FROM game WHERE name = '{game}'"
        cur.execute(sql)
        query = cur.fetchall()
        game_id = query[0][0]
        sql = f"SELECT id FROM platform WHERE code_name = '{platform}'"
        cur.execute(sql)
        query = cur.fetchall()
        platform_id = query[0][0]
        sql = f"SELECT id FROM game_version_platform WHERE version = '{version}' AND game_id = {game_id} AND platform_id = {platform_id}"
        cur.execute(sql)
        query = cur.fetchall()
        game_version_platform_id = query[0][0]
        sql = f"SELECT id FROM region WHERE code_name = '{region}'"
        cur.execute(sql)
        query = cur.fetchall()
        region_id = query[0][0]
        sql = f"SELECT id FROM event_type WHERE code_name = '{event_type}'"
        cur.execute(sql)
        query = cur.fetchall()
        event_type_id = query[0][0]
        sql = f"SELECT id FROM {table} WHERE code_name = '{event_code_name}'"
        cur.execute(sql)
        query = cur.fetchall()
        if query == []:
            sql = f"INSERT INTO {table}(name, code_name, playlist, brackets, type_id, region_id, game_version_platform_id) VALUES(?,?,?,?,?,?,?)"
            cur.execute(sql, (code_names_dict[event_type] + " " + event_number, event_code_name, playlist, brackets, event_type_id, region_id, game_version_platform_id))
            conn.commit()

    # 4
    table = "duel"
    for i in range(len(duels_list)):
        player1 = duels_list[i][idx_dict["player1"]]
        player2 = duels_list[i][idx_dict["player2"]]
        duel_type = duels_list[i][idx_dict["duel_type"]]
        event = duels_list[i][idx_dict["event"]]
        duel_order = duels_list[i][idx_dict["duel"]]
        video = duels_list[i][idx_dict["video"]]
        sql = f"SELECT id FROM player WHERE name = '{player1}'"
        cur.execute(sql)
        query = cur.fetchall()
        player1_id = query[0][0]
        sql = f"SELECT id FROM player WHERE name = '{player2}'"
        cur.execute(sql)
        query = cur.fetchall()
        player2_id = query[0][0]
        sql = f"SELECT id FROM duel_type WHERE code_name = '{duel_type}'"
        cur.execute(sql)
        query = cur.fetchall()
        duel_type_id = query[0][0]
        sql = f"SELECT id FROM event WHERE code_name = '{event}'"
        cur.execute(sql)
        query = cur.fetchall()
        event_id = query[0][0]
        sql = f"SELECT id FROM {table} WHERE player1_id = '{player1_id}' AND player2_id = '{player2_id}' AND duel_order = '{duel_order}' AND video = '{video}' AND type_id = '{duel_type_id}' AND event_id = '{event_id}'"
        cur.execute(sql)
        query = cur.fetchall()
        if query == []:
            sql = f"INSERT INTO {table}(player1_id, player2_id, duel_order, video, type_id, event_id) VALUES(?,?,?,?,?,?)"
            cur.execute(sql, (player1_id, player2_id, duel_order, video, duel_type_id, event_id))
            conn.commit()

    # 5
    table = "combat"
    for i in range(len(battles_list)):
        player1 = battles_list[i][idx_dict["player1"]]
        player2 = battles_list[i][idx_dict["player2"]]
        character1 = battles_list[i][idx_dict["character1"]]
        character2 = battles_list[i][idx_dict["character2"]]
        duel = battles_list[i][idx_dict["duel"]]
        event = battles_list[i][idx_dict["event"]]
        sql = f"SELECT id FROM player WHERE name = '{player1}'"
        cur.execute(sql)
        query = cur.fetchall()
        player1_id = query[0][0]
        sql = f"SELECT id FROM player WHERE name = '{player2}'"
        cur.execute(sql)
        query = cur.fetchall()
        player2_id = query[0][0]
        sql = f"SELECT id FROM character WHERE name = '{character1}'"
        cur.execute(sql)
        query = cur.fetchall()
        character1_id = query[0][0]
        sql = f"SELECT id FROM character WHERE name = '{character2}'"
        cur.execute(sql)
        query = cur.fetchall()
        character2_id = query[0][0]
        sql = f"SELECT id FROM event WHERE code_name = '{event}'"
        cur.execute(sql)
        query = cur.fetchall()
        event_id = query[0][0]
        sql = f"SELECT id, player1_id, player2_id FROM duel WHERE duel_order = '{duel}' AND event_id = '{event_id}'"
        cur.execute(sql)
        query = cur.fetchall()
        duel_id, p1_id, p2_id = query[0][:3]
        sql = f"SELECT id FROM {table} WHERE character1_id = '{character1_id}' AND character2_id = '{character2_id}' AND combat_order = '{i}' AND duel_id = '{duel_id}'"
        cur.execute(sql)
        query = cur.fetchall()
        if query == []:
            if player1_id == p1_id and player2_id == p2_id:
                sql = f"INSERT INTO {table}(character1_id, character2_id, combat_order, duel_id) VALUES(?,?,?,?)"
                cur.execute(sql, (character1_id, character2_id, i, duel_id))
                conn.commit()
            if player1_id == p2_id and player2_id == p1_id:
                sql = f"INSERT INTO {table}(character1_id, character2_id, combat_order, duel_id) VALUES(?,?,?,?)"
                cur.execute(sql, (character2_id, character1_id, i, duel_id))
                conn.commit()

    # 6
    table = "round"
    for i in range(len(battles_list)):
        r1_p1 = battles_list[i][idx_dict["r1_p1"]]
        r2_p1 = battles_list[i][idx_dict["r2_p1"]]
        r3_p1 = battles_list[i][idx_dict["r3_p1"]]
        r4_p1 = battles_list[i][idx_dict["r4_p1"]]
        r5_p1 = battles_list[i][idx_dict["r5_p1"]]
        p1_rounds = [r1_p1, r2_p1, r3_p1, r4_p1, r5_p1]
        r1_p2 = battles_list[i][idx_dict["r1_p2"]]
        r2_p2 = battles_list[i][idx_dict["r2_p2"]]
        r3_p2 = battles_list[i][idx_dict["r3_p2"]]
        r4_p2 = battles_list[i][idx_dict["r4_p2"]]
        r5_p2 = battles_list[i][idx_dict["r5_p2"]]
        p2_rounds = [r1_p2, r2_p2, r3_p2, r4_p2, r5_p2]
        sql = f"SELECT id FROM combat WHERE combat_order = '{i}'"
        cur.execute(sql)
        query = cur.fetchall()
        combat_id = query[0][0]
        player_side = 1
        for j in range(len(p1_rounds)):
            sql = f"SELECT id FROM {table} WHERE player_side = '{player_side}' AND round_order = '{j+1}' AND result = '{p1_rounds[j]}' AND combat_id = '{combat_id}'"
            cur.execute(sql)
            query = cur.fetchall()
            if query == []:
                sql = f"INSERT INTO {table}(player_side, round_order, result, combat_id) VALUES(?,?,?,?)"
                cur.execute(sql, (player_side, j+1, p1_rounds[j], combat_id))
                conn.commit()
        player_side = 2
        for j in range(len(p2_rounds)):
            sql = f"SELECT id FROM {table} WHERE player_side = '{player_side}' AND round_order = '{j+1}' AND result = '{p2_rounds[j]}' AND combat_id = '{combat_id}'"
            cur.execute(sql)
            query = cur.fetchall()
            if query == []:
                sql = f"INSERT INTO {table}(player_side, round_order, result, combat_id) VALUES(?,?,?,?)"
                cur.execute(sql, (player_side, j+1, p2_rounds[j], combat_id))
                conn.commit()

    # return cur.lastrowid



if __name__ == '__main__':

    ''' DATABASE PATH '''
    database = "backend/PySQLiteSSLT.db"
    conn = create_connection(database)

    ''' TABLES CREATION '''

    # Tablas de primer nivel

    table_game = '''CREATE TABLE IF NOT EXISTS game (
        id integer PRIMARY KEY,
        name text NOT NULL,
        code_name text NOT NULL
    );'''

    table_platform = '''CREATE TABLE IF NOT EXISTS platform (
        id integer PRIMARY KEY,
        name text NOT NULL,
        code_name text NOT NULL
    );'''

    table_region = '''CREATE TABLE IF NOT EXISTS region (
        id integer PRIMARY KEY,
        name text NOT NULL,
        code_name text NOT NULL
    );'''

    table_event_type = '''CREATE TABLE IF NOT EXISTS event_type (
        id integer PRIMARY KEY,
        name text NOT NULL,
        code_name text NOT NULL
    );'''

    table_duel_type = '''CREATE TABLE IF NOT EXISTS duel_type (
        id integer PRIMARY KEY,
        name text NOT NULL,
        code_name text NOT NULL,
        name_synonymous text,
        code_name_synonymous text
    );'''

    table_player = '''CREATE TABLE IF NOT EXISTS player (
        id integer PRIMARY KEY,
        name text NOT NULL,
        playlist text
    );'''

    table_character = '''CREATE TABLE IF NOT EXISTS character (
        id integer PRIMARY KEY,
        name text NOT NULL,
        playlist text
    );'''

    # Tablas de segundo nivel

    table_game_version_platform = '''CREATE TABLE IF NOT EXISTS game_version_platform (
        id integer PRIMARY KEY,
        version text NOT NULL,
        game_id integer NOT NULL,
        platform_id NOT NULL,
        FOREIGN KEY (game_id) REFERENCES game (id),
        FOREIGN KEY (platform_id) REFERENCES platform (id)
    );'''

    # Tablas de tercer nivel

    table_event = '''CREATE TABLE IF NOT EXISTS event (
        id integer PRIMARY KEY,
        name text NOT NULL,
        code_name text NOT NULL,
        playlist text NOT NULL,
        brackets text NOT NULL,
        type_id integer NOT NULL,
        region_id integer NOT NULL,
        game_version_platform_id integer NOT NULL,
        FOREIGN KEY (type_id) REFERENCES event_type (id),
        FOREIGN KEY (region_id) REFERENCES region (id),
        FOREIGN KEY (game_version_platform_id) REFERENCES game_version_platform (id)
    );'''

    # Tablas de cuarto nivel

    table_duel = '''CREATE TABLE IF NOT EXISTS duel (
        id integer PRIMARY KEY,
        player1_id integer NOT NULL,
        player2_id integer NOT NULL,
        duel_order integer NOT NULL,
        video text NOT NULL,
        type_id integer NOT NULL,
        event_id integer NOT NULL,
        FOREIGN KEY (player1_id) REFERENCES player (id),
        FOREIGN KEY (player2_id) REFERENCES player (id),
        FOREIGN KEY (type_id) REFERENCES duel_type (id),
        FOREIGN KEY (event_id) REFERENCES game_version_platform (id)
    );'''

    # Tablas de quinto nivel

    table_combat = '''CREATE TABLE IF NOT EXISTS combat (
        id integer PRIMARY KEY,
        character1_id integer NOT NULL,
        character2_id integer NOT NULL,
        combat_order integer NOT NULL,
        duel_id integer NOT NULL,
        FOREIGN KEY (character1_id) REFERENCES character (id),
        FOREIGN KEY (character2_id) REFERENCES character (id),
        FOREIGN KEY (duel_id) REFERENCES duel (id)
    );'''

    # Tablas de sexto nivel

    table_round = '''CREATE TABLE IF NOT EXISTS round (
        id integer PRIMARY KEY,
        player_side text NOT NULL,
        round_order integer NOT NULL,
        result text NOT NULL,
        combat_id integer NOT NULL,
        FOREIGN KEY (combat_id) REFERENCES combat (id)
    );'''    

    if conn is not None:
        # 1
        create_table(conn, table_game)
        create_table(conn, table_platform)
        create_table(conn, table_region)
        create_table(conn, table_event_type)
        create_table(conn, table_duel_type)
        create_table(conn, table_player)
        create_table(conn, table_character)
        # 2
        create_table(conn, table_game_version_platform)
        # 3
        create_table(conn, table_event)
        # 4
        create_table(conn, table_duel)
        # 5
        create_table(conn, table_combat)
        # 6
        create_table(conn, table_round)
    else:
        print(colored("Error! cannot create the database connection.", "red"))

    ''' INSERTING DATA '''

    csv_data_path = "backend/SCMdb - SSLT.csv"
    columns_dict, battles_list, idx_dict, duels_list = ssf.load_csv_data(csv_data_path)
    data_insertion(conn, columns_dict, battles_list, idx_dict, duels_list)

# select G.name, GVP.version, PL.code_name, E.code_name, P1.name, CH1.name, P2.name, CH2.name, D.duel_order, C.combat_order, R.player_side, R.round_order, R.result from round R
# inner join combat C on R.combat_id = C.id
# inner join character CH1 on CH1.id = C.character1_id
# inner join character CH2 on CH2.id = C.character2_id
# inner join duel D on D.id = C.duel_id
# inner join player P1 on P1.id = D.player1_id
# inner join player P2 on P2.id = D.player2_id
# inner join duel_type DT on DT.id = D.type_id
# inner join event E on E.id = D.event_id
# inner join event_type ET on ET.id = E.type_id
# inner join region RE on RE.id = E.region_id
# inner join game_version_platform GVP on GVP.id = E.game_version_platform_id
# inner join game G on G.id = GVP.game_id
# inner join platform PL on PL.id = GVP.platform_id

# select * from duel D
# inner join combat C on C.duel_id = D.id

# select P1.name, CH1.name, P2.name, CH2.name from duel D
# inner join player P1 on P1.id = D.player1_id
# inner join player P2 on P2.id = D.player2_id
# inner join combat C on C.duel_id = D.id
# inner join character CH1 on CH1.id = C.character1_id
# inner join character CH2 on CH2.id = C.character2_id