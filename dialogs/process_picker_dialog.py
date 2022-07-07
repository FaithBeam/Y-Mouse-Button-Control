from PySide6.QtCore import Slot
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, \
    QListWidget, QMessageBox, QLineEdit

from process_monitor import get_processes


class ProcessPickerDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Application")

        # Row 1
        label_1 = QLabel("Select from the list of running applications")
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.on_refresh_clicked)
        r1_h_layout = QHBoxLayout()
        r1_h_layout.addWidget(label_1)
        r1_h_layout.addWidget(refresh_button)

        # Row 2
        self.process_list_widget = QListWidget()
        self.process_list_widget.addItems(get_processes())
        self.process_list_widget.currentTextChanged.connect(self.on_selected_process_changed)

        # Row 3
        label_2 = QLabel("Or type in/browse to the application executable file")

        # Row 4
        application_label = QLabel('Application')
        self.application_text_edit = QLineEdit()
        r4_h_layout = QHBoxLayout()
        r4_h_layout.addWidget(application_label)
        r4_h_layout.addWidget(self.application_text_edit)

        # Row 5
        description_label = QLabel("Description")
        self.description_line_edit = QLineEdit()
        r5_h_layout = QHBoxLayout()
        r5_h_layout.addWidget(description_label)
        r5_h_layout.addWidget(self.description_line_edit)

        # Row 6
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.button_box = QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.on_ok_clicked)
        self.button_box.rejected.connect(self.reject)

        v_layout = QVBoxLayout()
        v_layout.addLayout(r1_h_layout)
        v_layout.addWidget(self.process_list_widget)
        v_layout.addWidget(label_2)
        v_layout.addLayout(r4_h_layout)
        v_layout.addLayout(r5_h_layout)
        v_layout.addWidget(self.button_box)

        self.setLayout(v_layout)

    def get_selected_process(self) -> str:
        if len(self.process_list_widget.selectedIndexes()) == 1:
            return self.process_list_widget.selectedItems()[0].text()

    def get_description(self) -> str:
        return self.description_line_edit.text()

    def get_application(self) -> str:
        return self.application_text_edit.text()

    def on_selected_process_changed(self, value):
        self.description_line_edit.setText(value)
        self.application_text_edit.setText(value)

    @Slot()
    def on_refresh_clicked(self):
        self.process_list_widget.clear()
        self.process_list_widget.addItems(get_processes())

    @Slot()
    def on_ok_clicked(self):
        if len(self.process_list_widget.selectedIndexes()) < 1:
            QMessageBox.information(self, "", "You have to select a process name or select cancel.")
        else:
            self.accept()
