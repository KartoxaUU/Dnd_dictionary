from Data.Windows.base_window import BasePage
from PySide6.QtWidgets import QMessageBox


class ClassesPage(BasePage):
    """Страница с классами"""

    def __init__(self, parent=None, go_back_callback=None):
        super().__init__("Data/Screens/classes.ui", parent)
