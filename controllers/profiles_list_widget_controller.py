from PySide6.QtCore import Slot, QObject, Qt
from PySide6.QtWidgets import QListView
from dialogs.process_picker_dialog import ProcessPickerDialog
from models.profile import Profile, Profiles
from models.profiles_list_model import ProfilesListModel


class ProfilesListWidgetController(QObject):
    def __init__(self, profiles: Profiles, profiles_list_model: ProfilesListModel,) -> None:
        super().__init__()
        self._profiles = profiles
        self._profiles_list_model = profiles_list_model

    @Slot()
    def add(self):
        dlg = ProcessPickerDialog()
        if dlg.exec():
            proc = dlg.get_selected_process()
            description = dlg.get_description()
            application = dlg.get_application()
            self._profiles_list_model.add_profile(Profile(name=f"{proc} - {description}", process=application, description=description))

    @Slot()
    def delete(self, index):
        self._profiles_list_model.remove_profile(index)

    @Slot(object)
    def on_selected_profile_changed(self, profile_list_view: QListView):
        for index in profile_list_view.selectedIndexes():
            profile_name = self._profiles_list_model.data(index, Qt.DisplayRole)
            for p in self._profiles.profiles:
                if p.name == profile_name:
                    self._profiles.current_profile = p
                    break
