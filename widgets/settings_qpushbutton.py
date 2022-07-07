from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QSize
from widgets.mouse_button_combobox import MouseButtonComboBox


class SettingsButton(QPushButton):
    def __init__(self, icon, combo: MouseButtonComboBox, size=QSize(10, 10)):
        super().__init__()
        self.setIcon(icon)
        self.setIconSize(size)
        self.combo = combo
        self.setStyleSheet("QPushButton:disabled {background-color: darkgray}")
        self.set_enabled_disabled()

    def set_enabled_disabled(self):
        current_action = self.combo.get_action(self.combo.currentIndex())
        if current_action.can_raise_dialog and current_action.keys is not None:
            self.setEnabled(True)
        else:
            self.setEnabled(False)
