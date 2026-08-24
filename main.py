import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QStyleFactory, QWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt

from data_manager import DataManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.dm = DataManager()

        # Проверяем, что файл существует
        ui_path = "Data/Screens/main_menu.ui"
        print(f"Ищем файл: {ui_path}")
        print(f"   Абсолютный путь: {os.path.abspath(ui_path)}")
        print(f"   Файл существует: {os.path.exists(ui_path)}")

        self.load_ui()
        self.connect_signals()

    def load_ui(self):
        """Загружает UI из .ui файла"""

        ui_path = "Data/Screens/main_menu.ui"

        if not os.path.exists(ui_path):
            QMessageBox.critical(self, "Ошибка", f"Файл main_menu.ui не найден!")
            sys.exit(1)

        ui_file = QFile(ui_path)
        if not ui_file.open(QFile.ReadOnly):
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл: {ui_path}")
            sys.exit(1)

        loader = QUiLoader()

        # Пробуем загрузить
        print("Загружаем UI...")
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        if not self.ui:
            print("UI не загружен!")
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить интерфейс")
            sys.exit(1)

        print("UI загружен!")
        print(f"   Тип: {type(self.ui)}")
        print(f"   Дочерних виджетов: {len(self.ui.children())}")

        # Проверяем, есть ли виджеты
        for child in self.ui.children():
            print(
                f"   - {child.__class__.__name__}: {child.objectName() if hasattr(child, 'objectName') else 'no name'}")

        # Устанавливаем как центральный виджет
        self.setCentralWidget(self.ui)
        self.setWindowTitle("D&D Dictionary")

        # Устанавливаем размер
        self.resize(1920, 1080)
        self.setMinimumSize(1200, 800)

        # Центрируем
        screen = QApplication.primaryScreen().size()
        self.move(
            (screen.width() - 1920) // 2 if screen.width() > 1920 else 0,
            (screen.height() - 1080) // 2 if screen.height() > 1080 else 0
        )

        # Принудительно показываем виджеты
        self.ui.setVisible(True)
        self.ui.show()

        print(f"   Размер окна: {self.width()} x {self.height()}")
        print(f"   Центральный виджет: {self.centralWidget()}")

    def connect_signals(self):
        """Подключает кнопки к функциям"""
        button_map = {
            'Button_items': self.show_items,
            'Button_classes': self.show_classes,
            'Button_Spells': self.show_spells,
            'Button_races': self.show_races,
            'Button_backstories': self.show_backstories,
            'Button_Bestiary': self.show_monsters,
            'Button_mechanics': self.show_mechanics,
        }

        for name, handler in button_map.items():
            if hasattr(self.ui, name):
                btn = getattr(self.ui, name)
                btn.clicked.connect(handler)
                print(f"Подключена кнопка: {name}")
            else:
                print(f"Кнопка не найдена: {name}")

    def show_not_implemented(self, feature_name):
        QMessageBox.information(
            self,
            "В разработке",
            f"Раздел '{feature_name}' пока в разработке.\nДитенахуй"
        )

    def show_items(self):
        self.show_not_implemented("Предметы")

    def show_classes(self):
        self.show_not_implemented("Классы")

    def show_spells(self):
        self.show_not_implemented("Заклинания")

    def show_races(self):
        self.show_not_implemented("Негры")

    def show_backstories(self):
        self.show_not_implemented("Предыстории")

    def show_monsters(self):
        self.show_not_implemented("Бестиарий")

    def show_mechanics(self):
        self.show_not_implemented("Механики")

    def closeEvent(self, event):
        self.dm.close()
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))

    window = MainWindow()
    window.show()

    print("Приложение запущено!")
    sys.exit(app.exec())


if __name__ == '__main__':
    main()