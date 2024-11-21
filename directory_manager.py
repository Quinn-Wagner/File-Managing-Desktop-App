import os
import shutil
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from ui_components import setup_ui

from ui_components import setup_ui

class FileMoverApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Mover App")
        self.setGeometry(100, 100, 850, 500)

        self.source_dir_edit, self.source_dir_button, self.source_file_list, self.source_sort_dropdown, \
        self.target_dir_edit, self.target_dir_button, self.target_file_list, self.target_sort_dropdown, \
        self.move_button = setup_ui(self)

        self.source_dir_button.clicked.connect(self.select_source_directory)
        self.target_dir_button.clicked.connect(self.select_target_directory)
        self.move_button.clicked.connect(self.move_selected_files)

        self.source_sort_dropdown.currentIndexChanged.connect(lambda: self.sort_files(self.source_file_list, self.source_dir_edit.text(), self.source_sort_dropdown.currentIndex()))
        self.target_sort_dropdown.currentIndexChanged.connect(lambda: self.sort_files(self.target_file_list, self.target_dir_edit.text(), self.target_sort_dropdown.currentIndex()))


    def select_source_directory(self):
        source_directory = QFileDialog.getExistingDirectory(self, "Select Source Directory")
        if source_directory:
            self.source_dir_edit.setText(source_directory)
            self.load_files(source_directory, self.source_file_list)

    def select_target_directory(self):
        target_directory = QFileDialog.getExistingDirectory(self, "Select Target Directory")
        if target_directory:
            self.target_dir_edit.setText(target_directory)
            self.load_files(target_directory, self.target_file_list)

    def load_files(self, directory, list_widget):
        """
        Load the list of files from the specified directory into the given list widget.
        """
        list_widget.clear()
        if directory and os.path.exists(directory):
            files = os.listdir(directory)
            for file in files:
                list_widget.addItem(file) 

    def move_selected_files(self):
        """
        Move the selected files from the source directory to the target directory.
        """
        source_directory = self.source_dir_edit.text()
        target_directory = self.target_dir_edit.text()
        
        if not source_directory or not target_directory:
            QMessageBox.warning(self, "Warning", "Please select both source and target directories.")
            return

        selected_items = self.source_file_list.selectedItems() 
        if not selected_items:
            QMessageBox.warning(self, "Warning", "No files selected to move.")
            return

        for item in selected_items:
            file_name = item.text()
            source_file_path = os.path.join(source_directory, file_name)
            target_file_path = os.path.join(target_directory, file_name)
            try:
                shutil.move(source_file_path, target_file_path)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error moving file '{file_name}': {str(e)}")
                continue

        self.load_files(source_directory, self.source_file_list)
        self.load_files(target_directory, self.target_file_list)

    def sort_files(self, list_widget, directory, sort_option):
        """
        Sort files in the given list widget based on the selected sort option.
        """
        if not directory or not os.path.exists(directory):
            return

        files = os.listdir(directory)

        if sort_option == 0:  # Sort by File Type (Ascending)
            files.sort(key=lambda x: os.path.splitext(x)[1])
        elif sort_option == 1:  # Sort by File Type (Descending)
            files.sort(key=lambda x: os.path.splitext(x)[1], reverse=True)
        elif sort_option == 2:  # Sort Alphabetically (Ascending)
            files.sort()
        elif sort_option == 3:  # Sort Alphabetically (Descending)
            files.sort(reverse=True)
        elif sort_option == 4:  # Sort by Last Modified Date (Ascending)
            files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)))
        elif sort_option == 5:  # Sort by Last Modified Date (Descending)
            files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)

        # Update the list widget with the sorted files
        list_widget.clear()
        for file in files:
            list_widget.addItem(file)