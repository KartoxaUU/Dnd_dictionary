# Data/Windows/base_window.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import os
from data_manager import DataManager


class BasePage(QWidget):
    """Базовый класс для всех страниц"""
    EN_TO_RU = {
        'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г',
        'i': 'ш', 'o': 'щ', 'p': 'з', '[': 'х', ']': 'ъ',
        'a': 'ф', 's': 'ы', 'd': 'в', 'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о',
        'k': 'л', 'l': 'д', ';': 'ж', "'": 'э',
        'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь',
        ',': 'б', '.': 'ю', '/': '.'
    }

    RU_TO_EN = {v: k for k, v in EN_TO_RU.items()}

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

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui)

        print(f"Загружен UI: {self.ui_path}")

    def setup_ui(self):
        """Метод для настройки UI (переопределяется в наследниках)"""
        pass

    def fix_keyboard_layout(self, text):
        """
        Исправляет текст, если он был введён в неправильной раскладке.
        Если текст содержит больше английских букв — переводим с английской на русскую.
        Если больше русских — переводим с русской на английскую.
        """
        if not text:
            return text
        en_count = sum(1 for ch in text if ch.lower() in self.EN_TO_RU)
        ru_count = sum(1 for ch in text if ch.lower() in self.RU_TO_EN)
        if en_count > ru_count:
            return ''.join(self.EN_TO_RU.get(ch.lower(), ch) for ch in text)
        elif ru_count > en_count:
            return ''.join(self.RU_TO_EN.get(ch.lower(), ch) for ch in text)
        else:
            return text

    def create_search_filter(self, search_text, name_getter):
        """
        Создаёт функцию-фильтр для поиска с учётом раскладки.
        """
        search_text = search_text.strip().lower()
        if not search_text:
            return lambda obj: True
        variants = [search_text]
        fixed = self.fix_keyboard_layout(search_text)
        if fixed and fixed != search_text:
            variants.append(fixed)

        # Создаём функцию-фильтр
        def filter_func(obj):
            name = name_getter(obj).lower()
            # Проверяем каждый вариант
            for variant in variants:
                if variant in name:
                    return True
            return False

        return filter_func

    def filter_items_by_name(self, items, search_text, name_getter):
        """
        Универсальный метод для фильтрации списка объектов по названию
        с учётом неправильной раскладки.
        """
        if not search_text or not search_text.strip():
            return items

        filter_func = self.create_search_filter(search_text, name_getter)
        return list(filter(filter_func, items))

    def closeEvent(self, event):
        self.dm.close()
        event.accept()