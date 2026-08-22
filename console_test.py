# console_app.py

import os
from data_manager import DataManager
from dm_test import print_section


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def parse_numbers(input_str):
    """Парсит ввод вида '1,2,3' или '1-3' в список"""
    if not input_str:
        return []

    input_str = input_str.replace(' ', '')
    result = []

    # Обработка диапазона: '1-3' → [1, 2, 3]
    if '-' in input_str:
        parts = input_str.split('-')
        if len(parts) == 2:
            start = int(parts[0]) if parts[0].isdigit() else 1
            end = int(parts[1]) if parts[1].isdigit() else start
            result = list(range(start, end + 1))
        return result

    # Обработка списка: '1,2,3' → [1, 2, 3]
    for part in input_str.split(','):
        if part.isdigit():
            result.append(int(part))

    return result


def select_multiple(options, title="Выберите опции (через запятую, например: 1,3,5):"):
    """Универсальная функция для множественного выбора"""
    print(f"\n   {title}")
    for i, opt in enumerate(options, 1):
        print(f"     {i}. {opt}")

    choice = input("   Ваш выбор: ")
    numbers = parse_numbers(choice)

    if not numbers:
        return []

    selected = []
    for num in numbers:
        if 1 <= num <= len(options):
            selected.append(options[num - 1])

    return selected


def get_rarities():
    """Выбор нескольких редкостей"""
    rarities = ["Обычный", "Необычный", "Редкий", "Очень редкий", "Легендарный"]
    return select_multiple(rarities, "Выберите редкости (через запятую, например: 1,3,5):")


def get_levels():
    """Выбор нескольких уровней заклинаний"""
    levels = ["Заговор (0)", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    selected = select_multiple(levels, "Выберите уровни (через запятую, например: 1,3,5):")
    return [0 if l == "Заговор (0)" else int(l) for l in selected]


def get_schools():
    """Выбор нескольких школ магии"""
    schools = [
        "Воплощение", "Ограждение", "Иллюзия", "Некромантия",
        "Преобразование", "Очарование", "Прорицание", "Вызов"
    ]
    return select_multiple(schools, "Выберите школы магии (через запятую, например: 1,3,5):")


def get_sizes():
    """Выбор нескольких размеров монстров"""
    sizes = ["Маленький", "Средний", "Большой", "Огромный", "Громадный"]
    return select_multiple(sizes, "Выберите размеры (через запятую, например: 1,3,5):")


def get_types():
    """Выбор нескольких типов монстров"""
    types = [
        "Гуманоид", "Зверь", "Дракон", "Нежить", "Исчадие",
        "Фея", "Великан", "Чудовище", "Растение", "Конструкт", "Элементаль"
    ]
    return select_multiple(types, "Выберите типы (через запятую, например: 1,3,5):")


def get_dangers():
    """Выбор нескольких опасностей монстров"""
    dangers = ["0", "1/8", "1/4", "1/2", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    return select_multiple(dangers, "Выберите опасности (через запятую, например: 1,3,5):")


def get_components():
    """Выбор нескольких компонентов заклинаний"""
    components = ["Вербальный (В)", "Соматический (С)", "Материальный (М)"]
    selected = select_multiple(components, "Выберите компоненты (через запятую, например: 1,3):")
    mapping = {"Вербальный (В)": "В", "Соматический (С)": "С", "Материальный (М)": "М"}
    return [mapping[c] for c in selected]


def main():
    dm = DataManager()

    while True:
        clear_screen()
        print("=" * 60)
        print("📚 D&D ASSISTANT — КОНСОЛЬНЫЙ РЕЖИМ")
        print("=" * 60)
        print("  📖 ПРОСМОТР")
        print("   1. Показать все расы")
        print("   2. Показать все классы")
        print("   3. Показать все предметы")
        print("   4. Показать всех монстров")
        print("   5. Показать все заклинания")
        print()
        print("  🔍 ФИЛЬТРЫ (с множественным выбором)")
        print("   6. Фильтр предметов")
        print("   7. Фильтр монстров")
        print("   8. Фильтр заклинаний")
        print()
        print("  ➕ ДОБАВЛЕНИЕ")
        print("   9. Добавить предмет")
        print("  10. Добавить монстра")
        print()
        print("  ✏️ ОБНОВЛЕНИЕ")
        print("  11. Обновить предмет")
        print("  12. Обновить монстра")
        print()
        print("  🗑️ УДАЛЕНИЕ")
        print("  13. Удалить предмет")
        print("  14. Удалить монстра")
        print()
        print("  0. Выход")
        print("=" * 60)

        choice = input("\n👉 Выберите действие: ")

        # ============================================================
        # ПРОСМОТР
        # ============================================================

        if choice == "1":
            races = dm.get_all_races()
            print_section("РАСЫ")
            for race in races:
                print(f"  • {race.name} (скорость: {race.speed})")
            input("\nНажмите Enter для продолжения...")

        elif choice == "2":
            classes = dm.get_all_classes()
            print_section("КЛАССЫ")
            for cls in classes:
                print(f"  • {cls.name} (к{cls.hit_die})")
            input("\nНажмите Enter для продолжения...")

        elif choice == "3":
            items = dm.get_all_items()
            print_section("ПРЕДМЕТЫ")
            for item in items:
                custom = "🔓" if item.is_custom else "🔒"
                print(f"  {custom} {item.name} ({item.rarity})")
            input("\nНажмите Enter для продолжения...")

        elif choice == "4":
            monsters = dm.get_all_monsters()
            print_section("МОНСТРЫ")
            for monster in monsters:
                custom = "🔓" if monster.is_custom else "🔒"
                print(f"  {custom} {monster.name} (КД: {monster.armor_class}, Опасность: {monster.danger})")
            input("\nНажмите Enter для продолжения...")

        elif choice == "5":
            spells = dm.get_all_spells()
            print_section("ЗАКЛИНАНИЯ")
            for spell in spells[:10]:
                ritual = "🔮" if spell.ritual else ""
                conc = "⚡" if spell.concentration else ""
                print(f"  {ritual}{conc} {spell.name} ({spell.level} ур., {spell.school})")
            if len(spells) > 10:
                print(f"  ... и ещё {len(spells) - 10} заклинаний")
            input("\nНажмите Enter для продолжения...")

        # ============================================================
        # ФИЛЬТРЫ (с множественным выбором)
        # ============================================================

        elif choice == "6":

            print_section("ФИЛЬТР ПРЕДМЕТОВ")

            filters = {}

            # Редкости (множественный выбор)

            rarities = get_rarities()

            if rarities:
                filters['rarities'] = rarities

            # Булевы фильтры

            print("\n   Дополнительные фильтры (y/n):")

            for filter_name, filter_key in [

                ("Магические", "is_magical"),
                ("Оружие", "is_weapon"),
                ("Броня", "is_armor"),
                ("Зелья", "is_potion"),
                ("Чудесные", "is_wonderful_object"),
                ("Воинские", "is_warrior"),
                ("Кастомные", "is_custom")

            ]:

                val = input(f"   {filter_name}? (y/n): ").lower()

                if val in ('y', 'yes', 'да'):
                    filters[filter_key] = True
                elif val in ('n', 'no', 'нет'):
                    filters[filter_key] = False

            # Исключения

            print("\n   Исключить (y/n):")

            for filter_name, filter_key in [

                ("Оружие", "not_is_weapon"),
                ("Броню", "not_is_armor"),
                ("Зелья", "not_is_potion"),
                ("Магические", "not_is_magical"),
                ("Чудесные", "not_is_wonderful_object"),
                ("Воинские", "not_is_warrior"),
                ("Кастомные", "not_is_custom")

            ]:

                val = input(f"   Исключить {filter_name}? (y/n): ").lower()
                if val in ('y', 'yes', 'да'):
                    filters[filter_key] = True

            # Поиск по названию

            search = input("\n   Поиск по названию (Enter для пропуска): ")

            if search:
                filters['search'] = search

            # Сортировка

            print("\n   Сортировка:")
            print("     1. По названию")
            print("     2. По редкости")

            sort_choice = input("   Выберите (или Enter для пропуска): ")

            if sort_choice == "1":
                filters['sort_by'] = 'name'
            elif sort_choice == "2":
                filters['sort_by'] = 'rarity'

            items = dm.filter_items(**filters)

            if items:
                print_section("РЕЗУЛЬТАТЫ")
                for item in items:
                    custom = "🔓" if item.is_custom else "🔒"
                    warrior = "⚔️" if item.is_warrior else ""
                    print(f"  {custom}{warrior} {item.name} ({item.rarity})")

            else:

                print("\n  ⚠️ Ничего не найдено")

            input("\nНажмите Enter для продолжения...")

        elif choice == "7":
            print_section("ФИЛЬТР МОНСТРОВ")

            filters = {}

            # Размеры (множественный выбор)
            sizes = get_sizes()
            if sizes:
                filters['sizes'] = sizes

            # Типы (множественный выбор)
            types = get_types()
            if types:
                filters['types'] = types

            # Опасности (множественный выбор)
            dangers = get_dangers()
            if dangers:
                filters['dangers'] = dangers

            # Кастомные
            custom = input("\n   Только кастомные? (y/n): ").lower()
            if custom in ('y', 'yes', 'да'):
                filters['is_custom'] = True
            elif custom in ('n', 'no', 'нет'):
                filters['is_custom'] = False

            # Поиск по названию
            search = input("\n   Поиск по названию (Enter для пропуска): ")
            if search:
                filters['search'] = search

            # Сортировка
            print("\n   Сортировка:")
            print("     1. По названию")
            print("     2. По опасности")
            print("     3. По размеру")
            sort_choice = input("   Выберите (или Enter для пропуска): ")
            if sort_choice == "1":
                filters['sort_by'] = 'name'
            elif sort_choice == "2":
                filters['sort_by'] = 'danger'
            elif sort_choice == "3":
                filters['sort_by'] = 'size'

            monsters = dm.filter_monsters(**filters)

            if monsters:
                print_section("РЕЗУЛЬТАТЫ")
                for monster in monsters:
                    custom = "🔓" if monster.is_custom else "🔒"
                    print(f"  {custom} {monster.name} ({monster.tipe}, Опасность: {monster.danger})")
            else:
                print("\n  ⚠️ Ничего не найдено")
            input("\nНажмите Enter для продолжения...")

        elif choice == "8":
            print_section("ФИЛЬТР ЗАКЛИНАНИЙ")

            filters = {}

            # Уровни (множественный выбор)
            levels = get_levels()
            if levels:
                filters['levels'] = levels

            # Школы (множественный выбор)
            schools = get_schools()
            if schools:
                filters['schools'] = schools

            # Компоненты (множественный выбор)
            components = get_components()
            if components:
                filters['components'] = components

            # Концентрация
            print("\n   Фильтры (y/n):")
            for filter_name, filter_key in [
                ("С концентрацией", "concentration"),
                ("Ритуал", "ritual"),
                ("Только кастомные", "is_custom")
            ]:
                val = input(f"   {filter_name}? (y/n): ").lower()
                if val in ('y', 'yes', 'да'):
                    filters[filter_key] = True
                elif val in ('n', 'no', 'нет'):
                    filters[filter_key] = False

            # Поиск по названию
            search = input("\n   Поиск по названию (Enter для пропуска): ")
            if search:
                filters['search'] = search

            # Сортировка
            print("\n   Сортировка:")
            print("     1. По уровню")
            print("     2. По названию")
            print("     3. По школе")
            sort_choice = input("   Выберите (или Enter для пропуска): ")
            if sort_choice == "1":
                filters['sort_by'] = 'level'
            elif sort_choice == "2":
                filters['sort_by'] = 'name'
            elif sort_choice == "3":
                filters['sort_by'] = 'school'

            spells = dm.filter_spells(**filters)

            if spells:
                print_section("РЕЗУЛЬТАТЫ")
                for spell in spells:
                    ritual = "🔮" if spell.ritual else ""
                    conc = "⚡" if spell.concentration else ""
                    print(f"  {ritual}{conc} {spell.name} ({spell.level} ур., {spell.school})")
            else:
                print("\n  ⚠️ Ничего не найдено")
            input("\nНажмите Enter для продолжения...")

        # ============================================================
        # ДОБАВЛЕНИЕ
        # ============================================================

        elif choice == "9":

            print_section("ДОБАВЛЕНИЕ ПРЕДМЕТА")

            name = input("Название: ")
            rarity = input("Редкость (Обычный/Необычный/Редкий/Легендарный): ")
            description = input("Описание: ")
            is_magical = input("Магический? (y/n): ").lower() == 'y'
            is_weapon = input("Оружие? (y/n): ").lower() == 'y'
            is_armor = input("Броня? (y/n): ").lower() == 'y'
            is_potion = input("Зелье? (y/n): ").lower() == 'y'
            is_wonderful = input("Чудесный предмет? (y/n): ").lower() == 'y'
            is_warrior = input("Воинский предмет? (y/n): ").lower() == 'y'  # ← ДОБАВЛЕНО

            dm.add_item(

                name=name,
                rarity=rarity,
                description=description,
                is_magical=is_magical,
                is_weapon=is_weapon,
                is_armor=is_armor,
                is_potion=is_potion,
                is_wonderful_object=is_wonderful,
                is_warrior=is_warrior  # ← ДОБАВЛЕНО

            )

            print(f"\n✅ Предмет '{name}' добавлен!")

            input("\nНажмите Enter для продолжения...")

        elif choice == "10":
            print_section("ДОБАВЛЕНИЕ МОНСТРА")
            name = input("Название: ")
            hits = input("Хиты (например: 13 (3к6+3)): ")
            armor_class = int(input("КД: "))
            speed = input("Скорость: ")
            description = input("Описание: ")
            size = input("Размер (Средний/Большой/Огромный): ") or "Средний"
            tipe = input("Тип (Гуманоид/Дракон/Зверь...): ") or "Гуманоид"
            danger = input("Опасность (1/4, 1, 2...): ") or "1"

            dm.add_monster(
                name=name,
                hits=hits,
                armor_class=armor_class,
                speed=speed,
                description=description,
                size=size,
                tipe=tipe,
                danger=danger
            )
            print(f"\n✅ Монстр '{name}' добавлен!")
            input("\nНажмите Enter для продолжения...")

        # ============================================================
        # ОБНОВЛЕНИЕ
        # ============================================================

        elif choice == "11":

            print_section("ОБНОВЛЕНИЕ ПРЕДМЕТА")

            name = input("Введите название предмета для обновления: ")

            item = dm.get_item_by_name(name)

            if not item:
                print(f"\n❌ Предмет '{name}' не найден")

                input("\nНажмите Enter для продолжения...")

                continue

            if not item.is_custom:
                print(f"\n❌ Предмет '{name}' встроенный (нельзя редактировать)")

                input("\nНажмите Enter для продолжения...")

                continue

            print(f"\n📋 Текущие данные: {item.name} ({item.rarity})")
            print("   Оставьте поле пустым, чтобы не менять")
            new_name = input(f"Новое название [{item.name}]: ") or item.name
            new_rarity = input(f"Новая редкость [{item.rarity}]: ") or item.rarity
            new_description = input(f"Новое описание [{item.description[:50]}...]: ") or item.description
            current_warrior = "Да" if item.is_warrior else "Нет"
            warrior_input = input(f"Воинский предмет? [{current_warrior}] (y/n): ").lower()

            if warrior_input in ('y', 'yes', 'да'):
                new_warrior = True

            elif warrior_input in ('n', 'no', 'нет'):
                new_warrior = False

            else:
                new_warrior = item.is_warrior

            dm.update_item(

                item.id,

                name=new_name,
                rarity=new_rarity,
                description=new_description,
                is_warrior=new_warrior

            )

            print(f"\n✅ Предмет обновлён!")
            input("\nНажмите Enter для продолжения...")

        elif choice == "12":
            print_section("ОБНОВЛЕНИЕ МОНСТРА")
            name = input("Введите название монстра для обновления: ")
            monster = dm.get_monster_by_name(name)

            if not monster:
                print(f"\n❌ Монстр '{name}' не найден")
                input("\nНажмите Enter для продолжения...")
                continue

            if not monster.is_custom:
                print(f"\n❌ Монстр '{name}' встроенный (нельзя редактировать)")
                input("\nНажмите Enter для продолжения...")
                continue

            print(f"\n📋 Текущие данные: {monster.name} (Опасность: {monster.danger})")
            print("   Оставьте поле пустым, чтобы не менять")

            new_name = input(f"Новое название [{monster.name}]: ") or monster.name
            new_hits = input(f"Новые хиты [{monster.hits}]: ") or monster.hits
            new_description = input(f"Новое описание [{monster.description[:50]}...]: ") or monster.description
            new_danger = input(f"Новая опасность [{monster.danger}]: ") or monster.danger

            dm.update_monster(
                monster.id,
                name=new_name,
                hits=new_hits,
                description=new_description,
                danger=new_danger
            )
            print(f"\n✅ Монстр обновлён!")
            input("\nНажмите Enter для продолжения...")

        # ============================================================
        # УДАЛЕНИЕ
        # ============================================================

        elif choice == "13":
            print_section("УДАЛЕНИЕ ПРЕДМЕТА")
            name = input("Введите название предмета для удаления: ")
            item = dm.get_item_by_name(name)

            if not item:
                print(f"\n❌ Предмет '{name}' не найден")
                input("\nНажмите Enter для продолжения...")
                continue

            if not item.is_custom:
                print(f"\n❌ Предмет '{name}' встроенный (нельзя удалить)")
                input("\nНажмите Enter для продолжения...")
                continue

            confirm = input(f"\n⚠️ Удалить предмет '{name}'? (y/n): ")
            if confirm.lower() == 'y':
                dm.delete_item(item.id)
                print(f"\n✅ Предмет '{name}' удалён!")
            else:
                print("\n❌ Отменено")

            input("\nНажмите Enter для продолжения...")

        elif choice == "14":
            print_section("УДАЛЕНИЕ МОНСТРА")
            name = input("Введите название монстра для удаления: ")
            monster = dm.get_monster_by_name(name)

            if not monster:
                print(f"\n❌ Монстр '{name}' не найден")
                input("\nНажмите Enter для продолжения...")
                continue

            if not monster.is_custom:
                print(f"\n❌ Монстр '{name}' встроенный (нельзя удалить)")
                input("\nНажмите Enter для продолжения...")
                continue

            confirm = input(f"\n⚠️ Удалить монстра '{name}'? (y/n): ")
            if confirm.lower() == 'y':
                dm.delete_monster(monster.id)
                print(f"\n✅ Монстр '{name}' удалён!")
            else:
                print("\n❌ Отменено")

            input("\nНажмите Enter для продолжения...")

        # ============================================================
        # ВЫХОД
        # ============================================================

        elif choice == "0":
            print("\n👋 До свидания!")
            break

        else:
            print("\n❌ Неверный выбор!")
            input("\nНажмите Enter для продолжения...")

    dm.close()


if __name__ == "__main__":
    main()