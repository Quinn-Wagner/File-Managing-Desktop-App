import os
import shutil
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from ui_components import setup_ui

class FileMoverApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Managing App")
        self.setGeometry(100, 100, 850, 500)

        self.source_dir_edit, self.source_dir_button, self.source_sort_dropdown, self.source_file_list, \
        self.target_dir_edit, self.target_dir_button, self.target_sort_dropdown, self.target_file_list, \
        self.move_button, self.delete_button, self.copy_button = setup_ui(self)

        self.source_dir_button.clicked.connect(self.select_source_directory)
        self.target_dir_button.clicked.connect(self.select_target_directory)
        self.move_button.clicked.connect(self.move_selected_files)
        self.delete_button.clicked.connect(self.delete_selected_files)
        self.copy_button.clicked.connect(self.copy_selected_files)

        self.source_sort_dropdown.currentIndexChanged.connect(
            lambda: self.sort_files(self.source_file_list, self.source_dir_edit.text(), self.source_sort_dropdown.currentIndex())
        )
        self.target_sort_dropdown.currentIndexChanged.connect(
            lambda: self.sort_files(self.target_file_list, self.target_dir_edit.text(), self.target_sort_dropdown.currentIndex())
        )

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
        list_widget.clear()
        if directory and os.path.exists(directory):
            files = os.listdir(directory)
            for file in files:
                list_widget.addItem(file)
                
    def is_directory(self, path):
        return os.path.isdir(path)
    
    def confirm_action(self, action, item_name):
        response = QMessageBox.question(self, "Confirm Action", f"Are you sure you want to {action} '{item_name}'?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return response == QMessageBox.Yes

    def move_selected_files(self):
        selected_items = self.source_file_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "No files or directories selected to move.")
            return

        source_directory = self.source_dir_edit.text()
        target_directory = self.target_dir_edit.text()

        if not source_directory or not target_directory:
            QMessageBox.warning(self, "Warning", "Please select both source and target directories.")
            return

        for item in selected_items:
            file_name = item.text()
            source_file_path = os.path.join(source_directory, file_name)
            target_file_path = os.path.join(target_directory, file_name)

            if self.confirm_action("move", file_name):
                try:
                    shutil.move(source_file_path, target_file_path)
                except PermissionError:
                    QMessageBox.warning(self, "Permission Denied", f"You do not have permission to move '{file_name}'.")
                    continue
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Error moving file '{file_name}': {str(e)}")
                    continue

        self.load_files(source_directory, self.source_file_list)
        self.load_files(target_directory, self.target_file_list)

    def delete_selected_files(self):
        selected_items = self.source_file_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "No files or directories selected to delete.")
            return

        source_directory = self.source_dir_edit.text()

        if not source_directory:
            QMessageBox.warning(self, "Warning", "Please select a source directory.")
            return

        for item in selected_items:
            file_name = item.text()
            file_path = os.path.join(source_directory, file_name)

            if self.confirm_action("delete", file_name):
                if self.is_directory(file_path):
                    try:
                        shutil.rmtree(file_path)
                    except PermissionError:
                        QMessageBox.warning(self, "Permission Denied", f"You do not have permission to delete '{file_name}'.")
                        continue
                    except Exception as e:
                        QMessageBox.warning(self, "Error", f"Error deleting directory '{file_name}': {str(e)}")
                        continue
                else:
                    try:
                        os.remove(file_path)
                    except PermissionError:
                        QMessageBox.warning(self, "Permission Denied", f"You do not have permission to delete '{file_name}'.")
                        continue
                    except Exception as e:
                        QMessageBox.warning(self, "Error", f"Error deleting file '{file_name}': {str(e)}")
                        continue

        self.load_files(source_directory, self.source_file_list)

    def copy_selected_files(self):
        selected_items = self.source_file_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "No files or directories selected to copy.")
            return

        source_directory = self.source_dir_edit.text()
        target_directory = self.target_dir_edit.text()

        if not source_directory or not target_directory:
            QMessageBox.warning(self, "Warning", "Please select both source and target directories.")
            return

        for item in selected_items:
            file_name = item.text()
            source_file_path = os.path.join(source_directory, file_name)
            target_file_path = os.path.join(target_directory, file_name)

            if self.confirm_action("copy", file_name):
                if self.is_directory(source_file_path):
                    try:
                        shutil.copytree(source_file_path, target_file_path)
                    except PermissionError:
                        QMessageBox.warning(self, "Permission Denied", f"You do not have permission to copy '{file_name}'.")
                        continue
                    except Exception as e:
                        QMessageBox.warning(self, "Error", f"Error copying directory '{file_name}': {str(e)}")
                        continue
                else:
                    try:
                        shutil.copy(source_file_path, target_file_path)
                    except PermissionError:
                        QMessageBox.warning(self, "Permission Denied", f"You do not have permission to copy '{file_name}'.")
                        continue
                    except Exception as e:
                        QMessageBox.warning(self, "Error", f"Error copying file '{file_name}': {str(e)}")
                        continue

        self.load_files(source_directory, self.source_file_list)
        self.load_files(target_directory, self.target_file_list)

    def sort_files(self, list_widget, directory, sort_option):
        if not directory or not os.path.exists(directory):
            return

        files = os.listdir(directory)

        if sort_option == 0:
            files.sort(key=lambda x: os.path.splitext(x)[1])
        elif sort_option == 1:
            files.sort(key=lambda x: os.path.splitext(x)[1], reverse=True)
        elif sort_option == 2:
            files.sort()
        elif sort_option == 3:
            files.sort(reverse=True)
        elif sort_option == 4:
            files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)))
        elif sort_option == 5:
            files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)

        list_widget.clear()
        for file in files:
            list_widget.addItem(file)