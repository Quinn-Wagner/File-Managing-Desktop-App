import sys
import os
import shutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, 
    QWidget, QLabel, QLineEdit, QListWidget, QFileDialog, QMessageBox
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

        # Directory layout to hold source and target side by side
        directory_layout = QHBoxLayout()

        # Source directory layout
        source_layout = QVBoxLayout()
        source_layout.setSpacing(10)
        
        # Source directory selection widgets
        source_button_layout = QHBoxLayout()  # Horizontal layout for input and button
        self.source_dir_edit = QLineEdit()
        self.source_dir_edit.setReadOnly(True)
        self.source_dir_button = QPushButton("Browse Source")
        self.source_dir_button.clicked.connect(self.select_source_directory)
        source_button_layout.addWidget(self.source_dir_edit)
        source_button_layout.addWidget(self.source_dir_button)

        # Add source label, button layout, and file list to source layout
        source_layout.addWidget(QLabel("Source Directory:"))
        source_layout.addLayout(source_button_layout)
        source_layout.addWidget(QLabel("Source Directory Files:"))
        self.source_file_list = QListWidget()
        source_layout.addWidget(self.source_file_list)

        # Target directory layout
        target_layout = QVBoxLayout()
        target_layout.setSpacing(10)
        
        # Target directory selection widgets
        target_button_layout = QHBoxLayout()  # Horizontal layout for input and button
        self.target_dir_edit = QLineEdit()
        self.target_dir_edit.setReadOnly(True)
        self.target_dir_button = QPushButton("Browse Target")
        self.target_dir_button.clicked.connect(self.select_target_directory)
        target_button_layout.addWidget(self.target_dir_edit)
        target_button_layout.addWidget(self.target_dir_button)

        # Add target label, button layout, and file list to target layout
        target_layout.addWidget(QLabel("Target Directory:"))
        target_layout.addLayout(target_button_layout)
        target_layout.addWidget(QLabel("Target Directory Files:"))
        self.target_file_list = QListWidget()
        target_layout.addWidget(self.target_file_list)

        # Add both source and target layouts to the directory layout
        directory_layout.addLayout(source_layout)
        directory_layout.addLayout(target_layout)

        # Add directory layout to the main layout
        main_layout.addLayout(directory_layout)

        # Move button to move selected files
        self.move_button = QPushButton("Move Selected Files")
        self.move_button.clicked.connect(self.move_selected_files)
        self.move_button.setStyleSheet("padding: 10px; font-size: 14px;")
        main_layout.addWidget(self.move_button, alignment=Qt.AlignCenter)

        # Set the main layout for the central widget
        self.central_widget.setLayout(main_layout)

    def select_source_directory(self):
        """
        Open a file dialog to select the source directory and load the files.
        """
        source_directory = QFileDialog.getExistingDirectory(self, "Select Source Directory")
        if source_directory:
            self.source_dir_edit.setText(source_directory)  # Set the path in the input box
            self.load_files(source_directory, self.source_file_list)

    def select_target_directory(self):
        """
        Open a file dialog to select the target directory and load the files.
        """
        target_directory = QFileDialog.getExistingDirectory(self, "Select Target Directory")
        if target_directory:
            self.target_dir_edit.setText(target_directory)  # Set the path in the input box
            self.load_files(target_directory, self.target_file_list)

    def load_files(self, directory, list_widget):
        """
        Load the list of files from the specified directory into the given list widget.
        """
        list_widget.clear()  # Clear any existing files in the list widget
        if directory and os.path.exists(directory):  # Check if the directory exists
            files = os.listdir(directory)  # Get the list of files
            for file in files:
                list_widget.addItem(file)  # Add each file to the list widget

    def move_selected_files(self):
        """
        Move the selected files from the source directory to the target directory.
        """
        source_directory = self.source_dir_edit.text()
        target_directory = self.target_dir_edit.text()
        
        # Check if directories are set
        if not source_directory or not target_directory:
            QMessageBox.warning(self, "Warning", "Please select both source and target directories.")
            return

        selected_items = self.source_file_list.selectedItems()  # Get the selected files
        if not selected_items:
            QMessageBox.warning(self, "Warning", "No files selected to move.")
            return

        # Move each selected file to the target directory
        for item in selected_items:
            file_name = item.text()
            source_file_path = os.path.join(source_directory, file_name)
            target_file_path = os.path.join(target_directory, file_name)
            try:
                shutil.move(source_file_path, target_file_path)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error moving file '{file_name}': {str(e)}")
                continue

        # Refresh the list widgets after the move
        self.load_files(source_directory, self.source_file_list)
        self.load_files(target_directory, self.target_file_list)

# Initialize the application and display the main window
app = QApplication(sys.argv)
window = FileMoverApp()
window.show()
sys.exit(app.exec_())