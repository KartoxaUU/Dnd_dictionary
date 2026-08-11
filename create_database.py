import os
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, ForeignKey, Float
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import CheckConstraint

Base = declarative_base()

# Таблицы

class Race(Base):

    __tablename__ = 'races'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    stats_bonus = Column(String(40))
    age = Column(String(200))
    size = Column(String(20))
    speed = Column(Integer)
    description = Column(Text)
    image_path = Column(String(200))

    abilities = relationship("RacicalAbility", back_populates="race", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Race(name={self.name}"

class RacicalAbility(Base):

    __tablename__ = 'race_abilities'

    id = Column(Integer, primary_key=True)
    race_id = Column(Integer, ForeignKey('races.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(Text)

    race = relationship("Race", back_populates="abilities")

class Class(Base):

    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    hit_die = Column(Integer)
    possession_armor = Column(String(100))
    possession_weapon = Column(String(200))
    possesion_instruments = Column(String(200))
    possesion_savingthrows = Column(String(100))
    possesion_skills = Column(String(400))
    equipment_choice1 = Column(String(100))
    equipment_choice2 = Column(String(100))
    equipment_choice3 = Column(String(100))
    equipment_choice4 = Column(String(100))

    abilities = relationship("ClassAbility", back_populates="class", cascade="all, delete-orphan")
    subclasses = relationship("Subclass", back_populates="class", cascade="all, delete-orphan")
    features = relationship("Feature", back_populates="class", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Class(name={self.name}"

class ClassAbility(Base):

    __tablename__ = 'class_abilities'

    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey('classes.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    level = Column(Integer)

    parent_class = relationship("Class", back_populates="abilities")

    def __repr__(self):
        return f"ClassAbility(name={self.name})"

class Feature(Base):

    __tablename__ = 'features'

    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey('classes.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(50))
    description = Column(Text)
    level = Column(Integer)

    parent_class = relationship("Class", back_populates="features")

    def __repr__(self):
        return f"Feature(name={self.name})"

class Subclass(Base):

    __tablename__ = 'subclasses'

    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey('classes.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text)

    parent_class = relationship("Class", back_populates="subclasses")
    subclass_abilities = relationship("SubclassAbility", back_populates="subclass", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Subclass(name={self.name}"

class SubclassAbility(Base):

    __tablename__ = 'subclass_abilities'

    id = Column(Integer, primary_key=True)
    subclass_id = Column(Integer, ForeignKey('subclasses.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    level = Column(Integer)

    subclass = relationship("Subclass", back_populates="subclass_abilities")

    def __repr__(self):
        return f"SubclassAbility(name={self.name})"

class Backstory(Base):

    __tablename__ = 'backstories'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    possesion_skills = Column(String(100))
    possesion_instruments = Column(String(200))
    equipment = Column(String(200))
    skill = Column(Text)

