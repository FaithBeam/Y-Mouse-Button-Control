from models.profile import Profiles
from profile import Profile
from typing import Union, Any

from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt, QPersistentModelIndex


class ProfilesListModel(QAbstractListModel):
    def __init__(self, profiles: Profiles):
        super().__init__()
        self.profiles = profiles
        self.checks = {}
        self.do_checks()

    def do_checks(self):
        for i in range(len(self.profiles.profiles)):
            self.checks[QPersistentModelIndex(self.index(i, 0))] = self.profiles.profiles[i].checked_value

    def check_state(self, index):
        if index in self.checks.keys():
            return self.checks[index]
        else:
            return Qt.Unchecked

    def add_profile(self, profile: Profile):
        index = self.rowCount()
        self.beginInsertRows(QModelIndex(), index, index)
        self.profiles.add(profile)
        self.endInsertRows()
        self.checks[QPersistentModelIndex(self.index(index, 0))] = self.profiles.profiles[index].checked_value

    def remove_profile(self, index):
        self.beginRemoveRows(QModelIndex(), index, index)
        self.profiles.remove(index)
        self.endRemoveRows()

    def data(self, index: Union[QModelIndex, QPersistentModelIndex], role: int = None) -> Any:
        if role == Qt.CheckStateRole:
            return self.check_state(QPersistentModelIndex(index))
        if role == Qt.DisplayRole:
            profile = self.profiles.profiles[index.row()]
            return profile.name
        return None

    def setData(
        self,
        index: Union[QModelIndex, QPersistentModelIndex],
        value: Any,
        role: int = None,
    ) -> bool:
        if role == Qt.EditRole:
            profile = self.profiles.profiles[index.row()]
            profile.name = value
            return True

        if role == Qt.CheckStateRole:
            profile = self.profiles.profiles[index.row()]
            profile.checked_value = value
            profile.trigger()
            self.checks[QPersistentModelIndex(index)] = value
            return True

        return False

    def flags(self, index: Union[QModelIndex, QPersistentModelIndex]) -> Qt.ItemFlags:
        return (
            QAbstractListModel.flags(self, index)
            | Qt.ItemIsUserCheckable
            | Qt.ItemIsEditable
            | Qt.ItemIsSelectable
        )

    def rowCount(self, parent=QModelIndex()):
        return len(self.profiles.profiles)
