from mypy.traverser import has_str_expression

from Data.Windows.base_window import BasePage
from PySide6.QtWidgets import QMessageBox, QListWidgetItem
from PySide6.QtCore import Qt


class BestiaryPage(BasePage):
    """Страница с монстрми"""

    def __init__(self, parent=None, go_back_callback=None):
        super().__init__("Data/Screens/bestiary.ui", parent)
        self.go_back_callback = go_back_callback
        self.all_bestiary = []

        self.setup_ui()
        self.setup_filters()
        self.load_bestiary()


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
            self.ui.listWidget.itemClicked.connect(self.on_bestiary_selected)
            print("Подключена кнопка: listWidget")

        if hasattr(self.ui, 'Bestiary_name'):
            self.ui.Bestiary_name.setTextFormat(Qt.RichText)
            print("Найден лейбл: Bestiary_name")

        if hasattr(self.ui, 'Bestiary_description'):
            self.ui.Bestiary_name.setTextFormat(Qt.RichText)
            print("Найден лейбл: Bestiary_description")

        if hasattr(self.ui, 'filters'):
            print("Найден фрейм: filters")
            self.ui.filters.setVisible(False)

        if hasattr(self.ui, 'frame_filters'):
            print("Найден фрейм: frame_filters")
            self.ui.frame_filters.setVisible(False)

        if hasattr(self.ui, 'Choose_Delete'):
            print("Найден фрейм: Choose_Delete")
            self.ui.Choose_Delete.setVisible(False)

        if hasattr(self.ui, 'Choose_Editing'):
            print('Найден фрейм: Choose_Editing')
            self.ui.Choose_Editing.setVisible(False)

        if hasattr(self.ui, 'Create'):
            print('Найден фрейм: Create')
            self.ui.Create.setVisible(False)

        if hasattr(self.ui, 'Editing'):
            print('Найден фрейм: Editing')
            self.ui.Editing.setVisible(False)

        if hasattr(self.ui, 'Frame_Underlay'):
            print('Найден фрейм: Frame_Underlay')
            self.ui.Frame_Underlay.setVisible(False)

        if hasattr(self.ui, 'pushButton_General_Create'):
            print('Найден фрейм: pushButton_General_Create')
            self.ui.pushButton_General_Create.clicked.connect(
                lambda: self.raise_dialog(self.ui.Create)
            )

        if hasattr(self.ui, 'pushButton_General_Delete'):
            print('Найден фрейм: pushButton_General_Delete')
            self.ui.pushButton_General_Delete.clicked.connect(
                lambda: self.raise_dialog(self.ui.Choose_Delete)
            )

        if hasattr(self.ui, 'pushButton_General_Editing'):
            print('Найден фрейм: pushButton_General_Editing')
            self.ui.pushButton_General_Editing.clicked.connect(
                lambda: self.raise_dialog(self.ui.Choose_Editing)
            )

        if hasattr(self.ui, 'pushButton_Back_Delete'):
            self.ui.pushButton_Back_Delete.clicked.connect(self.close_all_dialogs)

        if hasattr(self.ui, 'pushButton_BackChooseEditing'):
            self.ui.pushButton_BackChooseEditing.clicked.connect(self.close_all_dialogs)

        if hasattr(self.ui, 'pushButton_Back_Create'):
            self.ui.pushButton_Back_Create.clicked.connect(self.close_all_dialogs)

        if hasattr(self.ui, 'pushButton_Back_Editing'):
            self.ui.pushButton_Back_Editing.clicked.connect(self.close_all_dialogs)

    def raise_dialog(self, dialog):
        dialog.setVisible(True)
        self.ui.Frame_Underlay.setVisible(True)

    def close_all_dialogs(self):
        """Скрывает оверлей и все фреймы-диалоги."""
        self.ui.Frame_Underlay.setVisible(False)
        if hasattr(self.ui, 'Choose_Delete'):
            self.ui.Choose_Delete.setVisible(False)
        if hasattr(self.ui, 'Choose_Editing'):
            self.ui.Choose_Editing.setVisible(False)
        if hasattr(self.ui, 'Create'):
            self.ui.Create.setVisible(False)
        if hasattr(self.ui, 'Editing'):
            self.ui.Editing.setVisible(False)

    def load_bestiary(self):
        """Загружает список бестиария"""

        if not hasattr(self.ui, 'listWidget'):
            print("listWidget не найден")
            return

        self.ui.listWidget.clear()

        self.all_bestiary = self.dm.get_all_monsters()

        if not self.all_bestiary:
            item = QListWidgetItem("Тут пусто:(")
            item.setData(Qt.UserRole, None)
            self.ui.listWidget.addItem(item)
            return

        self.display_bestiary(self.all_bestiary)
        print(f"Загружено бестиария: {len(self.all_bestiary)}")

    def collect_filters(self):
        """Собирает все активные фильтры в словарь под filter_monsters"""
        filters = {}

        # ===== ОПАСНОСТЬ (danger) =====
        if hasattr(self.ui, 'comboBox_danger'):
            danger = self.ui.comboBox_danger.currentText().strip()
            if danger and danger != "Все":
                filters['dangers'] = [danger]

        # ===== РАЗМЕР (size) =====
        if hasattr(self.ui, 'comboBox_size'):
            size = self.ui.comboBox_size.currentText().strip()
            if size and size != "Все":
                filters['sizes'] = [size]

        # ===== ТИП (type) =====
        if hasattr(self.ui, 'comboBox_type'):
            type = self.ui.comboBox_type.currentText().strip()
            if type and type != "Все":
                filters['types'] = [type]

        # ===== CUSTOM =====
        if hasattr(self.ui, 'checkBox_custom'):
            if self.ui.checkBox_custom.isChecked():
                filters['is_custom'] = True

        return filters

    def setup_filters(self):
        """Подключает сигналы фильтров"""
        if not self.ui:
            return

        if hasattr(self.ui, 'comboBox_danger'):
            self.ui.comboBox_danger.currentTextChanged.connect(self.apply_filters)
            print("Подключен comboBox_danger")

        if hasattr(self.ui, 'comboBox_size'):
            self.ui.comboBox_size.currentTextChanged.connect(self.apply_filters)
            print("Подключен comboBox_size")

        if hasattr(self.ui, 'comboBox_type'):
            self.ui.comboBox_type.currentTextChanged.connect(self.apply_filters)
            print("Подключен comboBox_type")

        if hasattr(self.ui, 'checkBox_custom'):
            self.ui.checkBox_custom.stateChanged.connect(self.apply_filters)
            print("Подключен checkBox_custom ")

    def apply_filters(self):
        """Применяет фильтры к списку монстров"""
        filters = self.collect_filters()
        print(f"Фильтры: {filters}")

        filtered = self.dm.filter_monsters(**filters)

        if hasattr(self.ui, 'search_input'):
            search_text = self.ui.search_input.text().strip()
            if search_text:
                filtered = self.filter_items_by_name(
                    filtered,
                    search_text,
                    lambda x: x.name
                )

        self.display_bestiary(filtered)
        print(f"   Найдено: {len(filtered)}")

    def display_bestiary(self, bestiary):
        """Отображает список бестиария"""

        if not hasattr(self.ui, 'listWidget'):
            return

        self.ui.listWidget.clear()


        for bestiary_obj in bestiary:
            item = QListWidgetItem(bestiary_obj.name)
            item.setData(Qt.UserRole, bestiary_obj)
            self.ui.listWidget.addItem(item)

    def go_back(self):
        """Возврат в главное меню"""
        print("Возврат в главное меню")
        if self.go_back_callback:
            self.go_back_callback()
        else:
            print("go_back_callback не передан!")

    def on_bestiary_selected(self, item):
        """Обработчик выбора бестиария из списка"""
        bestiary_obj = item.data(Qt.UserRole)

        if not bestiary_obj:
            QMessageBox.information(self, "Информация", "бестиарии не найдена в БД")
            return

        print(f"\nВыбран монстр: {bestiary_obj.name}")
        self.show_bestiary_details(bestiary_obj)

    def show_bestiary_details(self, bestiary_obj):
        """Выводит данные о монстре в правой панели."""

        # ---------- ИМЯ ----------
        if hasattr(self.ui, 'Bestiary_name'):
            self.ui.Bestiary_name.setStyleSheet("""
                QLabel {
                    background-color: #f8f9fa;
                    border: 1px solid #dee2e6;
                    border-radius: 8px;
                    padding: 17px;
                    font-size: 50px;
                    color: #333;
                }""")
            self.ui.Bestiary_name.setText(f"<b>{bestiary_obj.name}</b>")

        # ---------- ОПИСАНИЕ ----------
        if not hasattr(self.ui, 'Bestiary_description'):
            return

        self.ui.Bestiary_description.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 15px;
                font-size: 17px;
                color: #333;
            }""")

        def is_empty(value):
            """Пусто ли значение (None, '', 'None', пробелы)."""
            if value is None:
                return True
            s = str(value).strip()
            return s == "" or s == "None"

        def mod(value):
            """Модификатор характеристики D&D: (значение - 10) // 2."""
            try:
                m = (int(value) - 10) // 2
            except (TypeError, ValueError):
                return "—"
            return f"+{m}" if m >= 0 else str(m)

        # ---------- ШАПКА: размер, тип, опасность ----------
        header = f"<i>{bestiary_obj.size} {bestiary_obj.type}, опасность {bestiary_obj.danger}</i>"

        # ---------- БАЗОВЫЕ БОЕВЫЕ ПАРАМЕТРЫ (обязательные) ----------
        text = (
            f"{header}<br><br>"
            f"<b>Хиты:</b> {bestiary_obj.hits}<br>"
            f"<b>Класс доспеха:</b> {bestiary_obj.armor_class}<br>"
            f"<b>Скорость:</b> {bestiary_obj.speed}<br>"
        )

        # ---------- ХАРАКТЕРИСТИКИ (обязательные) ----------
        text += "<br><b>Характеристики:</b><br>"
        text += (
            f"СИЛ {bestiary_obj.strengh} ({mod(bestiary_obj.strengh)}) &nbsp; "
            f"ЛОВ {bestiary_obj.agility} ({mod(bestiary_obj.agility)}) &nbsp; "
            f"ВЫН {bestiary_obj.endurance} ({mod(bestiary_obj.endurance)})<br>"
            f"ИНТ {bestiary_obj.intelligence} ({mod(bestiary_obj.intelligence)}) &nbsp; "
            f"МУД {bestiary_obj.wisdom} ({mod(bestiary_obj.wisdom)}) &nbsp; "
            f"ХАР {bestiary_obj.charisma} ({mod(bestiary_obj.charisma)})<br>"
        )

        # ---------- ОПЦИОНАЛЬНЫЕ СТРОКИ ----------
        optional_fields = [
            ("Спасброски", bestiary_obj.savingthrows),
            ("Навыки", bestiary_obj.skills),
            ("Сопротивления", bestiary_obj.resists),
            ("Иммунитет к урону", bestiary_obj.immunity_damage),
            ("Иммунитет к состояниям", bestiary_obj.immunity_status),
            ("Чувства", bestiary_obj.feelings),
            ("Языки", bestiary_obj.language),
            ("Бонус мастерства", bestiary_obj.mastery_bonus),
        ]

        optional_text = ""
        for label, value in optional_fields:
            if not is_empty(value):
                optional_text += f"<b>{label}:</b> {value}<br>"

        if optional_text:
            text += "<br>" + optional_text

        # ---------- БЛОКИ ТЕКСТА (каждый — только если не пуст) ----------
        text_blocks = [
            ("Пассивные способности", bestiary_obj.passive_skills),
            ("Действия", bestiary_obj.actions),
            ("Реакции", bestiary_obj.reaction),
            ("Легендарные действия", bestiary_obj.legendary_actions),
            ("Мифические действия", bestiary_obj.mythical_actions),
            ("Логово", bestiary_obj.lair),
        ]

        for label, value in text_blocks:
            if not is_empty(value):
                text += f"<br><b>{label}:</b><br>{value}<br>"

        # ---------- ОПИСАНИЕ МОНСТРА ----------
        if not is_empty(bestiary_obj.description):
            text += f"<br>{bestiary_obj.description}"

        self.ui.Bestiary_description.setText(text)











