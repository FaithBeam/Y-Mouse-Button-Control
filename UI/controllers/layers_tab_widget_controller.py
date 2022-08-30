from PySide6.QtCore import Slot
from UI.dialogs.some_dialog import SomeDialog
from UI.models.mapping_commands import MappingFactory, MappingInterface
from UI.models.action_type import ActionTypeFactory
from UI.models.profile import Profiles
from UI.widgets.mouse_button_combobox import MouseButtonComboBox


class LayersTabWidgetController:
    def __init__(self, profiles: Profiles):
        self._profiles = profiles

    @Slot(object)
    def on_combo_settings_clicked(self, combo: MouseButtonComboBox):
        self._raise_dialog(combo)

    def _raise_dialog(self, combo: MouseButtonComboBox):
        current_target_action = combo.get_action(combo.currentIndex())
        if current_target_action.can_raise_dialog:
            dlg = SomeDialog.create_dialog(combo.currentIndex(), combo.get_action(combo.currentIndex()).keys)
            if dlg.exec():
                mapping = MappingFactory.create(
                    combo.currentIndex(),
                    keys=dlg.custom_keys_qlineedit.text(),
                    action_type=ActionTypeFactory.create(dlg.action_type_qcombobox.currentIndex() + 1)
                )

                self.set_button(mapping, combo)

    def set_button(self, base_action: MappingInterface, combo: MouseButtonComboBox):
        if combo.button == 'lmb':
            self._profiles.current_profile.layer_1.left_mouse_button = base_action
        elif combo.button == 'rmb':
            self._profiles.current_profile.layer_1.right_mouse_button = base_action
        elif combo.button == 'mmb':
            self._profiles.current_profile.layer_1.middle_mouse_button = base_action
        elif combo.button == 'mb4':
            self._profiles.current_profile.layer_1.mouse_button_4 = base_action
        elif combo.button == 'mb5':
            self._profiles.current_profile.layer_1.mouse_button_5 = base_action
        elif combo.button == 'scrollUp':
            self._profiles.current_profile.layer_1.scroll_up = base_action
        elif combo.button == 'scrollDown':
            self._profiles.current_profile.layer_1.scroll_down = base_action
        elif combo.button == 'tiltWheelLeft':
            self._profiles.current_profile.layer_1.tilt_wheel_left = base_action
        elif combo.button == 'tiltWheelRight':
            self._profiles.current_profile.layer_1.tilt_wheel_right = base_action
        self._profiles.current_profile.trigger()
        self._profiles.current_profile_edited()
        combo.update_action(base_action)

    @Slot(int)
    def combobox_index_changed(self, combo: MouseButtonComboBox):
        current_action = combo.get_action(combo.currentIndex())
        if current_action.can_raise_dialog and current_action.keys is None:
            self._raise_dialog(combo)
        else:
            self.set_button(combo.get_action(combo.currentIndex()), combo)

