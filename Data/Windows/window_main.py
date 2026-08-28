from PySide6.QtWidgets import QMainWindow, QStackedWidget, QVBoxLayout, QWidget
from Data.Windows.page_main import MainMenuPage
from Data.Windows.page_classes import ClassesPage


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

        # Показываем главное меню
        self.show_page('main')

    def load_pages(self):
        """Загружает все страницы"""
        self.pages = {
            'main': MainMenuPage(self, self.show_page),
            'classes': ClassesPage(self, self.go_back),
            #'items': ItemsPage(self, self.show_page),
            # 'spells': SpellsPage(self, self.show_page),
            # 'races': RacesPage(self, self.show_page),
            # 'backstories': BackstoriesPage(self, self.show_page),
            # 'monsters': MonstersPage(self, self.show_page),
            # 'mechanics': MechanicsPage(self, self.show_page),
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
            'Бестиарий': 'monsters',
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