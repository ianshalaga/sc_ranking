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

from sqlalchemy.ext.hybrid import hybrid_property

from enum import Enum
import numpy as np
import utils as ut
from collections import defaultdict


''' Engine '''

DB_ENGINE = "sqlite"
DB_API = "pysqlite"
DB_PATH = "backend/SSLEdb.db"
ENGINE = create_engine(f"{DB_ENGINE}+{DB_API}:///{DB_PATH}", echo=True, future=True)

''' DATA '''

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

''' @UTILITIES CLASS '''

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


class EventsStats:
    def __init__(self,
                 played_list,
                 played_number,
                 results_dict):
        self.played_list = played_list
        self.played_number = played_number
        self.results_dict = results_dict

    ''' Methods '''
    # Getters
    def get_played_list(self):
        return self.played_list
    
    def get_played_number(self):
        return self.played_number
    
    def get_results_dict(self):
        return self.results_dict
    
    # Setters
    def set_played_list(self, played_list):
        self.played_list = played_list
    
    def set_played_number(self, played_number):
        self.played_number = played_number
    
    def set_results_dict(self, results_dict):
        self.results_dict = results_dict


class DuelsStats:
    def __init__(self,
                 played_list,
                 won_list,
                 lost_list,
                 played_number,
                 won_number,
                 lost_number,
                 win_rate,
                 win_lose_ratio):
        self.played_list = played_list
        self.won_list = won_list
        self.lost_list = lost_list
        self.played_number = played_number
        self.won_number = won_number
        self.lost_number = lost_number
        self.win_rate = win_rate
        self.win_lose_ratio = win_lose_ratio
    
    ''' Methods '''
    def get_played_list(self):
        return self.played_list


class CombatsStats:
    def __init__(self,
                 played_list,
                 won_list,
                 lost_list,
                 draw_list,
                 played_number,
                 won_number,
                 lost_number,
                 draw_number,
                 win_rate,
                 win_lose_ratio):
        self.played_list = played_list
        self.won_list = won_list
        self.lost_list = lost_list
        self.draw_list = draw_list
        self.played_number = played_number
        self.won_number = won_number
        self.lost_number = lost_number
        self.draw_number = draw_number
        self.win_rate = win_rate
        self.win_lose_ratio = win_lose_ratio
    
    ''' Methods '''
    def get_played_list(self):
        return self.played_list

    def get_won_list(self):
        return self.won_list

    def get_lost_list(self):
        return self.lost_list

    def get_draw_list(self):
        return self.draw_list

    def get_played_number(self):
        return self.played_number

    def get_won_number(self):
        return self.won_number

    def get_lost_number(self):
        return self.lost_number

    def get_draw_number(self):
        return self.draw_number

    def get_win_rate(self):
        return self.win_rate

    def get_win_lose_ratio(self):
        return self.win_lose_ratio


class RoundsStats:
    def __init__(self,
                 played,
                 won,
                 lost,
                 played_p1,
                 won_p1,
                 lost_p1,
                 played_p2,
                 won_p2,
                 lost_p2,
                 win_rate,
                 win_lose_ratio,
                 win_rate_p1,
                 win_lose_ratio_p1,
                 win_rate_p2,
                 win_lose_ratio_p2):
        self.played = played
        self.won = won
        self.lost = lost
        self.played_p1 = played_p1
        self.won_p1 = won_p1
        self.lost_p1 = lost_p1
        self.played_p2 = played_p2
        self.won_p2 = won_p2
        self.lost_p2 = lost_p2
        self.win_rate = win_rate
        self.win_lose_ratio = win_lose_ratio
        self.win_rate_p1 = win_rate_p1
        self.win_lose_ratio_p1 = win_lose_ratio_p1
        self.win_rate_p2 = win_rate_p2
        self.win_lose_ratio_p2 = win_lose_ratio_p2

    ''' Methods '''
    # Getters
    def get_played(self):
        return self.played
    def get_won(self):
        return self.won
    def get_lost(self):
        return self.lost
    def get_played_p1(self):
        return self.played_p1
    def get_won_p1(self):
        return self.won_p1
    def get_lost_p1(self):
        return self.lost_p1
    def get_played_p2(self):
        return self.played_p2
    def get_won_p2(self):
        return self.won_p2
    def get_lost_p2(self):
        return self.lost_p2
    def get_win_rate(self):
        return self.win_rate
    def get_win_lose_ratio(self):
        return self.win_lose_ratio
    def get_win_rate_p1(self):
        return self.win_rate_p1
    def get_win_lose_ratio_p1(self):
        return self.win_lose_ratio_p1
    def get_win_rate_p2(self):
        return self.win_rate_p2
    def get_win_lose_ratio_p2(self):
        return self.win_lose_ratio_p2


# class RoundStats:
#     def __init__(self,
#                  played,
#                  won,
#                  lost,
#                  win_rate,
#                  win_lose_ratio):
#         self.played = played
#         self.won = won
#         self.lost = lost
#         self.win_rate = win_rate
#         self.win_lose_rati = win_lose_ratio
    

''' @ENUMS '''

class Modality(Enum):
    EVENT_SYSTEM = 1
    COMPETITORS_TYPE = 2

class EventSystem(Enum):
    TOURNAMENT = 1
    LEAGUE = 2
    DUEL = 3

class EntityType(Enum):
    PLAYER = 1
    CHARACTER = 2
    PLAYER_CHARACTER = 3
    TEAM = 4

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

class CombatSide(Enum):
    SIDE1 = 1
    SIDE2 = 2

class LvlFactor(Enum):
    A = -0.04
    B = 1

class PerformanceMetric(Enum):
    WIN_RATE = 1
    WIN_LOSE_RATIO = 2

FUNC = np.arctan


''' ClassTables '''

Base = declarative_base()


''' Event group '''

class Game(Base):
    __tablename__ = "game"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    _name = Column(String, nullable=False)
    _code_name = Column(String, nullable=False)

    ''' Relationships '''
    game_version_platforms = relationship("GameVersionPlatform", back_populates="game", cascade="all, delete-orphan")

    ''' Methods '''
    # Getters
    @hybrid_property
    def name(self):
        return self._name
    
    @hybrid_property
    def code_name(self):
        return self._code_name


class Platform(Base):
    __tablename__ = "platform"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    _name = Column(String, nullable=False)
    _code_name = Column(String, nullable=False)

    ''' Relationships '''
    game_version_platforms = relationship("GameVersionPlatform", back_populates="platform", cascade="all, delete-orphan")

    ''' Methods '''
    # Getters
    @hybrid_property
    def name(self):
        return self._name
    
    @hybrid_property
    def code_name(self):
        return self._code_name


class GameVersionPlatform(Base):
    __tablename__ = "game_version_platform"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    _version = Column(String, nullable=False)

    platform_id = Column(Integer, ForeignKey("platform.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("game.id"), nullable=False)

    ''' Relationships '''
    game = relationship("Game", back_populates="game_version_platforms")
    platform = relationship("Platform", back_populates="game_version_platforms")
    events = relationship("Event", back_populates="game_version_platform", cascade="all, delete-orphan")

    ''' Methods '''
    # Getters
    @hybrid_property
    def version(self):
        return self._version
    
    # Game
    def get_game_name(self):
        self.game.name

    def get_game_code_name(self):
        self.game.code_name

    # Platform
    def get_platform_name(self):
        self.platform.name

    def get_platform_code_name(self):
        self.platform.code_name


class Region(Base):
    __tablename__ = "region"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    _name = Column(String, nullable=False)
    _code_name = Column(String, nullable=False)

    ''' Relationships '''
    events = relationship("Event", back_populates="region", cascade="all, delete-orphan")

    ''' Methods '''
    # Getters
    @hybrid_property
    def name(self):
        return self._name
    
    @hybrid_property
    def code_name(self):
        return self._code_name
    

class LifeTime(Base):
    __tablename__ = "lifetime"

    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)

    ''' Relationships '''
    seasons = relationship("Season", back_populates="lifetime", cascade="all, delete-orphan")

    ''' Methods '''
    # Seasons
    def get_seasons_list(self):
        return list(sorted(self.seasons, key=lambda x:x.season_order))
    
    def get_seasons_number(self):
        return len(self.get_seasons_list())

    # Ranking
    def get_points_earned(self):
        points_earned_dict = defaultdict(int)
        for season in self.get_seasons_list():
            for competitor, points in season.get_points_earned().items():
                points_earned_dict[competitor] += points
        return dict(points_earned_dict)
    
    # def get_ranking(self, duels_list):
    #     ranking = dict()
    #     for competitor, points in self.get_points_earned().items():
    #         ranking[competitor] = points * competitor.get_win_lose_ratio(self)
    #     return dict(sorted(ranking.items(), key=lambda x:x[1]), reverse=True)


class Season(Base):
    __tablename__ = "season"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    _name = Column(String, nullable=False)
    _code_name = Column(String, nullable=False)
    _season_order = Column(Integer, nullable=False)

    lifetime_id = Column(Integer, ForeignKey("lifetime.id"), nullable=False)

    ''' Relationships '''
    lifetime = relationship("LifeTime", back_populates="seasons")
    events = relationship("Event", back_populates="season", cascade="all, delete-orphan")

    ''' Methods '''
    # Getters
    @hybrid_property
    def name(self):
        return self._name
    
    @hybrid_property
    def code_name(self):
        return self._code_name
    
    @hybrid_property
    def season_order(self):
        return self._season_order

    # Stats
    def get_season_stats(self):     
        return ut.SeasonStats(self.get_events_list(),
                              self.get_events_number(),
                              self.get_events_player_list(),
                              self.get_events_player_number(),
                              self.get_events_player_rate(),
                              self.get_events_team_list(),
                              self.get_events_team_number(),
                              self.get_events_team_rate(),
                              self.get_events_tournament_list(),
                              self.get_events_tournament_number(),
                              self.get_events_tournament_rate(),
                              self.get_events_league_list(),
                              self.get_events_league_number(),
                              self.get_events_league_rate(),
                              self.get_duels_list(),
                              self.get_duels_number(),
                              self.get_duels_statistics(),
                              self.get_combats_list(),
                              self.get_combats_number(),
                              self.get_combats_statistics(),
                              self.get_rounds_list(),
                              self.get_rounds_number(),
                              self.get_rounds_statistics(),
                              self.get_players_list(),
                              self.get_players_number(),
                              self.get_players_statistics(),
                              self.get_players_most_participations(),
                              self.get_teams_list(),
                              self.get_teams_number(),
                              self.get_teams_statistics(),
                              self.get_teams_most_participations(),
                              self.get_characters_list(),
                              self.get_characters_number(),
                              self.get_characters_statistics(),
                              self.get_characters_most_participations(),
                              self.get_player_characters_list(),
                              self.get_player_characters_number(),
                              self.get_player_characters_statistics(),
                              self.get_player_characters_most_participations(),
                              self.get_winners_player_list(),
                              self.get_winners_player_number(),
                              self.get_winners_team_list(),
                              self.get_winners_team_number())

    # Events
    def get_events_list(self):
        ''' List of total events of a season. '''
        return list(sorted(self.events, key=lambda x:x.event_order))
         
    def get_events_number(self):
        ''' Number of total events of a season. '''
        return len(self.get_events_list())

    # Events modalities
    def _get_events_modality_list(self, event_modality, modality):
        modality_list = list()
        for event in self.get_events_list():
            if event_modality == Modality.EVENT_SYSTEM.name:
                if modality == EventSystem.TOURNAMENT.name:
                    modality_list.append(event)
                elif modality == EventSystem.LEAGUE.name:
                    modality_list.append(event)
                else:
                    raise ValueError(f"Invalid modality: {modality}")
            elif event_modality == Modality.COMPETITORS_TYPE.name:
                if modality == CompetitorType.PLAYER.name:
                    modality_list.append(event)
                elif modality == CompetitorType.TEAM.name:
                    modality_list.append(event)
                else:
                    raise ValueError(f"Invalid modality: {modality}")
            else:
                raise ValueError(f"Invalid event_modality: {event_modality}")
        return modality_list
            
    # Modality: PLAYER
    def get_events_player_list(self):
        return self._get_events_modality_list(Modality.COMPETITORS_TYPE.name, CompetitorType.PLAYER.name)

    def get_events_player_number(self):
        return len(self.get_events_player_list())

    def get_events_player_rate(self):
        return self.get_events_player_number() / self.get_events_number()

    # Modality: TEAM
    def get_events_team_list(self):
        return self._get_events_modality_list(Modality.COMPETITORS_TYPE.name, CompetitorType.TEAM.name)

    def get_events_team_number(self):
        return len(self.get_events_team_list())

    def get_events_team_rate(self):
        return self.get_events_team_number() / self.get_events_number()
    
    # Modality: TOURNAMENT
    def get_events_tournament_list(self):
        return self._get_events_modality_list(Modality.EVENT_SYSTEM.name, EventSystem.TOURNAMENT.name)

    def get_events_tournament_number(self):
        return len(self.get_events_tournament_list())

    def get_events_tournament_rate(self):
        return self.get_events_tournament_number() / self.get_events_number()

    # Modality: LEAGUE
    def get_events_league_list(self):
        return self._get_events_modality_list(Modality.EVENT_SYSTEM.name, EventSystem.LEAGUE.name)

    def get_events_league_number(self):
        return len(self.get_events_league_list())

    def get_events_league_rate(self):
        return self.get_events_league_number() / self.get_events_number()

    # Lists getters
    def _get_criterion_list(self, criterion):
        ''' List of criterion for event. '''
        criterion_list = list()
        for event in self.get_events_list():
            criterion_list += getattr(event, f"get_{criterion.lower()}s_list")
        return criterion_list
    
    def _get_criterion_number_by_event_list(self, criterion):
        '''
        For statistics.
        List of numbers of criterion by event of a season.
        '''
        criterion_number_by_event_list = list()
        for event in self.get_events_list():
            criterion_number_by_event_list.append(getattr(event, f"get_{criterion.lower()}s_number"))
        return criterion_number_by_event_list

    # Challenge: DUEL
    def get_duels_list(self):
        return self._get_criterion_list(ChallengeType.DUEL.name)
    
    def get_duels_number(self):
        return len(self.get_duels_list())

    def get_duels_number_by_event_list(self):
        return self._get_criterion_number_by_event_list(ChallengeType.DUEL.name)

    def get_duels_statistics(self):
        return ut.get_statistics(self.get_duels_number_by_event_list())

    # Challenge: COMBAT
    def get_combats_list(self):
        return self._get_criterion_list(ChallengeType.COMBAT.name)
    
    def get_combats_number(self):
        return len(self.get_combats_list())
    
    def get_combats_number_by_event_list(self):
        return self._get_criterion_number_by_event_list(ChallengeType.COMBAT.name)

    def get_combats_statistics(self):
        return ut.get_statistics(self.get_combats_number_by_event_list())
    
    # Challenge: ROUND
    def get_rounds_list(self):
        return self._get_criterion_list(ChallengeType.ROUND.name)
    
    def get_rounds_number(self):
        return len(self.get_rounds_list())
    
    def get_rounds_number_by_event_list(self):
        return self._get_criterion_number_by_event_list(ChallengeType.ROUND.name)

    def get_rounds_statistics(self):
        return ut.get_statistics(self.get_rounds_number_by_event_list())

    # Entities
    def _get_entity_most_participations(self, entity_type):
        ''' For statistics. '''
        entities_list = getattr(self, f"get_{entity_type}s_list")
        return ut.get_multimode(entities_list)

    # Entity: PLAYER
    def get_players_list(self):
        return self._get_criterion_list(EntityType.PLAYER.name)
    
    def get_players_number(self):
        return len(self.get_players_list())
    
    def get_players_number_by_event_list(self):
        return self._get_criterion_number_by_event_list(EntityType.PLAYER.name)
    
    def get_players_statistics(self):
        return ut.get_statistics(self.get_players_number_by_event_list())
    
    def get_players_most_participations(self):
        return self._get_entity_most_participations(EntityType.PLAYER.name)

    # Entity: TEAM
    def get_teams_list(self):
        return self._get_criterion_list(EntityType.TEAM.name)
    
    def get_teams_number(self):
        return len(self.get_teams_list())

    def get_teams_number_by_event_list(self):
        return self._get_criterion_number_by_event_list(EntityType.TEAM.name)
    
    def get_teams_statistics(self):
        return ut.get_statistics(self.get_teams_number_by_event_list())
    
    def get_teams_most_participations(self):
        return self._get_entity_most_participations(EntityType.TEAM.name)

    # Entity: CHARACTER
    def get_characters_list(self):
        return self._get_criterion_list(EntityType.CHARACTER.name)
    
    def get_characters_number(self):
        return len(self.get_characters_list())
    
    def get_characters_number_by_event_list(self):
        return self._get_criterion_number_by_event_list(EntityType.CHARACTER.name)
    
    def get_characters_statistics(self):
        return ut.get_statistics(self.get_characters_number_by_event_list())
    
    def get_characters_most_participations(self):
        return self._get_entity_most_participations(EntityType.CHARACTER.name)

    # Entity: PLAYER_CHARACTER
    def get_player_characters_list(self):
        return self._get_criterion_list(EntityType.PLAYER_CHARACTER.name)
    
    def get_player_characters_number(self):
        return len(self.get_player_characters_list())
    
    def get_player_characters_number_by_event_list(self):
        return self._get_criterion_number_by_event_list(EntityType.PLAYER_CHARACTER.name)
    
    def get_player_characters_statistics(self):
        return ut.get_statistics(self.get_player_characters_number_by_event_list())
    
    def get_player_characters_most_participations(self):
        return self._get_entity_most_participations(EntityType.PLAYER_CHARACTER.name)

    # Winners
    def _get_winners_entity_list(self, competitor_type):
        winners_entity_list = list()
        for event in self.get_events_list():
            winners_entity_list.append(getattr(event, f"get_winner_{competitor_type}"))
        return winners_entity_list
    
    # Winner: PLAYER
    def get_winners_player_list(self):
        return self._get_winners_entity_list(CompetitorType.PLAYER.name)
    
    def get_winners_player_number(self):
        return len(self.get_winners_player_list())
    
    # Winner: TEAM
    def get_winners_team_list(self):
        return self._get_winners_entity_list(CompetitorType.TEAM.name)
    
    def get_winners_team_number(self):
        return len(self.get_winners_team_list())
    
    # Ranking
    def get_ranking(self):
        ranking = dict()
        for competitor, points in self.get_points_earned().items():
            ranking[competitor] = points * competitor.get_win_lose_ratio(self)
        return dict(sorted(ranking.items(), key=lambda x:x[1]), reverse=True)


class EventModality(Base):
    __tablename__ = "event_modality"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    _competitor_type = Column(String, nullable=False) # Player, Team
    _event_system = Column(String, nullable=False) # Tournament, League, Duel

    ''' Relationships '''
    events = relationship("Event", back_populates="event_modality", cascade="all, delete-orphan")

    ''' Methods '''
    @hybrid_property
    def competitor_type(self):
        return self._competitor_type

    @hybrid_property
    def event_system(self):
        return self._event_system


class Event(Base):
    __tablename__ = "event"

    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    _name = Column(String, nullable=False)
    _code_name = Column(String, nullable=False)
    _link_raw = Column(String, nullable=False)
    _link_summarized = Column(String, nullable=False)
    _playlist = Column(String, nullable=False)
    _bracket = Column(String, nullable=False)
    _date = Column(DateTime, nullable=False)
    _event_order = Column(Integer, nullable=False)

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
    @hybrid_property
    def name(self):
        return self._name
    
    @hybrid_property
    def code_name(self):
        return self._code_name
    
    @hybrid_property
    def link_raw(self):
        return self._link_raw
    
    @hybrid_property
    def link_summarized(self):
        return self._link_summarized
    
    @hybrid_property
    def playlist(self):
        return self._playlist
    
    @hybrid_property
    def bracket(self):
        return self._bracket
    
    @hybrid_property
    def date(self):
        return self._date
    
    @hybrid_property
    def event_order(self):
        return self._event_order

    def get_event_system(self): # TOURNAMENT, LEAGUE, DUEL
        return self.event_modality.event_system

    def get_competitor_type(self): # PLAYER, TEAM
        return self.event_modality.competitor_type
    
    # Stats
    def get_event_stats(self):
        return ut.EventStats(self.get_duels_list(),
                             self.get_duels_number(),
                             self.get_combats_list(),
                             self.get_combats_number(),
                             self.get_combats_statistics(),
                             self.get_rounds_list(),
                             self.get_rounds_number(),
                             self.get_rounds_statistics(),
                             self.get_competitors_list(),
                             self.get_competitors_number(),
                             self.get_competitors_statistics(),
                             self.get_competitors_most_participations(),
                             self.get_characters_list(),
                             self.get_characters_number(),
                             self.get_characters_statistics(),
                             self.get_characters_most_participations(),
                             self.get_player_characters_list(),
                             self.get_player_characters_number(),
                             self.get_player_characters_statistics(),
                             self.get_player_characters_most_participations(),
                             self.get_winner(),
                             self.get_results())

    # Duels
    def get_duels_list(self):
        ''' List of duels of an event. '''
        return list(sorted(self.duels, key=lambda x:x.duel_order))
         
    def get_duels_number(self):
        ''' Number of duels of an event. '''
        return len(self.get_duels_list())
    
    # Lists getters
    def _get_criterion_list(self, criterion):
        ''' List of criterion for duel. '''
        criterion_list = list()
        for duel in self.duels:
            criterion_list += getattr(duel, f"get_{criterion.lower()}s_list")
        return criterion_list
    
    def _get_criterion_number_by_duel_list(self, criterion):
        '''
        For statistics.
        List of numbers of criterion by duel of an event.
        '''
        criterion_number_by_duel_list = list()
        for duel in self.get_duels_list():
            criterion_number_by_duel_list.append(getattr(duel, f"get_{criterion.lower()}s_number"))
        return criterion_number_by_duel_list

    # Challenge: COMBAT
    def get_combats_list(self):
        return self._get_criterion_list(ChallengeType.COMBAT.name)
    
    def get_combats_number(self):
        return len(self.get_combats_list())
    
    def get_combats_number_by_duel_list(self):
        return self._get_criterion_number_by_duel_list(ChallengeType.COMBAT.name)
    
    def get_combats_statistics(self):
        return ut.get_statistics(self.get_combats_number_by_duel_list())

    # Challenge: ROUND
    def get_rounds_list(self):
        return self._get_criterion_list(ChallengeType.ROUND.name)
    
    def get_rounds_number(self):
        return len(self.get_rounds_list())
    
    def get_rounds_number_by_duel_list(self):
        return self._get_criterion_number_by_duel_list(ChallengeType.ROUND.name)
    
    def get_rounds_statistics(self):
        return ut.get_statistics(self.get_rounds_number_by_duel_list())

    # Entities
    def _get_entity_most_participations(self, entity_type):
        ''' For statistics. '''
        entities_list = getattr(self, f"get_{entity_type}s_list")
        return ut.get_multimode(entities_list)

    # Competitors
    def get_competitors_list(self):
        return self._get_criterion_list(self.get_competitor_type())
    
    def get_competitors_number(self):
        return len(self.get_competitors_list())
    
    def get_competitors_number_by_duel_list(self):
        return self._get_criterion_number_by_duel_list(self.get_competitor_type())
    
    def get_competitors_statistics(self):
        return ut.get_statistics(self.get_competitors_number_by_duel_list())
    
    def get_competitors_most_participations(self):
        return self._get_entity_most_participations(self.get_competitor_type())

    # Entity: CHARACTER
    def get_characters_list(self):
        return self._get_criterion_list(EntityType.CHARACTER.name)
    
    def get_characters_number(self):
        return len(self.get_characters_list())
    
    def get_characters_number_by_duel_list(self):
        return self._get_criterion_number_by_duel_list(EntityType.CHARACTER.name)
    
    def get_characters_statistics(self):
        return ut.get_statistics(self.get_characters_number_by_duel_list())
    
    def get_characters_most_participations(self):
        return self._get_entity_most_participations(EntityType.CHARACTER.name)

    # Entity: PLAYER_CHARACTER
    def get_player_characters_list(self):
        return self._get_criterion_list(EntityType.PLAYER_CHARACTER.name)
    
    def get_player_characters_number(self):
        return len(self.get_player_characters_list())
    
    def get_player_characters_number_by_duel_list(self):
        return self._get_criterion_number_by_duel_list(EntityType.PLAYER_CHARACTER.name)
    
    def get_player_characters_statistics(self):
        return ut.get_statistics(self.get_player_characters_number_by_duel_list())
    
    def get_player_characters_most_participations(self):
        return self._get_entity_most_participations(EntityType.PLAYER_CHARACTER.name)

    # Winner
    def get_winner(self):
        ''' The winner of the event is the winner of the last duel. '''
        return self.get_duels_list()[-1].get_winner()

    # Results
    def get_results(self):
        competitors_list = list()
        if self.get_competitor_type == CompetitorType.PLAYER.name:
            competitors_list = self.get_players_list()
        elif self.get_competitor_type == CompetitorType.TEAM.name:
            competitors_list = self.get_teams_list()
        else:
            raise ValueError(f"Invalid competitor_type: {self.get_competitor_type()}")
        # @@@@ Implementar función get_result en player y team
        return sorted(competitors_list, key=lambda x:x.get_result(self), reverse=True)

    # Ranking
    def get_points_earned(self):
        points_earned_dict = defaultdict(int)
        for duel in self.get_duels_list():
            for competitor, points in duel.get_points_earned().items():
                points_earned_dict[competitor] += points
        return dict(points_earned_dict)
    
    def get_ranking(self):
        ranking = dict()
        for competitor, points in self.get_points_earned().items():
            ranking[competitor] = points * competitor.get_win_lose_ratio(self)
        return dict(sorted(ranking.items(), key=lambda x:x[1]), reverse=True)
    

''' Duel group '''

class DuelType(Base):
    __tablename__ = "duel_type"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    _description = Column(String, nullable=True)
    _name = Column(String, nullable=False)
    _code_name = Column(String, nullable=False)
    _name_synonymous = Column(String, nullable=True)
    _code_name_synonymous = Column(String, nullable=True)

    ''' Relationships '''
    duels = relationship("Duel", back_populates="duel_type", cascade="all, delete-orphan")

    ''' Methods '''  
    # Getters
    @hybrid_property
    def description(self):
        return self._description
    
    @hybrid_property
    def name(self):
        return self._name
    
    @hybrid_property
    def code_name(self):
        return self._code_name
    
    @hybrid_property
    def name_synonymous(self):
        return self._name_synonymous
    
    @hybrid_property
    def code_name_synonymous(self):
        return self._code_name_synonymous


class Video(Base):
    __tablename__ = "video"

    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    _url = Column(String, nullable=False)

    duel_id = Column(Integer, ForeignKey("duel.id"), nullable=False)

    ''' Relationships '''
    duel = relationship("Duel", back_populates="videos")

    ''' Methods '''
    # Getters
    @hybrid_property
    def url(self):
        return self._url


class Duel(Base):
    __tablename__ = "duel"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    _duel_order = Column(Integer, nullable=False)

    event_id = Column(Integer, ForeignKey("event.id"), nullable=False)
    duel_type_id = Column(Integer, ForeignKey("duel_type.id"), nullable=False)

    ''' Relationships '''
    event = relationship("Event", back_populates="duels")
    duel_type = relationship("DuelType", back_populates="duels")
    videos = relationship("Video", back_populates="duel", cascade="all, delete-orphan")
    combats = relationship("Combat", back_populates="duel", cascade="all, delete-orphan")

    ''' Methods '''
    # Getters
    @hybrid_property
    def duel_order(self):
        return self._duel_order

    def get_competitor_type(self):
        return self.event.get_competitor_type()

    def get_videos(self):
        return self.videos # @@@@ ¿Ordenar?
    
    # Stats
    def get_duel_stats(self):
        # Total combats
        combats_list = self.get_combats_list()
        combats_number = self.get_combats_number()
        # Rounds
        rounds_list = self.get_rounds_list()
        rounds_number = self.get_rounds_number()
        rounds_statistics = self.get_rounds_statistics()
        # Competitors
        competitors_list = self.get_competitors_list()
        competitors_number = self.get_competitors_number()
        competitors_statistics = self.get_competitors_statistics()
        competitors_most_participations = self.get_competitors_most_participations()
        # Characters
        characters_list = self.get_characters_list()
        characters_number = self.get_characters_number()
        characters_statistics = self.get_characters_statistics()
        characters_most_participations = self.get_characters_most_participations()
        # Player Characters
        player_characters_list = self.get_player_characters_list()
        player_characters_number = self.get_player_characters_number()
        player_characters_statistics = self.get_player_characters_statistics()
        player_characters_most_participations = self.get_player_characters_most_participations()
        # Results
        results = self.get_results()
        winner = self.get_winner()
        return ut.DuelStats(combats_list,
                            combats_number,
                            rounds_list,
                            rounds_number,
                            rounds_statistics,
                            competitors_list,
                            competitors_number,
                            competitors_statistics,
                            competitors_most_participations,
                            characters_list,
                            characters_number,
                            characters_statistics,
                            characters_most_participations,
                            player_characters_list,
                            player_characters_number,
                            player_characters_statistics,
                            player_characters_most_participations,
                            results,
                            winner)

    # Combats
    def get_combats_list(self):
        ''' List of combats of a duel. '''
        return list(sorted(self.combats, key=lambda x:x.combat_order))
    
    def get_combats_number(self):
        ''' Number of combats of a duel. '''
        return len(self.get_combats_list())

    # Lists getters
    def _get_criterion_list(self, criterion):
        ''' List of criterion for combat. '''
        criterion_list = list()
        for combat in self.combats:
            criterion_list += getattr(combat, f"get_{criterion.lower()}s_list")
        return criterion_list
    
    def _get_criterion_number_by_combat_list(self, criterion):
        '''
        For statistics.
        List of numbers of criterion by combat of a duel.
        '''
        criterion_number_by_combat_list = list()
        for combat in self.get_combats_list():
            criterion_number_by_combat_list.append(getattr(combat, f"get_{criterion.lower()}s_number"))
        return criterion_number_by_combat_list

    # Challenge: ROUND
    def get_rounds_list(self):
        return self._get_criterion_list(ChallengeType.ROUND.name)
    
    def get_rounds_number(self):
        return len(self.get_rounds_list())

    def get_rounds_number_by_combat_list(self):
        return self._get_criterion_number_by_combat_list(ChallengeType.ROUND.name)
    
    def get_rounds_statistics(self):
        return ut.get_statistics(self.get_rounds_number_by_combat_list())

    # Entities
    def _get_entity_most_participations(self, entity_type):
        ''' For statistics. '''
        entities_list = getattr(self, f"get_{entity_type}s_list")
        return ut.get_multimode(entities_list)

    # Competitors
    def get_competitors_list(self):
        return self._get_criterion_list(self.get_competitor_type())
    
    def get_competitors_number(self):
        return len(self.get_competitors_list())
    
    def get_competitors_number_by_combat_list(self): # @@@@ Innecesario
        return self._get_criterion_number_by_combat_list(self.get_competitor_type())
    
    def get_competitors_statistics(self): # @@@@ Innecesario
        return ut.get_statistics(self.get_competitors_number_by_combat_list())
    
    def get_competitors_most_participations(self):
        return self._get_entity_most_participations(self.get_competitor_type())

    # Entity: CHARACTER
    def get_characters_list(self):
        return self._get_criterion_list(EntityType.CHARACTER.name)
    
    def get_characters_number(self):
        return len(self.get_characters_list())
    
    def get_characters_number_by_combat_list(self): # @@@@ Innecesario
        return self._get_criterion_number_by_combat_list(EntityType.CHARACTER.name)
    
    def get_characters_statistics(self): # @@@@ Innecesario
        return ut.get_statistics(self.get_characters_number_by_combat_list())
    
    def get_characters_most_participations(self):
        return self._get_entity_most_participations(EntityType.CHARACTER.name)

    # Entity: PLAYER_CHARACTER
    def get_player_characters_list(self):
        return self._get_criterion_list(EntityType.PLAYER_CHARACTER.name)
    
    def get_player_characters_number(self):
        return len(self.get_player_characters_list())
    
    def get_player_characters_number_by_combat_list(self): # @@@@ Innecesario
        return self._get_criterion_number_by_combat_list(EntityType.PLAYER_CHARACTER.name)
    
    def get_player_characters_statistics(self): # @@@@ Innecesario
        return ut.get_statistics(self.get_player_characters_number_by_combat_list())
    
    def get_player_characters_most_participations(self):
        return self._get_entity_most_participations(EntityType.PLAYER_CHARACTER.name)

    # Results
    def get_results(self):
        combats_won_dict = defaultdict(int)
        for combat in self.get_combats_list():
            combats_won_dict[combat.get_competitor1()] += combat.get_win_point_competitor1()
            combats_won_dict[combat.get_competitor2()] += combat.get_win_point_competitor2()
        return dict(sorted(dict(combats_won_dict).items(), key=lambda x:x[1], reverse=True))

    # Winner
    def get_winner(self):
        return self.get_results().keys()[0]
    
    # Ranking
    def _get_combats_data(self):
        combats_data_dict = defaultdict(ut.CombatsData)
        for combat in self.get_combats_list():
            combat_data_obj = combat.get_combat_data()
            # Competitor 1
            if combats_data_dict.get(combat.get_competitor1()) is None:
                combats_data_dict[combat.get_competitor1()].win_points = combat_data_obj.win_points_competitor1() # Combats won player 1
                combats_data_dict[combat.get_competitor1()].points_earned = combat_data_obj.points_earned_competitor1() # Points earned player 1
            else:
                combats_data_dict[combat.get_competitor1()].win_points += combat_data_obj.win_points_competitor1 # Combats won player 1
                combats_data_dict[combat.get_competitor1()].points_earned += combat_data_obj.points_earned_competitor1 # Points earned player 1
            # Competitor 2
            if combats_data_dict.get(combat.get_competitor2()) is None:
                combats_data_dict[combat.get_competitor2()].win_points = combat_data_obj.win_points_competitor2() # Combats won player 2
                combats_data_dict[combat.get_competitor2()].points_earned = combat_data_obj.points_earned_competitor2() # Points earned player 2
            else:
                combats_data_dict[combat.get_competitor2()].win_points += combat_data_obj.win_points_competitor2 # Combats won player 2
                combats_data_dict[combat.get_competitor2()].points_earned += combat_data_obj.points_earned_competitor2 # Points earned player 2
        return dict(combats_data_dict)
    
    def _get_beating_factors(self):
        beating_factors_dict = dict()
        combats_data_dict = self._get_combats_data()
        for competitor in self.get_competitors_list():
            beating_factors_dict[competitor] = ut.beating_factor(combats_data_dict[competitor].win_points,
                                                                 self.get_combats_number())
        return beating_factors_dict
    
    def get_points_earned(self):
        points_earned_dict = dict()
        for competitor in self.get_competitors_list():
            points_earned_dict[competitor] = self._get_combats_data()[competitor].points_earned * \
                                             self._get_beating_factors()[competitor]
        return points_earned_dict


class Stage(Base):
    __tablename__ = "stage"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    _name = Column(String, nullable=False)
    _ring_out = Column(Boolean, nullable=False)
    _walls_destructible = Column(Boolean, nullable=False)
    _walls_low = Column(Boolean, nullable=False)
    _walls_high = Column(Boolean, nullable=False)

    ''' Relationships '''
    combats = relationship("Combat", back_populates="stage", cascade="all, delete-orphan")

    ''' Methods '''
    # Getters
    @hybrid_property
    def name(self):
        return self._name

    @hybrid_property
    def ring_out(self):
        return self._ring_out

    @hybrid_property
    def walls_destructible(self):
        return self._walls_destructible

    @hybrid_property
    def walls_low(self):
        return self._walls_low

    @hybrid_property
    def walls_high(self):
        return self._walls_high

    # Combats
    def get_combats_list(self):
        return self.combats

    def get_combats_number(self):
        return len(self.combats)
    
    # Rounds
    def get_rounds_played_number(self):
        rounds_played_number = 0
        for combat in self.combats:
            rounds_played_number += combat.get_rounds_played_number()
        return rounds_played_number


class Combat(Base):
    __tablename__ = "combat"

    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    _combat_order = Column(Integer, nullable=False)

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
    @hybrid_property
    def combat_order(self):
        return self._combat_order

    def get_competitor_type(self):
        return self.duel.get_competitor_type()

    # Stats
    def get_combat_stats(self):
        return ut.CombatStats(self.get_rounds_list(),
                              self.get_rounds_number(),
                              self.get_competitors_list(),
                              self.get_characters_list(),
                              self.get_player_characters_list(),
                              self.get_winner())

    # Data
    def get_combat_data(self):
        return ut.CombatData(self.get_win_point_competitor1(),
                             self.get_win_point_competitor2(),
                             self.get_points_earned_competitor1(),
                             self.get_points_earned_competitor2())

    # Rounds
    def get_rounds_list(self):
        return list(sorted(self.rounds, key=lambda x:x.round_order))
    
    def get_rounds_number(self):
        return len(self.get_rounds_list())

    # # Players
    # def get_players_list(self):
    #     return list(sorted([self.player1, self.player2], key=lambda x:x.name))
    
    # # Teams
    # def get_teams_list(self):
    #     return list(sorted([self.team1, self.team2], key=lambda x:x.name))
    
    # Competitors
    def _get_competitor(self, side):
        competitor = None
        if self.get_competitor_type() == CompetitorType.PLAYER.name:
            competitor = getattr(self, f"player{side}")
        elif self.get_competitor_type() == CompetitorType.TEAM.name:
            competitor = getattr(self, f"team{side}")
        else:
            raise ValueError(f"Invalid competitor_type: {self.get_competitor_type()}")
        return competitor

    def get_competitor1(self):
        return self._get_competitor(1)

    def get_competitor2(self):
        return self._get_competitor(2)

    def get_competitors_list(self):
        return list(sorted([self.get_competitor1(), self.get_competitor2], key=lambda x:x.name))

    # Characters
    def get_characters_list(self):
        return list(sorted([self.character1, self.character2], key=lambda x:x.name))
    
    # PlayersCharacters
    def player_character1(self):
        return list(set(self.player1.get_players_characters()) & set(self.character1.get_players_characters()))[0]

    def player_character2(self):
        return list(set(self.player2.get_players_characters()) & set(self.character2.get_players_characters()))[0]

    def get_player_characters_list(self):
        return list(sorted(list(self.player_character1(), self.player_character2()), key=lambda x:x.name))

    # Results
    def _get_rounds_data(self):
        ''' Extract all data of a round. '''
        rounds_data_obj = ut.RoundData(0, 0, 0, 0)
        for round in self.get_rounds_list():
            round_data_obj = round.get_round_data()
            rounds_data_obj.points_player1 += round_data_obj.points_player1 # Points raw player 1
            rounds_data_obj.points_player2 += round_data_obj.points_player2 # Points raw player 2
            rounds_data_obj.result_player1 += round_data_obj.result_player1 # Rounds won player 1
            rounds_data_obj.result_player2 += round_data_obj.result_player2 # Rounds won player 2
        return rounds_data_obj

    def get_beating_factor_player1(self):
        ''' Rounds beating factor for player 1. '''
        return ut.beating_factor(self._get_rounds_data().result_player1, self.get_rounds_number())
    
    def get_beating_factor_player2(self):
        ''' Rounds beating factor for player 2. '''
        return ut.beating_factor(self._get_rounds_data().result_player2, self.get_rounds_number())
    
    def is_draw(self):
        ''' Determines if the combat is a draw. '''
        draw = False
        if self.get_beating_factor_player1() == self.get_beating_factor_player2():
            draw = True
        return draw

    def get_result(self):
        winner = None
        loser = None
        if not self.is_draw():
            if self.get_beating_factor_player1() > self.get_beating_factor_player2():
                winner = self.get_competitor1()
                loser = self.get_competitor2()
            else:
                winner = self.get_competitor2()
                loser = self.get_competitor1()
        return ut.CombatResult(winner, loser)

    def get_winner(self):
        return self.get_result().winner
    
    def get_loser(self): # No se usa
        return self.get_result().loser
    
    def _get_win_point_competitor(self, side):
        win_point_competitor = 0
        if self.is_draw() or self.get_winner() == getattr(self, f"get_competitor{side}"):
            win_point_competitor = 1
        return win_point_competitor
    
    def get_win_point_competitor1(self):
        return self._get_win_point_competitor(CombatSide.SIDE1.value)
    
    def get_win_point_competitor2(self):
        return self._get_win_point_competitor(CombatSide.SIDE2.value)

    # Ranking
    def _get_level_factor(self, side):
        ''' side: 1, 2 '''
        win_rate_competitor1 = self.get_competitor1().get_combats_win_rate()
        win_rate_competitor2 = self.get_competitor2().get_combats_win_rate()
        diff = 0
        if side == CombatSide.SIDE1.value:
            diff = win_rate_competitor1 - win_rate_competitor2
        elif side == CombatSide.SIDE2.value:
            diff = win_rate_competitor2 - win_rate_competitor1
        else:
            raise ValueError(f"Invalid player side: {side}")
        return ut.level_factor(LvlFactor.A.name, LvlFactor.B.name, diff)

    def get_level_factor_competitor1(self):
        return self._get_level_factor(CombatSide.SIDE1.value)
    
    def get_level_factor_competitor2(self):
        return self._get_level_factor(CombatSide.SIDE2.value)
    
    # Points earned
    def _get_points_earned(self, side):
        ''' side: 1, 2 '''
        points_earned = 0
        if side == CombatSide.SIDE1.value:
            points_earned = self._get_rounds_data().points_player1 * \
                            self.get_beating_factor_player1() * \
                            self.get_level_factor_competitor1()
        elif side == CombatSide.SIDE2.value:
            points_earned = self._get_rounds_data().points_player2 * \
                            self.get_beating_factor_player2() * \
                            self.get_level_factor_competitor2()
        else:
            raise ValueError(f"Invalid player side: {side}")
        return points_earned

    def get_points_earned_competitor1(self):
        return self._get_points_earned(CombatSide.SIDE1.value)
    
    def get_points_earned_competitor2(self):
        return self._get_points_earned(CombatSide.SIDE2.value)


class Round(Base):
    __tablename__ = "round"

    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    _round_order = Column(Integer, nullable=False) # 1, 2, ...
    _result_player1 = Column(String, nullable=False) # D, W, PW, WY, WB, LY, LB, PL
    _result_player2 = Column(String, nullable=False) # D, W, PW, WY, WB, LY, LB, PL

    combat_id = Column(Integer, ForeignKey("combat.id"), nullable=False)

    ''' Relationships '''
    combat = relationship("Combat", back_populates="rounds")

    ''' Methods '''
    # Getters
    @hybrid_property
    def round_order(self):
        return self._round_order
    
    @hybrid_property
    def result_player1(self):
        return self._result_player1
    
    @hybrid_property
    def result_player2(self):
        return self._result_player2

    # Data
    def get_round_data(self):
        return ut.RoundData(self.get_points_player1(),
                            self.get_points_player2(),
                            self.get_result_player1(),
                            self.get_result_player2())
    
    # Points
    def get_points_player1(self):
        return ROUNDS_POINTS[self.result_player1]

    def get_points_player2(self):
        return ROUNDS_POINTS[self.result_player2]

    # Results
    def _get_result_player(self, side):
        ''' Returns 1 when result_player is in win conditions. '''
        result = 0
        if getattr(self, f"result_player{side}") in ROUND_WIN_CONDITIONS:
            result = 1
        return result

    def get_result_player1(self):
        return self._get_result_player(1)

    def get_result_player2(self):
        return self._get_result_player(2)


''' Entities group '''

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

    # Events stats
    def get_events_stats(self, combats_list):
        events_played_set = set()
        for combat in combats_list:
            events_played_set.add(combat.get_event())
        events_played_list = list(sorted(list(events_played_set), key=lambda x:x.get_event_order()))
        events_played_number = len(events_played_list)
        events_stats_obj = EventsStats(events_played_list,
                                       events_played_number,
                                       None)
        return events_stats_obj
    
    # Combats stats
    def get_combats_stats(self, func_wlr, combats_list):
        combats_played_list = list()
        combats_won_list = list()
        combats_lost_list = list()
        combats_draw_list = list()
        for combat in combats_list:
            combats_played_list.append(combat)
            if self in combat.get_winners_entities_list(): # player, character, team
                combats_won_list.append(combat)
            if self in combat.get_losers_entities_list(): # player, character, team
                combats_lost_list.append(combat)
            if combat.is_draw():
                combats_draw_list.append(combat)
        combats_played_list = list(sorted(combats_played_list, key=lambda x:x.get_combat_order()))
        combats_won_list = list(sorted(combats_won_list, key=lambda x:x.get_combat_order()))
        combats_lost_list = list(sorted(combats_lost_list, key=lambda x:x.get_combat_order()))
        combats_draw_list = list(sorted(combats_draw_list, key=lambda x:x.get_combat_order()))
        combats_played_number = len(combats_played_list)
        combats_won_number = len(combats_won_list)
        combats_lost_number = len(combats_lost_list)
        combats_draw_number = len(combats_draw_list)
        victories = combats_won_number + combats_draw_number
        defeats = combats_lost_number
        played = combats_played_number
        win_rate = ut.win_rate(victories, played)
        win_lose_ratio = ut.win_lose_ratio(func_wlr, victories, defeats)
        combats_stats_obj = CombatsStats(combats_played_list,
                                         combats_won_list,
                                         combats_lost_list,
                                         combats_draw_list,
                                         combats_played_number,
                                         combats_won_number,
                                         combats_lost_number,
                                         combats_draw_number,
                                         win_rate,
                                         win_lose_ratio)
        return combats_stats_obj

    # Rounds stats
    def get_rounds_stats(self, func_wlr, combats_p1_list, combats_p2_list):
        rounds_played_p1 = 0
        rounds_played_p2 = 0
        rounds_won_p1 = 0
        rounds_lost_p1 = 0
        rounds_won_p2 = 0
        rounds_lost_p2 = 0
        for combat in combats_p1_list:
            rounds_played_p1 += combat.get_rounds_played_number()
            rounds_won_p1 += combat.get_rounds_won_p1_number()
            rounds_lost_p1 += combat.get_rounds_lost_p1_number()
        for combat in combats_p2_list:
            rounds_played_p2 += combat.get_rounds_played_number()
            rounds_won_p2 += combat.get_rounds_won_p2_number()
            rounds_lost_p2 += combat.get_rounds_lost_p2_number()
        rounds_played = rounds_played_p1 + rounds_played_p2
        rounds_won = rounds_won_p1 + rounds_won_p2
        rounds_lost = rounds_lost_p1 + rounds_lost_p2
        win_rate = ut.win_rate(rounds_won, rounds_played)
        win_rate_p1 = ut.win_rate(rounds_won_p1, rounds_played_p1)
        win_rate_p2 = ut.win_rate(rounds_won_p2, rounds_played_p2)
        win_lose_ratio = ut.win_lose_ratio(func_wlr, rounds_won, rounds_lost)
        win_lose_ratio_p1 = ut.win_lose_ratio(func_wlr, rounds_won_p1, rounds_lost_p1)
        win_lose_ratio_p2 = ut.win_lose_ratio(func_wlr, rounds_won_p2, rounds_lost_p2)
        rounds_stats_obj = RoundsStats(rounds_played,
                                       rounds_won,
                                       rounds_lost,
                                       rounds_played_p1,
                                       rounds_won_p1,
                                       rounds_lost_p1,
                                       rounds_played_p2,
                                       rounds_won_p2,
                                       rounds_lost_p2,
                                       win_rate,
                                       win_lose_ratio,
                                       win_rate_p1,
                                       win_lose_ratio_p1,
                                       win_rate_p2,
                                       win_lose_ratio_p2)
        return rounds_stats_obj

    # Combats stages stats
    def get_combats_stage_stats(self, func_wlr, combats_list):
        combats_stage_dict = dict()
        stages_set = set()
        for combat in combats_list:
            stages_set.add(combat.get_stage())
        stages_list = list(sorted(list(stages_set), key=lambda x:x.get_name()))
        for stage in stages_list:
            combats_stage_dict[stage] = list()
        for combat in combats_list:
            combats_stage_dict[combat.get_stage()].append(combat)
            if self in combat.get_winners_entities_list():
                combats_stage_dict[combat.get_stage()].append(combat)
            if self in combat.get_losers_entities_list():
                combats_stage_dict[combat.get_stage()].append(combat)
            if combat.is_draw():
                combats_stage_dict[combat.get_stage()].append(combat)
        for stage, combats_list in combats_stage_dict.items():
            combats_stage_dict[stage] = self.get_combats_stats(func_wlr, combats_list)
    

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

    # Events stats
    def get_events_stats(self, combats_list):
        events_stats_obj = super().get_events_stats(combats_list)
        events_results_dict = dict()
        for event in events_stats_obj.get_played_list():
            events_results_dict[event] = event.get_results_dict()[self]
        events_stats_obj.set_results_dict(events_results_dict)
        return events_stats_obj

    # Combats stats
    def get_combats_stats(self, func_wlr, combats_list):
        return super().get_combats_stats(func_wlr, combats_list)

    # Rounds stats
    def get_rounds_stats(self, func_wlr, combats_p1_list, combats_p2_list):
        return super().get_rounds_stats(func_wlr, combats_p1_list, combats_p2_list)

    # Combats stage stats
    def get_combats_stage_stats(self, func_wlr, combats_list):
        return super().get_combats_stage_stats(func_wlr, combats_list)

    # Duels stats
    def get_duels_stats(self, func_wlr, combats_list):
        duels_played_set = set()
        duels_won_set = set()
        duels_lost_set = set()
        for combat in combats_list:
            duel = combat.get_duel()
            duels_played_set.add(duel)
            if duel.get_winner() == self:
                duels_won_set.add(duel)
            if self in duel.get_losers_list():
                duels_lost_set.add(duel)
        duels_played_list = list(sorted(list(duels_played_set), key=lambda x:x.get_duel_order()))
        duels_won_list = list(sorted(list(duels_won_set), key=lambda x:x.get_duel_order()))
        duels_lost_list = list(sorted(list(duels_lost_set), key=lambda x:x.get_duel_order()))
        duels_played_number = len(duels_played_list)
        duels_won_number = len(duels_won_list)
        duels_lost_number = len(duels_lost_list)
        win_rate = ut.win_rate(duels_won_number, duels_played_number)
        win_lose_ratio = ut.win_lose_ratio(func_wlr, duels_won_number, duels_lost_number)
        duels_stats_obj = DuelsStats(duels_played_list, # @@@@
                                     duels_won_list,
                                     duels_lost_list,
                                     duels_played_number,
                                     duels_won_number,
                                     duels_lost_number,
                                     win_rate,
                                     win_lose_ratio)
        
    # Ranking
    def get_win_lose_ratio(self, duels_list):
        ... # @@@@


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

    def get_playlist(self): # @@@@ hacer correctamente el getter
        return self.playlist
    
    def get_country(self):
        return self.country

    def get_social_medias_list(self):
        return self.social_medias
    
    def get_teams_list(self):
        return self.teams

    def combats(self):
        return self.combats_p1 + self.combats_p2
    
    def get_players_characters(self):
        return self.players_characters

    # Events stats
    def get_events_stats(self):
        return super().get_events_stats(self.combats())

    # Combats stats
    def get_combats_stats(self, func_wlr):
        return super().get_combats_stats(func_wlr, self.combats())
    
    def get_combats_p1_stats(self, func_wlr):
        return super().get_combats_stats(func_wlr, self.combats_p1)
    
    def get_combats_p2_stats(self, func_wlr):
        return super().get_combats_stats(func_wlr, self.combats_p2)

    # Combats stage stats
    def get_combats_stage_stats(self, func_wlr):
        return super().get_combats_stage_stats(func_wlr, self.combats())

    def get_combats_stage_p1_stats(self, func_wlr):
        return super().get_combats_stage_stats(func_wlr, self.combats_p1)
    
    def get_combats_stage_p2_stats(self, func_wlr):
        return super().get_combats_stage_stats(func_wlr, self.combats_p2)
    
    # Rounds stats
    def get_rounds_stats(self, func_wlr):
        rounds_stats_obj = super().get_rounds_stats(func_wlr, self.combats_p1, self.combats_p2)
        round_stats_obj = RoundStats(rounds_stats_obj.get_played(),
                                     rounds_stats_obj.get_won(),
                                     rounds_stats_obj.get_lost(),
                                     rounds_stats_obj.get_win_rate(),
                                     rounds_stats_obj.get_win_lose_ratio())
        return round_stats_obj
        
    def get_rounds_stats_p1(self, func_wlr):
        rounds_stats_obj = super().get_rounds_stats(func_wlr, self.combats_p1, self.combats_p2)
        round_stats_obj = RoundStats(rounds_stats_obj.get_played_p1(),
                                     rounds_stats_obj.get_won_p1(),
                                     rounds_stats_obj.get_lost_p1(),
                                     rounds_stats_obj.get_win_rate_p1(),
                                     rounds_stats_obj.get_win_lose_ratio_p1())
        return round_stats_obj
    
    def get_rounds_stats_p2(self, func_wlr):
        rounds_stats_obj = super().get_rounds_stats(func_wlr, self.combats_p1, self.combats_p2)
        round_stats_obj = RoundStats(rounds_stats_obj.get_played_p2(),
                                     rounds_stats_obj.get_won_p2(),
                                     rounds_stats_obj.get_lost_p2(),
                                     rounds_stats_obj.get_win_rate_p2(),
                                     rounds_stats_obj.get_win_lose_ratio_p2())
        return round_stats_obj

    # Duels stats
    def get_duels_stats(self, func_wlr):
        return super().get_duels_stats(func_wlr, self.combats())

    # Team duels stats
    def get_team_duels_stats(self, func_wlr):
        duels_stats_obj = self.get_duels_stats(func_wlr)
        team_duels_played_list = list()
        team_duels_won_list = list()
        team_duels_lost_list = list()
        for duel in duels_stats_obj.get_played_list():
            if duel.is_team_duel():
                team_duels_played_list.append(duel)
        for duel in duels_stats_obj.get_won_list():
            if duel.is_team_duel():
                team_duels_won_list.append(duel)
        for duel in duels_stats_obj.get_lost_list():
            if duel.is_team_duel():
                team_duels_lost_list.append(duel)
        team_duels_played_number = len(team_duels_played_list)
        team_duels_won_number = len(team_duels_won_list)
        team_duels_lost_number = len(team_duels_lost_list)
        win_rate = ut.win_rate(team_duels_won_number, team_duels_played_number)
        win_lose_ratio = ut.win_lose_ratio(func_wlr, team_duels_won_number, team_duels_lost_number)
        team_duels_stats_obj = DuelsStats(team_duels_played_list,
                                          team_duels_won_list,
                                          team_duels_lost_list,
                                          team_duels_played_number,
                                          team_duels_won_number,
                                          team_duels_lost_number,
                                          win_rate,
                                          win_lose_ratio)
        return team_duels_stats_obj


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
    
    def combats(self):
        return self.combats_p1 + self.combats_p2
    
    # Country
    def get_country(self):
        country = None # When is an international team
        countries_set = set()
        for player in self.players:
            countries_set.add(player.get_country())
        if len(countries_set) == 1:
            country = list(countries_set)[0]
        return country

    # Events stats
    def get_events_stats(self):
        return super().get_events_stats(self.combats())

    # Combats stats
    def get_combats_stats(self, func_wlr):
        return super().get_combats_stats(func_wlr, self.combats())
    
    def get_combats_stats_p1(self, func_wlr):
        return super().get_combats_stats(func_wlr, self.combats_p1)
    
    def get_combats_stats_p1(self, func_wlr):
        return super().get_combats_stats(func_wlr, self.combats_p1)
    
    # Combats stage stats
    def get_combats_stage_stats(self, func_wlr):
        return super().get_combats_stage_stats(func_wlr, self.combats())
    
    def get_combats_stage_stats_p1(self, func_wlr):
        return super().get_combats_stage_stats(func_wlr, self.combats_p1)
    
    def get_combats_stage_stats_p2(self, func_wlr):
        return super().get_combats_stage_stats(func_wlr, self.combats_p2)

    # Rounds stats
    def get_rounds_stats(self, func_wlr):
        rounds_stats_obj = super().get_rounds_stats(func_wlr, self.combats_p1, self.combats_p2)
        round_stats_obj = RoundStats(rounds_stats_obj.get_played(),
                                     rounds_stats_obj.get_won(),
                                     rounds_stats_obj.get_lost(),
                                     rounds_stats_obj.get_win_rate(),
                                     rounds_stats_obj.get_win_lose_ratio())
        return round_stats_obj
        
    def get_rounds_stats_p1(self, func_wlr):
        rounds_stats_obj = super().get_rounds_stats(func_wlr, self.combats_p1, self.combats_p2)
        round_stats_obj = RoundStats(rounds_stats_obj.get_played_p1(),
                                     rounds_stats_obj.get_won_p1(),
                                     rounds_stats_obj.get_lost_p1(),
                                     rounds_stats_obj.get_win_rate_p1(),
                                     rounds_stats_obj.get_win_lose_ratio_p1())
        return round_stats_obj
    
    def get_rounds_stats_p2(self, func_wlr):
        rounds_stats_obj = super().get_rounds_stats(func_wlr, self.combats_p1, self.combats_p2)
        round_stats_obj = RoundStats(rounds_stats_obj.get_played_p2(),
                                     rounds_stats_obj.get_won_p2(),
                                     rounds_stats_obj.get_lost_p2(),
                                     rounds_stats_obj.get_win_rate_p2(),
                                     rounds_stats_obj.get_win_lose_ratio_p2())
        return round_stats_obj
    
    # Duels stats
    def get_duels_stats(self, func_wlr):
        return super().get_duels_stats(func_wlr, self.combats())


class Character(Entity):
    __tablename__ = "character"
    
    ''' Attributes '''
    id = Column(Integer, ForeignKey('entity.id'), primary_key=True, nullable=False)
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
    
    def combats(self):
        return self.combats_p1 + self.combats_p2
    
    def get_players_characters(self):
        return self.players_characters

    # Events stats
    def get_events_stats(self):
        return super().get_events_stats(self.combats())
    
    # Combats stats
    def get_combats_stats(self, func_wlr):
        return super().get_combats_stats(func_wlr, self.combats())
    
    def get_combats_stats_p1(self, func_wlr):
        return super().get_combats_stats(func_wlr, self.combats_p1)
    
    def get_combats_stats_p2(self, func_wlr):
        return super().get_combats_stats(func_wlr, self.combats_p2)

    # Combats stage stats
    def get_combats_stage_stats(self, func_wlr):
        return super().get_combats_stage_stats(func_wlr, self.combats())
    
    def get_combats_stage_stats_p1(self, func_wlr):
        return super().get_combats_stage_stats(func_wlr, self.combats_p1)
    
    def get_combats_stage_stats_p2(self, func_wlr):
        return super().get_combats_stage_stats(func_wlr, self.combats_p2)

    # Rounds stats
    def get_rounds_stats(self, func_wlr):
        rounds_stats_obj = super().get_rounds_stats(func_wlr, self.combats_p1, self.combats_p2)
        round_stats_obj = RoundStats(rounds_stats_obj.get_played(),
                                     rounds_stats_obj.get_won(),
                                     rounds_stats_obj.get_lost(),
                                     rounds_stats_obj.get_win_rate(),
                                     rounds_stats_obj.get_win_lose_ratio())
        return round_stats_obj
        
    def get_rounds_stats_p1(self, func_wlr):
        rounds_stats_obj = super().get_rounds_stats(func_wlr, self.combats_p1, self.combats_p2)
        round_stats_obj = RoundStats(rounds_stats_obj.get_played_p1(),
                                     rounds_stats_obj.get_won_p1(),
                                     rounds_stats_obj.get_lost_p1(),
                                     rounds_stats_obj.get_win_rate_p1(),
                                     rounds_stats_obj.get_win_lose_ratio_p1())
        return round_stats_obj
    
    def get_rounds_stats_p2(self, func_wlr):
        rounds_stats_obj = super().get_rounds_stats(func_wlr, self.combats_p1, self.combats_p2)
        round_stats_obj = RoundStats(rounds_stats_obj.get_played_p2(),
                                     rounds_stats_obj.get_won_p2(),
                                     rounds_stats_obj.get_lost_p2(),
                                     rounds_stats_obj.get_win_rate_p2(),
                                     rounds_stats_obj.get_win_lose_ratio_p2())
        return round_stats_obj


class PlayerCharacter(Entity):
    __tablename__ = "player_character"

    ''' Attributes '''
    id = Column(Integer, ForeignKey('entity.id'), primary_key=True, nullable=False)

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
    
    def get_combats(self, player):
        ''' Player: 1, 2 '''
        combats = list()
        getter = ""
        if player == 1:
            getter = "get_combats_p1"
        else:
            getter = "get_combats_p2"
        for combat_player in getattr(self.player, getter):
            for combat_character in getattr(self.character, getter):
                if combat_player == combat_character:
                    combats.append(combat_player)
        return combats

    def combats_p1(self):
        return self.get_combats(1)
    
    def combats_p2(self):
        return self.get_combats(2)
    
    def combats(self):
        return self.combats_p1() + self.combats_p2()

    # Events stats
    def get_events_stats(self):
        return super().get_events_stats(self.combats())

    # Combats stats
    def get_combats_stats(self, func_wlr):
        return super().get_combats_stats(func_wlr, self.combats())

    def get_combats_stats_p1(self, func_wlr):
        return super().get_combats_stats(func_wlr, self.combats_p1())

    def get_combats_stats_p2(self, func_wlr):
        return super().get_combats_stats(func_wlr, self.combats_p2())

    # Combats stage stats
    def get_combats_stage_stats(self, func_wlr):
        return super().get_combats_stage_stats(func_wlr, self.combats())

    def get_combats_stage_stats(self, func_wlr):
        return super().get_combats_stage_stats(func_wlr, self.combats_p1())

    def get_combats_stage_stats(self, func_wlr):
        return super().get_combats_stage_stats(func_wlr, self.combats_p2())

    # Rounds stats
    def get_rounds_stats(self, func_wlr):
        rounds_stats_obj = super().get_rounds_stats(func_wlr, self.combats_p1(), self.combats_p2())
        round_stats_obj = RoundStats(rounds_stats_obj.get_played(),
                                     rounds_stats_obj.get_won(),
                                     rounds_stats_obj.get_lost(),
                                     rounds_stats_obj.get_win_rate(),
                                     rounds_stats_obj.get_win_lose_ratio())
        return round_stats_obj
        
    def get_rounds_stats_p1(self, func_wlr):
        rounds_stats_obj = super().get_rounds_stats(func_wlr, self.combats_p1(), self.combats_p2())
        round_stats_obj = RoundStats(rounds_stats_obj.get_played_p1(),
                                     rounds_stats_obj.get_won_p1(),
                                     rounds_stats_obj.get_lost_p1(),
                                     rounds_stats_obj.get_win_rate_p1(),
                                     rounds_stats_obj.get_win_lose_ratio_p1())
        return round_stats_obj
    
    def get_rounds_stats_p2(self, func_wlr):
        rounds_stats_obj = super().get_rounds_stats(func_wlr, self.combats_p1(), self.combats_p2())
        round_stats_obj = RoundStats(rounds_stats_obj.get_played_p2(),
                                     rounds_stats_obj.get_won_p2(),
                                     rounds_stats_obj.get_lost_p2(),
                                     rounds_stats_obj.get_win_rate_p2(),
                                     rounds_stats_obj.get_win_lose_ratio_p2())
        return round_stats_obj
    


''' Schema generation '''

Base.metadata.create_all(ENGINE)