from typing import Optional, Tuple
from PySide6.QtCore import Slot, Qt, QTimer
from PySide6.QtWidgets import QComboBox
from UI.models.mapping_commands import MappingInterface
from UI.models.action_combobox_model import ActionComboBoxModel


class MouseButtonComboBox(QComboBox):
    def __init__(self, button: str, action_interface: Optional[MappingInterface] = None):
        super().__init__()
        self.model = ActionComboBoxModel(action_interface)
        self.setModel(self.model)
        self.button = button
        self.setMinimumWidth(300)
        if action_interface is not None:
            self.setCurrentIndex(action_interface.index)
        if 'scroll' in button or 'tilt' in button:
            self._scroll_timer = QTimer(self)

    def get_action(self, index: int) -> MappingInterface:
        return self.model.data(self.model.index(index), ActionComboBoxModel.ReturnActionRole)

    def update_action(self, base_action: MappingInterface):
        self.model.setData(self.model.index(base_action.index), base_action, Qt.EditRole)
        self.setCurrentIndex(base_action.index)

    def set_model(self, index_and_action: Tuple[int, ActionComboBoxModel]):
        self.model = index_and_action[1]
        self.setModel(self.model)
        self.setCurrentIndex(index_and_action[0])

    def new_model(self, action_interface: Optional[MappingInterface] = None):
        if action_interface is None:
            self.model = ActionComboBoxModel()
        else:
            self.model = ActionComboBoxModel(action_interface)
        self.setModel(self.model)
        if action_interface is not None:
            self.setCurrentIndex(action_interface.index)

    @Slot(bool)
    def highlight(self, value: bool):
        if value:
            self.setStyleSheet("background-color: yellow")
        else:
            self.setStyleSheet("background-color: white")

    @Slot(bool)
    def scroll_highlight(self, value: bool, time=200):
        if not self._scroll_timer.isActive():
            self.setStyleSheet("background-color: yellow")
            self._scroll_timer.singleShot(time, self._unhighlight)

    def _unhighlight(self):
        self.setStyleSheet("background-color: white")
