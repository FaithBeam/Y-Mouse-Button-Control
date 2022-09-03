from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListView,
    QPushButton,
    QGroupBox,
    QHBoxLayout,
    QGridLayout,
)
from UI.controllers.profiles_list_widget_controller import ProfilesListWidgetController
from UI.models.profile import Profiles
from UI.models.profiles_list_model import ProfilesListModel


class ProfilesListWidget(QWidget):
    def __init__(self, profiles: Profiles) -> None:
        super().__init__()
        self._profiles = profiles
        self._profiles_list_model = ProfilesListModel(profiles)

        self.profiles_list_widget_controller = ProfilesListWidgetController(self._profiles, self._profiles_list_model)

        profiles_list_view = QListView()
        profiles_list_view.setModel(self._profiles_list_model)

        self.delete_button = QPushButton("Delete")
        add_button = QPushButton("Add")

        listview_groupbox_vlayout_gridlayout = QGridLayout()
        listview_groupbox_vlayout_gridlayout.addWidget(add_button)
        listview_groupbox_vlayout_gridlayout.addWidget(self.delete_button)

        listview_groupbox_vlayout = QVBoxLayout()
        listview_groupbox_vlayout.addWidget(profiles_list_view)
        listview_groupbox_vlayout.addLayout(listview_groupbox_vlayout_gridlayout)

        profiles_listview_groupbox = QGroupBox("Application / Window Profiles:")
        profiles_listview_groupbox.setLayout(listview_groupbox_vlayout)

        profiles_hlayout = QHBoxLayout()
        profiles_hlayout.addWidget(profiles_listview_groupbox)

        self.setLayout(profiles_hlayout)

        profiles_list_view_selection_model = profiles_list_view.selectionModel()
        profiles_list_view_selection_model.selectionChanged.connect(lambda x: self.profiles_list_widget_controller.on_selected_profile_changed(profiles_list_view))
        self._profiles.on_current_profile_changed.connect(self._on_current_profile_changed)
        self.delete_button.clicked.connect(lambda x: self.profiles_list_widget_controller.delete(profiles_list_view.selectedIndexes()[0].row()))
        add_button.clicked.connect(self.profiles_list_widget_controller.add)

        profiles_list_view.setCurrentIndex(self._profiles_list_model.index(0, 0))

    @Slot(object)
    def _on_current_profile_changed(self, value):
        if value.name == "Default":
            self.delete_button.setEnabled(False)
        else:
            self.delete_button.setEnabled(True)
