from PySide6.QtCore import QObject, Signal
from pynput.mouse import Listener, Button


class MouseHandler(QObject):
    on_lmb_click = Signal(bool)
    on_rmb_click = Signal(bool)
    on_mmb_click = Signal(bool)
    on_mb4_click = Signal(bool)
    on_mb5_click = Signal(bool)
    on_scroll_up = Signal(bool)
    on_scroll_down = Signal(bool)

    def __init__(self):
        super().__init__()
        self._listener = Listener(on_move=None, on_click=self._on_mouse_click, on_scroll=self._on_scroll)
        self._listener.start()

    def _on_mouse_click(self, x, y, button: Button, pressed):
        if button.name == "left":
            self.on_lmb_click.emit(pressed)
        elif button.name == "right":
            self.on_rmb_click.emit(pressed)
        elif button.name == "middle":
            self.on_mmb_click.emit(pressed)
        elif button.name == "button8" or button.name == "x1":
            self.on_mb4_click.emit(pressed)
        elif button.name == "button9" or button.name == "x2":
            self.on_mb5_click.emit(pressed)

    def _on_scroll(self, x, y, dx, dy):
        if dy < 0:
            self.on_scroll_down.emit(True)
        else:
            self.on_scroll_up.emit(True)
