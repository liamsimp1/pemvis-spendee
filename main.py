import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile
from ui.main_window import MainWindow

def load_stylesheet(app):
    style_file = QFile("style.qss")
    if style_file.open(QFile.ReadOnly | QFile.Text):
        stylesheet = style_file.readAll().data().decode()
        app.setStyleSheet(stylesheet)
        style_file.close()
        return True
    else:
        return False

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { background-color: #ffffff; }")
    
    from database.init_db import initialize_database
    initialize_database()
    
    load_stylesheet(app)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()