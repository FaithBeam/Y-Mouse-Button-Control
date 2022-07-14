from typing import Optional

from PySide6.QtCore import Signal, QObject

from models.mapping_commands import MappingInterface, NothingMapping


class Layer(QObject):
    on_left_mouse_button_changed = Signal(object)
    on_right_mouse_button_changed = Signal(object)
    on_middle_mouse_button_changed = Signal(object)
    on_mouse_button_4_changed = Signal(object)
    on_mouse_button_5_changed = Signal(object)
    on_scroll_up_changed = Signal(object)
    on_scroll_down_changed = Signal(object)
    on_tilt_wheel_left_changed = Signal(object)
    on_tilt_wheel_right_changed = Signal(object)

    def to_json(self):
        return {
            "layerName": self.name,
            "leftButton": self.left_mouse_button.to_json() if self.left_mouse_button else None,
            "rightButton": self.right_mouse_button.to_json() if self.right_mouse_button else None,
            "middleButton": self.middle_mouse_button.to_json() if self.middle_mouse_button else None,
            "mouseButton4": self.mouse_button_4.to_json() if self.mouse_button_4 else None,
            "mouseButton5": self.mouse_button_5.to_json() if self.mouse_button_5 else None,
            "scrollUp": self.scroll_up.to_json() if self.scroll_up else None,
            "scrollDown": self.scroll_down.to_json() if self.scroll_down else None,
            "tiltWheelLeft": self.tilt_wheel_left.to_json() if self.tilt_wheel_left else None,
            "tiltWheelRight": self.tilt_wheel_right.to_json() if self.tilt_wheel_right else None,
        }

    @property
    def name(self):
        return self._name

    @property
    def left_mouse_button(self):
        return self._left_mouse_button

    @left_mouse_button.setter
    def left_mouse_button(self, value: MappingInterface):
        self._left_mouse_button = value
        self.on_left_mouse_button_changed.emit(value)

    @property
    def right_mouse_button(self):
        return self._right_mouse_button

    @right_mouse_button.setter
    def right_mouse_button(self, value: MappingInterface):
        self._right_mouse_button = value
        self.on_right_mouse_button_changed.emit(value)

    @property
    def middle_mouse_button(self):
        return self._middle_mouse_button

    @middle_mouse_button.setter
    def middle_mouse_button(self, value: MappingInterface):
        self._middle_mouse_button = value
        self.on_middle_mouse_button_changed.emit(value)

    @property
    def mouse_button_4(self):
        return self._mouse_button_4

    @mouse_button_4.setter
    def mouse_button_4(self, value: MappingInterface):
        self._mouse_button_4 = value
        self.on_mouse_button_4_changed.emit(value)

    @property
    def mouse_button_5(self):
        return self._mouse_button_5

    @mouse_button_5.setter
    def mouse_button_5(self, value: MappingInterface):
        self._mouse_button_5 = value
        self.on_mouse_button_5_changed.emit(value)

    @property
    def scroll_up(self):
        return self._scroll_up

    @scroll_up.setter
    def scroll_up(self, value: MappingInterface):
        self._scroll_up = value
        self.on_scroll_up_changed.emit(value)

    @property
    def scroll_down(self):
        return self._scroll_down

    @scroll_down.setter
    def scroll_down(self, value: MappingInterface):
        self._scroll_down = value
        self.on_scroll_down_changed.emit(value)

    @property
    def tilt_wheel_left(self):
        return self._tilt_wheel_left

    @tilt_wheel_left.setter
    def tilt_wheel_left(self, value: MappingInterface):
        self._tilt_wheel_left = value
        self.on_tilt_wheel_left_changed.emit(value)

    @property
    def tilt_wheel_right(self):
        return self._tilt_wheel_right

    @tilt_wheel_right.setter
    def tilt_wheel_right(self, value: MappingInterface):
        self._tilt_wheel_right = value
        self.on_tilt_wheel_right_changed.emit(value)

    def __init__(
            self,
            name: Optional[str] = None,
            left_mouse_button: Optional[MappingInterface] = NothingMapping(),
            right_mouse_button: Optional[MappingInterface] = NothingMapping(),
            middle_mouse_button: Optional[MappingInterface] = NothingMapping(),
            mouse_button_4: Optional[MappingInterface] = NothingMapping(),
            mouse_button_5: Optional[MappingInterface] = NothingMapping(),
            scroll_up: Optional[MappingInterface] = NothingMapping(),
            scroll_down: Optional[MappingInterface] = NothingMapping(),
            tilt_wheel_left: Optional[MappingInterface] = NothingMapping(),
            tilt_wheel_right: Optional[MappingInterface] = NothingMapping(),
    ):
        super().__init__()
        self._name = name
        self._left_mouse_button = left_mouse_button
        self._right_mouse_button = right_mouse_button
        self._middle_mouse_button = middle_mouse_button
        self._mouse_button_4 = mouse_button_4
        self._mouse_button_5 = mouse_button_5
        self._scroll_up = scroll_up
        self._scroll_down = scroll_down
        self._tilt_wheel_left = tilt_wheel_left
        self._tilt_wheel_right = tilt_wheel_right

    def do_click(self, pressed: bool, button: str):
        if button == 'lmb':
            self._try_run(pressed, self._left_mouse_button)
        elif button == 'rmb':
            self._try_run(pressed, self._right_mouse_button)
        elif button == 'mmb':
            self._try_run(pressed, self._middle_mouse_button)
        elif button == 'mb4':
            self._try_run(pressed, self._mouse_button_4)
        elif button == 'mb5':
            self._try_run(pressed, self._mouse_button_5)
        elif button == 'scroll_up':
            self._try_run(pressed, self._scroll_up)
        elif button == 'scroll_down':
            self._try_run(pressed, self._scroll_down)
        elif button == 'tilt_left':
            self._try_run(pressed, self._tilt_wheel_left)
        elif button == 'tilt_right':
            self._try_run(pressed, self._tilt_wheel_right)

    def _try_run(self, pressed, mapping):
        if mapping is not None and not isinstance(mapping, NothingMapping):
            mapping.run(pressed)
