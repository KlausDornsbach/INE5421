from control.app_control import AppControl
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication([])
    app_control = AppControl()
    app.exec()

if __name__ == '__main__':
    main()
