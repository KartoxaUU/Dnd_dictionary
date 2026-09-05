from PySide6.QtGui import QPixmap

from Data.Windows.base_window import BasePage
from PySide6.QtWidgets import QMessageBox, QListWidgetItem
from PySide6.QtCore import Qt


class RacesPage(BasePage):
    """Страница с расами"""

    def __init__(self, parent=None, go_back_callback=None):
        super().__init__("Data/Screens/races.ui", parent)
        self.go_back_callback = go_back_callback
        self.all_races = []

        self.setup_ui()
        self.load_races()

    def setup_ui(self):
        """Подключаем кнопки"""

        if not self.ui:
            return

        if hasattr(self.ui, 'btn_back'):
            btn = getattr(self.ui, 'btn_back')
            btn.clicked.connect(self.go_back)
            print("Подключена кнопка: btn_back")

        if hasattr(self.ui, 'search_input'):
            self.ui.search_input.textChanged.connect(self.filter_races)

        if hasattr(self.ui, 'listWidget'):
            self.ui.listWidget.itemClicked.connect(self.on_race_selected)
            print("Подключена кнопка: listWidget")

        if hasattr(self.ui, 'Race_info'):
            print("Найден лейбл: Race_info")

        if hasattr(self.ui, 'Race_icon'):
            print("Найден лейбл: Race_icon")

        if hasattr(self.ui, 'Race_name'):
            print("Найден лейбл: Race_name")

        if hasattr(self.ui, 'Race_abilities'):
            print("Найден лейбл: Race_abilities")


    def load_races(self):
        """Загружает список рас"""

        if not hasattr(self.ui, 'listWidget'):
            print("listWidget не найден")
            return

        self.ui.listWidget.clear()

        self.all_races = self.dm.get_all_races()

        if not self.all_races:
            item = QListWidgetItem("Тут пусто:(")
            item.setData(Qt.UserRole, None)
            self.ui.listWidget.addItem(item)
            return

        self.display_races(self.all_races)
        print(f"Загружено рас: {len(self.all_races)}")

    def filter_races(self, search_text):
        """Фильтрует расы по названию"""

        if not hasattr(self.ui, 'search_input'):
            return

        search_text = search_text.strip().lower()

        if not search_text:
            self.display_races(self.all_races)
            return

        filtred = self.filter_items_by_name(
            self.all_races,
            search_text,
            lambda x: x.name
        )

        self.display_races(filtred)
        print(f"Найдено рас: {len(filtred)}")

    def display_races(self, races):
        """Отображает список рас"""

        if not hasattr(self.ui, 'listWidget'):
            return

        self.ui.listWidget.clear()


        for race_obj in races:
            item = QListWidgetItem(race_obj.name)
            item.setData(Qt.UserRole, race_obj)
            self.ui.listWidget.addItem(item)

    def go_back(self):
        """Возврат в главное меню"""
        print("Возврат в главное меню")
        if self.go_back_callback:
            self.go_back_callback()
        else:
            print("go_back_callback не передан!")

    def on_race_selected(self, item):
        """Обработчик выбора расы из списка"""
        race_obj = item.data(Qt.UserRole)

        if not race_obj:
            QMessageBox.information(self, "Информация", "Раса не найдена в БД")
            return

        print(f"\nВыбрана раса: {race_obj.name}")
        self.show_race_details(race_obj)

    def show_race_details(self, race_obj):
        """Выводит данные о расе"""

        if not hasattr(self.ui, 'Race_info'):
            print("Race_info не найден")
            return

        self.set_race_icon(race_obj)

        if hasattr(self.ui, 'Race_name'):
            self.ui.Race_name.setText(f"<b>{race_obj.name}</b>")
            self.ui.Race_name.setStyleSheet("""
                        QLabel {
                            background-color: #f8f9fa;
                            border: 1px solid #dee2e6;
                            border-radius: 8px;
                            padding: 15px;
                            font-size: 50px;
                            color: #333;
                        }""")

        if hasattr(self.ui, 'Race_info'):
            self.ui.Race_info.setText(race_obj.description)
            self.ui.Race_info.setStyleSheet("""
                        QLabel {
                            background-color: #f8f9fa;
                            border: 1px solid #dee2e6;
                            border-radius: 8px;
                            padding: 15px;
                            font-size: 17px;
                            color: #333;
                        }""")

        if hasattr(self.ui, 'Race_abilities'):
            abilities = ""
            race_abilities = self.dm.get_race_abilities_by_race(race_obj)
            for ability in race_abilities:
                abilities = abilities + f"""
<b>{ability.name}</b>.<br> {ability.description}<br>"""

            text = f"""
            <b>Увеличение характеристик:</b> {race_obj.stats_bonus}
            <br>
            <b>Продолжительность жизни:</b> {race_obj.age}
            <br>
            <b>Размер:</b> {race_obj.size}
            <br>
            <b>Скорость:</b> {race_obj.speed} футов
            <br>
            {abilities}
            <b>Языки:</b> {race_obj.languages}
            """
            self.ui.Race_abilities.setStyleSheet("""
                                    QLabel {
                                        background-color: #f8f9fa;
                                        border: 1px solid #dee2e6;
                                        border-radius: 8px;
                                        padding: 15px;
                                        font-size: 17px;
                                        color: #333;
                                    }""")
            self.ui.Race_abilities.setText(text)


    def set_race_icon(self, race_obj):
        """Устанавливает рисунок класса при отображении информации"""

        if not hasattr(self.ui, 'Race_icon'):
            return

        icon_path = getattr(race_obj, 'image_path', None)

        pixmap = QPixmap(icon_path)

        if not pixmap.isNull():
            width = 300
            height = 300

            pixmap = pixmap.scaled(
                width, height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )

            self.ui.Race_icon.setPixmap(pixmap)
            self.ui.Race_icon.setScaledContents(True)
            self.ui.Race_icon.setStyleSheet("""
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




