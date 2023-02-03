from sqlalchemy import create_engine, \
                       Column, \
                       Integer, \
                       String, \
                       Boolean, \
                       DateTime, \
                       or_, \
                       ForeignKey, \
                       Table

from sqlalchemy.orm import declarative_base, \
                           relationship, \
                           Session

from enum import Enum
import numpy as np


''' Engine '''

DB_ENGINE = "sqlite"
DB_API = "pysqlite"
DB_PATH = "backend/SSLEdb.db"
ENGINE = create_engine(f"{DB_ENGINE}+{DB_API}:///{DB_PATH}", echo=True, future=True)

''' Utils '''

ROUNDS_POINTS = {
    "D": 240,
    "PW": 240,
    "W": 240,
    "WY": 168,
    "WB": 84,
    "LY": 168,
    "LB": 84,
    "PL": 0
}

ROUND_WIN_CONDITIONS = ["D", "PW", "W", "WY", "WB"]
ROUND_LOSE_CONDITIONS = ["LY", "LB", "PL"]

class Scoreboard:
    def __init__(self, result_player1, result_player2):
        self.player1 = result_player1
        self.player2 = result_player2

    ''' Methods '''
    # Getters
    def get_player1(self):
        return self.player1
    
    def get_player2(self):
        return self.player2

    def get_total(self):
        return self.player1 + self.player2

    # Setters
    def add_to_player1(self, number):
        self.player1 += number

    def add_to_player2(self, number):
        self.player2 += number

    
class EventSystem(Enum):
    TOURNAMENT = 1
    LEAGUE = 2

class CompetitorType(Enum):
    PLAYER = 1
    TEAM = 2

class CompetitorStatus(Enum):
    WINNER = 1
    LOSER = 2

class ChallengeType(Enum):
    ROUND = 1
    COMBAT = 2
    DUEL = 3
    EVENT = 4

class ChallengeStatus(Enum):
    PLAYED = 1
    WON = 2
    LOST = 3
    DRAW = 4

class EntityType(Enum):
    PLAYER = 1
    CHARACTER = 2
    PLAYERCHARACTER = 3
    TEAM = 4

class CombatStatus(Enum):
    PLAYED = 1
    WON = 2
    LOST = 3
    DRAW = 4

class RoundStatus(Enum):
    PLAYED = 1
    WON = 2
    LOST = 3

class PlayerSide(Enum):
    P1 = 1
    P2 = 2
    BOTH = 3

class LvlFactor(Enum):
    A = -0.04
    B = 1

class PerformanceMetric(Enum):
    WIN_RATE = 1
    WIN_LOSE_RATIO = 2

FUNC = np.arctan


''' ClassTables '''

Base = declarative_base()

# Event group

class Game(Base):
    __tablename__ = "game"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    code_name = Column(String, nullable=False)

    ''' Relationships '''
    game_version_platforms = relationship("GameVersionPlatform", back_populates="game", cascade="all, delete-orphan")


class Platform(Base):
    __tablename__ = "platform"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    code_name = Column(String, nullable=False)

    ''' Relationships '''
    game_version_platforms = relationship("GameVersionPlatform", back_populates="platform", cascade="all, delete-orphan")


class GameVersionPlatform(Base):
    __tablename__ = "game_version_platform"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    version = Column(String, nullable=False)

    platform_id = Column(Integer, ForeignKey("platform.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("game.id"), nullable=False)

    ''' Relationships '''
    game = relationship("Game", back_populates="game_version_platforms")
    platform = relationship("Platform", back_populates="game_version_platforms")
    events = relationship("Event", back_populates="game_version_platform", cascade="all, delete-orphan")


class Region(Base):
    __tablename__ = "region"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    code_name = Column(String, nullable=False)

    ''' Relationships '''
    events = relationship("Event", back_populates="region", cascade="all, delete-orphan")


class Season(Base):
    __tablename__ = "season"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    code_name = Column(String, nullable=False)
    season_order = Column(Integer, nullable=False)

    ''' Relationships '''
    events = relationship("Event", back_populates="season", cascade="all, delete-orphan")

    ''' Methods '''
    def get_season_order(self):
        return self.season_order

    def get_events_list(self):
        events_list = list(sorted(self.events, key=lambda x:x.get_event_order()))
        return events_list
    
    def get_events_number(self):
        return len(self.get_events_list())


class EventModality(Base):
    __tablename__ = "event_modality"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    competitor_type = Column(String, nullable=False)
    event_system = Column(String, nullable=False)

    ''' Relationships '''
    events = relationship("Event", back_populates="event_modality", cascade="all, delete-orphan")

    ''' Methods '''
    def get_competitor_type(self):
        return self.competitor_type

    def get_event_system(self):
        return self.event_system


class Event(Base):
    __tablename__ = "event"

    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    code_name = Column(String, nullable=False)
    link_raw = Column(String, nullable=False)
    link_summarized = Column(String, nullable=False)
    playlist = Column(String, nullable=False)
    bracket = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    event_order = Column(Integer, nullable=False)

    game_version_platform_id = Column(Integer, ForeignKey("game_version_platform.id"), nullable=False)
    region_id = Column(Integer, ForeignKey("region.id"), nullable=False)
    season_id = Column(Integer, ForeignKey("season.id"), nullable=False)
    event_modality_id = Column(Integer, ForeignKey("event_modality.id"), nullable=False)

    ''' Relationships '''
    game_version_platform = relationship("GameVersionPlatform", back_populates="events")
    region = relationship("Region", back_populates="events")
    season = relationship("Season", back_populates="events")
    event_modality = relationship("EventModality", back_populates="events")
    duels = relationship("Duel", back_populates="event", cascade="all, delete-orphan")

    ''' Methods '''
    # Getters
    def get_event_order(self):
        return self.event_order

    def get_event_system(self): # Tournament / League
        return self.event_modality.get_event_system()

    def get_competitors_type(self): # Players / Teams
        return self.event_modality.get_competitor_type()
    
    # Members
    def get_teams_list(self):
        teams_list = list()
        for duel in self.duels:
            teams_list += duel.get_teams_list()
        teams_list = list(set(teams_list)).sort()
        return teams_list
    
    def get_teams_number(self):
        return len(self.get_teams_list())

    def get_players_list(self):
        players_list = list()
        for duel in self.duels:
            players_list += duel.get_players_list()
        players_list = list(set(players_list)).sort()
        return players_list
    
    def get_players_number(self):
        return len(self.get_players_list())

    def get_characters_list(self):
        characters_list = list()
        for duel in self.duels:
            characters_list += duel.get_characters_list()
        characters_list = list(set(characters_list)).sort()
        return characters_list

    def get_characters_number(self):
        return len(self.get_characters_list())
    
    def get_results_dict(self):
        # for duel in self.duels:
        #     duel.get_points_earned()
        return

    # Duels
    def get_duels_played_list(self):
        return self.duels

    def get_duels_played_number(self):
        return len(self.duels)
    
    # Combats
    def get_combats_played_list(self):
        combats_list = list()
        for duel in self.duels:
            combats_list += duel.get_combats_played_list()
        return combats_list

    def get_combats_played_number(self):
        return len(self.get_combats_played_list)

    # Rounds
    def get_rounds_played_number(self):
        rounds_number = 0
        for duel in self.duels:
            rounds_number += duel.get_rounds_played_number()
        return rounds_number



    def get_teams_rivals_list(self, team_obj):
        # for team in self.get_teams_list():
        #     for duel in self.get_duels_played_list():
        #         if team in duel.get_teams_list():
        return

    def get_rivals_number(competitor):
        return

    def get_duels_played_list(competitor):
        return

    def get_duels_played_number(competitor):
        return

    def get_duels_won_list(competitor):
        return

    def get_duels_won_number(competitor):
        return

    def get_duels_lost_list(competitor):
        return

    def get_duels_lost_number(competitor):
        return

    def get_combats_played_list(competitor):
        return

    def get_combats_played_number(competitor):
        return

    def get_combats_won_list(competitor):
        return

    def get_combats_won_number(competitor):
        return

    def get_combats_lost_list(competitor):
        return

    def get_combats_lost_number(competitor):
        return

    def get_rounds_played_number(competitor):
        return

    def get_rounds_won_number(competitor):
        return

    def get_rounds_lost_number(competitor):
        return

    def get_event_duels_beating_factor(competitor):
        '''
        duels_beating_factor = duels_won / duels_played
        '''
        return

    def get_event_duels_win_rate(competitor):
        return

    def get_event_duels_wlr(competitor):
        return

    def get_event_combats_beating_factor(competitor):
        '''
        combats_beating_factor = combats_won / combats_played
        '''
        return

    def get_event_combats_win_rate(competitor):
        return

    def get_event_combats_wlr(competitor):
        return

    def get_event_rounds_beating_factor(competitor):
        '''
        rounds_beating_factor = combats_won / combats_played
        '''
        return

    def get_event_rounds_win_rate(competitor):
        return

    def get_event_rounds_wlr(competitor):
        return

    def get_competitor_position(competitor):
        return

    def get_positions_list():
        return


# Duel group

class DuelType(Base):
    __tablename__ = "duel_type"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    description = Column(String, nullable=True)
    name = Column(String, nullable=False)
    code_name = Column(String, nullable=False)
    name_synonymous = Column(String, nullable=True)
    code_name_synonymous = Column(String, nullable=True)

    ''' Relationships '''
    duels = relationship("Duel", back_populates="duel_type", cascade="all, delete-orphan")


class Video(Base):
    __tablename__ = "video"

    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    url = Column(String, nullable=False)

    duel_id = Column(Integer, ForeignKey("duel.id"), nullable=False)

    ''' Relationships '''
    duel = relationship("Duel", back_populates="videos")


class Duel(Base):
    __tablename__ = "duel"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    duel_order = Column(Integer, nullable=False)

    event_id = Column(Integer, ForeignKey("event.id"), nullable=False)
    duel_type_id = Column(Integer, ForeignKey("duel_type.id"), nullable=False)

    ''' Relationships '''
    event = relationship("Event", back_populates="duels")
    duel_type = relationship("DuelType", back_populates="duels")
    videos = relationship("Video", back_populates="duel", cascade="all, delete-orphan")
    combats = relationship("Combat", back_populates="duel", cascade="all, delete-orphan")

    ''' Methods '''
    # Getters
    def get_duel_type(self):
        return self.duel_type

    def get_event(self):
        return self.event

    def get_videos_list(self):
        return self.videos

    def get_combats_list(self):
        return self.combats
    
    # Members
    def get_teams_list(self):
        teams_list = list()
        for combat in self.combats:
            teams_list += combat.get_teams_list()
        teams_list = list(set(teams_list)).sort()
        return teams_list

    def get_teams_number(self):
        return len(self.get_teams_list())

    def get_players_list(self):
        players_list = list()
        for combat in self.combats:
            players_list += combat.get_players_list()
        players_list = list(set(players_list)).sort()
        return players_list
    
    def get_teams_members_dict_list(self):
        teams_members_dict_list = dict()
        teams_list = self.get_teams_list()
        for team in teams_list:
            teams_members_dict_list[team] = set()
        for combat in self.combats:
            teams_members_dict_list[combat.get_team1()].add(combat.get_player1())
            teams_members_dict_list[combat.get_team2()].add(combat.get_player2())
        for team in teams_list:
            teams_members_dict_list[team] = list(teams_members_dict_list[team])
        return teams_members_dict_list

    def get_players_number(self):
        return len(self.get_players_list())

    def get_characters_list(self):
        characters_list = list()
        for combat in self.combats:
            characters_list += combat.get_characters_list()
        characters_list = list(set(characters_list)).sort()
        return characters_list

    def get_characters_number(self):
        return len(self.get_characters_list())

    def is_team_duel(self):
        team_duel = False
        if self.event.get_competitors_type() == CompetitorType.TEAM.name:
            team_duel = True
        return team_duel

    # Combats
    def get_combats_played_list(self):
        ''' List of combats played in a duel '''
        return self.combats

    def get_combats_played_number(self):
        ''' Number of combats played in a duel '''
        return len(self.combats)
    
    # Combats entities
    def get_combats_status_entity_dict_list(self, combat_status, entity_type):
        ''' List of some status combats in a duel by entity '''
        combats_status_dict_list = dict() # Output
        entities_list = list() # List of entities in the duel
        if entity_type == EntityType.PLAYER.name: # Players
            entities_list = self.get_players_list()
        if entity_type == EntityType.CHARACTER.name: # Characters
            entities_list = self.get_characters_list()
        if entity_type == EntityType.TEAM.name: # Teams
            entities_list = self.get_characters_list()
        for entity in entities_list:
            combats_status_dict_list[entity] = list() # Output
            for combat in self.combats:
                combat_entities = list()
                entity_winner = None
                entity_loser = None
                if entity_type == EntityType.PLAYER.name:
                    combat_entities = combat.get_players_list()
                    entity_winner = combat.get_winner_player()
                    entity_loser = combat.get_loser_player()
                if entity_type == EntityType.CHARACTER.name:
                    combat_entities = combat.get_characters_list()
                    entity_winner = combat.get_winner_character()
                    entity_loser = combat.get_loser_character()
                if entity_type == EntityType.TEAM.name:
                    combat_entities = combat.get_teams_list()
                    entity_winner = combat.get_winner_team()
                    entity_loser = combat.get_loser_team()
                if combat_status == CombatStatus.PLAYED.name: # Combats played
                    if entity in combat_entities:
                        combats_status_dict_list[entity].append(combat)
                if combat_status == CombatStatus.WON.name: # Combats won
                    if entity_winner == entity:
                        combats_status_dict_list[entity].append(combat)
                if combat_status == CombatStatus.LOST.name: # Combats lost
                    if entity_loser == entity:
                        combats_status_dict_list[entity].append(combat)
                if combat_status == CombatStatus.DRAW.name: # Combats draw
                    if combat.is_draw():
                        for entity in combat_entities:
                            combats_status_dict_list[entity].append(combat)
        return combats_status_dict_list

    def get_combats_status_entity_dict_number(self, combat_status, entity_type):
        ''' Number of some status combats in a duel by entity '''
        combats_status_entity_dict_number = dict()
        combats_status_entity_dict_list = self.get_combats_status_entity_dict_list(combat_status, entity_type)
        for entity, combats_status_entity_list in combats_status_entity_dict_list.items():
            combats_status_entity_dict_number[entity] = len(combats_status_entity_list)
        return combats_status_entity_dict_number
    
    def get_combats_beating_factors_entity(self, entity_type):
        ''' Combats beating factors by entity '''
        combats_beating_factors_entities_dict = dict() # Output
        combats_played_entity_dict_number = dict()
        combats_won_entity_dict_number = dict()
        combats_draw_entity_dict_number = dict()
        entities_list = list()
        if entity_type == EntityType.PLAYER.name: # Players
            combats_played_entity_dict_number = self.get_combats_played_player_dict_number()
            combats_won_entity_dict_number = self.get_combats_won_player_dict_number()
            combats_draw_entity_dict_number = self.get_combats_draw_player_dict_number()
            entities_list = self.get_players_list()
        if entity_type == EntityType.CHARACTER.name: # Characters
            combats_played_entity_dict_number = self.get_combats_played_character_dict_number()
            combats_won_entity_dict_number = self.get_combats_won_character_dict_number()
            combats_draw_entity_dict_number = self.get_combats_draw_character_dict_number()
            entities_list = self.get_characters_list()
        if entity_type == EntityType.TEAM.name: # Teams
            combats_played_entity_dict_number = self.get_combats_played_team_dict_number()
            combats_won_entity_dict_number = self.get_combats_won_team_dict_number()
            combats_draw_entity_dict_number = self.get_combats_draw_team_dict_number()
            entities_list = self.get_teams_list()
        for entity in entities_list:
            if combats_won_entity_dict_number[entity] + combats_draw_entity_dict_number[entity] == 0:
                combats_beating_factors_entities_dict[entity] = (1 / combats_played_entity_dict_number[entity]) / 2
            else:
                combats_beating_factors_entities_dict[entity] = (combats_won_entity_dict_number[entity] + combats_draw_entity_dict_number[entity]) / combats_played_entity_dict_number[entity]
        return combats_beating_factors_entities_dict
    
    def get_results_entity_dict(self, entity_type):
        results_entity_dict = dict() # Output
        combats_beating_factors_entity_dict = dict()
        if entity_type == EntityType.PLAYER.name:
            combats_beating_factors_entity_dict = self.get_combats_beating_factors_players()
        if entity_type == EntityType.TEAM.name:
            combats_beating_factors_entity_dict = self.get_combats_beating_factors_teams()
        combats_beating_factors_entity_dict = dict(sorted(combats_beating_factors_entity_dict.items(), key=lambda x:x[1]))
        for i, entity in enumerate(combats_beating_factors_entity_dict.keys()):
            results_entity_dict[i+1] = entity
        return results_entity_dict
    
    def get_winner_entity(self, entity_type):
        results_entity_dict = dict()
        if entity_type == EntityType.PLAYER.name:
            results_entity_dict = self.get_results_players_dict()
        if entity_type == EntityType.TEAM.name:
            results_entity_dict = self.get_results_teams_dict()
        return list(results_entity_dict.values())[0]
    
    def get_losers_entity_list(self, entity_type):
        results_entity_dict = dict()
        if entity_type == EntityType.PLAYER.name:
            results_entity_dict = self.get_results_players_dict()
        if entity_type == EntityType.TEAM.name:
            results_entity_dict = self.get_results_teams_dict()
        return list(results_entity_dict.values())[1:]

    # Combats players
    def get_combats_played_player_dict_list(self):
        ''' List of combats played in a duel by player '''
        return self.get_combats_status_entity_dict_list(CombatStatus.PLAYED.name, EntityType.PLAYER.name)

    def get_combats_played_player_dict_number(self):
        ''' Number of combats played in a duel by player '''
        return self.get_combats_status_entity_dict_number(CombatStatus.PLAYED.name, EntityType.PLAYER.name)

    def get_combats_won_player_dict_list(self):
        ''' List of combats won in a duel by player '''
        return self.get_combats_status_entity_dict_list(CombatStatus.WON.name, EntityType.PLAYER.name)

    def get_combats_won_player_dict_number(self):
        ''' Number of combats won in a duel by player '''
        return self.get_combats_status_entity_dict_number(CombatStatus.WON.name, EntityType.PLAYER.name)
    
    def get_combats_lost_player_dict_list(self):
        ''' List of combats lost in a duel by player '''
        return self.get_combats_status_entity_dict_list(CombatStatus.LOST.name, EntityType.PLAYER.name)

    def get_combats_lost_player_dict_number(self):
        ''' Number of combats lost in a duel by player '''
        return self.get_combats_status_entity_dict_number(CombatStatus.LOST.name, EntityType.PLAYER.name)

    def get_combats_draw_player_dict_list(self):
        ''' List of combats draw in a duel by player '''
        return self.get_combats_status_entity_dict_list(CombatStatus.DRAW.name, EntityType.PLAYER.name)

    def get_combats_draw_player_dict_number(self):
        ''' Number of combats draw in a duel by player '''
        return self.get_combats_status_entity_dict_number(CombatStatus.DRAW.name, EntityType.PLAYER.name)

    def get_combats_beating_factors_players(self):
        ''' Combats beating factors by player '''
        return self.get_combats_beating_factors_entity(EntityType.PLAYER.name)
    
    def get_results_players_dict(self):
        ''' Duels results by player '''
        return self.get_results_entity_dict(EntityType.PLAYER.name)

    def get_winner_player(self):
        ''' Duel winner by player '''
        return self.get_winner_entity(EntityType.PLAYER.name)
    
    def get_losers_player_list(self):
        ''' Duel losers list by player '''
        return self.get_losers_entity_list(EntityType.PLAYER.name)
    
    # Combats characters
    def get_combats_played_character_dict_list(self):
        ''' List of combats played in a duel by character '''
        return self.get_combats_status_entity_dict_list(CombatStatus.PLAYED.name, EntityType.CHARACTER.name)

    def get_combats_played_character_dict_number(self):
        ''' Number of combats played in a duel by character '''
        return self.get_combats_status_entity_dict_number(CombatStatus.PLAYED.name, EntityType.CHARACTER.name)

    def get_combats_won_character_dict_list(self):
        ''' List of combats won in a duel by character '''
        return self.get_combats_status_entity_dict_list(CombatStatus.WON.name, EntityType.CHARACTER.name)

    def get_combats_won_character_dict_number(self):
        ''' Number of combats won in a duel by character '''
        return self.get_combats_status_entity_dict_number(CombatStatus.WON.name, EntityType.CHARACTER.name)
    
    def get_combats_lost_character_dict_list(self):
        ''' List of combats lost in a duel by character '''
        return self.get_combats_status_entity_dict_list(CombatStatus.LOST.name, EntityType.CHARACTER.name)

    def get_combats_lost_character_dict_number(self):
        ''' Number of combats lost in a duel by character '''
        return self.get_combats_status_entity_dict_number(CombatStatus.LOST.name, EntityType.CHARACTER.name)

    def get_combats_draw_character_dict_list(self):
        ''' List of combats draw in a duel by character '''
        return self.get_combats_status_entity_dict_list(CombatStatus.DRAW.name, EntityType.CHARACTER.name)

    def get_combats_draw_character_dict_number(self):
        ''' Number of combats draw in a duel by character '''
        return self.get_combats_status_entity_dict_number(CombatStatus.DRAW.name, EntityType.CHARACTER.name)
    
    def get_combats_beating_factors_characters(self):
        ''' Combats beating factors by character '''
        return self.get_combats_beating_factors_entity(EntityType.CHARACTER.name)

    # Combats teams
    def get_combats_played_team_dict_list(self):
        ''' List of combats played in a duel by team '''
        return self.get_combats_status_entity_dict_list(CombatStatus.PLAYED.name, EntityType.TEAM.name)

    def get_combats_played_team_dict_number(self):
        ''' Number of combats played in a duel by team '''
        return self.get_combats_status_entity_dict_number(CombatStatus.PLAYED.name, EntityType.TEAM.name)

    def get_combats_won_team_dict_list(self):
        ''' List of combats won in a duel by team '''
        return self.get_combats_status_entity_dict_list(CombatStatus.WON.name, EntityType.TEAM.name)

    def get_combats_won_team_dict_number(self):
        ''' Number of combats won in a duel by team '''
        return self.get_combats_status_entity_dict_number(CombatStatus.WON.name, EntityType.TEAM.name)
    
    def get_combats_lost_team_dict_list(self):
        ''' List of combats lost in a duel by team '''
        return self.get_combats_status_entity_dict_list(CombatStatus.LOST.name, EntityType.TEAM.name)

    def get_combats_lost_team_dict_number(self):
        ''' Number of combats lost in a duel by team '''
        return self.get_combats_status_entity_dict_number(CombatStatus.LOST.name, EntityType.TEAM.name)

    def get_combats_draw_team_dict_list(self):
        ''' List of combats draw in a duel by team '''
        return self.get_combats_status_entity_dict_list(CombatStatus.DRAW.name, EntityType.TEAM.name)

    def get_combats_draw_team_dict_number(self):
        ''' Number of combats draw in a duel by team '''
        return self.get_combats_status_entity_dict_number(CombatStatus.DRAW.name, EntityType.TEAM.name)
    
    def get_combats_beating_factors_teams(self):
        ''' Combats beating factors by team '''
        return self.get_combats_beating_factors_entity(EntityType.TEAM.name)

    def get_results_teams_dict(self):
        ''' Duels results by team '''
        return self.get_results_entity_dict(EntityType.TEAM.name)

    def get_winner_team(self):
        ''' Duel winner by team '''
        return self.get_winner_entity(EntityType.TEAM.name)
    
    def get_winner_team_members_list(self):
        ''' Members of winner team in a duel '''
        winner_team = self.get_winner_team()
        teams_members_dict_list = self.get_teams_members_dict_list()
        return teams_members_dict_list[winner_team]
    
    def get_losers_team_list(self):
        ''' Duel losers list by team '''
        return self.get_losers_entity_list(EntityType.TEAM.name)

    def get_losers_teams_members_list(self):
        ''' Members of losers teams in a duel '''
        losers_teams_members_list = list()
        teams_members_dict_list = self.get_teams_members_dict_list()
        losers_teams = self.get_losers_team_list()
        for team in losers_teams:
            losers_teams_members_list += teams_members_dict_list[team]
        return losers_teams_members_list

    # Rounds 
    def get_rounds_played_number(self):
        rounds_number = 0
        for combat in self.combats:
            rounds_number += combat.get_rounds_played_number()
        return rounds_number

    # Rounds entities
    def get_rounds_status_entity_dict_number(self, round_status, entity_type):
        ''' Number of some status rounds in a duel by entity '''
        combats_status_dict_number = dict() # Output
        entities_list = list() # List of entities in the duel
        if entity_type == EntityType.PLAYER.name: # Players
            entities_list = self.get_players_list()
        if entity_type == EntityType.CHARACTER.name: # Characters
            entities_list = self.get_characters_list()
        if entity_type == EntityType.TEAM.name: # Teams
            entities_list = self.get_characters_list()
        for entity in entities_list:
            combats_status_dict_number[entity] = 0 # Output
            for combat in self.combats:
                combat_entities = list()
                entity_p1 = None
                entity_p2 = None
                if entity_type == EntityType.PLAYER.name:
                    combat_entities = combat.get_players_list()
                    entity_p1 = combat.get_player1()
                    entity_p2 = combat.get_player2()
                if entity_type == EntityType.CHARACTER.name:
                    combat_entities = combat.get_characters_list()
                    entity_p1 = combat.get_character1()
                    entity_p2 = combat.get_character2()
                if entity_type == EntityType.TEAM.name:
                    combat_entities = combat.get_teams_list()
                    entity_p1 = combat.get_team1()
                    entity_p2 = combat.get_team2()
                if round_status == CombatStatus.PLAYED.name: # Rounds played
                    if entity in combat_entities:
                        combats_status_dict_number[entity] += combat.get_rounds_played_number()
                if round_status == CombatStatus.WON.name: # Rounds won
                    if entity in entities_list:
                        if entity_p1 == entity:
                            combats_status_dict_number[entity] += combat.get_rounds_won_p1_number()
                        elif entity_p2 == entity:
                            combats_status_dict_number[entity] += combat.get_rounds_won_p2_number()
                if round_status == CombatStatus.LOST.name: # Rounds lost
                    if entity in entities_list:
                        if entity_p1 == entity:
                            combats_status_dict_number[entity] += combat.get_rounds_lost_p1_number()
                        elif entity_p2 == entity:
                            combats_status_dict_number[entity] += combat.get_rounds_lost_p2_number()
        return combats_status_dict_number

    def get_rounds_win_rate_entity(self, entity_type):
        ''' Rounds win rate by entity '''
        rounds_win_rate_entities_dict = dict() # Output
        rounds_played_entity_dict_number = dict()
        rounds_won_entity_dict_number = dict()
        entities_list = list()
        if entity_type == EntityType.PLAYER.name: # Players
            rounds_played_entity_dict_number = self.get_rounds_played_player_dict_number()
            rounds_won_entity_dict_number = self.get_rounds_won_player_dict_number()
            entities_list = self.get_players_list()
        if entity_type == EntityType.CHARACTER.name: # Characters
            rounds_played_entity_dict_number = self.get_rounds_played_character_dict_number()
            rounds_won_entity_dict_number = self.get_rounds_won_character_dict_number()
            entities_list = self.get_characters_list()
        if entity_type == EntityType.TEAM.name: # Teams
            rounds_played_entity_dict_number = self.get_rounds_played_team_dict_number()
            rounds_won_entity_dict_number = self.get_rounds_won_team_dict_number()
            entities_list = self.get_teams_list()
        for entity in entities_list:
            rounds_win_rate_entities_dict[entity] = rounds_won_entity_dict_number[entity] / rounds_played_entity_dict_number[entity]
        return rounds_win_rate_entities_dict

    # Rounds players
    def get_rounds_played_player_dict_number(self):
        ''' Number of rounds played in a duel by player '''
        return self.get_rounds_status_entity_dict_number(RoundStatus.PLAYED.name, EntityType.PLAYER.name)
    
    def get_rounds_won_player_dict_number(self):
        ''' Number of rounds won in a duel by player '''
        return self.get_rounds_status_entity_dict_number(RoundStatus.WON.name, EntityType.PLAYER.name)
    
    def get_rounds_lost_player_dict_number(self):
        ''' Number of rounds lost in a duel by player '''
        return self.get_rounds_status_entity_dict_number(RoundStatus.LOST.name, EntityType.PLAYER.name)
    
    def get_rounds_win_rate_players(self):
        ''' Rounds win rates by player '''
        return self.get_rounds_win_rate_entity(EntityType.PLAYER.name)
    
    # Rounds characters
    def get_rounds_played_character_dict_number(self):
        ''' Number of rounds played in a duel by character '''
        return self.get_rounds_status_entity_dict_number(RoundStatus.PLAYED.name, EntityType.CHARACTER.name)
    
    def get_rounds_won_character_dict_number(self):
        ''' Number of rounds won in a duel by character '''
        return self.get_rounds_status_entity_dict_number(RoundStatus.WON.name, EntityType.CHARACTER.name)
    
    def get_rounds_lost_character_dict_number(self):
        ''' Number of rounds lost in a duel by character '''
        return self.get_rounds_status_entity_dict_number(RoundStatus.LOST.name, EntityType.CHARACTER.name)
    
    def get_rounds_win_rate_characters(self):
        ''' Rounds win rates by character '''
        return self.get_rounds_win_rate_entity(EntityType.CHARACTER.name)
    
    # Rounds team
    def get_rounds_played_team_dict_number(self):
        ''' Number of rounds played in a duel by team '''
        return self.get_rounds_status_entity_dict_number(RoundStatus.PLAYED.name, EntityType.TEAM.name)
    
    def get_rounds_won_team_dict_number(self):
        ''' Number of rounds won in a duel by team '''
        return self.get_rounds_status_entity_dict_number(RoundStatus.WON.name, EntityType.TEAM.name)
    
    def get_rounds_lost_team_dict_number(self):
        ''' Number of rounds lost in a duel by team '''
        return self.get_rounds_status_entity_dict_number(RoundStatus.LOST.name, EntityType.TEAM.name)
    
    def get_rounds_win_rate_teams(self):
        ''' Rounds win rates by player '''
        return self.get_rounds_win_rate_entity(EntityType.TEAM.name)
    
    # Ranking
    def get_duel_points_raw_dict(self, entity_type):
        duel_points_raw_dict = dict()
        entities_list = list()
        if entity_type == EntityType.PLAYER.name:
            entities_list = self.get_players_list()
        if entity_type == EntityType.CHARACTER.name:
            entities_list = self.get_characters_list()
        if  entity_type == EntityType.TEAM.name:
            entities_list = self.get_teams_list()
        for entity in entities_list:
            duel_points_raw_dict[entity] = 0
        for combat in self.combats:
            if entity_type == EntityType.PLAYER.name:
                combat_points_earned_dict = combat.get_combat_points_earned_player_dict()
            if entity_type == EntityType.CHARACTER.name:
                combat_points_earned_dict = combat.get_combat_points_earned_character_dict()
            if  entity_type == EntityType.TEAM.name:
                combat_points_earned_dict = combat.get_combat_points_earned_team_dict()
            for entity, points_earned in combat_points_earned_dict.items():
                duel_points_raw_dict[entity] += points_earned
        return duel_points_raw_dict

    def get_duel_points_raw_player_dict(self):
        return self.get_duel_points_raw_dict(EntityType.PLAYER.name)

    def get_duel_points_raw_character_dict(self):
        return self.get_duel_points_raw_dict(EntityType.CHARACTER.name)

    def get_duel_points_raw_team_dict(self):
        return self.get_duel_points_raw_dict(EntityType.TEAM.name)

    def get_combats_level_factor_dict(self, entity_type): # Pendiente de análisis
        return
        
    def get_duel_points_earned_dict(self, entity_type):
        duel_points_earned_dict = dict()
        if entity_type == EntityType.PLAYER.name:
            duel_points_raw_dict = self.get_duel_points_raw_player_dict()
            combats_beating_factors = self.get_combats_beating_factors_players()
        if entity_type == EntityType.CHARACTER.name:
            duel_points_raw_dict = self.get_duel_points_raw_player_dict()
            combats_beating_factors = self.get_combats_beating_factors_characters()
        if  entity_type == EntityType.TEAM.name:
            duel_points_raw_dict = self.get_duel_points_raw_player_dict()
            combats_beating_factors = self.get_combats_beating_factors_teams()
        for entity, points_raw in duel_points_raw_dict.items():
            duel_points_earned_dict[entity] = points_raw * combats_beating_factors[entity]
        return duel_points_earned_dict

    def get_duel_points_earned_player_dict(self):
        return self.get_duel_points_earned_dict(self, EntityType.PLAYER.name)

    def get_duel_points_earned_character_dict(self):
        return self.get_duel_points_earned_dict(self, EntityType.CHARACTER.name)

    def get_duel_points_earned_team_dict(self):
        return self.get_duel_points_earned_dict(self, EntityType.TEAM.name)


# Combat group

class Stage(Base):
    __tablename__ = "stage"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    ring_out = Column(Boolean, nullable=False)
    walls_destructible = Column(Boolean, nullable=False)
    walls_low = Column(Boolean, nullable=False)
    walls_high = Column(Boolean, nullable=False)

    ''' Relationships '''
    combats = relationship("Combat", back_populates="stage", cascade="all, delete-orphan")

    ''' Methods ''' 
    # Rounds
    def get_rounds_played_number(self):
        rounds_played_number = 0
        for combat in self.combats:
            rounds_played_number += combat.get_rounds_played_number()
        return rounds_played_number
    
    # Combats
    def get_combats_played_list(self):
        return self.combats

    def get_combats_played_number(self):
        return len(self.combats)


class SocialMedia(Base):
    __tablename__ = "social_media"

    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    link = Column(String, nullable=False)

    player_id = Column(Integer, ForeignKey("player.id"), nullable=False)

    ''' Relationships '''
    player = relationship("Player", back_populates="social_medias")


class Country(Base):
    __tablename__ = "country"

    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    code_name = Column(String, nullable=False)
    flag_link = Column(String, nullable=False)

    ''' Relationships '''
    players = relationship("Player", back_populates="country", cascade="all, delete-orphan")

    ''' Methods '''
    def get_players_list(self):
        return self.players

    def get_players_numbers(self):
        return len(self.players)
    
    def get_country_results_dict(self):
        ''' Number of results by position '''
        country_ranking_dict = dict()
        for player in self.players():
            events_results_dict = player.get_events_results_dict()
            for position in events_results_dict.values():
                if country_ranking_dict.get(position):
                    country_ranking_dict[position] += 1
                else:
                    country_ranking_dict[position] = 1
        country_ranking_dict = dict(sorted(country_ranking_dict.items(), key=lambda x:x[0]))
        return country_ranking_dict


player_team = Table(
    "player_team",
    Base.metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("player_id", Integer, ForeignKey('player.id'), primary_key=True, nullable=False),
    Column("team_id", Integer, ForeignKey('team.id'), primary_key=True, nullable=False)
)


class Entity(Base):
    __tablename__ = "entity"
    __abstract__ = True

    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False) # Childs column

    __mapper_args__ = {
        "polymorphic_on": type,
    }

    ''' Methods '''
    # Getters
    def get_name(self):
        return self.name
    
    # Performance
    def get_win_rate(self, victories, played):
        return victories / played
    
    def get_win_lose_ratio(self, func, victories, defeats):
        win_lose_ratio = 0
        if defeats == 0:
            win_lose_ratio = victories
        elif victories == 0:
            win_lose_ratio = 0.5 / defeats
        elif defeats == 1:
            win_lose_ratio = victories * (3 / 4)
        else:
            win_lose_ratio = victories / defeats
        return func(win_lose_ratio)
    
    def get_performance(self, func, performance_metric, victories, defeats, played):
        performance = 0
        if performance_metric == PerformanceMetric.WIN_RATE.name:
            performance = self.get_win_rate(victories, played)
        if performance_metric == PerformanceMetric.WIN_LOSE_RATIO.name:
            performance = self.get_win_lose_ratio(func, victories, defeats)
        return performance

    # Events
    def get_events_played_list(self, combats_list):
        ''' List of events played by an entity '''
        events_played_set = set()
        for combat in combats_list:
            events_played_set.add(combat.get_event())
        events_played_list = list(sorted(list(events_played_set), key=lambda x:x.event_order))
        return events_played_list
    
    # def get_events_played_number(self, combats_list):
    #     ''' Number of events played by an entity '''
    #     return len(self.get_events_played_list(combats_list))
    
    # Combats lists
    def get_combats_status_list(self, challenge_status, combats_list):
        combats_status_list = list()
        for combat in combats_list:
            if challenge_status == ChallengeStatus.PLAYED.name:
                combats_status_list.append(combat)
            if challenge_status == ChallengeStatus.WON.name:
                if self in combat.get_winners_entities_list():
                    combats_status_list.append(combat)
            if challenge_status == ChallengeStatus.LOST.name:
                if self in combat.get_losers_entities_list():
                    combats_status_list.append(combat)
            if challenge_status == ChallengeStatus.DRAW.name:
                if combat.is_draw():
                    combats_status_list.append(combat)
        combats_status_list = list(sorted(combats_status_list, key=lambda x:x.combat_order))
        return combats_status_list
    
    # Combats numbers
    # def get_combats_status_number(self, combats_list):
    #     return len(combats_list)

    # Combats stages lists
    def get_stages_list(self, combats_list):
        stages_set = set()
        for combat in combats_list:
            stages_set.add(combat.get_stage())
        return list(stages_set)
    
    def get_combats_stage_status_dict_list(self, challenge_status, combats_list):
        combats_stage_status_dict_list = dict()
        for stage in self.get_stages_list(combats_list):
            combats_stage_status_dict_list[stage] = list()
        for combat in combats_list:
            if challenge_status == ChallengeStatus.PLAYED.name:
                combats_stage_status_dict_list[combat.get_stage()].append(combat)
            if challenge_status == ChallengeStatus.WON.name:
                if self in combat.get_winners_entities_list():
                    combats_stage_status_dict_list[combat.get_stage()].append(combat)
            if challenge_status == ChallengeStatus.LOST.name:
                if self in combat.get_losers_entities_list():
                    combats_stage_status_dict_list[combat.get_stage()].append(combat)
            if challenge_status == ChallengeStatus.DRAW.name:
                if combat.is_draw():
                    combats_stage_status_dict_list[combat.get_stage()].append(combat)
        return combats_stage_status_dict_list

    # Combats stages numbers
    def get_combats_stage_status_dict_number(self, combats_stage_dict_list):
        combats_stage_status_dict_number = dict()
        for stage, combats_stage_list in combats_stage_dict_list.items():
            combats_stage_status_dict_number[stage] = len(combats_stage_list)
        return combats_stage_status_dict_number

    # Combats stages performance
    def get_combats_stage_performance_dict(self, func, performance_metric, victories_dict, defeats_dict, played_dict):
        get_combats_stage_performance_dict = dict()
        for stage in victories_dict.keys():
            if performance_metric == PerformanceMetric.WIN_RATE.name:
                get_combats_stage_performance_dict[stage] = self.get_performance(func, PerformanceMetric.WIN_RATE.name, victories_dict[stage], defeats_dict[stage], played_dict[stage])
            if performance_metric == PerformanceMetric.WIN_LOSE_RATIO.name:
                get_combats_stage_performance_dict[stage] = self.get_performance(func, PerformanceMetric.WIN_LOSE_RATIO.name, victories_dict[stage], defeats_dict[stage], played_dict[stage])
        return get_combats_stage_performance_dict

    # Rounds
    def get_rounds_played_number(self, combats_list):
        rounds_played_number = 0
        for combat in combats_list:
            rounds_played_number += combat.get_rounds_played_number()

    def get_rounds_status_number(self, challenge_status, combats_list):
        rounds_status_number_obj = Scoreboard(0, 0)
        for combat in combats_list:
            if challenge_status == ChallengeStatus.WON.name:
                rounds_status_number_obj.add_to_player1(combat.get_rounds_won_p1_number())
                rounds_status_number_obj.add_to_player2(combat.get_rounds_won_p2_number())
            if challenge_status == ChallengeStatus.LOST.name:
                rounds_status_number_obj.add_to_player1(combat.get_rounds_lost_p1_number())
                rounds_status_number_obj.add_to_player2(combat.get_rounds_lost_p2_number())
        return rounds_status_number_obj
    

class Competitor(Entity):
    __tablename__ = "competitor"
    __abstract__ = True

    ''' Attributes '''
    id = Column(Integer, ForeignKey('entity.id'), primary_key=True, nullable=False)
    type = Column(String, nullable=False) # Childs column

    __mapper_args__ = {
        "polymorphic_on": type,
    }

    ''' Methods '''
    # Getters
    def get_name(self):
        return super().get_name()

    # Performance    
    def get_performance(self, func, performance_metric, victories, defeats, played):
        return super().get_performance(func, performance_metric, victories, defeats, played)

    # Events
    def get_events_played_list(self, combats_list):
        return super().get_events_played_list(combats_list)

    def get_events_result_dict(self, combats_list):
        events_results_dict = dict() # Output
        events_played_list = self.get_events_played_list(combats_list)
        for event in events_played_list:
            events_results_dict[event] = event.get_results_dict()[self]
        return events_results_dict

    # Combats lists
    def get_combats_status_list(self, challenge_status, combats_list):
        return super().get_combats_status_list(challenge_status, combats_list)

    # Combats stages list
    def get_combats_stage_status_dict_list(self, challenge_status, combats_list):
        return super().get_combats_stage_status_dict_list(challenge_status, combats_list)

    # Combats stages numbers
    def get_combats_stage_status_dict_number(self, combats_stage_dict_list):
        return super().get_combats_stage_status_dict_number(combats_stage_dict_list)

    # Combats stages performance
    def get_combats_stage_performance_dict(self, func, performance_metric, victories_dict, defeats_dict, played_dict):
        return super().get_combats_stage_performance_dict(func, performance_metric, victories_dict, defeats_dict, played_dict)

    # Rounds numbers
    def get_rounds_played_number(self, combats_list):
        return super().get_rounds_played_number(combats_list)
    
    def get_rounds_status_number(self, challenge_status, combats_list):
        return super().get_rounds_status_number(challenge_status, combats_list)

    # Duels lists
    def get_duels_status_list(self, challenge_status, combats_list):
        duels_status_set = set()
        for combat in combats_list:
            duel = combat.get_duel()
            if challenge_status == ChallengeStatus.PLAYED.name:
                duels_status_set.add(duel)
            if challenge_status == ChallengeStatus.WON.name:
                if duel.get_winner() == self:
                    duels_status_set.add(duel)
            if challenge_status == ChallengeStatus.LOST.name:
                if self in duel.get_losers_list():
                    duels_status_set.add(duel)
        duels_status_list = list(sorted(list(duels_status_set), key=lambda x:x.duel_order))
        return duels_status_list


class Player(Competitor):
    __tablename__ = "player"

    ''' Attributes '''
    id = Column(Integer, ForeignKey('competitor.id'), primary_key=True, nullable=False)
    playlist = Column(String, nullable=True)

    country_id = Column(Integer, ForeignKey("country.id"), nullable=False)

    __mapper_args__ = {"polymorphic_identity": "player"}

    ''' Relationships '''
    country = relationship("Country", back_populates="players")
    combats_p1 = relationship("Combat", back_populates="player1", cascade="all, delete-orphan")
    combats_p2 = relationship("Combat", back_populates="player2", cascade="all, delete-orphan")
    players_characters = relationship("PlayerCharacter", back_populates="player", cascade="all, delete-orphan")
    social_medias = relationship("SocialMedia", back_populates="player", cascade="all, delete-orphan")
    teams = relationship('Team', secondary=player_team, back_populates='players')

    ''' Methods '''
    # Getters
    def get_name(self):
        return super().get_name()

    def get_playlist(self):
        return self.playlist
    
    def get_country(self):
        return self.country

    def get_social_medias_list(self):
        return self.social_medias

    # Combats lists
    # P1
    def get_combats_played_p1_list(self):
        return super().get_combats_status_list(ChallengeStatus.PLAYED.name, self.combats_p1)

    def get_combats_won_p1_list(self):
        return super().get_combats_status_list(ChallengeStatus.WON.name, self.combats_p1)
    
    def get_combats_lost_p1_list(self):
        return super().get_combats_status_list(ChallengeStatus.LOST.name, self.combats_p1)

    def get_combats_draw_p1_list(self):
        return super().get_combats_status_list(ChallengeStatus.DRAW.name, self.combats_p1)
    
    # P2
    def get_combats_played_p2_list(self):
        return super().get_combats_status_list(ChallengeStatus.PLAYED.name, self.combats_p2)

    def get_combats_won_p2_list(self):
        return super().get_combats_status_list(ChallengeStatus.WON.name, self.combats_p2)
    
    def get_combats_lost_p2_list(self):
        return super().get_combats_status_list(ChallengeStatus.LOST.name, self.combats_p2)

    def get_combats_draw_p2_list(self):
        return super().get_combats_status_list(ChallengeStatus.DRAW.name, self.combats_p2)

    # BOTH
    def get_combats_played_list(self):
        return super().get_combats_status_list(ChallengeStatus.PLAYED.name, self.combats_p1 + self.combats_p2)

    def get_combats_won_list(self):
        return super().get_combats_status_list(ChallengeStatus.WON.name, self.combats_p1 + self.combats_p2)
    
    def get_combats_lost_list(self):
        return super().get_combats_status_list(ChallengeStatus.LOST.name, self.combats_p1 + self.combats_p2)

    def get_combats_draw_list(self):
        return super().get_combats_status_list(ChallengeStatus.DRAW.name, self.combats_p1 + self.combats_p2)

    # Combats numbers
    # P1
    def get_combats_played_p1_number(self):
        return len(self.get_combats_played_p1_list())

    def get_combats_won_p1_number(self):
        return len(self.get_combats_won_p1_list())
    
    def get_combats_lost_p1_number(self):
        return len(self.get_combats_lost_p1_list())
    
    def get_combats_draw_p1_number(self):
        return len(self.get_combats_draw_p1_list())

    # P2
    def get_combats_played_p2_number(self):
        return len(self.get_combats_played_p2_list())

    def get_combats_won_p2_number(self):
        return len(self.get_combats_won_p2_list())
    
    def get_combats_lost_p2_number(self):
        return len(self.get_combats_lost_p2_list())
    
    def get_combats_draw_p2_number(self):
        return len(self.get_combats_draw_p2_list())

    # BOTH
    def get_combats_played_number(self):
        return len(self.get_combats_played_list())

    def get_combats_won_number(self):
        return len(self.get_combats_won_list())
    
    def get_combats_lost_number(self):
        return len(self.get_combats_lost_list())
    
    def get_combats_draw_number(self):
        return len(self.get_combats_draw_list())
    
    # Combats performance
    # Win rate
    def get_combats_p1_win_rate(self, func):
        victories = self.get_combats_won_p1_number() + (self.get_combats_draw_p1_number() / 2)
        defeats = self.get_combats_lost_p1_number()
        played = self.get_combats_played_p1_number()
        return super().get_performance(func, PerformanceMetric.WIN_RATE.name, victories, defeats, played)

    def get_combats_p2_win_rate(self, func):
        victories = self.get_combats_won_p2_number() + (self.get_combats_draw_p2_number() / 2)
        defeats = self.get_combats_lost_p2_number()
        played = self.get_combats_played_p2_number()
        return super().get_performance(func, PerformanceMetric.WIN_RATE.name, victories, defeats, played)
    
    def get_combats_win_rate(self, func):
        victories = self.get_combats_won_number() + (self.get_combats_draw_number() / 2)
        defeats = self.get_combats_lost_number()
        played = self.get_combats_played_number()
        return super().get_performance(func, PerformanceMetric.WIN_RATE.name, victories, defeats, played)

    # Win lose ratio
    def get_combats_p1_win_lose_ratio(self, func):
        victories = self.get_combats_won_p1_number() + (self.get_combats_draw_p1_number() / 2)
        defeats = self.get_combats_lost_p1_number()
        played = self.get_combats_played_p1_number()
        return super().get_performance(func, PerformanceMetric.WIN_LOSE_RATIO.name, victories, defeats, played)

    def get_combats_p2_win_lose_ratio(self, func):
        victories = self.get_combats_won_p2_number() + (self.get_combats_draw_p2_number() / 2)
        defeats = self.get_combats_lost_p2_number()
        played = self.get_combats_played_p2_number()
        return super().get_performance(func, PerformanceMetric.WIN_LOSE_RATIO.name, victories, defeats, played)
    
    def get_combats_win_lose_ratio(self, func):
        victories = self.get_combats_won_number() + (self.get_combats_draw_number() / 2)
        defeats = self.get_combats_lost_number()
        played = self.get_combats_played_number()
        return super().get_performance(func, PerformanceMetric.WIN_LOSE_RATIO.name, victories, defeats, played)

    # Combats stage lists
    # P1
    def get_combats_stage_played_p1_dict_list(self):
        return super().get_combats_stage_status_dict_list(ChallengeStatus.PLAYED.name, self.combats_p1)

    def get_combats_stage_won_p1_dict_list(self):
        return super().get_combats_stage_status_dict_list(ChallengeStatus.WON.name, self.combats_p1)
    
    def get_combats_stage_lost_p1_dict_list(self):
        return super().get_combats_stage_status_dict_list(ChallengeStatus.LOST.name, self.combats_p1)
    
    def get_combats_stage_draw_p1_dict_list(self):
        return super().get_combats_stage_status_dict_list(ChallengeStatus.DRAW.name, self.combats_p1)

    # P2
    def get_combats_stage_played_p2_dict_list(self):
        return super().get_combats_stage_status_dict_list(ChallengeStatus.PLAYED.name, self.combats_p2)

    def get_combats_stage_won_p2_dict_list(self):
        return super().get_combats_stage_status_dict_list(ChallengeStatus.WON.name, self.combats_p2)
    
    def get_combats_stage_lost_p2_dict_list(self):
        return super().get_combats_stage_status_dict_list(ChallengeStatus.LOST.name, self.combats_p2)
    
    def get_combats_stage_draw_p2_dict_list(self):
        return super().get_combats_stage_status_dict_list(ChallengeStatus.DRAW.name, self.combats_p2)

    # BOTH
    def get_combats_stage_played_dict_list(self):
        return super().get_combats_stage_status_dict_list(ChallengeStatus.PLAYED.name, self.combats_p1 + self.combats_p2)

    def get_combats_stage_won_dict_list(self):
        return super().get_combats_stage_status_dict_list(ChallengeStatus.WON.name, self.combats_p1 + self.combats_p2)
    
    def get_combats_stage_lost_dict_list(self):
        return super().get_combats_stage_status_dict_list(ChallengeStatus.LOST.name, self.combats_p1 + self.combats_p2)
    
    def get_combats_stage_draw_dict_list(self):
        return super().get_combats_stage_status_dict_list(ChallengeStatus.DRAW.name, self.combats_p1 + self.combats_p2)

    # Combats stage numbers @@@@
    # P1
    def get_combats_stage_played_p1_dict_number(self):
        return super().get_combats_stage_played_dict_number(self.get_combats_played_p1_list())
    
    def get_combats_stage_won_p1_dict_number(self):
        return super().get_combats_stage_won_dict_number(self.get_combats_played_p1_list())
    
    def get_combats_stage_lost_p1_dict_number(self):
        return super().get_combats_stage_lost_dict_number(self.get_combats_played_p1_list())
    
    def get_combats_stage_draw_p1_dict_number(self):
        return super().get_combats_stage_draw_dict_number(self.get_combats_played_p1_list())
    
    # P2
    def get_combats_stage_played_p2_dict_number(self):
        return super().get_combats_stage_played_dict_number(self.get_combats_played_p2_list())
    
    def get_combats_stage_won_p2_dict_number(self):
        return super().get_combats_stage_won_dict_number(self.get_combats_played_p2_list())
    
    def get_combats_stage_lost_p2_dict_number(self):
        return super().get_combats_stage_lost_dict_number(self.get_combats_played_p2_list())
    
    def get_combats_stage_draw_p2_dict_number(self):
        return super().get_combats_stage_draw_dict_number(self.get_combats_played_p2_list())
    
    # BOTH
    def get_combats_stage_played_dict_number(self):
        return super().get_combats_stage_played_dict_number(self.get_combats_played_list())
    
    def get_combats_stage_won_dict_number(self):
        return super().get_combats_stage_won_dict_number(self.get_combats_played_list())
    
    def get_combats_stage_lost_dict_number(self):
        return super().get_combats_stage_lost_dict_number(self.get_combats_played_list())
    
    def get_combats_stage_draw_dict_number(self):
        return super().get_combats_stage_draw_dict_number(self.get_combats_played_list())

    # Combats stage performance
    # Win rate
    def get_combats_stage_win_rate_p1_dict(self, func):
        return super().get_combats_stage_win_rate_dict(func, self.get_combats_played_p1_list())
    
    def get_combats_stage_win_rate_p2_dict(self, func):
        return super().get_combats_stage_win_rate_dict(func, self.get_combats_played_p2_list())
    
    def get_combats_stage_win_rate_dict(self, func):
        return super().get_combats_stage_win_rate_dict(func, self.get_combats_played_list())

    # Win lose ratio
    def get_combats_stage_win_lose_ratio_p1_dict(self, func):
        return super().get_combats_stage_win_lose_ratio_dict(func, self.get_combats_played_p1_list())
    
    def get_combats_stage_win_lose_ratio_p2_dict(self, func):
        return super().get_combats_stage_win_lose_ratio_dict(func, self.get_combats_played_p2_list())
    
    def get_combats_stage_win_lose_ratio_dict(self, func):
        return super().get_combats_stage_win_lose_ratio_dict(func, self.get_combats_played_list())

    # Events
    def get_events_played_list(self):
        return super().get_events_played_list(self.get_combats_played_list())

    def get_events_played_number(self):
        return super().get_events_played_number(self.get_combats_played_list())
    
    def get_events_result_dict(self):
        return super().get_events_result_dict(self.get_combats_played_list())

    # Duels lists
    def get_duels_played_list(self):
        return super().get_duels_played_list(self.get_combats_played_list())

    def get_duels_won_list(self):
        return super().get_duels_won_list(self.get_combats_played_list())

    def get_duels_lost_list(self):
        return super().get_duels_lost_list(self.get_combats_played_list())

    # Duels numbers
    def get_duels_played_number(self):
        return super().get_duels_played_number(self.get_combats_played_list())

    def get_duels_won_number(self):
        return super().get_duels_won_number(self.get_combats_played_list())

    def get_duels_lost_number(self):
        return super().get_duels_lost_number(self.get_combats_played_list())

    # Duels performance
    def get_duels_win_rate(self, func):
        return super().get_duels_win_rate(func, self.get_combats_played_list())

    def get_duels_win_lose_ratio(self, func):
        return super().get_duels_win_lose_ratio(func, self.get_combats_played_list())

    # Rounds
    # P1
    def get_rounds_played_p1_number(self):
        return super().get_rounds_played_number(self.get_combats_played_p1_list())
    
    def get_rounds_won_p1_number(self):
        return super().get_rounds_won_number(self.get_combats_played_list()).get_player1()
    
    def get_rounds_lost_p1_number(self):
        return super().get_rounds_lost_number(self.get_combats_played_list()).get_player1()

    # P2
    def get_rounds_played_p2_number(self):
        return super().get_rounds_played_number(self.get_combats_played_p2_list())
    
    def get_rounds_won_p2_number(self):
        return super().get_rounds_won_number(self.get_combats_played_list()).get_player2()
    
    def get_rounds_lost_p2_number(self):
        return super().get_rounds_lost_number(self.get_combats_played_list()).get_player2()

    # BOTH
    def get_rounds_played_number(self):
        return super().get_rounds_played_number(self.get_combats_played_list())
    
    def get_rounds_won_number(self):
        return super().get_rounds_won_number(self.get_combats_played_list()).get_total()
    
    def get_rounds_lost_number(self):
        return super().get_rounds_lost_number(self.get_combats_played_list()).get_total()

    # Rounds performance
    # Win rate
    def get_rounds_p1_win_rate(self, func):
        return super().get_rounds_win_rate(func, self.get_combats_played_p1_list())
    
    def get_rounds_p2_win_rate(self, func):
        return super().get_rounds_win_rate(func, self.get_combats_played_p2_list())
    
    def get_rounds_win_rate(self, func):
        return super().get_rounds_win_rate(func, self.get_combats_played_list())

    # Win lose ratio
    def get_rounds_p1_win_lose_ratio(self, func):
        return super().get_rounds_win_lose_ratio(func, self.get_combats_played_p1_list())

    def get_rounds_p2_win_lose_ratio(self, func):
        return super().get_rounds_win_lose_ratio(func, self.get_combats_played_p2_list())
    
    def get_rounds_win_lose_ratio(self, func):
        return super().get_rounds_win_lose_ratio(func, self.get_combats_played_list())

    # Team duels lists
    def get_team_duels_status_list(self, challenge_status):
        team_duels_status_list = list()
        duels_status_list = list()
        if challenge_status == ChallengeStatus.PLAYED.name:
            duels_status_list = self.get_duels_played_list()
        if challenge_status == ChallengeStatus.WON.name:
            duels_status_list = self.get_duels_won_list()
        if challenge_status == ChallengeStatus.LOST.name:
            duels_status_list = self.get_duels_lost_list()
        for duel in duels_status_list:
            if duel.is_team_duel():
                team_duels_status_list.append(duel)
        return team_duels_status_list

    def get_team_duels_played_list(self):
        return self.get_team_duels_status_list(ChallengeStatus.PLAYED.name)
    
    def get_team_duels_won_list(self):
        return self.get_team_duels_status_list(ChallengeStatus.WON.name)
    
    def get_team_duels_lost_list(self):
        return self.get_team_duels_status_list(ChallengeStatus.LOST.name)

    # Team duels numbers
    def get_team_duels_played_number(self):
        return len(self.get_team_duels_played_list())
    
    def get_team_duels_won_number(self):
        return len(self.get_team_duels_won_list())
    
    def get_team_duels_lost_number(self):
        return len(self.get_team_duels_lost_list())

    # Team duels performance
    def get_team_duels_performance(self, func, performance_metric):
        team_duels_performance = 0
        victories = self.get_team_duels_won_number()
        defeats = self.get_team_duels_lost_number()
        played = self.get_team_duels_played_number()
        if performance_metric == PerformanceMetric.WIN_RATE.name:
            team_duels_performance = self.get_win_rate(victories, played)
        if performance_metric == PerformanceMetric.WIN_LOSE_RATIO.name:
            team_duels_performance = self.get_win_lose_ratio(func, victories, defeats)
        return team_duels_performance
    
    def get_team_duels_win_rate(self, func):
        return self.get_team_duels_performance(func, PerformanceMetric.WIN_RATE.name)
    
    def get_team_duels_win_lose_ratio(self, func):
        return self.get_team_duels_performance(func, PerformanceMetric.WIN_LOSE_RATIO.name)


class Team(Competitor):
    __tablename__ = "team"

    ''' Attributes '''
    id = Column(Integer, ForeignKey('competitor.id'), primary_key=True, nullable=False)
    initials = Column(String, nullable=False)

    __mapper_args__ = {"polymorphic_identity": "team"}

    ''' Relationships '''
    players = relationship('Player', secondary=player_team, back_populates='teams')
    combats_p1 = relationship("Combat", back_populates="team1", cascade="all, delete-orphan")
    combats_p2 = relationship("Combat", back_populates="team2", cascade="all, delete-orphan")

    ''' Methods '''
    # Getters
    def get_name(self):
        return super().get_name()
    
    def get_initials(self):
        return self.initials

    def get_team_members_list(self):
        return self.players
    
    # Country
    def get_country(self):
        country = None # When is an international team
        countries_set = set()
        for player in self.players:
            countries_set.add(player.get_country())
        if len(countries_set) == 1:
            country = list(countries_set)[0]
        return country
    
    # Combats lists
    # P1
    def get_combats_played_p1_list(self):
        return super().get_combats_played_list(self.combats_p1)

    def get_combats_won_p1_list(self):
        return super().get_combats_won_list(self.combats_p1)
    
    def get_combats_lost_p1_list(self):
        return super().get_combats_lost_list(self.combats_p1)
    
    def get_combats_draw_p1_list(self):
        return super().get_combats_draw_list(self.combats_p1)

    # P2
    def get_combats_played_p2_list(self):
        return super().get_combats_played_list(self.combats_p2)

    def get_combats_won_p2_list(self):
        return super().get_combats_won_list(self.combats_p2)
    
    def get_combats_lost_p2_list(self):
        return super().get_combats_lost_list(self.combats_p2)
    
    def get_combats_draw_p2_list(self):
        return super().get_combats_draw_list(self.combats_p2)

    # BOTH
    def get_combats_played_list(self):
        return super().get_combats_played_list(self.combats_p1 + self.combats_p2)

    def get_combats_won_list(self):
        return super().get_combats_won_list(self.combats_p1 + self.combats_p2)
    
    def get_combats_lost_list(self):
        return super().get_combats_lost_list(self.combats_p1 + self.combats_p2)
    
    def get_combats_draw_list(self):
        return super().get_combats_draw_list(self.combats_p1 + self.combats_p2)

    # Combats numbers
    # P1
    def get_combats_played_p1_number(self):
        return super().get_combats_played_number(self.combats_p1)
    
    def get_combats_won_p1_number(self):
        return super().get_combats_won_number(self.combats_p1)
    
    def get_combats_lost_p1_number(self):
        return super().get_combats_lost_number(self.combats_p1)
    
    def get_combats_draw_p1_number(self):
        return super().get_combats_draw_number(self.combats_p1)

    # P2
    def get_combats_played_p2_number(self):
        return super().get_combats_played_number(self.combats_p2)
    
    def get_combats_won_p2_number(self):
        return super().get_combats_won_number(self.combats_p2)
    
    def get_combats_lost_p2_number(self):
        return super().get_combats_lost_number(self.combats_p2)
    
    def get_combats_draw_p2_number(self):
        return super().get_combats_draw_number(self.combats_p2)

    # BOTH
    def get_combats_played_number(self):
        return super().get_combats_played_number(self.combats_p1 + self.combats_p2)
    
    def get_combats_won_number(self):
        return super().get_combats_won_number(self.combats_p1 + self.combats_p2)
    
    def get_combats_lost_number(self):
        return super().get_combats_lost_number(self.combats_p1 + self.combats_p2)
    
    def get_combats_draw_number(self):
        return super().get_combats_draw_number(self.combats_p1 + self.combats_p2)
    
    # Combats performance
    # Win rate
    def get_combats_p1_win_rate(self, func):
        return super().get_combats_win_rate(func, self.combats_p1)
    
    def get_combats_p2_win_rate(self, func):
        return super().get_combats_win_rate(func, self.combats_p2)
    
    def get_combats_win_rate(self, func):
        return super().get_combats_win_rate(func, self.combats_p1 + self.combats_p2)

    # Win lose ratio
    def get_combats_p1_win_lose_ratio(self, func):
        return super().get_combats_win_lose_ratio(func, self.combats_p1)

    def get_combats_p2_win_lose_ratio(self, func):
        return super().get_combats_win_lose_ratio(func, self.combats_p2)
    
    def get_combats_win_lose_ratio(self, func):
        return super().get_combats_win_lose_ratio(func, self.combats_p1 + self.combats_p2)

    # Combats stage lists
    # P1
    def get_combats_stage_played_p1_dict_list(self):
        return super().get_combats_stage_played_dict_list(self.get_combats_played_p1_list())

    def get_combats_stage_won_p1_dict_list(self):
        return super().get_combats_stage_won_dict_list(self.get_combats_played_p1_list())

    def get_combats_stage_lost_p1_dict_list(self):
        return super().get_combats_stage_lost_dict_list(self.get_combats_played_p1_list())

    def get_combats_stage_draw_p1_dict_list(self):
        return super().get_combats_stage_draw_dict_list(self.get_combats_played_p1_list())

    # P2
    def get_combats_stage_played_p2_dict_list(self):
        return super().get_combats_stage_played_dict_list(self.get_combats_played_p2_list())

    def get_combats_stage_won_p2_dict_list(self):
        return super().get_combats_stage_won_dict_list(self.get_combats_played_p2_list())

    def get_combats_stage_lost_p2_dict_list(self):
        return super().get_combats_stage_lost_dict_list(self.get_combats_played_p2_list())

    def get_combats_stage_draw_p2_dict_list(self):
        return super().get_combats_stage_draw_dict_list(self.get_combats_played_p2_list())

    # BOTH
    def get_combats_stage_played_dict_list(self):
        return super().get_combats_stage_played_dict_list(self.get_combats_played_list())

    def get_combats_stage_won_dict_list(self):
        return super().get_combats_stage_won_dict_list(self.get_combats_played_list())

    def get_combats_stage_lost_dict_list(self):
        return super().get_combats_stage_lost_dict_list(self.get_combats_played_list())

    def get_combats_stage_draw_dict_list(self):
        return super().get_combats_stage_draw_dict_list(self.get_combats_played_list())

    # Combats stage numbers
    # P1
    def get_combats_stage_played_p1_dict_number(self):
        return super().get_combats_stage_played_dict_number(self.get_combats_played_p1_list())
    
    def get_combats_stage_won_p1_dict_number(self):
        return super().get_combats_stage_won_dict_number(self.get_combats_played_p1_list())
    
    def get_combats_stage_lost_p1_dict_number(self):
        return super().get_combats_stage_lost_dict_number(self.get_combats_played_p1_list())
    
    def get_combats_stage_draw_p1_dict_number(self):
        return super().get_combats_stage_draw_dict_number(self.get_combats_played_p1_list())
    
    # P2
    def get_combats_stage_played_p2_dict_number(self):
        return super().get_combats_stage_played_dict_number(self.get_combats_played_p2_list())
    
    def get_combats_stage_won_p2_dict_number(self):
        return super().get_combats_stage_won_dict_number(self.get_combats_played_p2_list())
    
    def get_combats_stage_lost_p2_dict_number(self):
        return super().get_combats_stage_lost_dict_number(self.get_combats_played_p2_list())
    
    def get_combats_stage_draw_p2_dict_number(self):
        return super().get_combats_stage_draw_dict_number(self.get_combats_played_p2_list())
    
    # BOTH
    def get_combats_stage_played_dict_number(self):
        return super().get_combats_stage_played_dict_number(self.get_combats_played_list())
    
    def get_combats_stage_won_dict_number(self):
        return super().get_combats_stage_won_dict_number(self.get_combats_played_list())
    
    def get_combats_stage_lost_dict_number(self):
        return super().get_combats_stage_lost_dict_number(self.get_combats_played_list())
    
    def get_combats_stage_draw_dict_number(self):
        return super().get_combats_stage_draw_dict_number(self.get_combats_played_list())

    # Combats stage performance
    # Win rate
    def get_combats_stage_win_rate_p1_dict(self, func):
        return super().get_combats_stage_win_rate_dict(func, self.get_combats_played_p1_list())
    
    def get_combats_stage_win_rate_p2_dict(self, func):
        return super().get_combats_stage_win_rate_dict(func, self.get_combats_played_p2_list())
    
    def get_combats_stage_win_rate_dict(self, func):
        return super().get_combats_stage_win_rate_dict(func, self.get_combats_played_list())

    # Win lose ratio
    def get_combats_stage_win_lose_ratio_p1_dict(self, func):
        return super().get_combats_stage_win_lose_ratio_dict(func, self.get_combats_played_p1_list())
    
    def get_combats_stage_win_lose_ratio_p2_dict(self, func):
        return super().get_combats_stage_win_lose_ratio_dict(func, self.get_combats_played_p2_list())
    
    def get_combats_stage_win_lose_ratio_dict(self, func):
        return super().get_combats_stage_win_lose_ratio_dict(func, self.get_combats_played_list())

    # Events
    def get_events_played_list(self):
        return super().get_events_played_list(self.get_combats_played_list())

    def get_events_played_number(self):
        return super().get_events_played_number(self.get_combats_played_list())
    
    def get_events_result_dict(self):
        return super().get_events_result_dict(self.get_combats_played_list())
    
    # Duels lists
    def get_duels_played_list(self):
        return super().get_duels_played_list(self.get_combats_played_list())

    def get_duels_won_list(self):
        return super().get_duels_won_list(self.get_combats_played_list())

    def get_duels_lost_list(self):
        return super().get_duels_lost_list(self.get_combats_played_list())

    # Duels numbers
    def get_duels_played_number(self):
        return super().get_duels_played_number(self.get_combats_played_list())

    def get_duels_won_number(self):
        return super().get_duels_won_number(self.get_combats_played_list())

    def get_duels_lost_number(self):
        return super().get_duels_lost_number(self.get_combats_played_list())

    # Duels performance
    def get_duels_win_rate(self, func):
        return super().get_duels_win_rate(func, self.get_combats_played_list())

    def get_duels_win_lose_ratio(self, func):
        return super().get_duels_win_lose_ratio(func, self.get_combats_played_list())

    # Rounds
    # P1
    def get_rounds_played_p1_number(self):
        return super().get_rounds_played_number(self.get_combats_played_p1_list())
    
    def get_rounds_won_p1_number(self):
        return super().get_rounds_won_number(self.get_combats_played_list()).get_player1()
    
    def get_rounds_lost_p1_number(self):
        return super().get_rounds_lost_number(self.get_combats_played_list()).get_player1()

    # P2
    def get_rounds_played_p2_number(self):
        return super().get_rounds_played_number(self.get_combats_played_p2_list())
    
    def get_rounds_won_p2_number(self):
        return super().get_rounds_won_number(self.get_combats_played_list()).get_player2()
    
    def get_rounds_lost_p2_number(self):
        return super().get_rounds_lost_number(self.get_combats_played_list()).get_player2()

    # BOTH
    def get_rounds_played_number(self):
        return super().get_rounds_played_number(self.get_combats_played_list())
    
    def get_rounds_won_number(self):
        return super().get_rounds_won_number(self.get_combats_played_list()).get_total()
    
    def get_rounds_lost_number(self):
        return super().get_rounds_lost_number(self.get_combats_played_list()).get_total()

    # Rounds performance
    # Win rate
    def get_rounds_p1_win_rate(self, func):
        return super().get_rounds_win_rate(func, self.get_combats_played_p1_list())
    
    def get_rounds_p2_win_rate(self, func):
        return super().get_rounds_win_rate(func, self.get_combats_played_p2_list())
    
    def get_rounds_win_rate(self, func):
        return super().get_rounds_win_rate(func, self.get_combats_played_list())

    # Win lose ratio
    def get_rounds_p1_win_lose_ratio(self, func):
        return super().get_rounds_win_lose_ratio(func, self.get_combats_played_p1_list())

    def get_rounds_p2_win_lose_ratio(self, func):
        return super().get_rounds_win_lose_ratio(func, self.get_combats_played_p2_list())
    
    def get_rounds_win_lose_ratio(self, func):
        return super().get_rounds_win_lose_ratio(func, self.get_combats_played_list())


class Character(Entity):
    __tablename__ = "character"
    
    ''' Attributes '''
    id = Column(Integer, ForeignKey('entity.id'), primary_key=True, nullable=False)
    # id = Column(Integer, primary_key=True, nullable=False)
    # name = Column(String, nullable=False)
    playlist = Column(String, nullable=True)

    __mapper_args__ = {"polymorphic_identity": "character"}
    
    ''' Relationships '''
    combats_p1 = relationship("Combat", back_populates="character1", cascade="all, delete-orphan")
    combats_p2 = relationship("Combat", back_populates="character2", cascade="all, delete-orphan")
    players_characters = relationship("PlayerCharacter", back_populates="character", cascade="all, delete-orphan")

    ''' Methods '''
    # Getters
    def get_name(self):
        return super().get_name()

    def get_playlist(self):
        return self.playlist

    # Combats lists
    # P1
    def get_combats_played_p1_list(self):
        return super().get_combats_played_list(self.combats_p1)

    def get_combats_won_p1_list(self):
        return super().get_combats_won_list(self.combats_p1)

    def get_combats_lost_p1_list(self):
        return super().get_combats_lost_list(self.combats_p1)

    def get_combats_draw_p1_list(self):
        return super().get_combats_draw_list(self.combats_p1)
    
    # P2
    def get_combats_played_p2_list(self):
        return super().get_combats_played_list(self.combats_p2)

    def get_combats_won_p2_list(self):
        return super().get_combats_won_list(self.combats_p2)

    def get_combats_lost_p2_list(self):
        return super().get_combats_lost_list(self.combats_p2)

    def get_combats_draw_p2_list(self):
        return super().get_combats_draw_list(self.combats_p2)

    # BOTH
    def get_combats_played_list(self):
        return super().get_combats_played_list(self.combats_p1 + self.combats_p2)

    def get_combats_won_list(self):
        return super().get_combats_won_list(self.combats_p1 + self.combats_p2)

    def get_combats_lost_list(self):
        return super().get_combats_lost_list(self.combats_p1 + self.combats_p2)

    def get_combats_draw_list(self):
        return super().get_combats_draw_list(self.combats_p1 + self.combats_p2)

    # Combats numbers
    # P1
    def get_combats_played_p1_number(self):
        return super().get_combats_played_number(self.combats_p1)

    def get_combats_won_p1_number(self):
        return super().get_combats_won_number(self.combats_p1)

    def get_combats_lost_p1_number(self):
        return super().get_combats_lost_number(self.combats_p1)

    def get_combats_draw_p1_number(self):
        return super().get_combats_draw_number(self.combats_p1)
    
    # P2
    def get_combats_played_p2_number(self):
        return super().get_combats_played_number(self.combats_p2)

    def get_combats_won_p2_number(self):
        return super().get_combats_won_number(self.combats_p2)

    def get_combats_lost_p2_number(self):
        return super().get_combats_lost_number(self.combats_p2)

    def get_combats_draw_p2_number(self):
        return super().get_combats_draw_number(self.combats_p2)

    # BOTH
    def get_combats_played_number(self):
        return super().get_combats_played_number(self.combats_p1 + self.combats_p2)

    def get_combats_won_number(self):
        return super().get_combats_won_number(self.combats_p1 + self.combats_p2)

    def get_combats_lost_number(self):
        return super().get_combats_lost_number(self.combats_p1 + self.combats_p2)

    def get_combats_draw_number(self):
        return super().get_combats_draw_number(self.combats_p1 + self.combats_p2)
    
    # Combats performance
    # Win rate
    def get_combats_p1_win_rate(self, func):
        return super().get_combats_win_rate(func, self.combats_p1)

    def get_combats_p2_win_rate(self, func):
        return super().get_combats_win_rate(func, self.combats_p2)

    def get_combats_win_rate(self, func):
        return super().get_combats_win_rate(func, self.combats_p1 + self.combats_p2)

    # Win lose ratio
    def get_combats_p1_win_lose_ratio(self, func):
        return super().get_combats_win_lose_ratio(func, self.combats_p1)

    def get_combats_p2_win_lose_ratio(self, func):
        return super().get_combats_win_lose_ratio(func, self.combats_p2)

    def get_combats_win_lose_ratio(self, func):
        return super().get_combats_win_lose_ratio(func, self.combats_p1 + self.combats_p2)

    # Combats stage lists
    # P1
    def get_combats_stage_played_p1_dict_list(self):
        return super().get_combats_stage_played_dict_list(self.get_combats_played_p1_list())

    def get_combats_stage_won_p1_dict_list(self):
        return super().get_combats_stage_won_dict_list(self.get_combats_played_p1_list())

    def get_combats_stage_lost_p1_dict_list(self):
        return super().get_combats_stage_lost_dict_list(self.get_combats_played_p1_list())

    def get_combats_stage_draw_p1_dict_list(self):
        return super().get_combats_stage_draw_dict_list(self.get_combats_played_p1_list())

    # P2
    def get_combats_stage_played_p2_dict_list(self):
        return super().get_combats_stage_played_dict_list(self.get_combats_played_p2_list())

    def get_combats_stage_won_p2_dict_list(self):
        return super().get_combats_stage_won_dict_list(self.get_combats_played_p2_list())

    def get_combats_stage_lost_p2_dict_list(self):
        return super().get_combats_stage_lost_dict_list(self.get_combats_played_p2_list())

    def get_combats_stage_draw_p2_dict_list(self):
        return super().get_combats_stage_draw_dict_list(self.get_combats_played_p2_list())

    # BOTH
    def get_combats_stage_played_dict_list(self):
        return super().get_combats_stage_played_dict_list(self.get_combats_played_list())

    def get_combats_stage_won_dict_list(self):
        return super().get_combats_stage_won_dict_list(self.get_combats_played_list())

    def get_combats_stage_lost_dict_list(self):
        return super().get_combats_stage_lost_dict_list(self.get_combats_played_list())

    def get_combats_stage_draw_dict_list(self):
        return super().get_combats_stage_draw_dict_list(self.get_combats_played_list())

    # Combats stage numbers
    # P1
    def get_combats_stage_played_p1_dict_number(self):
        return super().get_combats_stage_played_dict_number(self.get_combats_played_p1_list())
    
    def get_combats_stage_won_p1_dict_number(self):
        return super().get_combats_stage_won_dict_number(self.get_combats_played_p1_list())
    
    def get_combats_stage_lost_p1_dict_number(self):
        return super().get_combats_stage_lost_dict_number(self.get_combats_played_p1_list())
    
    def get_combats_stage_draw_p1_dict_number(self):
        return super().get_combats_stage_draw_dict_number(self.get_combats_played_p1_list())
    
    # P2
    def get_combats_stage_played_p2_dict_number(self):
        return super().get_combats_stage_played_dict_number(self.get_combats_played_p2_list())
    
    def get_combats_stage_won_p2_dict_number(self):
        return super().get_combats_stage_won_dict_number(self.get_combats_played_p2_list())
    
    def get_combats_stage_lost_p2_dict_number(self):
        return super().get_combats_stage_lost_dict_number(self.get_combats_played_p2_list())
    
    def get_combats_stage_draw_p2_dict_number(self):
        return super().get_combats_stage_draw_dict_number(self.get_combats_played_p2_list())
    
    # BOTH
    def get_combats_stage_played_dict_number(self):
        return super().get_combats_stage_played_dict_number(self.get_combats_played_list())
    
    def get_combats_stage_won_dict_number(self):
        return super().get_combats_stage_won_dict_number(self.get_combats_played_list())
    
    def get_combats_stage_lost_dict_number(self):
        return super().get_combats_stage_lost_dict_number(self.get_combats_played_list())
    
    def get_combats_stage_draw_dict_number(self):
        return super().get_combats_stage_draw_dict_number(self.get_combats_played_list())

    # Combats stage performance
    # Win rate
    def get_combats_stage_win_rate_p1_dict(self, func):
        return super().get_combats_stage_win_rate_dict(func, self.get_combats_played_p1_list())
    
    def get_combats_stage_win_rate_p2_dict(self, func):
        return super().get_combats_stage_win_rate_dict(func, self.get_combats_played_p2_list())
    
    def get_combats_stage_win_rate_dict(self, func):
        return super().get_combats_stage_win_rate_dict(func, self.get_combats_played_list())

    # Win lose ratio
    def get_combats_stage_win_lose_ratio_p1_dict(self, func):
        return super().get_combats_stage_win_lose_ratio_dict(func, self.get_combats_played_p1_list())
    
    def get_combats_stage_win_lose_ratio_p2_dict(self, func):
        return super().get_combats_stage_win_lose_ratio_dict(func, self.get_combats_played_p2_list())
    
    def get_combats_stage_win_lose_ratio_dict(self, func):
        return super().get_combats_stage_win_lose_ratio_dict(func, self.get_combats_played_list())

    # Events
    def get_events_played_list(self):
        return super().get_events_played_list(self.get_combats_played_list())

    def get_events_played_number(self):
        return super().get_events_played_number(self.get_combats_played_list())

     # Rounds
    # P1
    def get_rounds_played_p1_number(self):
        return super().get_rounds_played_number(self.get_combats_played_p1_list())
    
    def get_rounds_won_p1_number(self):
        return super().get_rounds_won_number(self.get_combats_played_list()).get_player1()
    
    def get_rounds_lost_p1_number(self):
        return super().get_rounds_lost_number(self.get_combats_played_list()).get_player1()

    # P2
    def get_rounds_played_p2_number(self):
        return super().get_rounds_played_number(self.get_combats_played_p2_list())
    
    def get_rounds_won_p2_number(self):
        return super().get_rounds_won_number(self.get_combats_played_list()).get_player2()
    
    def get_rounds_lost_p2_number(self):
        return super().get_rounds_lost_number(self.get_combats_played_list()).get_player2()

    # BOTH
    def get_rounds_played_number(self):
        return super().get_rounds_played_number(self.get_combats_played_list())
    
    def get_rounds_won_number(self):
        return super().get_rounds_won_number(self.get_combats_played_list()).get_total()
    
    def get_rounds_lost_number(self):
        return super().get_rounds_lost_number(self.get_combats_played_list()).get_total()

    # Rounds performance
    # Win rate
    def get_rounds_p1_win_rate(self, func):
        return super().get_rounds_win_rate(func, self.get_combats_played_p1_list())
    
    def get_rounds_p2_win_rate(self, func):
        return super().get_rounds_win_rate(func, self.get_combats_played_p2_list())
    
    def get_rounds_win_rate(self, func):
        return super().get_rounds_win_rate(func, self.get_combats_played_list())

    # Win lose ratio
    def get_rounds_p1_win_lose_ratio(self, func):
        return super().get_rounds_win_lose_ratio(func, self.get_combats_played_p1_list())

    def get_rounds_p2_win_lose_ratio(self, func):
        return super().get_rounds_win_lose_ratio(func, self.get_combats_played_p2_list())
    
    def get_rounds_win_lose_ratio(self, func):
        return super().get_rounds_win_lose_ratio(func, self.get_combats_played_list())


class PlayerCharacter(Entity):
# class PlayerCharacter(Base): # @@@@
    __tablename__ = "player_character"

    ''' Attributes '''
    id = Column(Integer, ForeignKey('entity.id'), primary_key=True, nullable=False)
    # id = Column(Integer, primary_key=True, nullable=False)

    player_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    character_id = Column(Integer, ForeignKey("character.id"), nullable=False)

    __mapper_args__ = {"polymorphic_identity": "player_character"}

    ''' Relationships '''
    player = relationship("Player", back_populates="players_characters")
    character = relationship("Character", back_populates="players_characters")

    ''' Methods '''
    # Getters
    def get_name(self):
        return self.player.get_name() + "-" + self.character.get_name()
    
    # Combats lists
    def get_combats_status_side_list(self, combats_player, combats_character):
        combats_status_list = list()
        for combat_player in combats_player:
            for combat_character in combats_character:
                if combat_player == combat_character:
                    combats_status_list.append(combat_player)
        return combats_status_list
    
    def get_combats_status_list(self, challenge_status):
        combats_status_list = list()
        if challenge_status == ChallengeStatus.PLAYED.name:
            combats_status_list = self.get_combats_played_p1_list() + self.get_combats_played_p2_list()
        if challenge_status == ChallengeStatus.WON.name:
            combats_status_list = self.get_combats_won_p1_list() + self.get_combats_won_p2_list()
        if challenge_status == ChallengeStatus.LOST.name:
            combats_status_list = self.get_combats_lost_p1_list() + self.get_combats_lost_p2_list()
        if challenge_status == ChallengeStatus.DRAW.name:
            combats_status_list = self.get_combats_draw_p1_list() + self.get_combats_draw_p2_list()
        combats_status_list = list(sorted(combats_status_list, key=lambda x:x.get_combat_order()))
        return combats_status_list

    # P1
    def get_combats_played_p1_list(self):
        return self.get_combats_status_side_list(self.player.get_combats_played_p1_list(), self.character.get_combats_played_p1_list())
    
    def get_combats_won_p1_list(self):
        return self.get_combats_status_side_list(self.player.get_combats_won_p1_list(), self.character.get_combats_won_p1_list())
    
    def get_combats_lost_p1_list(self):
        return self.get_combats_status_side_list(self.player.get_combats_lost_p1_list(), self.character.get_combats_lost_p1_list())
    
    def get_combats_draw_p1_list(self):
        return self.get_combats_status_side_list(self.player.get_combats_draw_p1_list(), self.character.get_combats_draw_p1_list())
    
    # P2
    def get_combats_played_p2_list(self):
        return self.get_combats_status_side_list(self.player.get_combats_played_p2_list(), self.character.get_combats_played_p2_list())
    
    def get_combats_won_p2_list(self):
        return self.get_combats_status_side_list(self.player.get_combats_won_p2_list(), self.character.get_combats_won_p2_list())
    
    def get_combats_lost_p2_list(self):
        return self.get_combats_status_side_list(self.player.get_combats_lost_p2_list(), self.character.get_combats_lost_p2_list())
    
    def get_combats_draw_p2_list(self):
        return self.get_combats_status_side_list(self.player.get_combats_draw_p2_list(), self.character.get_combats_draw_p2_list())
    
    # BOTH
    def get_combats_played_list(self):
        return self.get_combats_status_list(ChallengeStatus.PLAYED.name)
    
    def get_combats_won_list(self):
        return self.get_combats_status_list(ChallengeStatus.WON.name)
    
    def get_combats_lost_list(self):
        return self.get_combats_status_list(ChallengeStatus.LOST.name)
    
    def get_combats_draw_list(self):
        return self.get_combats_status_list(ChallengeStatus.DRAW.name)
    
    # Combats numbers
    # P1
    def get_combats_played_p1_number(self):
        return len(self.get_combats_played_p1_list())
    
    def get_combats_won_p1_number(self):
        return len(self.get_combats_won_p1_list())
    
    def get_combats_lost_p1_number(self):
        return len(self.get_combats_lost_p1_list())

    def get_combats_draw_p1_number(self):
        return len(self.get_combats_draw_p1_list())
    
    # P2
    def get_combats_played_p2_number(self):
        return len(self.get_combats_played_p2_list())
    
    def get_combats_won_p2_number(self):
        return len(self.get_combats_won_p2_list())
    
    def get_combats_lost_p2_number(self):
        return len(self.get_combats_lost_p2_list())

    def get_combats_draw_p2_number(self):
        return len(self.get_combats_draw_p2_list())

    # BOTH
    def get_combats_played_number(self):
        return len(self.get_combats_played_list())
    
    def get_combats_won_number(self):
        return len(self.get_combats_won_list())
    
    def get_combats_lost_number(self):
        return len(self.get_combats_lost_list())

    def get_combats_draw_number(self):
        return len(self.get_combats_draw_list())

    # Combats performance
    # Win rate


    # Win lose ratio


    # Events
    def get_events_played_list(self):
        events_set = set()
        for combat_player in self.player.get_combats_played_list():
            for combat_character in self.character.get_combats_played_list():
                if combat_player == combat_character:
                    events_set.add(combat_player.get_event())
        events_list = list(events_set).sort()
        return events_list

    def get_events_played_number(self):
        return len(self.get_events_played_list())

    # Duels
    def get_duels_played_list(self):
        ''' List of duels in which PL-CH was present '''
        duels_set = set()
        for duel_player in self.player.get_duels_played_list():
            for duel_character in self.character.get_duels_played_list():
                if duel_player == duel_character:
                    duels_set.add(duel_player)
        duels_list = list(duels_set).sort()
        return duels_list
    
    def get_duels_played_number(self):
        ''' Number of duels in which PL-CH was present '''
        return len(self.get_duels_played_list())
    
    # Team duels
    def get_team_duels_played_list(self):
        ''' List of team duels in which PL-CH was present '''
        duels_set = set()
        for duel_player in self.player.get_team_duels_played_list():
            for duel_character in self.character.get_team_duels_played_list():
                if duel_player == duel_character:
                    duels_set.add(duel_player)
        duels_list = list(duels_set).sort()
        return duels_list
    
    def get_team_duels_played_number(self):
        ''' Number of team duels in which PL-CH was present '''
        return len(self.get_team_duels_played_list())
    
    # Win lose ratio
    def get_win_lose_ratio(self, func, challenge_type):
        win_lose_ratio = 0
        victories = 0
        defeats = 0
        if challenge_type == ChallengeType.COMBAT.name:
            victories = self.get_combats_won_number()
            defeats = self.get_combats_lost_number()
        if challenge_type == ChallengeType.ROUND.name:
            victories = self.get_rounds_won_number()
            defeats = self.get_rounds_lost_number()
        if defeats == 0:
            win_lose_ratio = victories
        elif victories == 0:
            win_lose_ratio = 0.5 / defeats
        elif defeats == 1:
            win_lose_ratio = victories * (3 / 4)
        else:
            win_lose_ratio = victories / defeats
        return func(win_lose_ratio)

    # Combats
    def get_combats_played_list(self):
        combats_set = set()
        for combat_player in self.player.get_combats_played_list():
            for combat_character in self.character.get_combats_played_list():
                if combat_player == combat_character:
                    combats_set.add(combat_player)
        combats_list = list(combats_set).sort()
        return combats_list
    
    def get_combats_played_number(self):
        return len(self.get_combats_played_list())
    
    def get_combats_won_list(self):
        combats_won_set = set()
        for combat in self.get_combats_played_list():
            if self.player == combat.get_winner_player() and self.character == combat.get_winner_character():
                combats_won_set.add(combat)
        combats_won_list = list(combats_won_set).sort()
        return combats_won_list
    
    def get_combats_won_number(self):
        return len(self.get_combats_won_list())
    
    def get_combats_lost_list(self):
        combats_lost_set = set()
        for combat in self.get_combats_played_list():
            if self.player == combat.get_loser_player() and self.character == combat.get_loser_character():
                combats_lost_set.add(combat)
        combats_lost_list = list(combats_lost_set).sort()
        return combats_lost_list
    
    def get_combats_lost_number(self):
        return len(self.get_combats_lost_list())
    
    def get_combats_draw_list(self):
        combats_list = list()
        for combat in self.get_combats_played_list():
            if combat.is_draw():
                combats_list.append(combat)
        return combats_list
    
    def get_combats_draw_number(self):
        return len(self.get_combats_draw_list())
    
    def get_combats_win_rate(self):
        return (self.get_combats_won_number() + (self.get_combats_draw_number() / 2)) / self.get_combats_played_number()

    def get_combats_win_lose_ratio(self, func):
        return self.get_win_lose_ratio(func, ChallengeType.COMBAT.name)
    
    # Rounds
    def get_rounds_played_number(self):
        rounds_played_number = 0
        for combat in self.get_combats_played_list():
            # if self.player in combat.get_players_list() and self.character in combat.get_characters_list():
            rounds_played_number += combat.get_rounds_played_number()
        return rounds_played_number
    
    def get_rounds_won_number(self):
        rounds_won_number = 0
        for combat in self.get_combats_played_list():
            if self.player == combat.get_player1() and self.character == combat.get_character1():
                rounds_won_number += combat.get_rounds_won_p1_number()
            if self.player == combat.get_player2() and self.character == combat.get_character2():
                rounds_won_number += combat.get_rounds_won_p2_number()
        return rounds_won_number

    def get_rounds_lost_number(self):
        rounds_lost_number = 0
        for combat in self.get_combats_played_list():
            if self.player == combat.get_player1() and self.character == combat.get_character1():
                rounds_lost_number += combat.get_rounds_lost_p1_number()
            if self.player == combat.get_player2() and self.character == combat.get_character2():
                rounds_lost_number += combat.get_rounds_lost_p2_number()
        return rounds_lost_number

    def get_rounds_win_rate(self):
        return self.get_rounds_won_number() / self.get_rounds_played_number()

    def get_rounds_win_lose_ratio(self, func):
        return self.get_win_lose_ratio(func, ChallengeType.ROUND.name)


class Combat(Base):
    __tablename__ = "combat"

    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    combat_order = Column(Integer, nullable=False)

    duel_id = Column(Integer, ForeignKey("duel.id"), nullable=False)
    stage_id = Column(Integer, ForeignKey("stage.id"), nullable=False)
    player1_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    player2_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    character1_id = Column(Integer, ForeignKey("character.id"), nullable=False)
    character2_id = Column(Integer, ForeignKey("character.id"), nullable=False)
    team1_id = Column(Integer, ForeignKey("team.id"), nullable=True)
    team2_id = Column(Integer, ForeignKey("team.id"), nullable=True)

    ''' Relationships '''
    duel = relationship("Duel", back_populates="combats")
    stage = relationship("Stage", back_populates="combats")
    player1 = relationship("Player", back_populates="combats_p1")
    player2 = relationship("Player", back_populates="combats_p2")
    character1 = relationship("Character", back_populates="combats_p1")
    character2 = relationship("Character", back_populates="combats_p2")
    team1 = relationship("Team", back_populates="combats_p1")
    team2 = relationship("Team", back_populates="combats_p2")
    rounds = relationship("Round", back_populates="combat", cascade="all, delete-orphan")

    ''' Methods '''
    # Getters
    def get_stage(self):
        return self.stage

    def get_duel(self):
        return self.duel

    # Events
    def get_event(self):
        return self.duel.get_event()

    # Players
    def get_player1(self):
        return self.player1

    def get_player2(self):
        return self.player2

    def get_players_list(self):
        players_list = [self.get_player1(), self.get_player2()]
        players_list.sort()
        return players_list

    # Characters
    def get_character1(self):
        return self.character1

    def get_character2(self):
        return self.character2    

    def get_characters_list(self):
        characters_list = [self.get_character1(), self.get_character2()]
        characters_list.sort()
        return characters_list

    # Teams
    def get_team1(self):
        return self.team1

    def get_team2(self):
        return self.team1

    def get_teams_list(self):
        teams_list = [self.get_team1(), self.get_team2()]
        teams_list.sort()
        return teams_list

    # Rounds
    def get_rounds_played_number(self):
        return len(self.rounds)

    def get_rounds_won_number(self):
        round_result_player1 = 0
        round_result_player2 = 0
        self.rounds.sort(key=lambda x: x.round_order)
        for round in self.rounds:
            round_result_obj = round.get_round_result()
            round_result_player1 += round_result_obj.player1
            round_result_player2 += round_result_obj.player2
        return Scoreboard(round_result_player1, round_result_player2)

    def get_rounds_won_p1_number(self):
        return self.get_rounds_won_number().player1

    def get_rounds_won_p2_number(self):
        return self.get_rounds_won_number().player2

    def get_rounds_lost_number(self):
        rounds_played_number = self.get_rounds_played_number()
        rounds_won_number_obj = self.get_rounds_won_number()
        rounds_lost_number_player1 = rounds_played_number - rounds_won_number_obj.player1
        rounds_lost_number_player2 = rounds_played_number - rounds_won_number_obj.player2
        return Scoreboard(rounds_lost_number_player1, rounds_lost_number_player2)

    def get_rounds_lost_p1_number(self):
        return self.get_rounds_lost_number().player1

    def get_rounds_lost_p2_number(self):
        return self.get_rounds_lost_number().player2

    # Combat
    def get_status_entity(self, competitor_status, entity_type):
        status_entity = None
        scoreboard_obj = self.get_rounds_beating_factor()
        entity1 = None
        entity2 = None
        scoreboard_entity1 = scoreboard_obj.player1
        scoreboard_entity2 = scoreboard_obj.player2
        if entity_type == EntityType.PLAYER.name:
            entity1 = self.player1
            entity2 = self.player2
        if entity_type == EntityType.CHARACTER.name:
            entity1 = self.character1
            entity2 = self.character2
        if entity_type == EntityType.TEAM.name:
            entity1 = self.team1
            entity2 = self.team2
        if competitor_status == CompetitorStatus.WINNER.name:
            if scoreboard_entity1 > scoreboard_entity2:
                status_entity = entity1
            elif scoreboard_entity1 < scoreboard_entity2:
                status_entity = entity2
        if competitor_status == CompetitorStatus.LOSER.name:
            if scoreboard_entity1 > scoreboard_entity2:
                status_entity = entity2
            elif scoreboard_entity1 < scoreboard_entity2:
                status_entity = entity1
        return status_entity
    
    def get_winner_player(self):
        return self.get_status_entity(CompetitorStatus.WINNER.name, EntityType.PLAYER.name)

    def get_winner_character(self):
        return self.get_status_entity(CompetitorStatus.WINNER.name, EntityType.CHARACTER.name)

    def get_winner_team(self):
        return self.get_status_entity(CompetitorStatus.WINNER.name, EntityType.TEAM.name)

    def get_loser_player(self):
        return self.get_status_entity(CompetitorStatus.LOSER.name, EntityType.PLAYER.name)

    def get_loser_character(self):
        return self.get_status_entity(CompetitorStatus.LOSER.name, EntityType.CHARACTER.name)

    def get_loser_team(self):
        return self.get_status_entity(CompetitorStatus.LOSER.name, EntityType.TEAM.name)

    def is_draw(self):
        draw = False
        scoreboard_obj = self.get_rounds_beating_factor()
        if scoreboard_obj.player1 == scoreboard_obj.player2:
            draw = True
        return draw

    # Ranking
    def get_rounds_beating_factor(self):
        rounds_beating_factor_player1 = 0
        rounds_beating_factor_player2 = 0
        rounds_played_number = self.get_rounds_played_number()
        rounds_won_number_obj = self.get_rounds_won_number()
        if rounds_won_number_obj.player1 == 0: # Player 1
            rounds_beating_factor_player1 = (1 / rounds_played_number) / 2
        else:
            rounds_beating_factor_player1 = rounds_won_number_obj.player1 / rounds_played_number
        if rounds_won_number_obj.player2 == 0: # Player 2
            rounds_beating_factor_player2 = (1 / rounds_played_number) / 2
        else:
            rounds_beating_factor_player2 = rounds_won_number_obj.player2 / rounds_played_number
        return Scoreboard(rounds_beating_factor_player1, rounds_beating_factor_player2)
    
    def get_rounds_level_factor(self):
        player1_win_rate = self.player1.get_rounds_win_rate()
        player2_win_rate = self.player2.get_rounds_win_rate()
        player1_rounds_lvl_factor = LvlFactor.A.value * (player1_win_rate - player2_win_rate) + LvlFactor.B.value
        player2_rounds_lvl_factor = LvlFactor.A.value * (player2_win_rate - player1_win_rate) + LvlFactor.B.value
        return Scoreboard(player1_rounds_lvl_factor, player2_rounds_lvl_factor)

    def get_combat_points_raw(self):
        points_p1 = 0
        points_p2 = 0
        self.rounds.sort(key=lambda x: x.round_order)
        for round in self.rounds:
            points_p1 += round.get_points_player1()
            points_p2 += round.get_points_player2()
        return Scoreboard(points_p1, points_p2)

    def get_combat_points_earned_dict(self, entity_type):
        combat_points_earned_dict = dict()
        combat_raw_points_obj = self.get_combat_points_raw() # Raw points
        rounds_beating_factor_obj = self.get_rounds_beating_factor() # Beating factors
        rounds_lvl_factor_obj = self.get_rounds_level_factor() # Level factors
        combat_earned_points_player1 = combat_raw_points_obj.player1 * rounds_beating_factor_obj.player1 * rounds_lvl_factor_obj.player1
        combat_earned_points_player2 = combat_raw_points_obj.player2 * rounds_beating_factor_obj.player2 * rounds_lvl_factor_obj.player2
        if entity_type == EntityType.PLAYER.name:
            combat_points_earned_dict[self.player1] = combat_earned_points_player1
            combat_points_earned_dict[self.player2] = combat_earned_points_player2
        if entity_type == EntityType.CHARACTER.name:
            combat_points_earned_dict[self.character1] = combat_earned_points_player1
            combat_points_earned_dict[self.character2] = combat_earned_points_player2
        if entity_type == EntityType.TEAM.name:
            combat_points_earned_dict[self.team1] = combat_earned_points_player1
            combat_points_earned_dict[self.team2] = combat_earned_points_player2
        return combat_points_earned_dict
    
    def get_combat_points_earned_player_dict(self):
        return self.get_combat_points_earned_dict(EntityType.PLAYER.name)
    
    def get_combat_points_earned_character_dict(self):
        return self.get_combat_points_earned_dict(EntityType.CHARACTER.name)
    
    def get_combat_points_earned_team_dict(self):
        return self.get_combat_points_earned_dict(EntityType.TEAM.name)


class Round(Base):
    __tablename__ = "round"

    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    round_order = Column(Integer, nullable=False)
    result_player1 = Column(String, nullable=False)
    result_player2 = Column(String, nullable=False)

    combat_id = Column(Integer, ForeignKey("combat.id"), nullable=False)

    ''' Relationships '''
    combat = relationship("Combat", back_populates="rounds")

    ''' Methods '''
    def get_points_player1(self):
        return ROUNDS_POINTS[self.result_player1]

    def get_points_player2(self):
        return ROUNDS_POINTS[self.result_player2]

    def get_round_result(self):
        result_player1 = 0
        result_player2 = 0
        if self.result_player1 in ROUND_WIN_CONDITIONS:
            result_player1 = 1
        if self.result_player2 in ROUND_WIN_CONDITIONS:
            result_player2 = 1
        return Scoreboard(result_player1, result_player2)


''' Schema generation '''

Base.metadata.create_all(ENGINE)