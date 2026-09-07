from Data.Windows.base_window import BasePage
from PySide6.QtWidgets import QMessageBox, QListWidgetItem
from PySide6.QtCore import Qt


class BackstoriesPage(BasePage):
    """Страница с предысториями"""

    def __init__(self, parent=None, go_back_callback=None):
        super().__init__("Data/Screens/backstories.ui", parent)
        self.go_back_callback = go_back_callback
        self.all_backstories = []

        self.setup_ui()
        self.load_backstories()

    def setup_ui(self):
        """Подключаем кнопки"""

        if not self.ui:
            return

        if hasattr(self.ui, 'btn_back'):
            btn = getattr(self.ui, 'btn_back')
            btn.clicked.connect(self.go_back)
            print("Подключена кнопка: btn_back")

        if hasattr(self.ui, 'search_input'):
            self.ui.search_input.textChanged.connect(self.filter_backstories)

        if hasattr(self.ui, 'listWidget'):
            self.ui.listWidget.itemClicked.connect(self.on_backstory_selected)
            print("Подключена кнопка: listWidget")

        if hasattr(self.ui, 'Backstory_name'):
            self.ui.Backstory_name.setTextFormat(Qt.RichText)
            print("Найден лейбл: Backstory_name")

        if hasattr(self.ui, 'Backstory_description'):
            self.ui.Backstory_name.setTextFormat(Qt.RichText)
            print("Найден лейбл: Backstory_description")


    def load_backstories(self):
        """Загружает список предысторий"""

        if not hasattr(self.ui, 'listWidget'):
            print("listWidget не найден")
            return

        self.ui.listWidget.clear()

        self.all_backstories = self.dm.get_all_backstories()

        if not self.all_backstories:
            item = QListWidgetItem("Тут пусто:(")
            item.setData(Qt.UserRole, None)
            self.ui.listWidget.addItem(item)
            return

        self.display_backstories(self.all_backstories)
        print(f"Загружено предысторий: {len(self.all_backstories)}")

    def filter_backstories(self, search_text):
        """Фильтрует предыстории по названию"""

        if not hasattr(self.ui, 'search_input'):
            return

        search_text = search_text.strip().lower()

        if not search_text:
            self.display_backstories(self.all_backstories)
            return

        filtred = self.filter_items_by_name(
            self.all_backstories,
            search_text,
            lambda x: x.name
        )

        self.display_backstories(filtred)
        print(f"Найдено предысторий: {len(filtred)}")

    def display_backstories(self, backstories):
        """Отображает список предысторий"""

        if not hasattr(self.ui, 'listWidget'):
            return

        self.ui.listWidget.clear()


        for backstory_obj in backstories:
            item = QListWidgetItem(backstory_obj.name)
            item.setData(Qt.UserRole, backstory_obj)
            self.ui.listWidget.addItem(item)

    def go_back(self):
        """Возврат в главное меню"""
        print("Возврат в главное меню")
        if self.go_back_callback:
            self.go_back_callback()
        else:
            print("go_back_callback не передан!")

    def on_backstory_selected(self, item):
        """Обработчик выбора предыстории из списка"""
        backstory_obj = item.data(Qt.UserRole)

        if not backstory_obj:
            QMessageBox.information(self, "Информация", "Предыстория не найдена в БД")
            return

        print(f"\nВыбрана предыстория: {backstory_obj.name}")
        self.show_backstory_details(backstory_obj)

    def show_backstory_details(self, backstory_obj):
        """Выводит данные о предыстории"""

        if hasattr(self.ui, 'Backstory_name'):
            self.ui.Backstory_name.setStyleSheet("""
                                            QLabel {
                                                background-color: #f8f9fa;
                                                border: 1px solid #dee2e6;
                                                border-radius: 8px;
                                                padding: 15px;
                                                font-size: 50px;
                                                color: #333;
                                            }""")
            self.ui.Backstory_name.setText(f"""<b>{backstory_obj.name}</b>""")

        if hasattr(self.ui, 'Backstory_description'):
            self.ui.Backstory_description.setStyleSheet("""
                                                    QLabel {
                                                        background-color: #f8f9fa;
                                                        border: 1px solid #dee2e6;
                                                        border-radius: 8px;
                                                        padding: 15px;
                                                        font-size: 17px;
                                                        color: #333;
                                                    }""")

            text = f"""
{backstory_obj.description}<br>
<b>Владение навыками:</b>{backstory_obj.possesion_skills}<br>
<b>Владение инструментами:</b>{backstory_obj.possesion_instruments}<br>"""

            if backstory_obj.possesion_languages:
                text += f"""{backstory_obj.possesion_languages}<br>"""

            text += f"""{backstory_obj.equipment}<br><br>
<b>Умение:{backstory_obj.skill_name}</b><br>
{backstory_obj.skill_description}"""

            self.ui.Backstory_description.setText(text)








