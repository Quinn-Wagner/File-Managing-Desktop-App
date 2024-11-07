
import sys
import os
import shutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, 
 QWidget, QLabel, QLineEdit,
)
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

        # GUI for selecting source and target directories

        # Source directory selection
        self.source_dir_label = QLabel("Source Directory:")
        self.source_dir_edit = QLineEdit()
        self.source_dir_edit.setReadOnly(True)
        self.source_dir_button = QPushButton("Browse Source")
        self.source_dir_button.clicked.connect(self.select_source_directory)

        # Target directory selection
        self.target_dir_label = QLabel("Target Directory:")
        self.target_dir_edit = QLineEdit()
        self.target_dir_edit.setReadOnly(True)
        self.target_dir_button = QPushButton("Browse Target")
        self.target_dir_button.clicked.connect(self.select_target_directory)

        # Add to the directory layout
        directory_layout = QHBoxLayout()
        directory_layout.addWidget(self.source_dir_label)
        directory_layout.addWidget(self.source_dir_edit)
        directory_layout.addWidget(self.source_dir_button)

        directory_layout.addWidget(self.target_dir_label)
        directory_layout.addWidget(self.target_dir_edit)
        directory_layout.addWidget(self.target_dir_button)

        # Add directory layout to the main layout
        main_layout.addLayout(directory_layout)

        # Button to move selected files with padding
        self.move_button = QPushButton("Move Selected Files")
        self.move_button.clicked.connect(self.move_selected_files)  # Button click event
        self.move_button.setStyleSheet("padding: 10px; font-size: 14px;")
        main_layout.addWidget(self.move_button, alignment=Qt.AlignCenter)

        # Set central widget layout
        self.central_widget.setLayout(main_layout)

    def select_source_directory(self):
        # Implementation for selecting source directory
        pass

    def select_target_directory(self):
        # Implementation for selecting target directory
        pass

    def move_selected_files(self):
        # Implementation for moving selected files
        pass

# Initialize the application and display the main window
app = QApplication(sys.argv)
window = FileMoverApp()
window.show()
sys.exit(app.exec_())
