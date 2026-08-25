from Data.Windows.base_window import *

class ClassWindow(BaseWindow):
    """Окно классов"""

    def __init__(self, datamanager, parent=None):
        super().__init__("Классы", datamanager, parent)

