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
    languages = Column(String(100))
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

    abilities = relationship("ClassAbility", back_populates="parent_class", cascade="all, delete-orphan")
    subclasses = relationship("Subclass", back_populates="parent_class", cascade="all, delete-orphan")
    features = relationship("Feature", back_populates="parent_class", cascade="all, delete-orphan")

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

class Item(Base):

    # Предметы

    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    rarity = Column(String(50), nullable=False)
    is_magical = Column(Boolean)
    is_weapon = Column(Boolean)
    configuration = Column(Boolean)
    is_armor = Column(Boolean)
    is_potion = Column(Boolean)
    is_wonderful_object = Column(Boolean)
    description = Column(Text)

class Monster(Base):

    # Мобы

    __tablename__ = 'monsters'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    hits = Column(Integer)
    armor_class = Column(Integer)
    speed = Column(Integer)
    stats = Column(String(60))
    feelings = Column(String(100))
    language = Column(String(200))
    danger = Column(Integer)
    mastery_bonus = Column(Integer)
    passive_skills = Column(Text)
    actions = Column(Text)
    reaction = Column(Text)
    legendary_actions = Column(Text)
    mythical_actions = Column(Text)
    lair = Column(Text)
    description = Column(Text)

class Rule(Base):

    # Правила

    __tablename__ = 'rules'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text)

# Создание бд

def create_database(db_path="assistant.db"):
    """Создание бд с таблицами"""

    if os.path.exists(db_path):
        os.remove(db_path)
        print("Старая бд удалена")

    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    Base.metadata.create_all(engine)
    print(f"Таблицы созданы в {db_path}")

    return engine

if __name__ == "__main__":
    #Создаем БД
    engine = create_database()

    #Создаем сессию для добавления данных
    Session = sessionmaker(bind=engine)
    session = Session()

    print("Добавляем текстовые данные")

    human = Race(
        name="Человек",
        stats_bonus="Значение всех характеристик увеличивается на 1",
        age="Становятся взрослыми в районе 20, не доживают до 100",
        size="От 5 до 6 футов. Размер - Средний",
        speed=30,
        languages="Общий + 1 на выбор",
        description="""Общая характеристика
Люди — самая многочисленная и политически влиятельная раса на большинстве континентов. Их главная отличительная черта — поразительная приспособляемость и неугасимое стремление к самосовершенствованию. Короткий по меркам других народов срок жизни (редко превышающий столетие) наделяет людей жгучей страстью к жизни и желанием оставить ощутимый след в истории.
Культура и общество
Люди не образуют единой цивилизации — их культура распадается на тысячи королевств, республик, кочевых племён и вольных городов. Они перенимают обычаи соседних рас, переосмысляют чужие изобретения и создают синкретические традиции. Именно люди чаще других основывают авантюристские гильдии, магические академии и торговые компании. Их общество подвижно: сословия не столь жестки, как у дварфов, а законы могут меняться под влиянием сильных личностей.
Мировоззрение и характер
Среди людей встречаются как величайшие герои, так и жесточайшие тираны. Их мировоззрение крайне вариативно: они могут быть образцом законности или воплощением хаоса, альтруизма или эгоизма. Амбициозность и жажда познания толкают их в самые опасные уголки мира. Люди не довольствуются настоящим — они постоянно строят планы, завоевывают земли, исследуют забытые руины и пишут трактаты.
Место в мире
Люди составляют ядро большинства межрасовых союзов и являются главными торговыми партнёрами для эльфов, гномов и полуросликов. Благодаря своей дипломатичности и прагматизму они часто выступают посредниками в конфликтах между древними расами. Их города — это шумные центры, где можно встретить представителей любого народа, а их корабли бороздят все известные моря.""")

    session.add(human)

    tiefling = Race(
        name="Тифлинг",
        stats_bonus="Увеличение Харизмы на 2 и Интеллекта на 1",
        age="Взрослеют с той же скоростью, что и люди, но живут несколько дольше — до 120–150 лет",
        size="От 5 до 6 футов. Размер - Средний",
        speed=30,
        languages="Общий + Инфернальный",
        description="""Общая характеристика
Тифлинги — раса, несущая на себе печать пламенных глубин Нижних планов. Их внешность выдаёт дьявольское наследие: рога, хвосты, глаза без зрачков, кожа красных, пурпурных или пепельных оттенков. Однако тифлинги не являются злыми по своей природе — они существа, вынужденные бороться с чужими предрассудками и собственной тёмной кровью. Их магический потенциал и стойкость перед лицом ненависти делают их выдающимися личностями.
Культура и общество
Тифлинги не имеют собственных королевств или государств — они рождаются среди других народов, чаще всего людей, и вынуждены искать своё место в чужом мире. Многие из них становятся изгоями, скитальцами или одиночками, но некоторые создают тайные общества, помогающие себе подобным. Тифлинги склонны к индивидуализму и самодостаточности, их культура — это культура выживания и адаптации. Они часто обращаются к магии, дипломатии или теневой деятельности, чтобы добиться власти или защиты.
Мировоззрение и характер
Тифлинги редко бывают равнодушными — их характер окрашен страстью, цинизмом или бунтарством. Среди них встречаются как аскеты, отвергающие своё наследие, так и те, кто сознательно принимает тёмную силу. Их мировоззрение колеблется от хаотично-доброго до законно-злого, но предрассудки окружающих часто толкают их к краю. Тифлинги ценят свободу, справедливость (по их собственному разумению) и личную силу. Многие из них становятся бардами, колдунами, чернокнижниками или плутами.
Место в мире
Тифлинги — это маргиналы и исключения в большинстве человеческих обществ. Их терпят, но редко принимают, используют их таланты, но боятся их происхождения. Тем не менее в крупных мегаполисах, где смешиваются расы и культуры, тифлинги могут находить уважение и признание. Они частые гости в портовых городах, торговых гильдиях и магических университетах — везде, где ценят знания и умение договариваться. В мире, где дьяволы — реальная угроза, каждый тифлинг несёт на себе бремя доказательства, что он не чудовище, а человек (или почти человек) с правом на свой путь."""
    )

    tiefling.abilities = [
    RacicalAbility(
        name="Темное зрение",
        description = "На расстоянии в 60 футов вы при тусклом освещении можете видеть так, как будто это яркое освещение, и в темноте так, как будто это тусклое освещение. В темноте вы не можете различать цвета, только оттенки серого.",
        ),
    RacicalAbility(
        name="Адское сопротивление",
        description = "Вы получаете сопротивление урону огнём"
        ),
    RacicalAbility(
        name = "Дьявольское наследие",
        description = "Начиная с 3-го уровня, вы можете один раз наложить заклинание адское возмездие [hellish rebuke] как заклинание 2-го уровня с помощью этой особенности. Начиная с 5-го уровня, вы также можете накладывать заклинание тьма [darkness] с помощью этой особенности. После накладывания одного из этих заклинаний с помощью особенности вы должны закончить продолжительный отдых, прежде чем сможете вновь наложить это заклинание таким образом. Кроме того, вы знаете заговор чудотворство [thaumaturgy]. Базовой характеристикой заклинаний для этих заклинаний является Харизма."
        )]

    session.add(tiefling)

    session.commit()

    print("Данные добавлены")

    print("Проверка данных")

    races = session.query(Race).all()

    print(f"\nВсе расы в БД ({len(races)} шт.):")
    for race in races:
        print(f"\n   {race.name}")
        print(f"     Бонус характеристик: {race.stats_bonus}")
        print(f"     Скорость: {race.speed} футов")
        print(f"     Языки: {race.languages}")
        print(f"     {race.description}")
        print(f"     Способностей: {len(race.abilities)}")
        for ability in race.abilities:
            print(f"       - {ability.name}")

    print("\n Только тифлинг \n")

    tiefling = session.query(Race).filter_by(name="Тифлинг").first()

    if tiefling:
        print(f"\nИмя: {tiefling.name}")
        print(f"Бонус характеристик: {tiefling.stats_bonus}")
        print(f"Скорость: {tiefling.speed} футов")
        print(f"Языки: {tiefling.languages}")
        print(f"\nСпособности Тифлинга:")
        for ability in tiefling.abilities:
            print(f"{ability.name}")
            print(f"{ability.description}")
        print(f"{tiefling.description}")

    session.close()
    print("Проверка завершена!")




