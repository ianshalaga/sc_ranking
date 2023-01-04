# from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
# from sqlalchemy.orm import declarative_base, relationship, Session

# db_engine = "sqlite"
# db_api = "pysqlite"
# db_path = "SSLEdb.db"
# engine = create_engine(f"{db_engine}+{db_api}:///{db_path}", echo=True, future=True)

# Base = declarative_base()


# ''' ClassTables '''

# class Game(Base):
#     __tablename__ = "game"

#     id = Column(Integer, primary_key=True, nullable=False)
#     name = Column(String, nullable=False)
#     code_name = Column(String, nullable=False)


# class Platfrom(Base):
#     __tablename__ = "platform"

#     id = Column(Integer, primary_key=True, nullable=False)
#     name = Column(String, nullable=False)
#     code_name = Column(String, nullable=False)


# class Region(Base):
#     __tablename__ = "region"

#     id = Column(Integer, primary_key=True, nullable=False)
#     name = Column(String, nullable=False)
#     code_name = Column(String, nullable=False)


# class EventType(Base):
#     __tablename__ = "event_type"

#     id = Column(Integer, primary_key=True, nullable=False)
#     name = Column(String, nullable=False)
#     code_name = Column(String, nullable=False)


# class DuelType(Base):
#     __tablename__ = "duel_type"

#     id = Column(Integer, primary_key=True, nullable=False)
#     name = Column(String, nullable=False)
#     code_name = Column(String, nullable=False)
#     name_synonymous = Column(String, nullable=False)
#     code_name_synonymous = Column(String, nullable=False)


# class Player(Base):
#     __tablename__ = "player"

#     id = Column(Integer, primary_key=True, nullable=False)
#     name = Column(String, nullable=False)
#     playlist = Column(String, nullable=True)


# class GameVersionPlatform(Base):
#     __tablename__ = "game_version_platform"

#     id = Column(Integer, primary_key=True, nullable=False)
#     version = Column(String, nullable=False)
#     game_id = Column(Integer, ForeignKey("game.id"), nullable=False)
#     platform_id = Column(Integer, ForeignKey("platform.id"), nullable=False)

#     game = relationship("Game")
#     platform = relationship("Platform")


# Base.metadata.create_all(engine)

from enum import Enum

class RoundResult(Enum):
    D = 240
    PW = 240
    W = 240
    WY = 168
    WB = 84
    LY = 168
    LB = 84
    PL = 0

variable = "WY"

print(RoundResult.D.name + "aasdasd")