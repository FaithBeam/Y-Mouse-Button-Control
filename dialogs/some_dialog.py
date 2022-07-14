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

    @Slot(object)
    def on_action_triggered(self, action_text: str):
        text = key_table.get(action_text)
        if text:
            new_line_text = self._line_edit.text() + text
            self._line_edit.setText(new_line_text)
