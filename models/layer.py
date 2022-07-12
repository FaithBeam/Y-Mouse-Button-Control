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

    def __init__(
            self,
            name: Optional[str] = None,
            left_mouse_button: Optional[MappingInterface] = NothingMapping(),
            right_mouse_button: Optional[MappingInterface] = NothingMapping(),
            middle_mouse_button: Optional[MappingInterface] = NothingMapping(),
            mouse_button_4: Optional[MappingInterface] = NothingMapping(),
            mouse_button_5: Optional[MappingInterface] = NothingMapping(),
            scroll_up: Optional[MappingInterface] = NothingMapping(),
            scroll_down: Optional[MappingInterface] = NothingMapping()
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

    def do_click(self, pressed: bool, button: str):
        match button:
            case "lmb":
                if self._left_mouse_button is not None and not isinstance(self._left_mouse_button, NothingMapping):
                    self._left_mouse_button.run(pressed)
            case "rmb":
                if self._right_mouse_button is not None and not isinstance(self._right_mouse_button, NothingMapping):
                    self._right_mouse_button.run(pressed)
            case "mmb":
                if self._middle_mouse_button is not None and not isinstance(self._middle_mouse_button, NothingMapping):
                    self._middle_mouse_button.run(pressed)
            case "mb4":
                if self._mouse_button_4 is not None and not isinstance(self._mouse_button_4, NothingMapping):
                    self._mouse_button_4.run(pressed)
            case "mb5":
                if self._mouse_button_5 is not None and not isinstance(self._mouse_button_5, NothingMapping):
                    self._mouse_button_5.run(pressed)
            case "scroll_up":
                if self._scroll_up is not None and not isinstance(self._scroll_up, NothingMapping):
                    self._scroll_up.run(pressed)
            case "scroll_down":
                if self._scroll_down is not None and not isinstance(self._scroll_down, NothingMapping):
                    self._scroll_down.run(pressed)
