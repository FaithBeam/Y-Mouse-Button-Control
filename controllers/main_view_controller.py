import json
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QFileDialog

from globals import app_name
from models.profile import Profiles


class MainViewController:
    def __init__(self, config, profiles: Profiles):
        self._profiles = profiles
        self._config = config

    @Slot()
    def on_save_profile_button_clicked(self, parent):
        save_path = QFileDialog.getSaveFileName(parent, 'Save Profile', "Profile.json")
        if save_path[0]:
            data = {}
            for p in self._profiles.profiles:
                data.update(p.to_json())
            with open(save_path[0], 'w') as f:
                f.write(json.dumps(data, indent=4))

    @Slot()
    def on_apply_clicked(self):
        data = {}
        for p in self._profiles.profiles:
            data.update(p.to_json())
        with open(self._config.profile_location, 'w') as f:
            f.write(json.dumps(data, indent=4))

    @Slot(object)
    def on_close_clicked(self, parent):
        QMainWindow.hide(parent)
        parent.tray.showMessage("", f"{app_name} has closed to the task bar.")
