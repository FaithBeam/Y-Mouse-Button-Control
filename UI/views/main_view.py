import os
import sys

import PySide6
from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QSystemTrayIcon, QMenu, QApplication, \
    QPushButton, QLabel

from UI.controllers.main_view_controller import MainViewController
from UI.models.profile import Profiles
from UI.widgets.layers_tab_widget import LayersTabWidget
from UI.widgets.profile_information_widget import ProfileInformationWidget
from UI.widgets.profiles_list_widget import ProfilesListWidget
from globals import app_name, app_version


class MainView(QMainWindow):
    def __init__(self, config, profiles: Profiles):
        super(MainView, self).__init__()
        self._profiles = profiles
        self._main_view_controller = MainViewController(config, profiles)
        self.window().setWindowTitle(f"{app_name} - {app_version}")
        self._profiles_list_widget = ProfilesListWidget(profiles)
        self._profile_information_widget = ProfileInformationWidget(profiles)
        self._layers_tab_widget = LayersTabWidget(profiles)
        settings_button = QPushButton("Settings")
        settings_button.setEnabled(False)
        save_profile_button = QPushButton("Save Profile")
        load_profile_button = QPushButton("Load Profile")
        load_profile_button.setEnabled(False)
        self._profile_label = QLabel("Profile:")
        apply_button = QPushButton("Apply")
        close_button = QPushButton("Close")
        save_profile_button.clicked.connect(lambda x: self._main_view_controller.on_save_profile_button_clicked(self))
        apply_button.clicked.connect(self._main_view_controller.on_apply_clicked)
        close_button.clicked.connect(lambda x: self._main_view_controller.on_close_clicked(self))
        bottom_row_hlayout = QHBoxLayout()
        bottom_row_hlayout.addWidget(settings_button)
        bottom_row_hlayout.addWidget(save_profile_button)
        bottom_row_hlayout.addWidget(load_profile_button)
        bottom_row_hlayout.addWidget(self._profile_label)
        bottom_row_hlayout.addWidget(apply_button)
        bottom_row_hlayout.addWidget(close_button)
        self.outer_vlayout = QVBoxLayout()
        self._v_layout = QVBoxLayout()
        self._v_layout.addWidget(self._layers_tab_widget)
        self._v_layout.addWidget(self._profile_information_widget)
        self._h_layout = QHBoxLayout()
        self._h_layout.addWidget(self._profiles_list_widget)
        self._h_layout.addLayout(self._v_layout)
        self.outer_vlayout.addLayout(self._h_layout)
        self.outer_vlayout.addLayout(bottom_row_hlayout)
        widget = QWidget()
        widget.setLayout(self.outer_vlayout)
        self.setCentralWidget(widget)
        self.tray = QSystemTrayIcon(parent=self)
        self.create_tray()
        self.on_current_profile_changed()
        self._profiles.on_current_profile_changed.connect(self.on_current_profile_changed)

    @Slot()
    def on_current_profile_changed(self):
        self._profile_label.setText(f"Profile:\t{self._profiles.current_profile.name}")

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        QMainWindow.hide(self)
        self.tray.showMessage("", f"{app_name} has closed to the task bar.")

    def create_tray(self):
        if getattr(sys, 'frozen', False):
            icon_path = file = os.path.join(sys._MEIPASS, "resources/mouse.png")
        else:
            icon_path = file = "resources/mouse.png"
        icon = QIcon(icon_path)
        self.tray = QSystemTrayIcon(parent=self)
        self.tray.setIcon(icon)
        self.tray.setVisible(True)
        self.tray.setToolTip(f"{app_name} - {app_version}")

        menu = QMenu(parent=self)
        action = QAction("Setup", parent=self)
        action.triggered.connect(self.show)
        menu.addAction(action)

        quit_action = QAction("Quit", parent=self)
        quit_action.triggered.connect(QApplication.quit)
        menu.addAction(quit_action)

        self.tray.setContextMenu(menu)
