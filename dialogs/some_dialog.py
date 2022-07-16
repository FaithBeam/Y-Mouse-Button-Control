from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QLineEdit, QVBoxLayout, QComboBox, QHBoxLayout, \
    QToolButton, QMenu
from models.action_type import ActionTypeFactory

key_table = {
    '&Alt': '{ALT}',
    '&Apps (Context Menu) key': '{APPS}',
    '&Backspace': '{BACKSPACE}',
    '&Break': '{BREAK}',
    '&CAPS Lock Toggle': '{CAPSLOCK}',
    '&Caps Lock Off': '{CAPSLOCKOFF}',
    '&Caps Lock On': '{CAPSLOCKON}',
    '&Control': '{CTRL}',
    '&Delete': '{DEL}',
    '&Down': '{DOWN}',
    '&End': '{END}',
    '&Escape': '{ESC}',
    '&F1': '{F1}',
    '&F2': '{F2}',
    '&F3': '{F3}',
    '&F4': '{F4}',
    '&F5': '{F5}',
    '&F6': '{F6}',
    '&F7': '{F7}',
    '&F8': '{F8}',
    '&F9': '{F9}',
    '&F10': '{F10}',
    '&F11': '{F11}',
    '&F12': '{F12}',
    '&F13': '{F13}',
    '&F14': '{F14}',
    '&F15': '{F15}',
    '&F16': '{F16}',
    '&F17': '{F17}',
    '&F18': '{F18}',
    '&F19': '{F19}',
    '&F20': '{F20}',
    '&Volume Up': '{VOL+}',
    '&Volume Down': '{VOL-}',
    '&Mute': '{MUTE}',
    '&Play/Pause': '{MEDIAPLAY}',
    '&Stop': '{MEDIASTOP}',
    '&Next Track': '{MEDIANEXT}',
    '&Previous Track': '{MEDIAPREV}',
    '&Home': '{HOME}',
    '&Insert': '{INS}',
    '&Left': '{LEFT}',
    '&Page Down': '{PGDN}',
    '&Page Up': '{PGUP}',
    '&Pause': '{PAUSE}',
    '&PrtScn': '{PRTSCN}',
    '&Return': '{RETURN}',
    '&Right': '{RIGHT}',
    '&Right Alt (Alt Gr)': '{RALT}',
    '&Right Control': '{RCTRL}',
    '&Right Shift': '{RSHIFT}',
    '&Right Windows Key': '{RWIN}',
    '&Scroll Lock Off': '{SCROLLLOCKOFF}',
    '&Scroll Lock On': '{SCROLLLOCKON}',
    '&Scroll Lock Toggle': '{SCROLLLOCK}',
    '&Shift': '{SHIFT}',
    '&Space': '{SPACE}',
    '&Tab': '{TAB}',
    '&Up': '{UP}',
    '&Windows Key': '{WIN}',
}


class SomeDialog:
    subclasses = {}

    @classmethod
    def register_subclass(cls, dialog_type):
        def decorator(subclass):
            cls.subclasses[dialog_type] = subclass
            return subclass

        return decorator

    @classmethod
    def create_dialog(cls, dialog_type, keys):
        if dialog_type not in cls.subclasses:
            raise ValueError('Bad dialog type type {}'.format(dialog_type))

        return cls.subclasses[dialog_type](keys)


@SomeDialog.register_subclass(2)
class SimulatedKeystrokesDialog(QDialog):
    index = 2

    def __init__(self, current_keys=''):
        super().__init__()
        self.setWindowTitle("Simulated Keystrokes")
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.button_box = QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        enter_custom_keys_qlabel = QLabel("Enter custom key(s)")
        row_2_hlayout = QHBoxLayout()
        self.custom_keys_qlineedit = QLineEdit()
        self.custom_keys_qlineedit.setText(current_keys)
        modifier_toolbutton = ModifierToolButton(self.custom_keys_qlineedit)
        row_2_hlayout.addWidget(self.custom_keys_qlineedit)
        row_2_hlayout.addWidget(modifier_toolbutton)
        how_to_send_keystrokes_qlabel = QLabel("How to send the simulated keystrokes:")
        self.action_type_qcombobox = QComboBox()
        self.action_type_qcombobox.addItems(ActionTypeFactory.get_action_types())
        self.action_type_qcombobox.model().item(3).setEnabled(False)
        self.action_type_qcombobox.model().item(4).setEnabled(False)

        v_layout = QVBoxLayout()
        v_layout.addWidget(enter_custom_keys_qlabel)
        v_layout.addLayout(row_2_hlayout)
        v_layout.addWidget(how_to_send_keystrokes_qlabel)
        v_layout.addWidget(self.action_type_qcombobox)
        v_layout.addWidget(self.button_box)

        self.setLayout(v_layout)


class ModifierToolButton(QToolButton):
    def __init__(self, line_edit: QLineEdit):
        super().__init__()
        self._line_edit = line_edit
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.setText("|")
        self.setIcon(QIcon(r'resources\curly-braces-icon.png'))
        self.setPopupMode(QToolButton.InstantPopup)
        self._create_modifier_keys_menu()
        self._create_standard_keys_menu()
        self._create_direction_keys_menu()
        self._create_function_keys_menu()
        self._create_media_keys_menu()

    def _create_modifier_keys_menu(self):
        mk_control_action = QAction("&Control", self)
        mk_right_control_action = QAction("&Right Control", self)
        mk_alt_action = QAction("&Alt", self)
        mk_right_alt_action = QAction("&Right Alt", self)
        mk_shift_action = QAction("&Shift", self)
        mk_right_shift_action = QAction("&Right Shift", self)
        mk_windows_key_action = QAction("&Windows Key", self)
        mk_right_windows_key_action = QAction("&Right Windows Key", self)
        mk_apps_key_action = QAction("&Apps (Context Menu) key", self)
        mk_control_action.triggered.connect(lambda x: self.on_action_triggered(mk_control_action.text()))
        mk_right_control_action.triggered.connect(lambda x: self.on_action_triggered(mk_right_control_action.text()))
        mk_alt_action.triggered.connect(lambda x: self.on_action_triggered(mk_alt_action.text()))
        mk_right_alt_action.triggered.connect(lambda x: self.on_action_triggered(mk_right_alt_action.text()))
        mk_shift_action.triggered.connect(lambda x: self.on_action_triggered(mk_shift_action.text()))
        mk_right_shift_action.triggered.connect(lambda x: self.on_action_triggered(mk_right_shift_action.text()))
        mk_windows_key_action.triggered.connect(lambda x: self.on_action_triggered(mk_windows_key_action.text()))
        mk_right_windows_key_action.triggered.connect(lambda x: self.on_action_triggered(mk_right_windows_key_action.text()))
        mk_apps_key_action.triggered.connect(lambda x: self.on_action_triggered(mk_apps_key_action.text()))
        mk_menu = QMenu(self)
        mk_menu.addAction(mk_control_action)
        mk_menu.addAction(mk_right_control_action)
        mk_menu.addAction(mk_alt_action)
        mk_menu.addAction(mk_right_alt_action)
        mk_menu.addAction(mk_shift_action)
        mk_menu.addAction(mk_right_shift_action)
        mk_menu.addAction(mk_windows_key_action)
        mk_menu.addAction(mk_right_windows_key_action)
        mk_menu.addAction(mk_apps_key_action)

        mk_base_action = QAction("&Modifier Keys", self)
        mk_base_action.setMenu(mk_menu)
        self.addAction(mk_base_action)

    def _create_standard_keys_menu(self):
        separator_1_action = QAction(self)
        separator_1_action.setSeparator(True)
        separator_2_action = QAction(self)
        separator_2_action.setSeparator(True)
        separator_3_action = QAction(self)
        separator_3_action.setSeparator(True)
        separator_4_action = QAction(self)
        separator_4_action.setSeparator(True)
        sk_escape_action = QAction('&Escape', self)
        sk_space_action = QAction('&Space', self)
        sk_return_action = QAction('&Return', self)
        sk_tab_action = QAction('&Tab', self)
        sk_backspace_action = QAction('&Backspace', self)
        sk_delete_action = QAction('&Delete', self)
        sk_insert_action = QAction('&Insert', self)
        sk_home_action = QAction('&Home', self)
        sk_end_action = QAction('&End', self)
        sk_pg_up_action = QAction('&Page Up', self)
        sk_pg_down_action = QAction('&Page Down', self)
        sk_prnt_screen_action = QAction('&PrntScn', self)
        sk_pause_action = QAction('&Pause', self)
        sk_break_action = QAction('&Break', self)
        sk_caps_lock_toggle_action = QAction('&CAPS Lock Toggle', self)
        sk_caps_lock_on_action = QAction('&Caps Lock On', self)
        sk_caps_lock_off_action = QAction('&Caps Lock Off', self)
        sk_scroll_lock_toggle = QAction('&Scroll Lock Toggle', self)
        sk_scroll_lock_on = QAction('&Scroll Lock On', self)
        sk_scroll_lock_off = QAction('&Scroll Lock Off', self)
        sk_escape_action.triggered.connect(lambda x: self.on_action_triggered(sk_escape_action.text()))
        sk_space_action.triggered.connect(lambda x: self.on_action_triggered(sk_space_action.text()))
        sk_return_action.triggered.connect(lambda x: self.on_action_triggered(sk_return_action.text()))
        sk_tab_action.triggered.connect(lambda x: self.on_action_triggered(sk_tab_action.text()))
        sk_backspace_action.triggered.connect(lambda x: self.on_action_triggered(sk_backspace_action.text()))
        sk_delete_action.triggered.connect(lambda x: self.on_action_triggered(sk_delete_action.text()))
        sk_insert_action.triggered.connect(lambda x: self.on_action_triggered(sk_insert_action.text()))
        sk_home_action.triggered.connect(lambda x: self.on_action_triggered(sk_home_action.text()))
        sk_end_action.triggered.connect(lambda x: self.on_action_triggered(sk_end_action.text()))
        sk_pg_up_action.triggered.connect(lambda x: self.on_action_triggered(sk_pg_up_action.text()))
        sk_pg_down_action.triggered.connect(lambda x: self.on_action_triggered(sk_pg_down_action.text()))
        sk_prnt_screen_action.triggered.connect(lambda x: self.on_action_triggered(sk_prnt_screen_action.text()))
        sk_pause_action.triggered.connect(lambda x: self.on_action_triggered(sk_pause_action.text()))
        sk_break_action.triggered.connect(lambda x: self.on_action_triggered(sk_break_action.text()))
        sk_caps_lock_toggle_action.triggered.connect(lambda x: self.on_action_triggered(sk_caps_lock_toggle_action.text()))
        sk_caps_lock_on_action.triggered.connect(lambda x: self.on_action_triggered(sk_caps_lock_on_action.text()))
        sk_caps_lock_off_action.triggered.connect(lambda x: self.on_action_triggered(sk_caps_lock_off_action.text()))
        sk_scroll_lock_toggle.triggered.connect(lambda x: self.on_action_triggered(sk_scroll_lock_toggle.text()))
        sk_scroll_lock_on.triggered.connect(lambda x: self.on_action_triggered(sk_scroll_lock_on.text()))
        sk_scroll_lock_off.triggered.connect(lambda x: self.on_action_triggered(sk_scroll_lock_off.text()))
        sk_menu = QMenu(self)
        sk_menu.addAction(sk_escape_action)
        sk_menu.addAction(sk_space_action)
        sk_menu.addAction(sk_return_action)
        sk_menu.addAction(sk_tab_action)
        sk_menu.addAction(sk_backspace_action)
        sk_menu.addAction(separator_1_action)
        sk_menu.addAction(sk_delete_action)
        sk_menu.addAction(sk_insert_action)
        sk_menu.addAction(sk_home_action)
        sk_menu.addAction(sk_end_action)
        sk_menu.addAction(sk_pg_up_action)
        sk_menu.addAction(sk_pg_down_action)
        sk_menu.addAction(separator_2_action)
        sk_menu.addAction(sk_prnt_screen_action)
        sk_menu.addAction(sk_pause_action)
        sk_menu.addAction(sk_break_action)
        sk_menu.addAction(separator_3_action)
        sk_menu.addAction(sk_caps_lock_toggle_action)
        sk_menu.addAction(sk_caps_lock_on_action)
        sk_menu.addAction(sk_caps_lock_off_action)
        sk_menu.addAction(separator_4_action)
        sk_menu.addAction(sk_scroll_lock_toggle)
        sk_menu.addAction(sk_scroll_lock_on)
        sk_menu.addAction(sk_scroll_lock_off)

        sk_base_action = QAction('&Standard Keys', self)
        sk_base_action.setMenu(sk_menu)
        self.addAction(sk_base_action)

    def _create_direction_keys_menu(self):
        up_action = QAction('&Up')
        down_action = QAction('&Down')
        left_action = QAction('&Left')
        right_action = QAction('&Right')

        up_action.triggered.connect(lambda x: self.on_action_triggered(up_action.text()))
        down_action.triggered.connect(lambda x: self.on_action_triggered(down_action.text()))
        left_action.triggered.connect(lambda x: self.on_action_triggered(left_action.text()))
        right_action.triggered.connect(lambda x: self.on_action_triggered(right_action.text()))

        menu = QMenu(self)
        menu.addAction(up_action)
        menu.addAction(down_action)
        menu.addAction(left_action)
        menu.addAction(right_action)

        base_action = QAction('&Direction Keys', self)
        base_action.setMenu(menu)
        self.addAction(base_action)

    def _create_function_keys_menu(self):
        f1_action = QAction('&F1')
        f2_action = QAction('&F2')
        f3_action = QAction('&F3')
        f4_action = QAction('&F4')
        f5_action = QAction('&F5')
        f6_action = QAction('&F6')
        f7_action = QAction('&F7')
        f8_action = QAction('&F8')
        f9_action = QAction('&F9')
        f10_action = QAction('&F10')
        f11_action = QAction('&F11')
        f12_action = QAction('&F12')
        f13_action = QAction('&F13')
        f14_action = QAction('&F14')
        f15_action = QAction('&F15')
        f16_action = QAction('&F16')
        f17_action = QAction('&F17')
        f18_action = QAction('&F18')
        f19_action = QAction('&F19')
        f20_action = QAction('&F20')
        f1_action.triggered.connect(lambda x: self.on_action_triggered(f1_action.text()))
        f2_action.triggered.connect(lambda x: self.on_action_triggered(f2_action.text()))
        f3_action.triggered.connect(lambda x: self.on_action_triggered(f3_action.text()))
        f4_action.triggered.connect(lambda x: self.on_action_triggered(f4_action.text()))
        f5_action.triggered.connect(lambda x: self.on_action_triggered(f5_action.text()))
        f6_action.triggered.connect(lambda x: self.on_action_triggered(f6_action.text()))
        f7_action.triggered.connect(lambda x: self.on_action_triggered(f7_action.text()))
        f8_action.triggered.connect(lambda x: self.on_action_triggered(f8_action.text()))
        f9_action.triggered.connect(lambda x: self.on_action_triggered(f9_action.text()))
        f10_action.triggered.connect(lambda x: self.on_action_triggered(f10_action.text()))
        f11_action.triggered.connect(lambda x: self.on_action_triggered(f11_action.text()))
        f12_action.triggered.connect(lambda x: self.on_action_triggered(f12_action.text()))
        f13_action.triggered.connect(lambda x: self.on_action_triggered(f13_action.text()))
        f14_action.triggered.connect(lambda x: self.on_action_triggered(f14_action.text()))
        f15_action.triggered.connect(lambda x: self.on_action_triggered(f15_action.text()))
        f16_action.triggered.connect(lambda x: self.on_action_triggered(f16_action.text()))
        f17_action.triggered.connect(lambda x: self.on_action_triggered(f17_action.text()))
        f18_action.triggered.connect(lambda x: self.on_action_triggered(f18_action.text()))
        f19_action.triggered.connect(lambda x: self.on_action_triggered(f19_action.text()))
        f20_action.triggered.connect(lambda x: self.on_action_triggered(f20_action.text()))
        menu = QMenu(self)
        menu.addAction(f1_action)
        menu.addAction(f2_action)
        menu.addAction(f3_action)
        menu.addAction(f4_action)
        menu.addAction(f5_action)
        menu.addAction(f6_action)
        menu.addAction(f7_action)
        menu.addAction(f8_action)
        menu.addAction(f9_action)
        menu.addAction(f10_action)
        menu.addAction(f11_action)
        menu.addAction(f12_action)
        menu.addAction(f13_action)
        menu.addAction(f14_action)
        menu.addAction(f15_action)
        menu.addAction(f16_action)
        menu.addAction(f17_action)
        menu.addAction(f18_action)
        menu.addAction(f19_action)
        menu.addAction(f20_action)
        base_action = QAction('&Function Keys', self)
        base_action.setMenu(menu)
        self.addAction(base_action)

    def _create_media_keys_menu(self):
        vol_up_action = QAction('&Volume Up')
        vol_down_action = QAction('&Volume Down')
        mute_action = QAction('&Mute')
        play_pause_action = QAction('&Play/Pause')
        stop_action = QAction('&Stop')
        next_action = QAction('&Next Track')
        previous_action = QAction('&Previous Track')
        vol_up_action.triggered.connect(lambda x: self.on_action_triggered(vol_up_action.text()))
        vol_down_action.triggered.connect(lambda x: self.on_action_triggered(vol_down_action.text()))
        mute_action.triggered.connect(lambda x: self.on_action_triggered(mute_action.text()))
        play_pause_action.triggered.connect(lambda x: self.on_action_triggered(play_pause_action.text()))
        stop_action.triggered.connect(lambda x: self.on_action_triggered(stop_action.text()))
        next_action.triggered.connect(lambda x: self.on_action_triggered(next_action.text()))
        previous_action.triggered.connect(lambda x: self.on_action_triggered(previous_action.text()))
        menu = QMenu(self)
        menu.addAction(vol_up_action)
        menu.addAction(vol_down_action)
        menu.addAction(mute_action)
        menu.addAction(play_pause_action)
        menu.addAction(stop_action)
        menu.addAction(next_action)
        menu.addAction(previous_action)
        base_action = QAction('&Media Keys', self)
        base_action.setMenu(menu)
        self.addAction(base_action)


    @Slot(object)
    def on_action_triggered(self, action_text: str):
        text = key_table.get(action_text)
        if text:
            new_line_text = self._line_edit.text() + text
            self._line_edit.setText(new_line_text)
