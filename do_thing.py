from mouse_handler import MouseHandler
from UI.models.profile import Profiles


class DoThing:
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
                        p.layer_1.do_click(pressed, button)
