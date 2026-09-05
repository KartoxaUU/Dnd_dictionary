from PySide6.QtGui import QPixmap
from sqlalchemy.sql.functions import count

from Data.Windows.base_window import BasePage
from PySide6.QtWidgets import QMessageBox, QListWidgetItem
from PySide6.QtCore import Qt


class ClassesPage(BasePage):
    """Страница с классами"""

    def __init__(self, parent=None, go_back_callback=None):
        super().__init__("Data/Screens/classes.ui", parent)
        self.go_back_callback = go_back_callback
        self.all_classes = []

        self.setup_ui()
        self.load_classes()

    def setup_ui(self):
        """Подключаем кнопки"""

        if not self.ui:
            return

        if hasattr(self.ui, 'btn_back'):
            btn = getattr(self.ui, 'btn_back')
            btn.clicked.connect(self.go_back)
            print("Подключена кнопка: btn_back")

        if hasattr(self.ui, 'search_input'):
            self.ui.search_input.textChanged.connect(self.filter_classes)
            print("Подключено поле поиска: search_input")

        if hasattr(self.ui, 'listWidget'):
            self.ui.listWidget.itemClicked.connect(self.on_class_selected)
            print("Подключен список: listWidget")

        if hasattr(self.ui, 'Class_help1'):
            self.ui.Class_help1.clicked.connect(self.toggle_feature)
            self.ui.Class_help1.setVisible(False)
            print("Подключена кнопка: Class_help1")

        if hasattr(self.ui, 'Class_help2'):
            self.ui.Class_help2.itemClicked.connect(self.show_subclass)
            print("Подключен список: Class_help2")

        if hasattr(self.ui, 'Class_info'):
            print("Найден лейбл: Class_info")

        if hasattr(self.ui, 'Class_icon'):
            print("Найден лейбл: Class_icon")

        if hasattr(self.ui, 'Class_name'):
            print("Найден лейбл: Class_name")

        if hasattr(self.ui, 'Class_abilities'):
            print("Найден лейбл: Class_abilities")

        if hasattr(self.ui, 'Class_features'):
            self.ui.Class_features.setVisible(False)
            print("Class_features скрыт")

        if hasattr(self.ui, 'Class_subclass'):
            print("Найден лейбл: Class_subclass")

    def load_classes(self):
        """Загружает список классов"""

        if not hasattr(self.ui, 'listWidget'):
            print("listWidget не найден")
            return

        self.ui.listWidget.clear()

        self.all_classes = self.dm.get_all_classes()

        if not self.all_classes:
            item = QListWidgetItem("Классы не найдены")
            item.setData(Qt.UserRole, None)
            self.ui.listWidget.addItem(item)
            return

        self.display_classes(self.all_classes)
        print(f"Загружено классов: {len(self.all_classes)}")

    def filter_classes(self, search_text):
        """Фильтрует классы по названию"""

        if not hasattr(self.ui, 'search_input'):
            return

        search_text = search_text.strip().lower()

        if not search_text:
            self.display_classes(self.all_classes)
            return

        filtered = self.filter_items_by_name(
            self.all_classes,
            search_text,
            lambda x: x.name
        )

        self.display_classes(filtered)
        print(f"Найдено классов: {len(filtered)}")

    def display_classes(self, classes):
        """Отображает список классов"""

        if not hasattr(self.ui, 'listWidget'):
            return

        self.ui.listWidget.clear()

        for class_obj in classes:
            item = QListWidgetItem(class_obj.name)
            item.setData(Qt.UserRole, class_obj)
            self.ui.listWidget.addItem(item)

    def go_back(self):
        """Возврат в главное меню"""
        print("Возврат в главное меню")
        if self.go_back_callback:
            self.go_back_callback()
        else:
            print("go_back_callback не передан!")

    def on_class_selected(self, item):
        """Обработчик выбора класса из списка"""
        class_obj = item.data(Qt.UserRole)

        if not class_obj:
            QMessageBox.information(self, "Информация", "Класс не найден в БД")
            return

        print(f"\nВыбран класс: {class_obj.name}")
        self.show_class_details(class_obj)

    def show_class_details(self, class_obj):
        """Выводит данные о классе"""

        if not hasattr(self.ui, 'Class_info'):
            print("Class_info не найден")
            return

        if hasattr(self.ui, 'Class_help1'):
            self.ui.Class_help1.setChecked(False)

        if hasattr(self.ui, 'Class_features'):
            self.ui.Class_features.setVisible(False)

        self.set_class_icon(class_obj)

        if hasattr(self.ui, 'Class_name'):
            self.ui.Class_name.setText(f"<b>{class_obj.name}</b>")
            self.ui.Class_name.setStyleSheet("""
                QLabel {
                    background-color: #f8f9fa;
                    border: 1px solid #dee2e6;
                    border-radius: 8px;
                    padding: 15px;
                    font-size: 50px;
                    color: #333;
                }
            """)

        text = f"""
        <b>Кость хитов:</b> к{class_obj.hit_die}
        <br>

        <b>Доспехи:</b> {class_obj.possession_armor or '—'}
        <br>

        <b>Оружие:</b> {class_obj.possession_weapon or '—'}
        <br>

        <b>Спасброски:</b> {class_obj.possession_savingthrows or '—'}
        <br>

        <b>Навыки:</b> {class_obj.possession_skills or '—'}
        <br><br>

        <b>Описание:</b>
        <br>
        {class_obj.description or 'Нет описания'}
        """

        self.ui.Class_info.setText(text)
        self.ui.Class_info.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 15px;
                font-size: 17px;
                color: #333;
            }
        """)

        # ===== СПОСОБНОСТИ КЛАССА =====
        if hasattr(self.ui, 'Class_abilities'):
            abilities = self.dm.get_all_class_abilities_by_class(class_obj)

            if abilities:
                self.ui.Class_abilities.setVisible(True)
                self.ui.Class_abilities.setStyleSheet("""
                    QLabel {
                        background-color: #f8f9fa;
                        border: 1px solid #dee2e6;
                        border-radius: 8px;
                        padding: 15px;
                        font-size: 17px;
                        color: #333;
                    }
                """)

                text = ""
                count = 0
                for ability in abilities:
                    if count == 0:
                        text += f"""
<b>{ability.name}</b>  <i>{ability.level} уровень</i>
<br>
{ability.description}
"""
                    else:
                        text += f"""
<br><br><b>{ability.name}</b>  <i>{ability.level} уровень</i>
<br>
{ability.description}
"""
                    count += 1
                self.ui.Class_abilities.setText(text)
            else:
                self.ui.Class_abilities.setVisible(False)

        # ===== ОСОБЫЕ СПОСОБНОСТИ (FEATURES) =====
        if hasattr(self.ui, 'Class_help1'):
            features = self.dm.get_feature_by_class(class_obj)

            if features:
                feature = features[0]
                self.ui.Class_help1.setText(feature.name)
                self.ui.Class_help1.setVisible(True)
                self.ui.Class_help1.setChecked(False)
                self.ui.Class_help1.setProperty("feature", feature)
            else:
                self.ui.Class_help1.setVisible(False)

        # ===== ПОДКЛАССЫ (SUBCLASSES) =====

        if hasattr(self.ui, 'Class_help2'):
            self.ui.Class_help2.clear()
            subclasses = self.dm.get_all_subclasses_by_class(class_obj)
            if subclasses:
                for subclass in subclasses:
                    item = QListWidgetItem(subclass.name)
                    item.setData(Qt.UserRole, subclass)
                    self.ui.Class_help2.addItem(item)


    def toggle_feature(self):
        """Переключатель: показать/скрыть Class_features"""
        if not hasattr(self.ui, 'Class_features'):
            return

        feature = self.ui.Class_help1.property("feature")
        if not feature:
            return

        if self.ui.Class_help1.isChecked():
            self.ui.Class_features.setStyleSheet("""
                QLabel {
                    background-color: #f8f9fa;
                    border: 1px solid #dee2e6;
                    border-radius: 8px;
                    padding: 15px;
                    font-size: 17px;
                    color: #333;
                }
            """)
            self.ui.Class_features.setText(f"""
<b>{feature.name}</b>
<br>
{feature.description}
""")
            self.ui.Class_features.setVisible(True)
            print(f"Показана фича: {feature.name}")
        else:
            self.ui.Class_features.setVisible(False)
            print(f"Скрыта фича: {feature.name}")

    def show_subclass(self, item):
        """Покаывает данные о подклассе"""

        subclass_obj = item.data(Qt.UserRole)

        if hasattr(self.ui, 'Class_subclass'):
            abilities = self.dm.get_subclass_abilities_by_subclass(subclass_obj)

            text = f"""
<b>{subclass_obj.name}</b>
<br>{subclass_obj.description}"""

            for ability in abilities:
                text = text + f"""<br><br><b>{ability.name}</b> <i>{ability.level} уровень</i> <br> {ability.description}"""

            self.ui.Class_subclass.setStyleSheet("""
                            QLabel {
                                background-color: #f8f9fa;
                                border: 1px solid #dee2e6;
                                border-radius: 8px;
                                padding: 15px;
                                font-size: 17px;
                                color: #333;
                            }
                        """)

            self.ui.Class_subclass.setText(text)



    def set_class_icon(self, class_obj):
        """Устанавливает рисунок класса при отображении информации"""

        if not hasattr(self.ui, 'Class_icon'):
            return

        icon_path = getattr(class_obj, 'image_path', None)
        if not icon_path:
            icon_path = "Data/Avatars/Classes/base.jpg"

        pixmap = QPixmap(icon_path)

        if not pixmap.isNull():
            width = 300
            height = 300

            pixmap = pixmap.scaled(
                width, height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )

            self.ui.Class_icon.setPixmap(pixmap)
            self.ui.Class_icon.setScaledContents(False)
            self.ui.Class_icon.setFixedSize(width, height)
            self.ui.Class_icon.setStyleSheet("""
                QLabel {
                    background-color: #f0f2f5;
                    border: 2px solid #dee2e6;
                    border-radius: 10px;
                }
            """)
            print(f"Картинка загружена: {icon_path}")
        else:
            print(f"Не удалось загрузить: {icon_path}")