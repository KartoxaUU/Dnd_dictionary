from Data.Windows.base_window import BasePage
from PySide6.QtWidgets import QMessageBox, QListWidgetItem
from PySide6.QtCore import Qt


class SpellsPage(BasePage):
    """Страница с заклинаниями"""

    def __init__(self, parent=None, go_back_callback=None):
        super().__init__("Data/Screens/spells.ui", parent)
        self.go_back_callback = go_back_callback
        self.all_spells = []

        self.setup_ui()
        self.setup_filters()
        self.load_spells()

    def setup_ui(self):
        """Подключаем кнопки"""

        if not self.ui:
            return

        if hasattr(self.ui, 'btn_back'):
            btn = getattr(self.ui, 'btn_back')
            btn.clicked.connect(self.go_back)
            print("Подключена кнопка: btn_back")

        if hasattr(self.ui, 'btn_filters'):
            self.ui.btn_filters.clicked.connect(self.toggle_filters)

        if hasattr(self.ui, 'search_input'):
            self.ui.search_input.textChanged.connect(self.apply_filters)

        if hasattr(self.ui, 'listWidget'):
            self.ui.listWidget.itemClicked.connect(self.on_spell_selected)
            print("Подключена кнопка: listWidget")

        if hasattr(self.ui, 'Spell_name'):
            self.ui.Spell_name.setTextFormat(Qt.RichText)
            print("Найден лейбл: Spell_name")

        if hasattr(self.ui, 'Spell_description'):
            self.ui.Spell_name.setTextFormat(Qt.RichText)
            print("Найден лейбл: Spell_description")

        if hasattr(self.ui, 'filters'):
            print("Найден фрейм: filters")
            self.ui.filters.setVisible(False)

        if hasattr(self.ui, 'frame_filters'):
            print("Найден фрейм: frame_filters")
            self.ui.frame_filters.setVisible(False)


    def load_spells(self):
        """Загружает список заклинаний"""

        if not hasattr(self.ui, 'listWidget'):
            print("listWidget не найден")
            return

        self.ui.listWidget.clear()

        self.all_spells = self.dm.get_all_spells()

        if not self.all_spells:
            item = QListWidgetItem("Тут пусто:(")
            item.setData(Qt.UserRole, None)
            self.ui.listWidget.addItem(item)
            return

        self.display_spells(self.all_spells)
        print(f"Загружено заклинаний: {len(self.all_spells)}")

    def collect_filters(self):
        """Собирает все активные фильтры в словарь"""
        filters = {}


        # ===== УРОВЕНЬ =====
        if hasattr(self.ui, 'comboBox_level'):
            level = self.ui.comboBox_level.currentText()
            if level and level != "Все":
                if level == "Заговор":
                    filters['levels'] = [0]
                else:
                    try:
                        filters['levels'] = [int(level)]
                    except ValueError:
                        pass

        # ===== ШКОЛА =====
        if hasattr(self.ui, 'comboBox_school'):
            school = self.ui.comboBox_school.currentText()
            if school and school != "Все":
                filters['schools'] = [school.lower()]

        # ===== КОМПОНЕНТЫ =====
        if hasattr(self.ui, 'comboBox_components'):
            comp = self.ui.comboBox_components.currentText()
            if comp and comp != "Все":
                components = [c.strip() for c in comp.split(",")]
                filters['components'] = components

        # ===== ВРЕМЯ =====
        if hasattr(self.ui, 'comboBox_time'):
            time_val = self.ui.comboBox_time.currentText()
            time_val = time_val.lower()
            if time_val and time_val != "все":
                if "действие" in time_val or time_val == "действие":
                    time_val = "1 " + time_val
                filters['time'] = time_val

        # ===== ТИП УРОНА =====
        if hasattr(self.ui, 'comboBox_damage'):
            damage = self.ui.comboBox_damage.currentText()
            if damage and damage != "Все":
                filters['damage_types'] = [damage.lower()]

        # ===== КОНЦЕНТРАЦИЯ =====
        if hasattr(self.ui, 'checkBox_concentration'):
            if self.ui.checkBox_concentration.isChecked():
                filters['concentration'] = True

        # ===== РИТУАЛ =====
        if hasattr(self.ui, 'checkBox_ritual'):
            if self.ui.checkBox_ritual.isChecked():
                filters['ritual'] = True

        # ===== СОРТИРОВКА =====
        filters['sort_by'] = 'level'

        return filters

    def setup_filters(self):
        """Подключает сигналы фильтров"""
        if not self.ui:
            return

        # ===== КОМБОБОКСЫ =====
        if hasattr(self.ui, 'comboBox_level'):
            self.ui.comboBox_level.currentTextChanged.connect(self.apply_filters)
            print("Подключен comboBox_level")

        if hasattr(self.ui, 'comboBox_school'):
            self.ui.comboBox_school.currentTextChanged.connect(self.apply_filters)
            print("Подключен comboBox_school")

        if hasattr(self.ui, 'comboBox_components'):
            self.ui.comboBox_components.currentTextChanged.connect(self.apply_filters)
            print("Подключен comboBox_components")

        if hasattr(self.ui, 'comboBox_time'):
            self.ui.comboBox_time.currentTextChanged.connect(self.apply_filters)
            print("Подключен comboBox_time")

        if hasattr(self.ui, 'comboBox_damage'):
            self.ui.comboBox_damage.currentTextChanged.connect(self.apply_filters)
            print("Подключен comboBox_damage")

        # ===== ЧЕКБОКСЫ =====
        if hasattr(self.ui, 'checkBox_ritual'):
            self.ui.checkBox_ritual.stateChanged.connect(self.apply_filters)
            print("Подключен checkBox_ritual")

        if hasattr(self.ui, 'checkBox_concentration'):
            self.ui.checkBox_concentration.stateChanged.connect(self.apply_filters)
            print("Подключен checkBox_concentration")

    def apply_filters(self):
        """Применяет фильтры к списку заклинаний"""
        filters = self.collect_filters()
        print(f"Фильтры: {filters}")

        filtered = self.dm.filter_spells(**filters)

        if hasattr(self.ui, 'search_input'):
            search_text = self.ui.search_input.text().strip()
            if search_text:
                filtered = self.filter_items_by_name(
                    filtered,
                    search_text,
                    lambda x: x.name
                )

        self.display_spells(filtered)
        print(f"   Найдено: {len(filtered)}")



    def display_spells(self, spells):
        """Отображает список заклинаний"""

        if not hasattr(self.ui, 'listWidget'):
            return

        self.ui.listWidget.clear()


        for spell_obj in spells:
            item = QListWidgetItem(f"""[{spell_obj.level}] {spell_obj.name}""")
            item.setData(Qt.UserRole, spell_obj)
            self.ui.listWidget.addItem(item)

    def go_back(self):
        """Возврат в главное меню"""
        print("Возврат в главное меню")
        if self.go_back_callback:
            self.go_back_callback()
        else:
            print("go_back_callback не передан!")

    def on_spell_selected(self, item):
        """Обработчик выбора заклинаний из списка"""
        spell_obj = item.data(Qt.UserRole)

        if not spell_obj:
            QMessageBox.information(self, "Информация", "заклинание не найдена в БД")
            return

        print(f"\nВыбрана заклинания: {spell_obj.name}")
        self.show_spell_details(spell_obj)

    def show_spell_details(self, spell_obj):
        """Выводит данные о заклинание"""

        if hasattr(self.ui, 'Spell_name'):
            self.ui.Spell_name.setStyleSheet("""
                                            QLabel {
                                                background-color: #f8f9fa;
                                                border: 1px solid #dee2e6;
                                                border-radius: 8px;
                                                padding: 17px;
                                                font-size: 50px;
                                                color: #333;
                                            }""")
            self.ui.Spell_name.setText(f"""<b>{spell_obj.name}</b>""")

        if hasattr(self.ui, 'Spell_description'):
            self.ui.Spell_description.setStyleSheet("""
                                                    QLabel {
                                                        background-color: #f8f9fa;
                                                        border: 1px solid #dee2e6;
                                                        border-radius: 8px;
                                                        padding: 15px;
                                                        font-size: 17px;
                                                        color: #333;
                                                    }""")
            if spell_obj.concentration:
                duration = f"""Концентрация, {spell_obj.duration}"""
            else:
                duration = spell_obj.duration

            classes = spell_obj.classes if hasattr(spell_obj, 'classes') else []
            if classes:
                classes_text = ", ".join([c.name for c in classes])
            else:
                classes_text = "—"

            subclasses = spell_obj.subclasses if hasattr(spell_obj, 'subclasses') else []
            if subclasses:
                subclass_names = []
                for s in subclasses:
                    if s.parent_class:
                        subclass_names.append(f"{s.name} ({s.parent_class.name})")
                    else:
                        subclass_names.append(s.name)
                subclasses_text = ", ".join(subclass_names)
            else:
                subclasses_text = "—"

            text = f"""<i>{spell_obj.level} уровень, {spell_obj.school}</i><br>
<b>Время накладывания:</b> {spell_obj.time}<br>
<b>Дистанция:</b> {spell_obj.distance}<br>
<b>Компоненты:</b> {spell_obj.components}<br>
<b>Длительность:</b> {duration}<br>
<b>Классы:</b> {classes_text}<br>
<b>Подклассы:</b> {subclasses_text}<br>
<br>
{spell_obj.description}<br>
<br>
"""
            if spell_obj.upper_level:
                text += f"""<b>На высоких уровнях: </b> {spell_obj.upper_level}"""

            self.ui.Spell_description.setText(text)








