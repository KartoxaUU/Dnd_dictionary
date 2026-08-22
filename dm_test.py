# test_data_manager.py

from data_manager import DataManager


def print_section(title):
    """Печатает раздел"""
    print("\n" + "=" * 60)
    print(f"🧪 {title}")
    print("=" * 60)


def test_races(dm):
    """Тестирование работы с расами"""
    print_section("ТЕСТ РАС")

    # 1. Все расы
    races = dm.get_all_races()
    print(f"\n📚 Все расы ({len(races)} шт.):")
    for race in races:
        print(f"  • {race.name} (скорость: {race.speed}, способностей: {len(race.abilities)})")

    # 2. Конкретная раса
    race = dm.get_race_by_name("Человек")
    if race:
        print(f"\n✅ Найдена раса: {race.name}")
        print(f"   Бонусы: {race.stats_bonus}")
        print(f"   Языки: {race.languages}")

    # 3. Способности расы
    abilities = dm.get_race_abilities_by_race(race)
    if abilities:
        print(f"\n📜 Способности расы {race.name}:")
        for ability in abilities:
            print(f"  • {ability.name}")


def test_classes(dm):
    """Тестирование работы с классами"""
    print_section("ТЕСТ КЛАССОВ")

    # 1. Все классы
    classes = dm.get_all_classes()
    print(f"\n⚔️ Все классы ({len(classes)} шт.):")
    for cls in classes:
        print(f"  • {cls.name} (к{cls.hit_die})")

    # 2. Конкретный класс
    cls = dm.get_class_by_name("Воин")
    if cls:
        print(f"\n✅ Найден класс: {cls.name}")
        print(f"   Кость хитов: к{cls.hit_die}")
        print(f"   Спасброски: {cls.possession_savingthrows}")

    # 3. Способности класса
    abilities = dm.get_all_class_abilities_by_class(cls)
    if abilities:
        print(f"\n📜 Базовые способности {cls.name}:")
        for ability in abilities:
            print(f"  • [{ability.level} ур.] {ability.name}")

    # 4. Подклассы
    subclasses = dm.get_all_subclasses_by_class(cls)
    if subclasses:
        print(f"\n📂 Подклассы {cls.name}:")
        for subclass in subclasses:
            print(f"  • {subclass.name}")

            # Способности подкласса
            subclass_abilities = dm.get_subclass_abilities_by_subclass(subclass)
            for ability in subclass_abilities:
                print(f"    - [{ability.level} ур.] {ability.name}")


def test_items_crud(dm):
    """Тестирование CRUD предметов"""
    print_section("ТЕСТ CRUD ПРЕДМЕТОВ")

    # Удаляем старые тестовые предметы
    old_items = dm.filter_items(search="Тестовый")
    for item in old_items:
        try:
            dm.delete_item(item.id)
            print(f"   🗑️ Удалён старый тестовый предмет: {item.name}")
        except:
            pass

    # 1. Все предметы (до добавления)
    all_items = dm.get_all_items()
    print(f"\n🗡️ Всего предметов в БД: {len(all_items)}")

    # 2. Добавление предмета
    print("\n➕ Добавляем тестовый предмет...")
    new_item = dm.add_item(
        name="Тестовый меч",
        rarity="Необычный",
        description="Тестовый меч для проверки CRUD",
        is_magical=True,
        is_weapon=True
    )
    print(f"   ✅ Добавлен: {new_item.name} (ID: {new_item.id})")
    print(f"   🔓 Кастомный: {new_item.is_custom}")

    # 3. Поиск по имени (вместо get_item_by_id)
    found = dm.get_item_by_name("Тестовый меч")
    if found:
        print(f"\n🔍 Найден по имени: {found.name}")
        print(f"   Редкость: {found.rarity}")
        print(f"   Магический: {found.is_magical}")
        print(f"   Оружие: {found.is_weapon}")

    # 4. Обновление предмета (используем ID из объекта)
    print("\n✏️ Обновляем предмет...")
    dm.update_item(new_item.id, description="Обновлённое описание", rarity="Редкий")

    # Проверяем, что обновилось (ищем по имени)
    updated = dm.get_item_by_name("Тестовый меч")
    if updated:
        print(f"   ✅ Обновлено: {updated.description}")
        print(f"   ✅ Редкость изменена на: {updated.rarity}")

    # 5. Проверка, что обновилось
    all_items_after = dm.get_all_items()
    print(f"\n📊 Всего предметов после добавления: {len(all_items_after)}")

    # 6. Удаление предмета
    print("\n🗑️ Удаляем тестовый предмет...")
    dm.delete_item(new_item.id)
    print(f"   ✅ Предмет удалён")

    # 7. Проверка, что удалилось
    deleted = dm.get_item_by_name("Тестовый меч")
    if deleted is None:
        print("   ✅ Подтверждено: предмета больше нет в БД")

    # 8. Фильтрация предметов
    print("\n🔍 Фильтр: только магические предметы")
    magical_items = dm.filter_items(is_magical=True)
    print(f"   Найдено магических предметов: {len(magical_items)}")
    for item in magical_items[:5]:
        print(f"    • {item.name} ({item.rarity})")


def test_monsters_crud(dm):
    """Тестирование CRUD монстров"""
    print_section("ТЕСТ CRUD МОНСТРОВ")

    # Все монстры
    monsters = dm.get_all_monsters()
    print(f"\n👾 Всего монстров в БД: {len(monsters)}")
    for monster in monsters[:5]:
        print(f"  • {monster.name} (ХП: {monster.hits}, КД: {monster.armor_class})")

    # Добавление монстра
    print("\n➕ Добавляем тестового монстра...")
    new_monster = dm.add_monster(
        name="Тестовый дракон",
        hits="120 (12к10+24)",
        armor_class=18,
        speed="40 футов, полёт 80 футов",
        description="Тестовый дракон для проверки CRUD",
        size="Огромный",
        tipe="Дракон",
        danger="5",
        language="Драконий",
        strengh=22,
        endurance=18
    )
    print(f"   ✅ Добавлен: {new_monster.name} (ID: {new_monster.id})")
    print(f"   🔓 Кастомный: {new_monster.is_custom}")
    print(f"   Размер: {new_monster.size}")
    print(f"   Тип: {new_monster.tipe}")
    print(f"   Опасность: {new_monster.danger}")

    # Поиск по имени
    found = dm.get_monster_by_name("Тестовый дракон")
    if found:
        print(f"\n🔍 Найден по имени: {found.name}")
        print(f"   Хиты: {found.hits}")
        print(f"   КД: {found.armor_class}")
        print(f"   Сила: {found.strengh}")
        print(f"   Телосложение: {found.endurance}")

    # Обновление монстра
    print("\n✏️ Обновляем монстра...")
    dm.update_monster(
        new_monster.id,
        description="Обновлённое описание дракона",
        danger="6"
    )
    updated = dm.get_monster_by_name("Тестовый дракон")
    if updated:
        print(f"   ✅ Обновлено: {updated.description}")
        print(f"   ✅ Опасность изменена на: {updated.danger}")

    # Удаление монстра
    print("\n🗑️ Удаляем тестового монстра...")
    dm.delete_monster(new_monster.id)
    print(f"   ✅ Монстр удалён")

    # Проверка, что удалилось
    deleted = dm.get_monster_by_name("Тестовый дракон")
    if deleted is None:
        print("   ✅ Подтверждено: монстра больше нет в БД")


def test_filters(dm):
    """Тестирование фильтров"""
    print_section("ТЕСТ ФИЛЬТРОВ")

    # 1. Фильтр предметов
    print("\n🔍 Фильтр предметов (редкости):")
    items = dm.filter_items(rarities=["Легендарный", "Редкий"])
    print(f"   Найдено редких/легендарных предметов: {len(items)}")
    for item in items[:5]:
        print(f"    • {item.name} ({item.rarity})")

    # 2. Фильтр предметов (исключение)
    print("\n🔍 Фильтр предметов (исключить зелья):")
    items_no_potions = dm.filter_items(not_is_potion=True)
    print(f"   Найдено предметов (кроме зелий): {len(items_no_potions)}")

    # 3. Фильтр монстров
    print("\n🔍 Фильтр монстров (размеры):")
    monsters = dm.filter_monsters(sizes=["Большой", "Огромный"])
    print(f"   Найдено больших/огромных монстров: {len(monsters)}")
    for monster in monsters[:5]:
        print(f"    • {monster.name} ({monster.size})")

    # 4. Фильтр монстров (типы)
    print("\n🔍 Фильтр монстров (типы):")
    monsters = dm.filter_monsters(types=["Дракон", "Зверь"])
    print(f"   Найдено драконов и зверей: {len(monsters)}")
    for monster in monsters[:5]:
        print(f"    • {monster.name} ({monster.tipe})")

    # 5. Фильтр заклинаний
    print("\n🔍 Фильтр заклинаний (уровни):")
    spells = dm.filter_spells(levels=[1, 2, 3])
    print(f"   Найдено заклинаний 1-3 уровня: {len(spells)}")
    for spell in spells[:5]:
        print(f"    • {spell.name} ({spell.level} ур., {spell.school})")


def main():
    """Главная функция тестирования"""
    print("\n" + "=" * 60)
    print("🧪 ЗАПУСК ТЕСТОВ DataManager")
    print("=" * 60)

    try:
        # Создаём экземпляр DataManager
        dm = DataManager("assistant.db")
        print("\n✅ DataManager успешно создан")

        # Запускаем тесты
        test_races(dm)
        test_classes(dm)
        test_items_crud(dm)
        test_monsters_crud(dm)
        test_filters(dm)

        print_section("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО! 🎉")

    except Exception as e:
        print(f"\n❌ ОШИБКА В ТЕСТЕ: {e}")
        import traceback
        traceback.print_exc()

    finally:
        dm.close()
        print("\n🔒 Соединение с БД закрыто")


if __name__ == "__main__":
    main()