from sqlalchemy.orm import declarative_base, \
                           relationship, \
                           Session

from sqlalchemy import create_engine, \
                       Column, \
                       Integer, \
                       String, \
                       Boolean, \
                       DateTime, \
                       or_, \
                       ForeignKey, \
                       Table

from enum import Enum


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

class Modality(Enum):
    PLAYER = 1
    TEAM = 2


''' ClassTables '''

Base = declarative_base()


class EventType(Base):
    __tablename__ = "event_type"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    code_name = Column(String, nullable=False)

    events = relationship("Event", back_populates="event_type", cascade="all, delete-orphan")


class Region(Base):
    __tablename__ = "region"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    code_name = Column(String, nullable=False)

    events = relationship("Event", back_populates="region", cascade="all, delete-orphan")

  
class GameVersionPlatform(Base):
    __tablename__ = "game_version_platform"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    version = Column(String, nullable=False)
    platform_id = Column(Integer, ForeignKey("platform.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("game.id"), nullable=False)

    events = relationship("Event", back_populates="game_version_platform", cascade="all, delete-orphan")
    platform = relationship("Platform", back_populates="game_version_platforms")
    game = relationship("Game", back_populates="game_version_platforms")


class Platform(Base):
    __tablename__ = "platform"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    code_name = Column(String, nullable=False)

    game_version_platforms = relationship("GameVersionPlatform", back_populates="platform", cascade="all, delete-orphan")


class Game(Base):
    __tablename__ = "game"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    code_name = Column(String, nullable=False)

    game_version_platforms = relationship("GameVersionPlatform", back_populates="game", cascade="all, delete-orphan")


class DuelType(Base):
    __tablename__ = "duel_type"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    code_name = Column(String, nullable=False)
    name_synonymous = Column(String, nullable=False)
    code_name_synonymous = Column(String, nullable=False)

    duels = relationship("Duel", back_populates="duel_type", cascade="all, delete-orphan")


class Stage(Base):
    __tablename__ = "stage"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    ring_out = Column(Boolean, nullable=False)
    walls_destructible = Column(Boolean, nullable=False)
    walls_low = Column(Boolean, nullable=False)
    walls_high = Column(Boolean, nullable=False)

    combats = relationship("Combat", back_populates="stage", cascade="all, delete-orphan")


class SocialMedia(Base):
    __tablename__ = "social_media"

    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    link = Column(String, nullable=False)
    player_id = Column(Integer, ForeignKey("player.id"), nullable=False)

    player = relationship("Player", back_populates="social_medias")


class Country(Base):
    __tablename__ = "country"

    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    code_name = Column(String, nullable=False)
    flag_link = Column(String, nullable=False)

    competitors = relationship("Competitor", back_populates="country", cascade="all, delete-orphan")


class CompetitorType(Base):
    __tablename__ = "competitor_type"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(String, nullable=False)

    events = relationship("Event", back_populates="competitor_type", cascade="all, delete-orphan")


class Event(Base):
    __tablename__ = "event"

    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    code_name = Column(String, nullable=False)
    playlist = Column(String, nullable=False)
    bracket = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)

    event_type_id = Column(Integer, ForeignKey("event_type.id"), nullable=False)
    competitor_type_id = Column(Integer, ForeignKey("competitor_type.id"), nullable=False)
    region_id = Column(Integer, ForeignKey("region.id"), nullable=False)
    game_version_platform_id = Column(Integer, ForeignKey("game_version_platform.id"), nullable=False)

    event_type = relationship("EventType", back_populates="events")
    competitor_type = relationship("CompetitorType", back_populates="events")
    region = relationship("Region", back_populates="events")
    game_version_platform = relationship("GameVersionPlatform", back_populates="events")
    duels = relationship("Duel", back_populates="event", cascade="all, delete-orphan")
    positions = relationship("Position", back_populates="event", cascade="all, delete-orphan")

    ''' Methods '''
    def get_competitors_type(self):
        return self.competitor_type.type

    def get_competitors_list():
        return

    def get_competitors_number():
        return

    def get_characters_list():
        return

    def get_characters_number():
        return

    def get_event_duels_played_list():
        return

    def get_event_duels_played_number():
        return
    
    def get_event_combats_played_list():
        return

    def get_event_combats_played_number():
        return

    def get_event_rounds_played_number():
        return

    def get_rivals_list(competitor):
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

  
class Duel(Base):
    __tablename__ = "duel"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    duel_order = Column(Integer, nullable=False)
    video = Column(String, nullable=False)
    duel_type_id = Column(Integer, ForeignKey("duel_type.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("event.id"), nullable=False)

    duel_type = relationship("DuelType", back_populates="duels")
    event = relationship("Event", back_populates="duels")
    combats = relationship("Combat", back_populates="duel", cascade="all, delete-orphan")

    ''' Methods '''
    def get_combats_played_list(self):
        return self.combats

    def get_combats_played_number(self):
        return len(self.combats)

    def get_rounds_played_number(self):
        duel_rounds_played_number = 0
        self.combats.sort(key=lambda x: x.combat_order)
        for combat in self.combats:
            duel_rounds_played_number += combat.get_rounds_played_number()
        return duel_rounds_played_number

    def get_players_list(self):
        players_set = set()
        self.combats.sort(key=lambda x: x.combat_order)
        for combat in self.combats:
            for player in combat.get_players_list():
                players_set.add(player)
        return list(players_set)

    def get_players_number(self):
        return len(self.get_players_list())

    def get_characters_list(self):
        characters_set = set()
        self.combats.sort(key=lambda x: x.combat_order)
        for combat in self.combats:
            for character in combat.get_characters_list():
                characters_set.add(character)
        return list(characters_set)

    def get_characters_number(self):
        return len(self.get_characters_list())

    def get_teams_list(self):
        teams_set = set()
        self.combats.sort(key=lambda x: x.combat_order)
        for combat in self.combats:
            for team in combat.get_teams_list():
                teams_set.add(team)
        return list(teams_set)

    def get_teams_number(self): 
        return len(self.get_teams_list())

    def get_duel_type(self):
        duel_type = Modality.PLAYER.name
        if self.get_teams_number() != 0:
            duel_type = Modality.TEAM.name
        return duel_type

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

    def get_competitors():
        return

    def get_characters():
        return
    
    def get_duel_beating_factor(Competitor):
        return

    def get_duel_winner():
        return


class Combat(Base):
    __tablename__ = "combat"

    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    combat_order = Column(Integer, nullable=False)
    stage_id = Column(Integer, ForeignKey("stage.id"), nullable=False)
    duel_id = Column(Integer, ForeignKey("duel.id"), nullable=False)
    player1_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    player2_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    character1_id = Column(Integer, ForeignKey("character.id"), nullable=False)
    character2_id = Column(Integer, ForeignKey("character.id"), nullable=False)
    team1_id = Column(Integer, ForeignKey("team.id"), nullable=True)
    team2_id = Column(Integer, ForeignKey("team.id"), nullable=True)

    stage = relationship("Stage", back_populates="combats")
    duel = relationship("Duel", back_populates="combats")
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

    # Players
    def get_player1(self):
        return self.player1

    def get_player2(self):
        return self.player2

    def get_players_list(self):
        return [self.get_player1(), self.get_player2()]

    # Characters
    def get_character1(self):
        return self.character1

    def get_character2(self):
        return self.character2    

    def get_characters_list(self):
        return [self.get_character1(), self.get_character2()]

    # Teams
    def get_team1(self):
        return self.team1

    def get_team2(self):
        return self.team1

    def get_teams_list(self):
        return [self.get_team1(), self.get_team2()]

    # Ranking
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

    def get_rounds_lost_number(self):
        rounds_played_number = self.get_rounds_played_number()
        rounds_won_number_obj = self.get_rounds_won_number()
        rounds_lost_number_player1 = rounds_played_number - rounds_won_number_obj.player1
        rounds_lost_number_player2 = rounds_played_number - rounds_won_number_obj.player2
        return Scoreboard(rounds_lost_number_player1, rounds_lost_number_player2)

    def get_rounds_beating_factor(self):
        '''
        beating_factor = rounds_won / rounds_played
        '''
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

    def get_rounds_level_factor(self): # Pendiente de análisis
        return

    def get_combat_points_raw(self):
        points_p1 = 0
        points_p2 = 0
        self.rounds.sort(key=lambda x: x.round_order)
        for round in self.rounds:
            points_p1 += round.get_points_player1()
            points_p2 += round.get_points_player2()
        return Scoreboard(points_p1, points_p2)

    def get_combat_points_earned(self):
        combat_raw_points_obj = self.get_combat_points_raw()
        rounds_beating_factor_obj = self.get_rounds_beating_factor()
        combat_earned_points_player1 = combat_raw_points_obj.player1 * rounds_beating_factor_obj.player1
        combat_earned_points_player2 = combat_raw_points_obj.player2 * rounds_beating_factor_obj.player2
        return Scoreboard(combat_earned_points_player1, combat_earned_points_player2)


class Round(Base):
    __tablename__ = "round"

    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    round_order = Column(Integer, nullable=False)
    result_player1 = Column(String, nullable=False)
    result_player2 = Column(String, nullable=False)
    combat_id = Column(Integer, ForeignKey("combat.id"), nullable=False)

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


player_team = Table(
    "player_team",
    Base.metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("player_id", Integer, ForeignKey('player.id'), primary_key=True, nullable=False),
    Column("team_id", Integer, ForeignKey('team.id'), primary_key=True, nullable=False)
)


class Player(Base):
    __tablename__ = "player"

    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    playlist = Column(String, nullable=True)
    competitor_id = Column(Integer, ForeignKey("competitor.id"), nullable=False)

    combats_p1 = relationship("Combat", back_populates="player1", cascade="all, delete-orphan")
    combats_p2 = relationship("Combat", back_populates="player2", cascade="all, delete-orphan")
    players_characters = relationship("PlayerCharacter", back_populates="player", cascade="all, delete-orphan")
    social_medias = relationship("SocialMedia", back_populates="player", cascade="all, delete-orphan")
    competitor = relationship("Competitor", back_populates="player")
    teams = relationship('Team', secondary=player_team, back_populates='players')

    ''' Methods '''
    def get_events_played_list():
        return

    def get_event_position():
        return

    def get_events_played_number():
        return

    def get_duels_played_list():
        return

    def get_duels_played_number():
        return

    def get_duels_won_list():
        return

    def get_duels_won_number():
        return

    def get_duels_lost_list():
        return

    def get_duels_lost_number():
        return

    def get_team_duels_played_list():
        return

    def get_team_duels_played_number():
        return

    def get_team_duels_won_list():
        return

    def get_team_duels_won_number():
        return

    def get_team_duels_lost_list():
        return

    def get_team_duels_lost_number():
        return

    def get_combats_played_list():
        return

    def get_combats_played_number():
        return

    def get_combats_won_list():
        return

    def get_combats_won_number():
        return

    def get_combats_lost_list():
        return

    def get_combats_lost_number():
        return

    def get_combats_draw_list():
        return

    def get_combats_draw_number():
        return

    def get_rounds_played_number():
        return

    def get_rounds_won_number():
        return

    def get_rounds_lost_number():
        return

    def get_duels_win_rate():
        return

    def get_team_duels_win_rate():
        return

    def get_combats_win_rate():
        return

    def get_rounds_win_rate():
        return

    def get_duels_wlr():
        return

    def get_team_duels_wlr():
        return

    def get_combats_wlr():
        return

    def get_rounds_wlr():
        return

    def get_player_level():
        return


class Character(Base):
    __tablename__ = "character"

    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    playlist = Column(String, nullable=True)

    combats_p1 = relationship("Combat", back_populates="character1", cascade="all, delete-orphan")
    combats_p2 = relationship("Combat", back_populates="character2", cascade="all, delete-orphan")
    players_characters = relationship("PlayerCharacter", back_populates="character", cascade="all, delete-orphan")

    ''' Methods '''
    

class PlayerCharacter(Base):
    __tablename__ = "player_character"

    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    player_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    character_id = Column(Integer, ForeignKey("character.id"), nullable=False)

    player = relationship("Player", back_populates="players_characters")
    character = relationship("Character", back_populates="players_characters")


class Team(Base):
    __tablename__ = "team"

    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    competitor_id = Column(Integer, ForeignKey("competitor.id"), nullable=False)

    competitor = relationship("Competitor", back_populates="team")
    players = relationship('Player', secondary=player_team, back_populates='teams')
    combats_p1 = relationship("Combat", back_populates="team1", cascade="all, delete-orphan")
    combats_p2 = relationship("Combat", back_populates="team2", cascade="all, delete-orphan")


class Competitor(Base):
    __tablename__ = "competitor"

    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    player_id = Column(Integer, ForeignKey("player.id"), nullable=True)
    team_id = Column(Integer, ForeignKey("team.id"), nullable=True)
    country_id = Column(Integer, ForeignKey("country.id"), nullable=False)

    player = relationship("Competitor", back_populates="competitor")
    team = relationship("Competitor", back_populates="competitor")
    country = relationship("Country", back_populates="competitors")
    positions = relationship("Position", back_populates="competitor", cascade="all, delete-orphan")

    ''' Methods '''
    def get_competitor_type():
        return


class Position(Base):
    __tablename__ = "position"

    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    position = Column(Integer, nullable=False)
    event_id = Column(Integer, ForeignKey("event.id"), nullable=False)
    competitor_id = Column(Integer, ForeignKey("event.id"), nullable=False)

    event = relationship("Event", back_populates="positions")
    competitor = relationship("Competitor", back_populates="positions")



''' Schema generation '''

Base.metadata.create_all(ENGINE)