from PySide6.QtGui import QPixmap

from Data.Windows.base_window import BasePage
from PySide6.QtWidgets import QMessageBox, QListWidgetItem
from PySide6.QtCore import Qt


class MechanicsPage(BasePage):
    """Страница с механиками"""

    def __init__(self, parent=None, go_back_callback=None):
        super().__init__("Data/Screens/mechanics.ui", parent)
        self.go_back_callback = go_back_callback
        self.all_mechanics = []

        self.setup_ui()
        self.load_mechanics()

    def setup_ui(self):
        """Подключаем кнопки"""

        if not self.ui:
            return

        if hasattr(self.ui, 'btn_back'):
            btn = getattr(self.ui, 'btn_back')
            btn.clicked.connect(self.go_back)
            print("Подключена кнопка: btn_back")

        if hasattr(self.ui, 'search_input'):
            self.ui.search_input.textChanged.connect(self.filter_mechanics)

        if hasattr(self.ui, 'listWidget'):
            self.ui.listWidget.itemClicked.connect(self.on_mechanic_selected)
            print("Подключена кнопка: listWidget")

        if hasattr(self.ui, 'Rule_name'):
            self.ui.Rule_name.setTextFormat(Qt.RichText)
            print("Найден лейбл: Rule_name")

        if hasattr(self.ui, 'Rule_description'):
            self.ui.Rule_name.setTextFormat(Qt.RichText)
            print("Найден лейбл: Rule_description")


    def load_mechanics(self):
        """Загружает список механик"""

        if not hasattr(self.ui, 'listWidget'):
            print("listWidget не найден")
            return

        self.ui.listWidget.clear()

        self.all_mechanics = self.dm.get_all_rules()

        if not self.all_mechanics:
            item = QListWidgetItem("Тут пусто:(")
            item.setData(Qt.UserRole, None)
            self.ui.listWidget.addItem(item)
            return

        self.display_mechanics(self.all_mechanics)
        print(f"Загружено механик: {len(self.all_mechanics)}")

    def filter_mechanics(self, search_text):
        """Фильтрует механики по названию"""

        if not hasattr(self.ui, 'search_input'):
            return

        search_text = search_text.strip().lower()

        if not search_text:
            self.display_mechanics(self.all_mechanics)
            return

        filtred = self.filter_items_by_name(
            self.all_mechanics,
            search_text,
            lambda x: x.name
        )

        self.display_mechanics(filtred)
        print(f"Найдено механик: {len(filtred)}")

    def display_mechanics(self, mechanics):
        """Отображает список механик"""

        if not hasattr(self.ui, 'listWidget'):
            return

        self.ui.listWidget.clear()


        for mechanic_obj in mechanics:
            item = QListWidgetItem(mechanic_obj.name)
            item.setData(Qt.UserRole, mechanic_obj)
            self.ui.listWidget.addItem(item)

    def go_back(self):
        """Возврат в главное меню"""
        print("Возврат в главное меню")
        if self.go_back_callback:
            self.go_back_callback()
        else:
            print("go_back_callback не передан!")

    def on_mechanic_selected(self, item):
        """Обработчик выбора механики из списка"""
        mechanic_obj = item.data(Qt.UserRole)

        if not mechanic_obj:
            QMessageBox.information(self, "Информация", "Механика не найдена в БД")
            return

        print(f"\nВыбрана механика: {mechanic_obj.name}")
        self.show_mechanic_details(mechanic_obj)

    def show_mechanic_details(self, mechanic_obj):
        """Выводит данные о расе"""

        if hasattr(self.ui, 'Rule_name'):
            self.ui.Rule_name.setStyleSheet("""
                                            QLabel {
                                                background-color: #f8f9fa;
                                                border: 1px solid #dee2e6;
                                                border-radius: 8px;
                                                padding: 15px;
                                                font-size: 50px;
                                                color: #333;
                                            }""")
            self.ui.Rule_name.setText(f"""<b>{mechanic_obj.name}</b>""")

        if hasattr(self.ui, 'Rule_description'):
            self.ui.Rule_description.setStyleSheet("""
                                                    QLabel {
                                                        background-color: #f8f9fa;
                                                        border: 1px solid #dee2e6;
                                                        border-radius: 8px;
                                                        padding: 15px;
                                                        font-size: 15px;
                                                        color: #333;
                                                    }""")
            self.ui.Rule_description.setText(mechanic_obj.description)








