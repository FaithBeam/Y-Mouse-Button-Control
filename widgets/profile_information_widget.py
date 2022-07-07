from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QGroupBox, QLabel, QGridLayout, QVBoxLayout
from models.profile import Profiles


class ProfileInformationWidget(QWidget):
    def __init__(self, profiles: Profiles):
        super(ProfileInformationWidget, self).__init__()

        self._profiles = profiles
        description_label = QLabel("Description")
        window_caption_label = QLabel("Window Caption")
        process_label = QLabel("Process")
        window_class_label = QLabel("Window Class")
        parent_class_label = QLabel("Parent Class")
        match_type_label = QLabel("Match Type")

        self.description_label_value = QLabel("N/A")
        self.window_caption_label_value = QLabel("N/A")
        self.process_label_value = QLabel("N/A")
        self.window_class_label_value = QLabel("N/A")
        self.parent_class_label_value = QLabel("N/A")
        self.match_type_label_value = QLabel("N/A")

        profile_information_groupbox_grid_layout = QGridLayout()
        profile_information_groupbox_grid_layout.addWidget(description_label, 0, 0)
        profile_information_groupbox_grid_layout.addWidget(window_caption_label, 1, 0)
        profile_information_groupbox_grid_layout.addWidget(process_label, 2, 0)
        profile_information_groupbox_grid_layout.addWidget(window_class_label, 3, 0)
        profile_information_groupbox_grid_layout.addWidget(parent_class_label, 4, 0)
        profile_information_groupbox_grid_layout.addWidget(match_type_label, 5, 0)

        profile_information_groupbox_grid_layout.addWidget(self.description_label_value, 0, 1)
        profile_information_groupbox_grid_layout.addWidget(self.window_caption_label_value, 1, 1)
        profile_information_groupbox_grid_layout.addWidget(self.process_label_value, 2, 1)
        profile_information_groupbox_grid_layout.addWidget(self.window_class_label_value, 3, 1)
        profile_information_groupbox_grid_layout.addWidget(self.parent_class_label_value, 4, 1)
        profile_information_groupbox_grid_layout.addWidget(self.match_type_label_value, 5, 1)

        self._profiles.on_current_profile_changed.connect(self._on_current_profile_changed)

        profile_information_groupbox = QGroupBox("Profile Information")
        profile_information_groupbox.setLayout(profile_information_groupbox_grid_layout)

        profile_information_widget_layout = QVBoxLayout()
        profile_information_widget_layout.addWidget(profile_information_groupbox)

        profile_information_groupbox_grid_layout.setColumnStretch(2, 999)

        self.setLayout(profile_information_widget_layout)

        self._on_current_profile_changed()

    @Slot()
    def _on_current_profile_changed(self):
        self.description_label_value.setText(self._profiles.current_profile.description)
        self.window_caption_label_value.setText(self._profiles.current_profile.window_caption)
        self.process_label_value.setText(self._profiles.current_profile.process)
        self.window_class_label_value.setText(self._profiles.current_profile.window_class)
        self.parent_class_label_value.setText(self._profiles.current_profile.parent_class)
        self.match_type_label_value.setText(self._profiles.current_profile.match_type)
