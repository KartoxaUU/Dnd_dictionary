from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt

class BaseWindow(QWidget):
    def __init__(self, title: str, data_manager, parent=None):
        super().__init__(parent)
        self.dm = data_manager
        self.window_title = title

        self.setWindowTitle(f"D&D Assistant - {self.window_title}")
        self.setGeometry(200, 200, 1200, 800)
        self.setMinimumSize(1200, 800)

        self.setup_ui()
        self.show()

    def setup_ui(self):
        """Создает базовый интерфейс"""

        layout = QVBoxLayout()

        title_label = QLabel(f"📚 {self.window_title}")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Блок "В разработке"
        dev_label = QLabel("🚧 В разработке")
        dev_label.setStyleSheet("font-size: 36px; color: #888;")
        dev_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(dev_label)

        dev_desc = QLabel("Этот раздел будет реализован в ближайшее время")
        dev_desc.setStyleSheet("font-size: 16px; color: #aaa;")
        dev_desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(dev_desc)

        layout.addStretch()

        # Кнопка назад
        back_btn = QPushButton("← Назад")
        back_btn.clicked.connect(self.close)
        back_btn.setMaximumWidth(200)
        back_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #4a4a4a;
                        color: white;
                        border-radius: 8px;
                        padding: 10px;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background-color: #5a5a5a;
                    }
                """)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(back_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

    def center_window(self):
        """Центрирует окно на экране"""
        screen = self.screen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
