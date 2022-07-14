from abc import ABC, abstractmethod
from threading import Thread
from time import sleep

from pynput.keyboard import Key
from pynput.mouse import Button
from globals import mouse_controller, keyboard_controller


class ActionTypeFactory:
    subclasses = {}

    @classmethod
    def get_action_types(cls) -> list[str]:
        return list(map(lambda x: x.description, cls.subclasses.values()))

    @classmethod
    def register_subclass(cls, action_type_type):
        def decorator(subclass):
            cls.subclasses[action_type_type] = subclass
            return subclass

        return decorator

    @classmethod
    def create(cls, action_type):
        if action_type not in cls.subclasses:
            raise ValueError('Bad action type {}'.format(action_type))

        return cls.subclasses[action_type]()


class ActionTypeInterface(ABC):
    @property
    @abstractmethod
    def index(self) -> int:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def short_description(self) -> str:
        pass

    @property
    @abstractmethod
    def enabled(self) -> bool:
        pass

    @abstractmethod
    def run(self, pressed, keys):
        pass

    @abstractmethod
    def stop(self, keys):
        pass


@ActionTypeFactory.register_subclass(1)
class MousePressedActionType(ActionTypeInterface):
    index = 1
    description = f"{index} As mouse is pressed"
    short_description = "pressed"
    enabled = True

    def __init__(self):
        super().__init__()
        self._keys = []

    def run(self, pressed, keys=None):
        self._keys = parse_string(keys)
        if pressed:
            for k in self._keys:
                keyboard_controller.tap(k)

    def stop(self, keys=None):
        pass


@ActionTypeFactory.register_subclass(2)
class MouseReleasedActionType(ActionTypeInterface):
    index = 2
    description = f"{index} As mouse is released"
    short_description = "released"
    enabled = True

    def __init__(self):
        super().__init__()
        self._keys = []

    def run(self, pressed, keys=None):
        self._keys = parse_string(keys)
        if not pressed:
            for k in self._keys:
                keyboard_controller.tap(k)

    def stop(self, keys=None):
        pass


@ActionTypeFactory.register_subclass(3)
class DuringActionType(ActionTypeInterface):
    index = 3
    description = f"{index} During (press on down, release on up)"
    short_description = "during"
    enabled = True

    def __init__(self):
        super().__init__()

    def run(self, pressed, keys=None):
        pass

    def stop(self, keys=None):
        pass


@ActionTypeFactory.register_subclass(4)
class ThreadDownActionType(ActionTypeInterface):
    index = 4
    description = f"{index} In another thread as mouse button is pressed"
    short_description = "thread-down"
    enabled = False

    def __init__(self):
        super().__init__()

    def run(self, pressed, keys=None):
        pass

    def stop(self, keys=None):
        pass


@ActionTypeFactory.register_subclass(5)
class ThreadUpActionType(ActionTypeInterface):
    index = 5
    description = f"{index} In another thread as mouse button is released"
    short_description = "thread-up"
    enabled = False

    def __init__(self):
        super().__init__()

    def run(self, pressed, keys=None):
        pass

    def stop(self, keys=None):
        pass


@ActionTypeFactory.register_subclass(6)
class RepeatActionType(ActionTypeInterface):
    index = 6
    description = f"{index} Repeatedly while the button is down"
    short_description = "repeat"
    enabled = True

    def __init__(self):
        super().__init__()
        self._my_thread = None
        self._state = False
        self._keys = []

    def run(self, pressed, keys=None):
        self._keys = parse_string(keys)
        if pressed:
            # this should never occur?
            if self._state:
                self._state = False
            else:
                self._state = True
                self._my_thread = Thread(target=self._actually_run, args=(), daemon=True)
                self._my_thread.start()
        else:
            self._state = False

    def _actually_run(self):
        while True:
            for k in self._keys:
                if self._state:
                    sleep(0.05)
                    if isinstance(k, str):
                        keyboard_controller.tap(k)
                    if isinstance(k, Key):
                        keyboard_controller.tap(k)
                    elif isinstance(k, Button):
                        mouse_controller.tap(k)
                else:
                    return

    def stop(self, keys=None):
        self._state = False


@ActionTypeFactory.register_subclass(7)
class StickyRepeatActionType(ActionTypeInterface):
    index = 7
    description = f"{index} Sticky (repeatedly until button is pressed again)"
    short_description = "sticky repeat"
    enabled = True

    def __init__(self):
        super().__init__()
        self._my_thread = None
        self._state = False
        self._keys = []

    def run(self, pressed, keys=None):
        self._keys = parse_string(keys)
        if pressed:
            if self._state:
                self._state = False
            else:
                self._state = True
                self._my_thread = Thread(target=self._actually_run, args=(), daemon=True)
                self._my_thread.start()

    def _actually_run(self):
        while True:
            for k in self._keys:
                if self._state:
                    sleep(0.05)
                    if isinstance(k, str):
                        keyboard_controller.tap(k)
                    if isinstance(k, Key):
                        keyboard_controller.tap(k)
                    elif isinstance(k, Button):
                        mouse_controller.tap(k)
                else:
                    return

    def stop(self, keys=None):
        self._state = False


@ActionTypeFactory.register_subclass(8)
class StickyHoldActionType(ActionTypeInterface):
    index = 8
    description = f"{index} Sticky (held down until button is pressed again)"
    short_description = "sticky hold"
    enabled = True

    def __init__(self):
        super().__init__()
        self._state = False
        self._keys = []

    def run(self, pressed: bool, keys: str):
        self._keys = parse_string(keys)
        # Holds key for games but is not repeated
        if pressed:
            if self._state:
                self.stop(keys)
            else:
                self._state = True
                for k in self._keys:
                    if isinstance(k, str):
                        keyboard_controller.press(k)
                    if isinstance(k, Key):
                        keyboard_controller.press(k)
                    elif isinstance(k, Button):
                        mouse_controller.press(k)

    def stop(self, keys: str):
        if self._state:
            for k in reversed(self._keys):
                if isinstance(k, str):
                    keyboard_controller.release(k)
                if isinstance(k, Key):
                    keyboard_controller.release(k)
                elif isinstance(k, Button):
                    mouse_controller.release(k)
            self._state = False


@ActionTypeFactory.register_subclass(9)
class PressedAndReleasedActionType(ActionTypeInterface):
    index = 9
    description = f"{index} As mouse button is pressed & when released"
    short_description = "pressed & released"
    enabled = True

    def __init__(self):
        super().__init__()
        self._keys = []

    def run(self, pressed: bool, keys: str):
        self._keys = parse_string(keys)
        for k in self._keys:
            if isinstance(k, str):
                keyboard_controller.press(k)
            if isinstance(k, Key):
                keyboard_controller.press(k)
            elif isinstance(k, Button):
                mouse_controller.press(k)

    def stop(self, keys):
        pass


modifier_table = {
    'ALT': Key.alt,
    'APPS': Key.menu,
    'BACKSPACE': Key.backspace,
    'BREAK': Key.pause,
    'CAPSLOCK': Key.caps_lock,
    'CTRL': Key.ctrl,
    'DEL': Key.delete,
    'DOWN': Key.down,
    'END': Key.end,
    'ESC': Key.esc,
    'HOME': Key.home,
    'INS': Key.insert,
    'LEFT': Key.left,
    'PGDN': Key.page_down,
    'PGUP': Key.page_up,
    'PAUSE': Key.pause,
    'PRTSCN': Key.print_screen,
    'RETURN': Key.enter,
    'RIGHT': Key.right,
    'RALT': Key.alt_r,
    'RCTRL': Key.ctrl_r,
    'RMB': Button.right,
    'RSHIFT': Key.shift_r,
    'RWIN': Key.cmd_r,
    'SCROLLLOCK': Key.scroll_lock,
    'SHIFT': Key.shift,
    'SPACE': Key.space,
    'TAB': Key.tab,
    'UP': Key.up,
    'WIN': Key.cmd,
}


def get_modifier(key):
    return modifier_table.get(key)


def parse_string(my_str: str) -> list:
    keys = []
    i = 0
    while i < len(my_str):
        if my_str[i] == '{':
            for j in range(i, len(my_str)):
                if my_str[j] == '}':
                    keys.append(get_modifier(my_str[i + 1:j]))
                    i = j
                    break
            i += 1
        else:
            keys.append(my_str[i])
            i += 1
    return keys
