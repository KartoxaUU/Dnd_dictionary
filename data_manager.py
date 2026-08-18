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

    def get_race_abilities_by_race(self, race):
        """Способности расы"""
        return self.session.query(RacicalAbility).filter(RacicalAbility.race == race).all()

    def get_all_classes(self):
        """Список всех классов"""
        return self.session.query(Class).all()

    def get_class_by_name(self, name):
        """Конкретный класс"""
        return self.session.query(Class).filter(Class.name == name).first()

    def get_feature_by_class(self, parent_class):
        """Фича по классу"""
        return self.session.query(Feature).filter(Feature.parent_class == parent_class).all()

    def get_all_class_abilities_by_class(self, parent_class):
        """Все способности класса"""
        return self.session.query(Class.abilities).filter(Class.parent_class == parent_class).all()

    def get_all_backstories(self):
        """Список всех предысторий"""
        return self.session.query(Backstory).all()

    def get_backstory_by_name(self, name):
        """Конкретная предыстория"""
        return self.session.query(Backstory).filter(Backstory.name == name).first()

    def get_all_subclasses_by_class(self, parent_class):
        """Список всех подклассов класса"""
        return self.session.query(Subclass).filter(Subclass.parent_class == parent_class).all()

    def get_subclass_abilities_by_subclass(self, subclass):
        """Способности подкласса"""
        return self.session.query(SubclassAbility).filter(SubclassAbility.subclass == subclass).all()

    def get_all_rules(self):
        """Список всех правил"""
        return self.session.query(Rule).all()

    def get_rule_by_name(self, name):
        """Конкретное правило"""
        return self.session.query(Rule).filter(Rule.name == name).first()

    def get_all_spells(self):
        """Список всех заклинаний"""
        return self.session.query(Spell).all()

    def get_spell_by_name(self, name):
        """Конкретное заклинание"""
        return self.session.query(Spell).filter(Spell.name == name).first()

    def get_all_monsters(self):
        """Список всех мобов"""
        return self.session.query(Monster).all()

    def get_monster_by_name(self, name):
        """Конкретный моб"""
        return self.session.query(Monster).filter(Monster.name == name).first()

    def get_all_items(self):
        """Список всех предметов"""
        return self.session.query(Item).all()

    def get_item_by_name(self, name):
        """Конкретный предмет"""
        return self.session.query(Item).filter(Item.name == name).first()

    # Фильтры

    def filter_spells(self, **kwargs):
        """
                            Фильтрация заклинаний

        Параметры:
            search (str): поиск по имени или описанию
            levels (list): список уровней (OR) — выбор нескольких
            schools (list): список школ (OR) — выбор нескольких
            class_names (list): список классов (OR) — выбор нескольких
            subclass_names (list): список подклассов (OR) — выбор нескольких
            concentration (bool): концентрация (Да/Нет)
            ritual (bool): ритуал (Да/Нет)
            components (list): список компонентов (OR) — В, С, М
            is_custom (bool): кастомное/встроенное
            sort_by (str): поле для сортировки
        """

        query = self.session.query(Spell)

        if 'search' in kwargs and kwargs['search']:
            s = kwargs['search']
            query = query.filter(
                Spell.name.contains(s),
                        Spell.description.contains(s)
            )

        if 'levels' in kwargs and kwargs['levels']:
            query = query.filter(Spell.level.in_(kwargs['levels']))

        if 'schools' in kwargs and kwargs['schools']:
            query = query.filter(Spell.school.in_(kwargs['schools']))

        if 'class_names' in kwargs and kwargs['class_names']:
            query = query.filter(Spell.class_name.contains(kwargs['class_names']))

        if 'subclass_names' in kwargs and kwargs['subclass_names']:
            query = query.filter(Spell.subclass_name.contains(kwargs['subclass_names']))

        if 'concentration' in kwargs and kwargs['concentration']:
            query = query.filter(Spell.concentration == kwargs['concentration'])

        if 'ritual' in kwargs and kwargs['ritual']:
            query = query.filter(Spell.ritual == kwargs['ritual'])

        if 'components' in kwargs and kwargs['components']:
            for comp in kwargs['components']:
                query = query.filter(Spell.components.contains(comp))

        if 'is_custom' in kwargs and kwargs['is_custom']:
            query = query.filter(Spell.is_custom == kwargs['is_custom'])

        if 'sort_by' in kwargs and kwargs['sort_by']:
            if kwargs['sort_by'] == 'level':
                query = query.order_by(Spell.level.asc())
            elif kwargs['sort_by'] == 'name':
                query = query.order_by(Spell.name.asc())
            elif kwargs['sort_by'] == 'school':
                query = query.order_by(Spell.school.asc())
            elif hasattr(Spell, kwargs['sort_by']):
                query = query.order_by(getattr(Spell, kwargs['sort_by']))

        return query.all()




