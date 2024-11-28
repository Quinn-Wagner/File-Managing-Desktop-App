from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel, QLineEdit, QListWidget, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView
 
def setup_ui(window):
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(25, 10, 25, 25)
    main_layout.setSpacing(20)
    directory_layout = QHBoxLayout()
    source_dir_edit, source_dir_button, source_sort_dropdown, source_file_list = create_directory_widgets_with_filter("Source Directory:")
    source_file_list.setSelectionMode(QAbstractItemView.MultiSelection)  # Enable multi-selection
    directory_layout.addLayout(create_directory_layout("Source Directory", source_dir_edit, source_dir_button, source_sort_dropdown, source_file_list))
    target_dir_edit, target_dir_button, target_sort_dropdown, target_file_list = create_directory_widgets_with_filter("Target Directory:")
    target_file_list.setSelectionMode(QAbstractItemView.MultiSelection)  # Enable multi-selection
    directory_layout.addLayout(create_directory_layout("Target Directory", target_dir_edit, target_dir_button, target_sort_dropdown, target_file_list))
    main_layout.addLayout(directory_layout)
    move_button = QPushButton("Move Selected Files")
    move_button.setStyleSheet("padding: 10px; font-size: 14px;")
    main_layout.addWidget(move_button, alignment=Qt.AlignCenter)
    central_widget.setLayout(main_layout)
    return source_dir_edit, source_dir_button, source_sort_dropdown, source_file_list, \
           target_dir_edit, target_dir_button, target_sort_dropdown, target_file_list, move_button
 
def create_directory_widgets_with_filter(label_text):
    dir_edit = QLineEdit()
    dir_edit.setReadOnly(True)
    dir_button = QPushButton(f"Browse {label_text.split()[0]}")
    sort_dropdown = QComboBox()
    sort_dropdown.addItems([
        "Sort by File Type (Ascending)",
        "Sort by File Type (Descending)",
        "Sort Alphabetically (Ascending)",
        "Sort Alphabetically (Descending)",
        "Sort by Last Modified Date (Ascending)",
        "Sort by Last Modified Date (Descending)"
    ])
    file_list = QListWidget()
    return dir_edit, dir_button, sort_dropdown, file_list
 
def create_directory_layout(label_text, dir_edit, dir_button, sort_dropdown, file_list):
    layout = QVBoxLayout()
    button_layout = QHBoxLayout()
    button_layout.addWidget(dir_edit)
    button_layout.addWidget(dir_button)
    label = QLabel(f"<b>{label_text}</b>")  # Bold text
    label.setStyleSheet("font-size: 16px;")  # Set font size (double typical size)
    layout.addWidget(label)
    layout.addLayout(button_layout)
    layout.addWidget(sort_dropdown)
    layout.addWidget(file_list)
    return layout
