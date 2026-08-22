from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session
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
        return self.session.query(ClassAbility).filter(ClassAbility.parent_class == parent_class).all()

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
            query = query.join(Spell.classes).filter(Class.name.in_(kwargs['class_names']))

        if 'subclass_names' in kwargs and kwargs['subclass_names']:
            query = query.join(Spell.subclasses).filter(Subclass.name.in_(kwargs['subclass_names']))

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

    def filter_items(self, **kwargs):
        """
           Фильтрация предметов

            Параметры (включение):
                search (str): поиск
                rarities (list): список редкостей
                is_magical (bool): магический
                is_weapon (bool): оружие
                is_armor (bool): броня
                is_potion (bool): зелье
                is_wonderful_object (bool): чудесный предмет
                is_custom (bool): кастомный
                sort_by (str): сортировка

            Параметры (исключение):
                not_is_weapon (bool): исключить оружие
                not_is_armor (bool): исключить броню
                not_is_potion (bool): исключить зелья
                not_is_magical (bool): исключить магические
                not_is_wonderful_object (bool): исключить чудесные предметы
                not_is_custom (bool): исключить кастомные
        """

        query = self.session.query(Item)

        if 'search' in kwargs and kwargs['search']:
            s = kwargs['search']
            query = query.filter(
                Item.name.contains(s),
                Item.description.contains(s)
            )

        if 'rarities' in kwargs and kwargs['rarities']:
            query = query.filter(Item.rarity.in_(kwargs['rarities']))
        if 'is_magical' in kwargs and kwargs['is_magical']:
            query = query.filter(Item.is_magical == kwargs['is_magical'])
        if 'is_weapon' in kwargs and kwargs['is_weapon']:
            query = query.filter(Item.is_weapon == kwargs['is_weapon'])
        if 'is_armor' in kwargs and kwargs['is_armor']:
            query = query.filter(Item.is_armor == kwargs['is_armor'])
        if 'is_potion' in kwargs and kwargs['is_potion']:
            query = query.filter(Item.is_potion == kwargs['is_potion'])
        if 'is_wonderful_object' in kwargs and kwargs['is_wonderful_object']:
            query = query.filter(Item.is_wonderful_object == kwargs['is_wonderful_object'])
        if 'is_warrior' in kwargs and kwargs['is_warrior']:
            query = query.filter(Item.is_warrior == kwargs['is_warrior'])
        if 'is_custom' in kwargs and kwargs['is_custom']:
            query = query.filter(Item.is_custom == kwargs['is_custom'])

        if 'not_is_magical' in kwargs and kwargs['not_is_magical']:
            query = query.filter(Item.is_magical == False)
        if 'not_is_armor' in kwargs and kwargs['not_is_armor']:
            query = query.filter(Item.is_armor == False)
        if 'not_is_potion' in kwargs and kwargs['not_is_potion']:
            query = query.filter(Item.is_potion == False)
        if 'not_is_weapon' in kwargs and kwargs['not_is_weapon']:
            query = query.filter(Item.is_weapon == False)
        if 'not_is_wonderful_object' in kwargs and kwargs['not_is_wonderful_object']:
            query = query.filter(Item.is_wonderful_object == False)
        if 'not_is_custom' in kwargs and kwargs['not_is_custom']:
            query = query.filter(Item.is_custom == False)
        if 'not_is_warrior' in kwargs and kwargs['not_is_warrior']:
            query = query.filter(Item.is_warrior == False)

        if 'sort_by' in kwargs and kwargs['sort_by']:
            if kwargs['sort_by'] == 'name':
                query = query.order_by(Item.name.asc())
            if kwargs['sort_by'] == 'rarity':
                query = query.order_by(Item.rarity.asc())

        return query.all()

    def filter_monsters(self, **kwargs):
        """
           Фильтрация монстров

           Параметры:
               search (str): поиск по имени или описанию
               sizes (list): список размеров (OR) — выбор нескольких
               types (list): список типов (OR) — выбор нескольких
               dangers (list): список опасностей (OR) — выбор нескольких
               is_custom (bool): кастомный
        """

        query = self.session.query(Monster)

        if 'search' in kwargs and kwargs['search']:
            s = kwargs['search']
            query = query.filter(
                Monster.name.contains(s),
                Monster.description.contains(s)
            )

        if 'sizes' in kwargs and kwargs['sizes']:
            query = query.filter(Monster.size.in_(kwargs['sizes']))

        if 'types' in kwargs and kwargs['types']:
            query = query.filter(Monster.type.in_(kwargs['types']))

        if 'dangers' in kwargs and kwargs['dangers']:
            query = query.filter(Monster.danger.in_(kwargs['dangers']))

        if 'is_custom' in kwargs and kwargs['is_custom']:
            query = query.filter(Monster.is_custom == kwargs['is_custom'])

        return query.all()

    # CRUD

    def add_item(self, name, rarity, description, **kwargs):
        """Добавляет новый предмет"""
        item = Item(
            name=name,
            description=description,
            rarity=rarity,
            is_potion=kwargs.get('is_potion', False),
            is_magical=kwargs.get('is_magical', False),
            is_wonderful_object=kwargs.get('is_wonderful_object', False),
            is_custom=True,
            is_warrior=kwargs.get('is_warrior', False),
            is_armor=kwargs.get('is_armor', False),
            is_weapon=kwargs.get('is_weapon', False)
        )
        self.session.add(item)
        self.session.commit()
        return item

    def update_item(self, item_id, **kwargs):
        """Обновляет кастомный предмет"""
        item = self.session.query(Item).get(item_id)
        if not item:
            raise ValueError(f"Предмет с ID {item_id} не найден")
        if not item.is_custom:
            raise ValueError("Нельзя редактировать встроенный предмет")

        for key, value in kwargs.items():
            if hasattr(item, key):
                setattr(item, key, value)

        self.session.commit()
        return item

    def delete_item(self, item_id):
        """Удаляет кастомный предмет"""
        item = self.session.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise ValueError(f"Предмет с ID {item_id} не найден")
        if not item.is_custom:
            raise ValueError("Нельзя удалить встроенный предмет")

        self.session.delete(item)
        self.session.commit()

        return True

    def add_monster(self, name, hits, armor_class, speed, **kwargs):
        """Добавляет нового монстра (по умолчанию кастомный)"""
        monster = Monster(
            name=name,
            hits=hits,
            armor_class=armor_class,
            speed=speed,
            description=kwargs.get('description', ''),
            size=kwargs.get('size', 'Средний'),
            tipe=kwargs.get('tipe', 'Гуманоид'),
            strengh=kwargs.get('strengh', 10),
            agility=kwargs.get('agility', 10),
            endurance=kwargs.get('endurance', 10),
            wisdom=kwargs.get('wisdom', 10),
            intelligence=kwargs.get('intelligence', 10),
            charisma=kwargs.get('charisma', 10),
            savingthrows=kwargs.get('savingthrows', ''),
            skills=kwargs.get('skills', ''),
            resists=kwargs.get('resists', ''),
            immunity_damage=kwargs.get('immunity_damage', ''),
            immunity_status=kwargs.get('immunity_status', ''),
            feelings=kwargs.get('feelings', ''),
            language=kwargs.get('language', 'Общий'),
            danger=kwargs.get('danger', '1'),
            mastery_bonus=kwargs.get('mastery_bonus', 2),
            passive_skills=kwargs.get('passive_skills', ''),
            actions=kwargs.get('actions', ''),
            reaction=kwargs.get('reaction', ''),
            legendary_actions=kwargs.get('legendary_actions', ''),
            mythical_actions=kwargs.get('mythical_actions', ''),
            lair=kwargs.get('lair', ''),
            is_custom=True)

        self.session.add(monster)
        self.session.commit()
        return monster

    def update_monster(self, monster_id, **kwargs):
        """Обновляет кастомного монстра"""

        monster = self.session.query(Monster).get(monster_id)

        if not monster:
            raise ValueError(f"Монстра с ID {monster_id} не найдено")
        if not monster.is_custom:
            raise ValueError("Нельзя редактировать встроенного монстра")

        for key, value in kwargs.items():
            if hasattr(monster, key):
                setattr(monster, key, value)

        self.session.commit()
        return monster

    def delete_monster(self, monster_id):
        """Удаляет кастомного монстра"""

        monster = self.session.query(Monster).filter(Monster.id == monster_id).first()

        if not monster:
            raise ValueError(f"Монстра с ID {monster_id} не найдено")
        if not monster.is_custom:
            raise ValueError("Нельзя удалить встроенного монстра")

        self.session.delete(monster)
        self.session.commit()
        return True
