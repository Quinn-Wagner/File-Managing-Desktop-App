import sys
import os
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QMessageBox
from PyQt5.QtCore import Qt

class FileMoverApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Mover App")
        self.setGeometry(100, 100, 850, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)

        # Button to move selected files with padding
        self.move_button = QPushButton("Move Selected Files")
        self.move_button.clicked.connect(self.move_selected_files)  # Button click event
        self.move_button.setStyleSheet("padding: 10px; font-size: 14px;")
        main_layout.addWidget(self.move_button, alignment=Qt.AlignCenter)

        # Set central widget layout
        self.central_widget.setLayout(main_layout)

        # Initialize source and target directory variables
        self.source_directory = None
        self.target_directory = None

    def move_selected_files(self):
        # Move selected files from source to target directory
        if not self.source_directory or not self.target_directory:
            QMessageBox.warning(self, "Warning", "Please select or enter both source and target directories.")
            return

        selected_items = self.source_file_list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select files to move.")
            return

        # Confirmation dialog to confirm the move
        file_names = [item.text() for item in selected_items]
        confirm = QMessageBox.question(
            self, "Confirm Move",
            f"Are you sure you want to move the following files?\n\n" + "\n".join(file_names),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            for item in selected_items:
                file_name = item.text()
                source_path = os.path.join(self.source_directory, file_name)
                target_path = os.path.join(self.target_directory, file_name)
                try:
                    shutil.move(source_path, target_path)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to move file {file_name}: {str(e)}")

            # Refresh file lists (assuming there are methods for this)
            self.load_files(self.source_directory, self.source_file_list_widget)
            self.load_files(self.target_directory, self.target_file_list_widget)

    def load_files(self, directory, list_widget):
        list_widget.clear()
        if directory and os.path.exists(directory):
            files = os.listdir(directory)
            for file in files:
                list_widget.addItem(file)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileMoverApp()
    window.show()
    sys.exit(app.exec_())