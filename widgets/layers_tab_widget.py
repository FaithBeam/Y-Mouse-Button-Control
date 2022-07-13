import os
import sys

from PySide6.QtCore import Slot
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QVBoxLayout, QTabWidget, QWidget, QLabel, QGridLayout

from controllers.layers_tab_widget_controller import LayersTabWidgetController
from models.profile import Profile, Profiles
from widgets.mouse_button_combobox import MouseButtonComboBox
from widgets.settings_qpushbutton import SettingsButton
from globals import mouse_handler


class LayersTabWidget(QWidget):
    def __init__(self, profiles: Profiles):
        super().__init__()
        self._profiles = profiles
        self._current_profile = profiles.current_profile
        self._profile = self._current_profile
        self._layers_tab_widget_controller = LayersTabWidgetController(profiles)
        self.mouse_combo_box_models = {}

        layer_name_qlabel = QLabel("Layer name")
        left_button_qlabel = QLabel("Left Button")
        right_button_qlabel = QLabel("Right Button")
        middle_button_qlabel = QLabel("Middle Button")
        mouse_button_4_qlabel = QLabel("Mouse Button 4")
        mouse_button_5_qlabel = QLabel("Mouse Button 5")
        wheel_up_qlabel = QLabel("Wheel Up")
        wheel_down_qlabel = QLabel("Wheel Down")
        tilt_wheel_left_qlabel = QLabel("Tilt Wheel Left")
        tilt_wheel_right_qlabel = QLabel("Tilt Wheel Right")

        self.layer_name_qlabel_value = QLabel("")
        self.left_button_combo = MouseButtonComboBox('lmb', self._profile.layer_1.left_mouse_button)
        self.right_button_combo = MouseButtonComboBox('rmb', self._profile.layer_1.right_mouse_button)
        self.middle_button_combo = MouseButtonComboBox('mmb', self._profile.layer_1.middle_mouse_button)
        self.mouse_button_4_combo = MouseButtonComboBox('mb4', self._profile.layer_1.mouse_button_4)
        self.mouse_button_5_combo = MouseButtonComboBox('mb5', self._profile.layer_1.mouse_button_5)
        self.scroll_up_combo = MouseButtonComboBox('scrollUp', self._profile.layer_1.scroll_up)
        self.scroll_down_combo = MouseButtonComboBox('scrollDown', self._profile.layer_1.scroll_down)
        self.tilt_wheel_left_combo = MouseButtonComboBox('tiltWheelLeft', self._profile.layer_1.tilt_wheel_left)
        self.tilt_wheel_right_combo = MouseButtonComboBox('tiltWheelRight', self._profile.layer_1.tilt_wheel_right)

        gear_icon_path = ""
        if getattr(sys, 'frozen', False):
            gear_icon_path = file = os.path.join(sys._MEIPASS, "resources/gear_icon.png")
        else:
            gear_icon_path = file = "resources/gear_icon.png"
        gear_icon_pixmap = QPixmap(gear_icon_path)
        gear_icon = QIcon(gear_icon_pixmap)

        self.left_button_settings_button = SettingsButton(gear_icon, self.left_button_combo)
        self.right_button_settings_button = SettingsButton(gear_icon, self.right_button_combo)
        self.middle_button_settings_button = SettingsButton(gear_icon, self.middle_button_combo)
        self.mouse_button_4_settings_button = SettingsButton(gear_icon, self.mouse_button_4_combo)
        self.mouse_button_5_settings_button = SettingsButton(gear_icon, self.mouse_button_5_combo)
        self.scroll_up_settings_button = SettingsButton(gear_icon, self.scroll_up_combo)
        self.scroll_down_settings_button = SettingsButton(gear_icon, self.scroll_down_combo)
        self.tilt_wheel_left_settings_button = SettingsButton(gear_icon, self.tilt_wheel_left_combo)
        self.tilt_wheel_right_settings_button = SettingsButton(gear_icon, self.tilt_wheel_right_combo)

        layer_1_widget_grid_layout = QGridLayout()
        layer_1_widget_grid_layout.addWidget(layer_name_qlabel, 0, 0)
        layer_1_widget_grid_layout.addWidget(left_button_qlabel, 1, 0)
        layer_1_widget_grid_layout.addWidget(right_button_qlabel, 2, 0)
        layer_1_widget_grid_layout.addWidget(middle_button_qlabel, 3, 0)
        layer_1_widget_grid_layout.addWidget(mouse_button_4_qlabel, 4, 0)
        layer_1_widget_grid_layout.addWidget(mouse_button_5_qlabel, 5, 0)
        layer_1_widget_grid_layout.addWidget(wheel_up_qlabel, 6, 0)
        layer_1_widget_grid_layout.addWidget(wheel_down_qlabel, 7, 0)
        layer_1_widget_grid_layout.addWidget(tilt_wheel_left_qlabel, 8, 0)
        layer_1_widget_grid_layout.addWidget(tilt_wheel_right_qlabel, 9, 0)

        layer_1_widget_grid_layout.addWidget(self.layer_name_qlabel_value, 0, 1)
        layer_1_widget_grid_layout.addWidget(self.left_button_combo, 1, 1)
        layer_1_widget_grid_layout.addWidget(self.right_button_combo, 2, 1)
        layer_1_widget_grid_layout.addWidget(self.middle_button_combo, 3, 1)
        layer_1_widget_grid_layout.addWidget(self.mouse_button_4_combo, 4, 1)
        layer_1_widget_grid_layout.addWidget(self.mouse_button_5_combo, 5, 1)
        layer_1_widget_grid_layout.addWidget(self.scroll_up_combo, 6, 1)
        layer_1_widget_grid_layout.addWidget(self.scroll_down_combo, 7, 1)
        layer_1_widget_grid_layout.addWidget(self.tilt_wheel_left_combo, 8, 1)
        layer_1_widget_grid_layout.addWidget(self.tilt_wheel_right_combo, 9, 1)

        layer_1_widget_grid_layout.addWidget(self.left_button_settings_button, 1, 2)
        layer_1_widget_grid_layout.addWidget(self.right_button_settings_button, 2, 2)
        layer_1_widget_grid_layout.addWidget(self.middle_button_settings_button, 3, 2)
        layer_1_widget_grid_layout.addWidget(self.mouse_button_4_settings_button, 4, 2)
        layer_1_widget_grid_layout.addWidget(self.mouse_button_5_settings_button, 5, 2)
        layer_1_widget_grid_layout.addWidget(self.scroll_up_settings_button, 6, 2)
        layer_1_widget_grid_layout.addWidget(self.scroll_down_settings_button, 7, 2)
        layer_1_widget_grid_layout.addWidget(self.tilt_wheel_left_settings_button, 8, 2)
        layer_1_widget_grid_layout.addWidget(self.tilt_wheel_right_settings_button, 9, 2)

        # Make only the mouse comboboxes resize
        layer_1_widget_grid_layout.setColumnStretch(1, 999)

        layer_1_widget = QWidget()
        layer_1_widget.setLayout(layer_1_widget_grid_layout)
        layers_tab_widgets = QTabWidget()
        layers_tab_widgets.addTab(layer_1_widget, "Layer 1")

        vlayout = QVBoxLayout()
        vlayout.addWidget(layers_tab_widgets)
        self.setLayout(vlayout)

        self._connect_everything()

    def _connect_everything(self):
        self.left_button_combo.activated.connect(lambda x: self._layers_tab_widget_controller.combobox_index_changed(self.left_button_combo))
        self.right_button_combo.activated.connect(lambda x: self._layers_tab_widget_controller.combobox_index_changed(self.right_button_combo))
        self.middle_button_combo.activated.connect(lambda x: self._layers_tab_widget_controller.combobox_index_changed(self.middle_button_combo))
        self.mouse_button_4_combo.activated.connect(lambda x: self._layers_tab_widget_controller.combobox_index_changed(self.mouse_button_4_combo))
        self.mouse_button_5_combo.activated.connect(lambda x: self._layers_tab_widget_controller.combobox_index_changed(self.mouse_button_5_combo))
        self.scroll_up_combo.activated.connect(lambda x: self._layers_tab_widget_controller.combobox_index_changed(self.scroll_up_combo))
        self.scroll_down_combo.activated.connect(lambda x: self._layers_tab_widget_controller.combobox_index_changed(self.scroll_down_combo))
        self.tilt_wheel_left_combo.activated.connect(lambda x: self._layers_tab_widget_controller.combobox_index_changed(self.tilt_wheel_left_combo))
        self.tilt_wheel_right_combo.activated.connect(lambda x: self._layers_tab_widget_controller.combobox_index_changed(self.tilt_wheel_right_combo))

        self.left_button_settings_button.clicked.connect(lambda x: self._layers_tab_widget_controller.on_combo_settings_clicked(self.left_button_combo))
        self.right_button_settings_button.clicked.connect(lambda x: self._layers_tab_widget_controller.on_combo_settings_clicked(self.right_button_combo))
        self.middle_button_settings_button.clicked.connect(lambda x: self._layers_tab_widget_controller.on_combo_settings_clicked(self.middle_button_combo))
        self.mouse_button_4_settings_button.clicked.connect(lambda x: self._layers_tab_widget_controller.on_combo_settings_clicked(self.mouse_button_4_combo))
        self.mouse_button_5_settings_button.clicked.connect(lambda x: self._layers_tab_widget_controller.on_combo_settings_clicked(self.mouse_button_5_combo))
        self.scroll_up_settings_button.clicked.connect(lambda x: self._layers_tab_widget_controller.on_combo_settings_clicked(self.scroll_up_combo))
        self.scroll_down_settings_button.clicked.connect(lambda x: self._layers_tab_widget_controller.on_combo_settings_clicked(self.scroll_down_combo))
        self.tilt_wheel_left_settings_button.clicked.connect(lambda x: self._layers_tab_widget_controller.on_combo_settings_clicked(self.tilt_wheel_left_combo))
        self.tilt_wheel_right_settings_button.clicked.connect(lambda x: self._layers_tab_widget_controller.on_combo_settings_clicked(self.tilt_wheel_right_combo))

        mouse_handler.on_lmb_click.connect(self.left_button_combo.highlight)
        mouse_handler.on_rmb_click.connect(self.right_button_combo.highlight)
        mouse_handler.on_mmb_click.connect(self.middle_button_combo.highlight)
        mouse_handler.on_mb4_click.connect(self.mouse_button_4_combo.highlight)
        mouse_handler.on_mb5_click.connect(self.mouse_button_5_combo.highlight)
        mouse_handler.on_scroll_up.connect(self.scroll_up_combo.scroll_highlight)
        mouse_handler.on_scroll_down.connect(self.scroll_down_combo.scroll_highlight)
        mouse_handler.on_tilt_wheel_left.connect(self.tilt_wheel_left_combo.scroll_highlight)
        mouse_handler.on_tilt_wheel_right.connect(self.tilt_wheel_right_combo.scroll_highlight)

        self._profiles.on_current_profile_changed.connect(self._on_current_profile_changed)

        self.left_button_combo.currentIndexChanged.connect(self.left_button_settings_button.set_enabled_disabled)
        self.right_button_combo.currentIndexChanged.connect(self.right_button_settings_button.set_enabled_disabled)
        self.middle_button_combo.currentIndexChanged.connect(self.middle_button_settings_button.set_enabled_disabled)
        self.mouse_button_4_combo.currentIndexChanged.connect(self.mouse_button_4_settings_button.set_enabled_disabled)
        self.mouse_button_5_combo.currentIndexChanged.connect(self.mouse_button_5_settings_button.set_enabled_disabled)
        self.left_button_combo.currentTextChanged.connect(self.left_button_settings_button.set_enabled_disabled)
        self.scroll_up_combo.currentIndexChanged.connect(self.scroll_up_settings_button.set_enabled_disabled)
        self.scroll_down_combo.currentIndexChanged.connect(self.scroll_down_settings_button.set_enabled_disabled)
        self.tilt_wheel_left_combo.currentIndexChanged.connect(self.tilt_wheel_left_settings_button.set_enabled_disabled)
        self.tilt_wheel_right_combo.currentIndexChanged.connect(self.tilt_wheel_right_settings_button.set_enabled_disabled)
        self.right_button_combo.currentTextChanged.connect(self.right_button_settings_button.set_enabled_disabled)
        self.middle_button_combo.currentTextChanged.connect(self.middle_button_settings_button.set_enabled_disabled)
        self.mouse_button_4_combo.currentTextChanged.connect(self.mouse_button_4_settings_button.set_enabled_disabled)
        self.mouse_button_5_combo.currentTextChanged.connect(self.mouse_button_5_settings_button.set_enabled_disabled)
        self.scroll_up_combo.currentTextChanged.connect(self.scroll_up_settings_button.set_enabled_disabled)
        self.scroll_down_combo.currentTextChanged.connect(self.scroll_down_settings_button.set_enabled_disabled)
        self.tilt_wheel_left_combo.currentTextChanged.connect(self.tilt_wheel_left_settings_button.set_enabled_disabled)
        self.tilt_wheel_right_combo.currentTextChanged.connect(self.tilt_wheel_right_settings_button.set_enabled_disabled)

    @Slot(object)
    def _on_current_profile_changed(self, new_profile: Profile):
        # region This region gives us history of the mouse combobox models for when the user switches between profiles
        if self._profile.name not in self.mouse_combo_box_models:
            self.mouse_combo_box_models[self._profile.name] = {}

        # Save current combo models to profile name
        self.mouse_combo_box_models[self._profile.name]["lmb"] = (self.left_button_combo.currentIndex(), self.left_button_combo.model)
        self.mouse_combo_box_models[self._profile.name]["rmb"] = (self.right_button_combo.currentIndex(), self.right_button_combo.model)
        self.mouse_combo_box_models[self._profile.name]["mmb"] = (self.middle_button_combo.currentIndex(), self.middle_button_combo.model)
        self.mouse_combo_box_models[self._profile.name]["mb4"] = (self.mouse_button_4_combo.currentIndex(), self.mouse_button_4_combo.model)
        self.mouse_combo_box_models[self._profile.name]["mb5"] = (self.mouse_button_5_combo.currentIndex(), self.mouse_button_5_combo.model)
        self.mouse_combo_box_models[self._profile.name]["scrollUp"] = (self.scroll_up_combo.currentIndex(), self.scroll_up_combo.model)
        self.mouse_combo_box_models[self._profile.name]["scrollDown"] = (self.scroll_down_combo.currentIndex(), self.scroll_down_combo.model)
        self.mouse_combo_box_models[self._profile.name]["tiltWheelLeft"] = (self.tilt_wheel_left_combo.currentIndex(), self.tilt_wheel_left_combo.model)
        self.mouse_combo_box_models[self._profile.name]["tiltWheelRight"] = (self.tilt_wheel_right_combo.currentIndex(), self.tilt_wheel_right_combo.model)

        # Restore existing profile combo models
        if new_profile.name in self.mouse_combo_box_models:
            self.left_button_combo.set_model(self.mouse_combo_box_models[new_profile.name]["lmb"])
            self.right_button_combo.set_model(self.mouse_combo_box_models[new_profile.name]["rmb"])
            self.middle_button_combo.set_model(self.mouse_combo_box_models[new_profile.name]["mmb"])
            self.mouse_button_4_combo.set_model(self.mouse_combo_box_models[new_profile.name]["mb4"])
            self.mouse_button_5_combo.set_model(self.mouse_combo_box_models[new_profile.name]["mb5"])
            self.scroll_up_combo.set_model(self.mouse_combo_box_models[new_profile.name]["scrollUp"])
            self.scroll_down_combo.set_model(self.mouse_combo_box_models[new_profile.name]["scrollDown"])
            self.tilt_wheel_left_combo.set_model(self.mouse_combo_box_models[new_profile.name]["tiltWheelLeft"])
            self.tilt_wheel_right_combo.set_model(self.mouse_combo_box_models[new_profile.name]["tiltWheelRight"])
        # New models for combos
        else:
            if new_profile.layer_1.left_mouse_button:
                self.left_button_combo.new_model(new_profile.layer_1.left_mouse_button)
            else:
                self.left_button_combo.new_model()
            if new_profile.layer_1.right_mouse_button:
                self.right_button_combo.new_model(new_profile.layer_1.right_mouse_button)
            else:
                self.right_button_combo.new_model()
            if new_profile.layer_1.middle_mouse_button:
                self.middle_button_combo.new_model(new_profile.layer_1.middle_mouse_button)
            else:
                self.middle_button_combo.new_model()
            if new_profile.layer_1.mouse_button_4:
                self.mouse_button_4_combo.new_model(new_profile.layer_1.mouse_button_4)
            else:
                self.mouse_button_4_combo.new_model()
            if new_profile.layer_1.mouse_button_5:
                self.mouse_button_5_combo.new_model(new_profile.layer_1.mouse_button_5)
            else:
                self.mouse_button_5_combo.new_model()
            if new_profile.layer_1.scroll_up:
                self.scroll_up_combo.new_model(new_profile.layer_1.scroll_up)
            else:
                self.scroll_up_combo.new_model()
            if new_profile.layer_1.scroll_down:
                self.scroll_down_combo.new_model(new_profile.layer_1.scroll_down)
            else:
                self.scroll_down_combo.new_model()
            if new_profile.layer_1.tilt_wheel_left:
                self.tilt_wheel_left_combo.new_model(new_profile.layer_1.tilt_wheel_left)
            else:
                self.tilt_wheel_left_combo.new_model()
            if new_profile.layer_1.tilt_wheel_right:
                self.tilt_wheel_right_combo.new_model(new_profile.layer_1.tilt_wheel_right)
            else:
                self.tilt_wheel_right_combo.new_model()
        # endregion

        self._profile = new_profile
