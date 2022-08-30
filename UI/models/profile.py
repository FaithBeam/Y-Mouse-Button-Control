from typing import Optional

from PySide6.QtCore import QObject, Signal

from UI.models.mapping_commands import MappingInterface
from UI.models.layer import Layer


class Profile(QObject):
    on_name_changed = Signal(str)
    on_layer_1_changed = Signal(object)
    on_layer_2_changed = Signal(object)
    on_description_changed = Signal(str)
    on_window_caption_changed = Signal(str)
    on_process_changed = Signal(object)
    on_window_class_changed = Signal(str)
    on_parent_class_changed = Signal(str)
    on_match_type_changed = Signal(str)
    on_checked_value_changed = Signal(int)
    on_anything_changed = Signal(object)

    def trigger(self):
        self.on_anything_changed.emit(self)

    def to_json(self):
        return {
            self.name: {
                "layer1": self.layer_1.to_json() if self.layer_1 else None,
                "layer2": self.layer_2.to_json() if self.layer_2 else None,
                "description": self.description,
                "windowCaption": self.window_caption,
                "process": self.process,
                "windowClass": self.window_class,
                "parentClass": self.parent_class,
                "matchType": self.match_type,
                "checked": self.checked_value
            }
        }

    @property
    def name(self):
        if self._name:
            return self._name
        else:
            return "N/A"

    @name.setter
    def name(self, value: str):
        self._name = value
        self.on_name_changed.emit(value)

    @property
    def layer_1(self):
        return self._layer_1

    @layer_1.setter
    def layer_1(self, value: MappingInterface):
        self._layer_1 = value
        self.on_layer_1_changed.emit(value)

    @property
    def layer_2(self):
        return self._layer_2

    @layer_2.setter
    def layer_2(self, value: MappingInterface):
        self._layer_2 = value
        self.on_layer_2_changed.emit(value)

    @property
    def description(self):
        if self._description:
            return self._description
        else:
            return "N/A"

    @description.setter
    def description(self, value: str):
        self._description = value
        self.on_description_changed.emit(value)

    @property
    def window_caption(self):
        if self._window_caption:
            return self._window_caption
        else:
            return "N/A"

    @window_caption.setter
    def window_caption(self, value: str):
        self._window_caption = value
        self.on_window_caption_changed.emit(value)

    @property
    def process(self):
        if len(self._process) > 0:
            return self._process
        else:
            return "N/A"

    @process.setter
    def process(self, value: str):
        self._process = value
        self.on_process_changed.emit(value)

    @property
    def window_class(self):
        if self._window_class:
            return self._window_class
        else:
            return "N/A"

    @window_class.setter
    def window_class(self, value: str):
        self._window_class = value
        self.on_window_class_changed.emit(value)

    @property
    def parent_class(self):
        if self._parent_class:
            return self._parent_class
        else:
            return "N/A"

    @parent_class.setter
    def parent_class(self, value: str):
        self._parent_class = value
        self.on_parent_class_changed.emit(value)

    @property
    def match_type(self):
        if self._match_type:
            return self._match_type
        else:
            return "N/A"

    @match_type.setter
    def match_type(self, value: str):
        self._match_type = value
        self.on_match_type_changed.emit(value)

    @property
    def checked_value(self):
        if self._checked_value:
            return self._checked_value
        else:
            return 0

    @checked_value.setter
    def checked_value(self, value: int):
        self._checked_value = value
        self.on_checked_value_changed.emit(value)

    def __init__(
            self,
            name: Optional[str] = None,
            layer_1: Optional[Layer] = Layer(),
            layer_2: Optional[Layer] = Layer(),
            description: Optional[str] = None,
            window_caption: Optional[str] = None,
            process: str = None,
            window_class: Optional[str] = None,
            parent_class: Optional[str] = None,
            match_type: Optional[str] = None,
            checked_value: Optional[int] = 0,
    ):
        super().__init__()
        self._name = name
        self._layer_1 = layer_1
        self._layer_2 = layer_2
        self._description = description
        self._window_caption = window_caption
        self._process = process
        self._window_class = window_class
        self._parent_class = parent_class
        self._match_type = match_type
        self._checked_value = checked_value


class Profiles(QObject):
    on_profile_added = Signal(object)
    on_profile_removed = Signal(object)
    on_current_profile_changed = Signal(object)
    on_current_profile_edited = Signal(object)

    def __init__(self):
        super().__init__()
        self._profiles = []
        self._current_profile = None

    def current_profile_edited(self):
        self.on_current_profile_edited.emit(self.current_profile)

    @property
    def current_profile(self) -> Profile:
        return self._current_profile

    @current_profile.setter
    def current_profile(self, value: Profile):
        self._current_profile = value
        self.on_current_profile_changed.emit(value)

    @property
    def profiles(self) -> list[Profile]:
        return self._profiles

    def add(self, profile: Profile):
        if profile not in self._profiles:
            self._profiles.append(profile)
            self.on_profile_added.emit(profile)

    def remove(self, index):
        del self._profiles[index]
