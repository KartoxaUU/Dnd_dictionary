from PySide6.QtWidgets import QMainWindow, QStackedWidget
from PySide6.QtGui import QShortcut, QKeySequence
from Data.Windows.page_main import MainMenuPage
from Data.Windows.page_classes import ClassesPage
from Data.Windows.page_races import RacesPage
from Data.Windows.page_mechanics import MechanicsPage
from Data.Windows.page_backstrories import BackstoriesPage
from Data.Windows.page_spells import SpellsPage
from Data.Windows.page_bestiary import BestiaryPage


class MainWindow(QMainWindow):
    """Главное окно приложения"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("D&D Dictionary")
        self.resize(1920, 1080)
        self.setMinimumSize(1200, 800)

        # Создаём стек
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Загружаем страницы
        self.pages = {}
        self.load_pages()

        self.shortcut_close()

        # Показываем главное меню
        self.show_page('main')

    def shortcut_close(self):
        self.shortcut_quit = QShortcut(QKeySequence("Esc"), self)
        self.shortcut_quit.activated.connect(self.shortcut_go_back)

    def shortcut_go_back(self):
        """Esc: если на странице открыт диалог — закрыть его, иначе — в главное меню."""
        current = self.stacked_widget.currentWidget()
        # Если страница умеет закрывать диалоги и диалог открыт — закрываем
        if hasattr(current, "close_all_dialogs") and hasattr(current, "is_any_dialog_open"):
            if current.is_any_dialog_open():
                current.close_all_dialogs()
                return
        self.go_back()

    def load_pages(self):
        """Загружает все страницы"""
        self.pages = {
            'main': MainMenuPage(self, self.show_page),
            'classes': ClassesPage(self, self.go_back),
            #'items': ItemsPage(self, self.show_page),
            'spells': SpellsPage(self, self.go_back),
            'races': RacesPage(self, self.go_back),
            'backstories': BackstoriesPage(self, self.go_back),
            'bestiary': BestiaryPage(self, self.go_back),
            'mechanics': MechanicsPage(self, self.go_back),
        }

        # Добавляем все страницы в стек
        for name, page in self.pages.items():
            self.stacked_widget.addWidget(page)
            print(f"Добавлена страница: {name}")

    def show_page(self, page_name):
        """Переключает на указанную страницу"""
        # Нормализуем имена
        page_map = {
            'Предметы': 'items',
            'Классы': 'classes',
            'Заклинания': 'spells',
            'Расы': 'races',
            'Предыстории': 'backstories',
            'Бестиарий': 'bestiary',
            'Механики': 'mechanics',
        }

        # Если передан русский заголовок — преобразуем
        if page_name in page_map:
            page_name = page_map[page_name]

        if page_name in self.pages:
            self.stacked_widget.setCurrentWidget(self.pages[page_name])
            print(f"Переключено на страницу: {page_name}")
            return True
        else:
            print(f"    Страница не найдена: {page_name}")
            return False

    def go_back(self):
        """Возврат в главное меню"""
        self.show_page('main')