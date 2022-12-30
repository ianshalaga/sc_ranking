from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, or_, ForeignKey


''' Engine '''

DB_ENGINE = "sqlite"
DB_API = "pysqlite"
DB_PATH = "LÑdb.db"
ENGINE = create_engine(f"{DB_ENGINE}+{DB_API}:///{DB_PATH}", echo=True, future=True)
# STATUS_CODES_ERROR = [404, 500]


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

    stage = relationship("Stage", back_populates="combats")

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