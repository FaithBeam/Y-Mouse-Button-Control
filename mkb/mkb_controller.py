from UI.models.mapping_commands import NothingMapping
from mkb.mouse_handler import MouseHandler
from UI.models.profile import Profiles


class MKBController:
    def __init__(self, mouse_handler: MouseHandler, profiles: Profiles, mutex, running_processes):
        self._mouse_handler = mouse_handler
        self._profiles = profiles
        self._mutex = mutex
        self._running_processes = running_processes
        self._mouse_handler.on_lmb_click.connect(lambda pressed: self._should_press(pressed, 'lmb'))
        self._mouse_handler.on_rmb_click.connect(lambda pressed: self._should_press(pressed, 'rmb'))
        self._mouse_handler.on_mmb_click.connect(lambda pressed: self._should_press(pressed, 'mmb'))
        self._mouse_handler.on_mb4_click.connect(lambda pressed: self._should_press(pressed, 'mb4'))
        self._mouse_handler.on_mb5_click.connect(lambda pressed: self._should_press(pressed, 'mb5'))
        self._mouse_handler.on_scroll_up.connect(lambda pressed: self._should_press(pressed, 'scroll_up'))
        self._mouse_handler.on_scroll_down.connect(lambda pressed: self._should_press(pressed, 'scroll_down'))
        self._mouse_handler.on_tilt_wheel_left.connect(lambda pressed: self._should_press(pressed, "tilt_left"))
        self._mouse_handler.on_tilt_wheel_right.connect(lambda pressed: self._should_press(pressed, "tilt_right"))

    def _should_press(self, pressed: bool, button: str):
        for p in self._profiles.profiles:
            if p.checked_value == 2:
                with self._mutex:
                    if p.process == "*" or [x for x in self._running_processes if p.process in x]:
                        if button == 'lmb':
                            self._try_run(pressed, p.layer_1.left_mouse_button)
                        elif button == 'rmb':
                            self._try_run(pressed, p.layer_1.right_mouse_button)
                        elif button == 'mmb':
                            self._try_run(pressed, p.layer_1.middle_mouse_button)
                        elif button == 'mb4':
                            self._try_run(pressed, p.layer_1.mouse_button_4)
                        elif button == 'mb5':
                            self._try_run(pressed, p.layer_1.mouse_button_5)
                        elif button == 'scroll_up':
                            self._try_run(pressed, p.layer_1.scroll_up)
                        elif button == 'scroll_down':
                            self._try_run(pressed, p.layer_1.scroll_down)
                        elif button == 'tilt_left':
                            self._try_run(pressed, p.layer_1.tilt_wheel_left)
                        elif button == 'tilt_right':
                            self._try_run(pressed, p.layer_1.tilt_wheel_right)

    def _try_run(self, pressed, mapping):
        if mapping is not None and not isinstance(mapping, NothingMapping):
            mapping.run(pressed)
