import sys
from PySide6.QtWidgets import QApplication, QStyleFactory
from Data.Windows.window_main import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))

    window = MainWindow()
    window.show()
    window.raise_()
    window.activateWindow()

    print("Приложение запущено!")
    sys.exit(app.exec())


if __name__ == '__main__':
    main()