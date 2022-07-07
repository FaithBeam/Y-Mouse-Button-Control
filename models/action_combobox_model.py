from typing import Union, Any

from PySide6 import QtCore
from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt, QPersistentModelIndex

from models.mapping_commands import MappingFactory


class ActionComboBoxModel(QAbstractListModel):
    ReturnActionRole = -1

    def __init__(self, action=None):
        super().__init__()
        self._actions = MappingFactory.get_mappings()
        if action is not None:
            for i in range(len(self._actions)):
                if isinstance(self._actions[i], type(action)):
                    self._actions.remove(self._actions[i])
                    self._actions.insert(i, action)
        self.action = action

    def data(self, index: Union[QModelIndex, QPersistentModelIndex], role: int = None) -> Any:
        if role == Qt.DisplayRole:
            return str(self._actions[index.row()])
        if role == self.ReturnActionRole:
            return self._actions[index.row()]

    def setData(
        self,
        index: Union[QModelIndex, QPersistentModelIndex],
        value: Any,
        role: int = None,
    ) -> bool:
        if role == Qt.EditRole:
            self.beginResetModel()
            self._actions[index.row()] = value
            self.dataChanged.emit(index.row(), index.column())
            self.endResetModel()
            return True

        return False

    def rowCount(self, parent=QModelIndex()):
        return len(self._actions)
