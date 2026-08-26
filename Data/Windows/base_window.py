from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import os
from data_manager import DataManager


class BasePage(QWidget):
    """Базовый класс для всех страниц"""

    def __init__(self, ui_path, parent=None):
        super().__init__(parent)
        self.dm = DataManager()
        self.ui_path = ui_path
        self.ui = None

        self.load_ui()
        self.setup_ui()

    def load_ui(self):
        """Загружает UI из .ui файла"""
        if not os.path.exists(self.ui_path):
            QMessageBox.critical(self, "Ошибка", f"Файл {self.ui_path} не найден!")
            return

        ui_file = QFile(self.ui_path)
        if not ui_file.open(QFile.ReadOnly):
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл: {self.ui_path}")
            return

        loader = QUiLoader()
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        if not self.ui:
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить интерфейс")
            return

        # Добавляем UI в layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui)

        print(f"Загружен UI: {self.ui_path}")

    def setup_ui(self):
        """Метод для настройки UI (переопределяется в наследниках)"""
        pass

    def closeEvent(self, event):
        self.dm.close()
        event.accept()