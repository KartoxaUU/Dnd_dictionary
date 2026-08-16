from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_database import *

class DataManager:
    """Управляет данными в бд"""

    def __init__(self, db_path="assistant.db"):
        engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close(self):
        self.session.close()

    # Справочные данные

    def get_all_races(self):
        """Список всех рас"""
        return self.session.query(Race).all()

    def get_race_by_name(self, name):
        """Конкретная раса"""
        return self.session.query(Race).filter(Race.name == name).first()

    def get_all_classes(self):
        """Список всех классов"""
        return self.session.query(Class).all()

    def get_class_by_name(self, name):
        """Конкретный класс"""
        return self.session.query(Class).filter(Class.name == name).first()

    def get_all_backstories(self):
        """Список всех предысторий"""
        return self.session.query(Backstory).all()

    def get_backstory_by_name(self, name):
        """"""
        return self.session.query(Backstory).filter(Backstory.name == name).first()

    def get_all_subclasses_by_class(self, parent_class):
        return self.session.query(Subclass).filter(Subclass.parent_class == parent_class).all()

    def get_all_rules(self):
        return self.session.query(Rule).all()

    def get_rule_by_name(self, name):
        return self.session.query(Rule).filter(Rule.name == name).first()



