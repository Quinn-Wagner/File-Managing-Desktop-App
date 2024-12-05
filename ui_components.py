from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel, QLineEdit, QListWidget, QComboBox, QCompleter
)
from PyQt5.QtCore import Qt, QDir
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileSystemModel, QAbstractItemView


def setup_ui(window):
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(25, 10, 25, 25)
    main_layout.setSpacing(20)

    directory_layout = QHBoxLayout()
    source_dir_edit, source_dir_button, source_sort_dropdown, source_file_list = create_directory_widgets_with_filter("Source Directory:")
    source_file_list.setSelectionMode(QAbstractItemView.MultiSelection)
    directory_layout.addLayout(create_directory_layout("Source Directory", source_dir_edit, source_dir_button, source_sort_dropdown, source_file_list))

    target_dir_edit, target_dir_button, target_sort_dropdown, target_file_list = create_directory_widgets_with_filter("Target Directory:")
    target_file_list.setSelectionMode(QAbstractItemView.MultiSelection)
    directory_layout.addLayout(create_directory_layout("Target Directory", target_dir_edit, target_dir_button, target_sort_dropdown, target_file_list))

    main_layout.addLayout(directory_layout)
    move_button = QPushButton("Move Selected Files")
    move_button.setStyleSheet("padding: 10px; font-size: 14px;")
    delete_button = QPushButton("Delete Selected Files")
    delete_button.setStyleSheet("padding: 10px; font-size: 14px;")
    copy_button = QPushButton("Copy Selected Files")
    copy_button.setStyleSheet("padding: 10px; font-size: 14px;")
    
    operation_buttons_layout = QHBoxLayout()
    operation_buttons_layout.addWidget(move_button)
    operation_buttons_layout.addWidget(delete_button)
    operation_buttons_layout.addWidget(copy_button)
    main_layout.addLayout(operation_buttons_layout)
    main_layout.setAlignment(Qt.AlignCenter)

    central_widget.setLayout(main_layout)

    setup_directory_autocomplete(source_dir_edit, source_file_list)
    setup_directory_autocomplete(target_dir_edit, target_file_list)

    return source_dir_edit, source_dir_button, source_sort_dropdown, source_file_list, \
           target_dir_edit, target_dir_button, target_sort_dropdown, target_file_list, move_button, delete_button, copy_button


def create_directory_widgets_with_filter(label_text):
    dir_edit = QLineEdit()
    dir_button = QPushButton()
    dir_button.setIcon(QIcon("images/folder.png"))
    dir_button.setToolTip(f"Browse {label_text.split()[0]}")

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
    label = QLabel(f"<b>{label_text}</b>")
    label.setStyleSheet("font-size: 16px;")
    layout.addWidget(label)
    layout.addLayout(button_layout)
    layout.addWidget(sort_dropdown)
    layout.addWidget(file_list)
    return layout


def setup_directory_autocomplete(line_edit, file_list):
    file_model = QFileSystemModel()
    file_model.setRootPath("")

    completer = QCompleter(file_model)
    completer.setCompletionMode(QCompleter.PopupCompletion)
    completer.setCaseSensitivity(Qt.CaseInsensitive)
    line_edit.setCompleter(completer)

    line_edit.textChanged.connect(lambda text: update_file_list(text, file_list))


def update_file_list(path, file_list):
    file_list.clear()
    if QDir(path).exists():
        entries = QDir(path).entryList(QDir.Files | QDir.NoDotAndDotDot)
        file_list.addItems(entries)