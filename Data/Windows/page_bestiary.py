from mypy.traverser import has_str_expression

from Data.Windows.base_window import BasePage
from PySide6.QtWidgets import (
    QMessageBox, QListWidgetItem,
    QStyledItemDelegate, QStyle,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette, QBrush

class BestiaryItemDelegate(QStyledItemDelegate):
    BASE_NORMAL   = QColor(240, 213, 163)
    BASE_HOVER    = QColor(255, 223, 160)
    BASE_SELECTED = QColor(230, 205, 155)
    CUSTOM_NORMAL   = QColor(250, 120, 120)
    CUSTOM_HOVER    = QColor(255, 160, 160)
    CUSTOM_SELECTED = QColor(220,  80,  80)

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)

        obj = index.data(Qt.UserRole)
        is_custom = bool(getattr(obj, "is_custom", False)) if obj is not None else False

        selected = bool(option.state & QStyle.State_Selected)
        hovered  = bool(option.state & QStyle.State_MouseOver)

        if is_custom:
            color = (self.CUSTOM_SELECTED if selected
                     else self.CUSTOM_HOVER if hovered
                     else self.CUSTOM_NORMAL)
        else:
            color = (self.BASE_SELECTED if selected
                     else self.BASE_HOVER if hovered
                     else self.BASE_NORMAL)

        option.palette.setColor(QPalette.Text, color)
        option.palette.setColor(QPalette.HighlightedText, color)
        option.palette.setColor(QPalette.WindowText, color)


class BestiaryPage(BasePage):
    """Страница с монстрми"""

    CHAR_BONUS_PAIRS = [
        ('spinBox_Strength_Editing', 'label_Bonus_Strength_Editing'),
        ('spinBox_Agility_Editing', 'label_Bonus_Agility_Editing'),
        ('spinBox_Endurance_Editing', 'label_Bonus_Endurance_Editing'),
        ('spinBox_Intelligence_Editing', 'label_Bonus_Intelligence_Editing'),
        ('spinBox_Wisdom_Editing', 'label_Bonus_Wisdom_Editing'),
        ('spinBox_Charisma_Editing', 'label_Bonus_Charisma_Editing'),
    ]

    CHAR_BONUS_PAIRS_CREATE = [
        ('spinBox_Strength_Create', 'label_Bonus_Strength_Create'),
        ('spinBox_Agility_Create', 'label_Bonus_Agility_Create'),
        ('spinBox_Endurance_Create', 'label_Bonus_Endurance_Create'),
        ('spinBox_Intelligence_Create', 'label_Bonus_Intelligence_Create'),
        ('spinBox_Wisdom_Create', 'label_Bonus_Wisdom_Create'),
        ('spinBox_Charisma_Create', 'label_Bonus_Charisma_Create'),
    ]

    def __init__(self, parent=None, go_back_callback=None):
        super().__init__("Data/Screens/bestiary.ui", parent)
        self.go_back_callback = go_back_callback
        self.all_bestiary = []

        self.setup_filters()
        self.load_bestiary()
        self.editing_obj = None

    def is_any_dialog_open(self) -> bool:
        """Открыт ли сейчас оверлей с каким-либо диалогом."""
        return (
                hasattr(self.ui, 'Frame_Underlay')
                and self.ui.Frame_Underlay.isVisible()
        )

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
            self.ui.listWidget.setItemDelegate(BestiaryItemDelegate(self.ui.listWidget))
            print("Подключена кнопка: listWidget")
            print("Установлен BestiaryItemDelegate")

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
                lambda: self.raise_create_dialog(self.ui.Create)
            )

        if hasattr(self.ui, 'pushButton_General_Delete'):
            self.ui.pushButton_General_Delete.clicked.connect(self.open_delete_dialog)

        if hasattr(self.ui, 'pushButton_Delete'):
            self.ui.pushButton_Delete.clicked.connect(self.confirm_delete)

        if hasattr(self.ui, 'pushButton_Back_Delete'):
            self.ui.pushButton_Back_Delete.clicked.connect(self.close_all_dialogs)

        if hasattr(self.ui, 'pushButton_BackChooseEditing'):
            self.ui.pushButton_BackChooseEditing.clicked.connect(self.close_all_dialogs)

        if hasattr(self.ui, 'pushButton_Back_Create'):
            self.ui.pushButton_Back_Create.clicked.connect(self.close_all_dialogs)

        if hasattr(self.ui, 'pushButton_Back_Editing'):
            self.ui.pushButton_Back_Editing.clicked.connect(self.close_all_dialogs)

        if hasattr(self.ui, 'pushButton_Create'):
            self.ui.pushButton_Create.clicked.connect(self.validate_and_create)

        if hasattr(self.ui, 'pushButton_General_Editing'):
            print('Найден фрейм: pushButton_General_Editing')
            self.ui.pushButton_General_Editing.clicked.connect(self.open_choose_editing)

        if hasattr(self.ui, 'pushButton_ChooseEditing'):
            self.ui.pushButton_ChooseEditing.clicked.connect(self.confirm_choose_editing)

        if hasattr(self.ui, 'pushButton_BackChooseEditing'):
            self.ui.pushButton_BackChooseEditing.clicked.connect(self.close_all_dialogs)

        if hasattr(self.ui, 'pushButton_Editing'):
            self.ui.pushButton_Editing.clicked.connect(self.validate_and_update)

        if hasattr(self.ui, 'pushButton_Back_Editing'):
            self.ui.pushButton_Back_Editing.clicked.connect(self.back_from_editing)

        for spin_name, label_name in self.CHAR_BONUS_PAIRS:
            if hasattr(self.ui, spin_name):
                getattr(self.ui, spin_name).valueChanged.connect(
                    lambda value, s=spin_name, l=label_name:
                        self.update_bonus_label(s, l)
                )
                print(f"Подключен бонус: {spin_name} → {label_name}")

        for spin_name, label_name in self.CHAR_BONUS_PAIRS_CREATE:
            if hasattr(self.ui, spin_name):
                getattr(self.ui, spin_name).valueChanged.connect(
                    lambda value, s=spin_name, l=label_name:
                        self.update_bonus_label(s, l)
                )
                print(f"Подключен бонус: {spin_name} → {label_name}")

    @staticmethod
    def mod(value):
        """Модификатор характеристики D&D: (значение - 10) // 2."""
        try:
            m = (int(value) - 10) // 2
        except (TypeError, ValueError):
            return "—"
        return f"+{m}" if m >= 0 else str(m)

    def update_bonus_label(self, spin_name, label_name):
        """Пересчитывает бонус для одной характеристики."""
        if not hasattr(self.ui, spin_name) or not hasattr(self.ui, label_name):
            return
        value = getattr(self.ui, spin_name).value()
        getattr(self.ui, label_name).setText(self.mod(value))

    def update_all_bonuses(self):
        """Пересчитывает бонусы всех характеристик в форме Editing."""
        for spin_name, label_name in self.CHAR_BONUS_PAIRS:
            self.update_bonus_label(spin_name, label_name)

    def update_all_bonuses_create(self):
        """Пересчитывает бонусы всех характеристик в форме Create."""
        for spin_name, label_name in self.CHAR_BONUS_PAIRS_CREATE:
            self.update_bonus_label(spin_name, label_name)

    def set_label_error(self, label_name, has_error):
        """Красит лейбл красным (или возвращает базовый цвет)."""
        if not hasattr(self.ui, label_name):
            return
        lbl = getattr(self.ui, label_name)
        if not hasattr(lbl, "base_style"):
            lbl.base_style = lbl.styleSheet()

        if has_error:
            lbl.setStyleSheet(lbl.base_style + """
                QLabel {
                    color: rgb(220, 60, 60) !important;
                    border: 1px solid rgb(220, 60, 60) !important;
                }""")
        else:
            lbl.setStyleSheet(lbl.base_style)

    def clear_errors_create(self):
        """Снимает красную подсветку со всех лейблов формы создания."""
        for label in (
                'label_Name_Create', 'label_Size_Create', 'label_Type_Create',
                'label_Hit_Create', 'label_Cd_Create', 'label_Speed_Create',
                'label_Danger_Create', 'label_Language_Create', 'label_Mastery_Create',
        ):
            self.set_label_error(label, False)

    def validate_and_create(self):
        if not hasattr(self.ui, 'label_Error_Create'):
            return

        errors = []
        self.clear_errors_create()

        # ---- обязательные текстовые поля ----
        text_required = [
            ('lineEdit_Name_Create', 'label_Name_Create', 'Имя'),
            ('lineEdit_Hit_Create', 'label_Hit_Create', 'Хиты'),
            ('lineEdit_Cd_Create', 'label_Cd_Create', 'Класс доспеха'),
            ('lineEdit_Speed_Create', 'label_Speed_Create', 'Скорость'),
            ('lineEdit_Language_Create', 'label_Language_Create', 'Языки'),
            ('lineEdit_Danger_Create', 'label_Danger_Create', 'Опасность'),
        ]
        values = {}
        for field_name, label_name, title in text_required:
            if not hasattr(self.ui, field_name):
                continue
            text = getattr(self.ui, field_name).text().strip()
            if not text:
                errors.append(f"«{title}» — обязательное поле")
                self.set_label_error(label_name, True)
            values[title] = text

        # ---- обязательные комбобоксы ----
        combo_required = [
            ('comboBox_Size_Create', 'label_Size_Create', 'Размер'),
            ('comboBox_Type_Create', 'label_Type_Create', 'Тип'),
        ]
        for field_name, label_name, title in combo_required:
            if not hasattr(self.ui, field_name):
                continue
            text = getattr(self.ui, field_name).currentText().strip()
            if not text:
                errors.append(f"«{title}» — выберите значение")
                self.set_label_error(label_name, True)
            values[title] = text

        # ---- опасность: число 0..20 или дробь 1/8, 1/4, 1/2 ----
        danger = values.get('Опасность', '')
        if danger and not self.is_valid_danger(danger):
            errors.append("«Опасность» — 0, 1/8, 1/4, 1/2 или целое 1–20")
            self.set_label_error('label_Danger_Create', True)

        # ---- бонус мастерства: целое ----
        mastery_int = 2
        if hasattr(self.ui, 'spinBox_Mastery_Create'):
            mastery_int = self.ui.spinBox_Mastery_Create.value()

        if errors:
            self.ui.label_Error_Create.setText("; ".join(errors))
            self.ui.label_Error_Create.setStyleSheet(
                "QLabel { color: rgb(220, 60, 60); font-size: 12px; }"
            )
            return

        # ---- необязательные ----
        def le(name):
            return getattr(self.ui, name).text().strip() if hasattr(self.ui, name) else ""

        def te(name):
            return getattr(self.ui, name).toPlainText().strip() if hasattr(self.ui, name) else ""

        def sb(name, default=10):
            return getattr(self.ui, name).value() if hasattr(self.ui, name) else default

        try:
            self.dm.add_monster(
                name=values['Имя'],
                hits=values['Хиты'],
                armor_class=values['Класс доспеха'],
                speed=values['Скорость'],
                description=te('textEdit_Description_Create'),
                size=values['Размер'],
                type=values['Тип'],
                danger=values['Опасность'],
                language=values['Языки'],
                mastery_bonus=mastery_int,

                strengh=sb('spinBox_Strength_Create'),
                agility=sb('spinBox_Agility_Create'),
                endurance=sb('spinBox_Endurance_Create'),
                intelligence=sb('spinBox_Intelligence_Create'),
                wisdom=sb('spinBox_Wisdom_Create'),
                charisma=sb('spinBox_Charisma_Create'),

                savingthrows=le('lineEdit_Saving_Throws_Create'),
                skills=le('lineEdit_Skills_Create'),
                resists=le('lineEdit_Resistance_Create'),
                immunity_damage=le('lineEdit_Damage_Imm_Create'),
                immunity_status=le('lineEdit_State_Create'),
                feelings=le('lineEdit_Feelings_Create'),

                passive_skills=te('textEdit_Capabilities_Create'),
                actions=te('textEdit_Actions_Create'),
                reaction=te('textEdit_Reactions_Create'),
                legendary_actions=te('textEdit_Legendary_Create'),
                mythical_actions=te('textEdit_Mythical_Create'),
                lair=te('textEdit_Lair_Create'),
            )
        except Exception as e:
            msg = str(e)
            if "UNIQUE constraint failed: monsters.name" in msg:
                msg = f"Монстр с именем «{values['Имя']}» уже существует"
            self.ui.label_Error_Create.setText(f"Ошибка сохранения: {msg}")
            self.ui.label_Error_Create.setStyleSheet(
                "QLabel { color: rgb(220, 60, 60); font-size: 12px; }"
            )
            return
            return

        # ---- успех ----
        self.ui.label_Error_Create.setText("Монстр создан!")
        self.ui.label_Error_Create.setStyleSheet(
            "QLabel { color: rgb(120, 200, 120); font-size: 12px; }"
        )
        self.reset_create_form()
        self.load_bestiary()
        self.close_all_dialogs()

    @staticmethod
    def is_valid_danger(value: str) -> bool:
        value = value.strip()
        if value in ("1/8", "1/4", "1/2"):
            return True
        try:
            return 0 <= int(value) <= 20
        except ValueError:
            return False

    def reset_create_form(self):
        self.clear_errors_create()

        for name in (
                'lineEdit_Name_Create', 'lineEdit_Hit_Create', 'lineEdit_Cd_Create',
                'lineEdit_Speed_Create', 'lineEdit_Language_Create', 'lineEdit_Danger_Create',
                'lineEdit_Saving_Throws_Create', 'lineEdit_Skills_Create',
                'lineEdit_Resistance_Create', 'lineEdit_Damage_Imm_Create',
                'lineEdit_State_Create', 'lineEdit_Feelings_Create',
        ):
            if hasattr(self.ui, name):
                getattr(self.ui, name).clear()

        for name in (
                'textEdit_Capabilities_Create', 'textEdit_Actions_Create',
                'textEdit_Reactions_Create', 'textEdit_Legendary_Create',
                'textEdit_Mythical_Create', 'textEdit_Lair_Create',
                'textEdit_Description_Create',
        ):
            if hasattr(self.ui, name):
                getattr(self.ui, name).clear()

        for name in (
                'spinBox_Strength_Create', 'spinBox_Agility_Create',
                'spinBox_Endurance_Create', 'spinBox_Intelligence_Create',
                'spinBox_Wisdom_Create', 'spinBox_Charisma_Create',
        ):
            if hasattr(self.ui, name):
                getattr(self.ui, name).setValue(10)

        if hasattr(self.ui, 'spinBox_Mastery_Create'):
            self.ui.spinBox_Mastery_Create.setValue(2)

        if hasattr(self.ui, 'comboBox_Size_Create'):
            self.ui.comboBox_Size_Create.setCurrentIndex(0)
        if hasattr(self.ui, 'comboBox_Type_Create'):
            self.ui.comboBox_Type_Create.setCurrentIndex(0)

        if hasattr(self.ui, 'label_Error_Create'):
            self.ui.label_Error_Create.setText("")
            self.ui.label_Error_Create.setStyleSheet("")

        self.update_all_bonuses_create()

    def open_choose_editing(self):
        if not hasattr(self.ui, 'listWidget_ChooseEditing'):  # ← ing
            return

        self.ui.listWidget_ChooseEditing.clear()

        customs = [m for m in self.dm.get_all_monsters()
                   if getattr(m, 'is_custom', False)]
        print(f"open_choose_editing: кастомных {len(customs)}")

        if not customs:
            item = QListWidgetItem("Нет кастомных монстров")
            item.setData(Qt.UserRole, None)
            self.ui.listWidget_ChooseEditing.addItem(item)
        else:
            for m in customs:
                item = QListWidgetItem(m.name)
                item.setData(Qt.UserRole, m)
                self.ui.listWidget_ChooseEditing.addItem(item)

        self.raise_dialog(self.ui.Choose_Editing)

    def confirm_choose_editing(self):
        """Берёт выбранного моба, заполняет Editing и показывает его."""
        if not hasattr(self.ui, 'listWidget_ChooseEditing'):
            return

        current = self.ui.listWidget_ChooseEditing.currentItem()
        if not current:
            QMessageBox.information(self, "Информация", "Выберите монстра в списке")
            return

        obj = current.data(Qt.UserRole)
        if not obj:
            return

        self.editing_obj = obj
        print(f"[DEBUG] editing_obj установлен: {self.editing_obj}, id={getattr(self.editing_obj, 'id', None)}")
        self.fill_editing_form(obj)

        self.ui.Choose_Editing.setVisible(False)
        self.ui.Editing.setVisible(True)
        self.ui.Frame_Underlay.setVisible(True)

    def fill_editing_form(self, obj):
        """Переносит данные моба в поля формы Editing."""

        def le(name, value):
            if hasattr(self.ui, name):
                getattr(self.ui, name).setText("" if value is None else str(value))

        def te(name, value):
            if hasattr(self.ui, name):
                getattr(self.ui, name).setPlainText("" if value is None else str(value))

        def cb(name, value):
            if hasattr(self.ui, name):
                getattr(self.ui, name).setCurrentText("" if value is None else str(value))

        def sb(name, value, default=10):
            if hasattr(self.ui, name):
                try:
                    getattr(self.ui, name).setValue(int(value))
                except (TypeError, ValueError):
                    getattr(self.ui, name).setValue(default)

        # обязательные
        le('lineEdit_Name_Editing', obj.name)
        le('lineEdit_Hit_Editing', obj.hits)
        le('lineEdit_Cd_Editing', obj.armor_class)
        le('lineEdit_Speed_Editing', obj.speed)
        le('lineEdit_Danger_Editing', obj.danger)
        le('lineEdit_Language_Editing', obj.language)

        cb('comboBox_Size_Editing', obj.size)
        cb('comboBox_Type_Editing', obj.type)

        sb('spinBox_Mastery_Editing', obj.mastery_bonus)

        # характеристики
        sb('spinBox_Strength_Editing', obj.strengh)
        sb('spinBox_Agility_Editing', obj.agility)
        sb('spinBox_Endurance_Editing', obj.endurance)
        sb('spinBox_Intelligence_Editing', obj.intelligence)
        sb('spinBox_Wisdom_Editing', obj.wisdom)
        sb('spinBox_Characteristics_Charisma_Editing', obj.charisma)  # ← как в .ui

        # необязательные
        le('lineEdit_Saving_Throws_Editing', obj.savingthrows)
        le('lineEdit_Skills_Editing', obj.skills)
        le('lineEdit_Resistance_Editing', obj.resists)
        le('lineEdit_Damage_Imm_Editing', obj.immunity_damage)  # Imm с большой I
        le('lineEdit_State_Imm_Editing', obj.immunity_status)  # Imm с большой I
        le('lineEdit_Feelings_Editing', obj.feelings)

        # текстовые блоки
        te('textEdit_Capabilities_Editing', obj.passive_skills)
        te('textEdit_Actions_Editing', obj.actions)
        te('textEdit_Reactions_Editing', obj.reaction)
        te('textEdit_Legendary_Editing', obj.legendary_actions)
        te('textEdit_Mythical_Editing', obj.mythical_actions)
        te('textEdit_Lair_Editing', obj.lair)
        te('textEdit_Description_Editing', obj.description)

        if hasattr(self.ui, 'label_Error_Editing'):
            self.ui.label_Error_Editing.setText("")
            self.ui.label_Error_Editing.setStyleSheet("")

        self.update_all_bonuses()


    def clear_errors_editing(self):
        """Снимает подсветку с лейблов формы редактирования."""
        for label in (
                'label_Name_Editing', 'label_Size_Editing', 'label_Type_Editing',
                'label_Hit_Editing', 'label_Cd_Editing', 'label_Speed_Editing',
                'label_Danger_Editing', 'label_Language_Editing', 'label_Mastery_Editing',
        ):
            self.set_label_error(label, False)

    def validate_and_update(self):
        print(f"[DEBUG] validate_and_update: editing_obj={self.editing_obj}")
        if not self.editing_obj:
            QMessageBox.information(self, "Информация",
                                    "Нет выбранного монстра для редактирования")
            return
        if not hasattr(self.ui, 'label_Error_Editing'):
            return

        errors = []
        self.clear_errors_editing()

        # обязательные текстовые
        text_required = [
            ('lineEdit_Name_Editing', 'label_Name_Editing', 'Имя'),
            ('lineEdit_Hit_Editing', 'label_Hit_Editing', 'Хиты'),
            ('lineEdit_Cd_Editing', 'label_Cd_Editing', 'Класс доспеха'),
            ('lineEdit_Speed_Editing', 'label_Speed_Editing', 'Скорость'),
            ('lineEdit_Language_Editing', 'label_Language_Editing', 'Языки'),
            ('lineEdit_Danger_Editing', 'label_Danger_Editing', 'Опасность'),
        ]
        values = {}
        for field_name, label_name, title in text_required:
            if not hasattr(self.ui, field_name):
                continue
            text = getattr(self.ui, field_name).text().strip()
            if not text:
                errors.append(f"«{title}» — обязательное поле")
                self.set_label_error(label_name, True)
            values[title] = text

        # обязательные комбобоксы
        combo_required = [
            ('comboBox_Size_Editing', 'label_Size_Editing', 'Размер'),
            ('comboBox_Type_Editing', 'label_Type_Editing', 'Тип'),
        ]
        for field_name, label_name, title in combo_required:
            if not hasattr(self.ui, field_name):
                continue
            text = getattr(self.ui, field_name).currentText().strip()
            if not text:
                errors.append(f"«{title}» — выберите значение")
                self.set_label_error(label_name, True)
            values[title] = text

        # опасность
        danger = values.get('Опасность', '')
        if danger and not self.is_valid_danger(danger):
            errors.append("«Опасность» — 0, 1/8, 1/4, 1/2 или целое 1–20")
            self.set_label_error('label_Danger_Editing', True)

        # бонус мастерства
        mastery_int = 2
        if hasattr(self.ui, 'spinBox_Mastery_Editing'):
            mastery_int = self.ui.spinBox_Mastery_Editing.value()

        if errors:
            self.ui.label_Error_Editing.setText("; ".join(errors))
            self.ui.label_Error_Editing.setStyleSheet(
                "QLabel { color: rgb(220, 60, 60); font-size: 12px; }"
            )
            return

        def le(name):
            return getattr(self.ui, name).text().strip() if hasattr(self.ui, name) else ""

        def te(name):
            return getattr(self.ui, name).toPlainText().strip() if hasattr(self.ui, name) else ""

        def sb(name, default=10):
            return getattr(self.ui, name).value() if hasattr(self.ui, name) else default

        try:
            print(f"[DEBUG] Размер: {values.get('Размер')!r}, Тип: {values.get('Тип')!r}")
            print(f"[DEBUG] В БД до: size={self.editing_obj.size!r}, type={self.editing_obj.type!r}")
            self.dm.update_monster(
                self.editing_obj.id,
                name=values['Имя'],
                hits=values['Хиты'],
                armor_class=values['Класс доспеха'],
                speed=values['Скорость'],
                size=values['Размер'],
                type=values['Тип'],
                danger=values['Опасность'],
                language=values['Языки'],
                mastery_bonus=mastery_int,

                strengh=sb('spinBox_Strength_Editing'),
                agility=sb('spinBox_Agility_Editing'),
                endurance=sb('spinBox_Endurance_Editing'),
                intelligence=sb('spinBox_Intelligence_Editing'),
                wisdom=sb('spinBox_Wisdom_Editing'),
                charisma=sb('spinBox_Characteristics_Charisma_Editing'),  # как в .ui

                savingthrows=le('lineEdit_Saving_Throws_Editing'),
                skills=le('lineEdit_Skills_Editing'),
                resists=le('lineEdit_Resistance_Editing'),
                immunity_damage=le('lineEdit_Damage_Imm_Editing'),
                immunity_status=le('lineEdit_State_Imm_Editing'),
                feelings=le('lineEdit_Feelings_Editing'),

                passive_skills=te('textEdit_Capabilities_Editing'),
                actions=te('textEdit_Actions_Editing'),
                reaction=te('textEdit_Reactions_Editing'),
                legendary_actions=te('textEdit_Legendary_Editing'),
                mythical_actions=te('textEdit_Mythical_Editing'),
                lair=te('textEdit_Lair_Editing'),
                description=te('textEdit_Description_Editing'),
            )
        except Exception as e:
            msg = str(e)
            if "UNIQUE constraint failed: monsters.name" in msg:
                msg = f"Монстр с именем «{values['Имя']}» уже существует"
                self.set_label_error('label_Name_Editing', True)
            self.ui.label_Error_Editing.setText(f"Ошибка сохранения: {msg}")
            self.ui.label_Error_Editing.setStyleSheet(
                "QLabel { color: rgb(220, 60, 60); font-size: 12px; }"
            )
            return

        # успех
        self.ui.label_Error_Editing.setText("Изменения сохранены!")
        self.ui.label_Error_Editing.setStyleSheet(
            "QLabel { color: rgb(120, 200, 120); font-size: 12px; }"
        )
        self.editing_obj = None
        self.load_bestiary()
        self.close_all_dialogs()

    def back_from_editing(self):
        """Назад из Editing → обратно в Choose_Editing."""
        self.editing_obj = None
        if hasattr(self.ui, 'Editing'):
            self.ui.Editing.setVisible(False)
        if hasattr(self.ui, 'Choose_Editing'):
            self.ui.Choose_Editing.setVisible(True)

    def open_delete_dialog(self):
        """Заполняет список кастомных монстров и открывает форму удаления."""
        if not hasattr(self.ui, 'listWidget_Delete'):
            return

        self.ui.listWidget_Delete.clear()

        customs = [m for m in self.dm.get_all_monsters()
                   if getattr(m, 'is_custom', False)]
        print(f"open_delete_dialog: кастомных {len(customs)}")

        if not customs:
            item = QListWidgetItem("Нет кастомных монстров")
            item.setData(Qt.UserRole, None)
            self.ui.listWidget_Delete.addItem(item)
        else:
            for m in customs:
                item = QListWidgetItem(m.name)
                item.setData(Qt.UserRole, m)
                self.ui.listWidget_Delete.addItem(item)

        self.raise_dialog(self.ui.Choose_Delete)

    def confirm_delete(self):
        """Удаляет выбранного кастомного монстра."""
        if not hasattr(self.ui, 'listWidget_Delete'):
            return

        current = self.ui.listWidget_Delete.currentItem()
        if not current:
            QMessageBox.information(self, "Информация", "Выберите монстра в списке")
            return

        obj = current.data(Qt.UserRole)
        if not obj:
            return

        # Дополнительное подтверждение
        reply = QMessageBox.question(
            self, "Удаление",
            f"Удалить монстра «{obj.name}»?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return

        try:
            self.dm.delete_monster(obj.id)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить: {e}")
            return

        self.load_bestiary()
        self.close_all_dialogs()

    def raise_dialog(self, dialog):
        dialog.setVisible(True)
        self.ui.Frame_Underlay.setVisible(True)

    def raise_create_dialog(self, dialog):
        self.raise_dialog(dialog)
        self.reset_create_form()

    def close_all_dialogs(self):
        """Скрывает оверлей и все фреймы-диалоги."""
        self.editing_obj = None
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











