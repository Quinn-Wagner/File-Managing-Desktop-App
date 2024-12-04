import sys
from PyQt5.QtWidgets import QApplication
from directory_manager import FileMoverApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileMoverApp()
    window.show()
    sys.exit(app.exec_())