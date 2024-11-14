from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel, QLineEdit, QListWidget
)
from PyQt5.QtCore import Qt

def setup_ui(window):
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    
    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(10, 10, 10, 10)
    main_layout.setSpacing(15)
    
    directory_layout = QHBoxLayout()
    
    source_dir_edit, source_dir_button, source_file_list = create_directory_widgets("Source Directory:")
    directory_layout.addLayout(create_directory_layout("Source Directory:", source_dir_edit, source_dir_button, source_file_list))
    
    target_dir_edit, target_dir_button, target_file_list = create_directory_widgets("Target Directory:")
    directory_layout.addLayout(create_directory_layout("Target Directory:", target_dir_edit, target_dir_button, target_file_list))
    
    main_layout.addLayout(directory_layout)
    
    move_button = QPushButton("Move Selected Files")
    move_button.setStyleSheet("padding: 10px; font-size: 14px;")
    main_layout.addWidget(move_button, alignment=Qt.AlignCenter)
    
    central_widget.setLayout(main_layout)
    
    return source_dir_edit, source_dir_button, source_file_list, \
           target_dir_edit, target_dir_button, target_file_list, move_button

def create_directory_widgets(label_text):
    dir_edit = QLineEdit()
    dir_edit.setReadOnly(True)
    dir_button = QPushButton(f"Browse {label_text.split()[0]}")
    file_list = QListWidget()
    return dir_edit, dir_button, file_list

def create_directory_layout(label_text, dir_edit, dir_button, file_list):
    layout = QVBoxLayout()
    button_layout = QHBoxLayout()
    button_layout.addWidget(dir_edit)
    button_layout.addWidget(dir_button)
    layout.addWidget(QLabel(label_text))
    layout.addLayout(button_layout)
    layout.addWidget(QLabel(f"{label_text} Files:"))
    layout.addWidget(file_list)
    return layout