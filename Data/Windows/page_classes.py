from PySide6.QtGui import QPixmap

from Data.Windows.base_window import BasePage
from PySide6.QtWidgets import QMessageBox, QListWidgetItem
from PySide6.QtCore import Qt


class ClassesPage(BasePage):
    """Страница с классами"""

    def __init__(self, parent=None, go_back_callback=None):
        super().__init__("Data/Screens/classes.ui", parent)
        self.go_back_callback = go_back_callback
        self.setup_ui()
        self.load_classes()

    def setup_ui(self):
        """Подключаем кнопки"""

        if not self.ui:
            return

        if hasattr(self.ui, 'Button_Back'):
            btn = getattr(self.ui, 'Button_Back')
            btn.clicked.connect(self.go_back)
            print("Подключена кнопка: Button_Back")

        if hasattr(self.ui, 'listWidget'):
            self.ui.listWidget.itemClicked.connect(self.on_class_selected)
            print("Подключена кнопка: listWidget")

        if hasattr(self.ui, 'Class_info'):
            print("Найден лейбл: Class_info")

        if hasattr(self.ui, 'Class_icon'):
            print("Найден лейбл: Class_icon")

        if hasattr(self.ui, 'Class_name'):
            print("Найден лейбл: Class_name")

        if hasattr(self.ui, 'Class_abilities'):
            print("Найден лейбл: Class_abilities")

    def load_classes(self):
        """Загружает список классов"""

        if not hasattr(self.ui, 'listWidget'):
            print("listWidget не найден")
            return

        self.ui.listWidget.clear()

        classes = self.dm.get_all_classes()

        if not classes:
            item = QListWidgetItem("Тут пусто:(")
            item.setData(Qt.UserRole, None)
            self.ui.listWidget.addItem(item)
            return

        for class_obj in classes:
            item = QListWidgetItem(class_obj.name)
            item.setData(Qt.UserRole, class_obj)
            self.ui.listWidget.addItem(item)

        print(f"Загружено классов: {len(classes)}")

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
        <span style="color: #555;">{class_obj.description or 'Нет описания'}</span>
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

        if hasattr(self.ui, 'Class_abilities'):
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
            abilities = self.dm.get_all_class_abilities_by_class(class_obj)
            text = f"""
            """
            for ability in abilities:
                text += f"""
<b>{ability.name}</b>  <i>{ability.level} уровень</i>
<br>

{ability.description}
<br>
<br>"""

            self.ui.Class_abilities.setText(text)

    def set_class_icon(self, class_obj):
        """Устанавливает рисунок класса при отображении информации"""

        if not hasattr(self.ui, 'Class_icon'):
            return

        icon_path = getattr(class_obj, 'image_path', None)

        pixmap = QPixmap(icon_path)

        if not pixmap.isNull():
            label_size = self.ui.Class_icon.size()
            width = self.ui.Class_icon.width()
            height = self.ui.Class_icon.height()

            pixmap = pixmap.scaled(
                width, height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )

            self.ui.Class_icon.setPixmap(pixmap)
            self.ui.Class_icon.setScaledContents(True)
            self.ui.Class_icon.setStyleSheet("""
                            QLabel {
                                background-color: #f0f2f5;
                                border: 2px solid #dee2e6;
                                border-radius: 10px;
                            }
                        """)
            print(f"Картинка загружена: {icon_path}")
        else:
            print(f"Неудалось загрузить : {icon_path}")
            return




