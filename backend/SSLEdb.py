from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, or_, ForeignKey
from enum import Enum


''' Engine '''

DB_ENGINE = "sqlite"
DB_API = "pysqlite"
DB_PATH = "LÑdb.db"
ENGINE = create_engine(f"{DB_ENGINE}+{DB_API}:///{DB_PATH}", echo=True, future=True)
# STATUS_CODES_ERROR = [404, 500]

class RoundResult(Enum):
    D = 240
    PW = 240
    W = 240
    WY = 168
    WB = 84
    LY = 168
    LB = 84
    PL = 0


''' ClassTables '''

Base = declarative_base()

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
    region_id = Column(Integer, ForeignKey("region.id"), nullable=False)
    game_version_platform_id = Column(Integer, ForeignKey("game_version_platform.id"), nullable=False)

    event_type = relationship("EventType", back_populates="events")
    region = relationship("Region", back_populates="events")
    game_version_platform = relationship("GameVersionPlatform", back_populates="events")
    duels = relationship("Duel", back_populates="event", cascade="all, delete-orphan")

    ''' Methods '''
    def get_competitors():
        return

    def get_characters():
        return

    def get_duels_played():
        return
    
    def get_combats_played():
        return

    def get_rounds_played():
        return

    def get_rivals(Competitor):
        return

    def get_duels_won(Competitor):
        return

    def get_duels_lost(Competitor):
        return

    def get_duels_wlr(Competitor):
        return

    def get_duels_buchholz_wlr(Competitor):
        return

    def get_results():
        return

    
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

  
class Duel(Base):
    __tablename__ = "duel"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    duel_order = Column(Integer, nullable=False)
    video = Column(String, nullable=False)
    duel_type_id = Column(Integer, ForeignKey("duel_type.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("event.id"), nullable=False)

    ''' Methods '''
    def get_rounds_played():
        return

    def get_combats_played():
        return
    
    def get_competitors():
        return

    def get_characters():
        return
    
    def get_combats_won(Competitor):
        return

    def get_combats_lost(Competitor):
        return

    def get_duel_beating_factor(Competitor):
        return

    def get_duel_winner():
        return

    duel_type = relationship("DuelType", back_populates="duels")
    event = relationship("Event", back_populates="duels")
    combats = relationship("Combat", back_populates="duel", cascade="all, delete-orphan")


class DuelType(Base):
    __tablename__ = "duel_type"
    
    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    code_name = Column(String, nullable=False)
    name_synonymous = Column(String, nullable=False)
    code_name_synonymous = Column(String, nullable=False)

    duels = relationship("Duel", back_populates="duel_type", cascade="all, delete-orphan")


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

    stage = relationship("Stage", back_populates="combats")
    duel = relationship("Duel", back_populates="combats")
    player1 = relationship("Player", back_populates="combats_p1")
    player2 = relationship("Player", back_populates="combats_p2")
    character1 = relationship("Character", back_populates="combats_p1")
    character2 = relationship("Character", back_populates="combats_p2")
    rounds = relationship("Round", back_populates="combat", cascade="all, delete-orphan")

    ''' Methods '''
    def get_rounds_played():
        return


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


class Round(Base):
    __tablename__ = "round"

    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    round_order = Column(Integer, nullable=False)
    result_player1 = Column(String, nullable=False)
    result_player2 = Column(String, nullable=False)
    combat_id = Column(Integer, ForeignKey("combat.id"), nullable=False)

    combat = relationship("Combat", back_populates="rounds")


class Player(Base):
    __tablename__ = "player"

    ''' Attributes '''
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    playlist = Column(String, nullable=True)

    combats_p1 = relationship("Combat", back_populates="player1", cascade="all, delete-orphan")
    combats_p2 = relationship("Combat", back_populates="player2", cascade="all, delete-orphan")

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