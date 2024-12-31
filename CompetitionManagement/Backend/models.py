from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    competitions = relationship('Competition', back_populates='creator')

class Competition(Base):
    __tablename__ = 'competitions'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    participants = relationship('Participant', back_populates='competition')
    matches = relationship('Match', back_populates='competition')
    creator = relationship('User', back_populates='competitions')

class Participant(Base):
    __tablename__ = 'participants'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    competition_id = Column(Integer, ForeignKey('competitions.id'), nullable=False)
    competition = relationship('Competition', back_populates='participants')

class Match(Base):
    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True)
    competition_id = Column(Integer, ForeignKey('competitions.id'), nullable=False)
    round = Column(Integer, nullable=False)
    team1_id = Column(Integer, ForeignKey('participants.id'), nullable=True)
    team2_id = Column(Integer, ForeignKey('participants.id'), nullable=True)
    winner_id = Column(Integer, ForeignKey('participants.id'), nullable=True)
    date = Column(DateTime, nullable=True)
    competition = relationship('Competition', back_populates='matches')
