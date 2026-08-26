from Data.Windows.base_window import BasePage
from PySide6.QtWidgets import QMessageBox


class MainMenuPage(BasePage):
    """Главная страница с меню"""

    def __init__(self, parent=None, show_page_callback=None):
        super().__init__("Data/Screens/main_menu.ui", parent)
        self.show_page_callback = show_page_callback
        self.setup_ui()

    def setup_ui(self):
        """Подключает кнопки"""
        if not self.ui:
            return

        button_map = {
            'Button_items': lambda: self._on_button_clicked("Предметы"),
            'Button_classes': lambda: self._on_button_clicked("Классы"),
            'Button_Spells': lambda: self._on_button_clicked("Заклинания"),
            'Button_races': lambda: self._on_button_clicked("Расы"),
            'Button_backstories': lambda: self._on_button_clicked("Предыстории"),
            'Button_Bestiary': lambda: self._on_button_clicked("Бестиарий"),
            'Button_mechanics': lambda: self._on_button_clicked("Механики"),
        }

        for btn_name, handler in button_map.items():
            if hasattr(self.ui, btn_name):
                btn = getattr(self.ui, btn_name)
                btn.clicked.connect(handler)
                print(f"Подключена кнопка: {btn_name}")

    def _on_button_clicked(self, page_name):
        """Обработчик нажатия на кнопку меню"""
        # Проверяем, существует ли такая страница
        if self.show_page_callback:
            # Пытаемся переключиться на страницу
            success = self.show_page_callback(page_name)
            if not success:
                self.show_not_implemented(page_name)

    def show_not_implemented(self, feature_name):
        QMessageBox.information(
            self,
            "В разработке",
            f"Раздел '{feature_name}' пока в разработке.\nСкоро появится! 🚀"
        )