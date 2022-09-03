from abc import ABC, abstractmethod


class MappingInterface(ABC):
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
    def can_raise_dialog(self) -> bool:
        pass

    @abstractmethod
    def run(self, pressed):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def to_json(self) -> dict:
        pass


class MappingFactory:
    subclasses = {}

    @classmethod
    def get_mappings(cls) -> list[MappingInterface]:
        # lmao
        # return objects with integer keys from subclasses
        filtered = list(map(lambda x: cls.subclasses[x], list(filter(lambda k: isinstance(k, int), cls.subclasses.keys()))))
        mappings = []
        for a in filtered:
            if a.can_raise_dialog:
                mappings.append(a(None))
            else:
                mappings.append(a())
        return mappings

    @classmethod
    def register_subclass(cls, command_mapping):
        def decorator(subclass):
            cls.subclasses[command_mapping] = subclass
            return subclass

        return decorator

    @classmethod
    def create(cls, mapping_type, **kwargs):
        if mapping_type not in cls.subclasses:
            raise ValueError('Bad mapping type {}'.format(mapping_type))

        return cls.subclasses[mapping_type](kwargs)


@MappingFactory.register_subclass('nothing')
@MappingFactory.register_subclass(0)
class NothingMapping(MappingInterface):
    index = 0
    description = "** No Change (Don't intercept) **"
    can_raise_dialog = False

    def __init__(self):
        pass

    def __str__(self):
        return self.description

    def run(self, pressed: bool):
        pass

    def stop(self):
        pass

    def to_json(self) -> dict:
        pass


@MappingFactory.register_subclass('disabled')
@MappingFactory.register_subclass(1)
class DisabledMapping(MappingInterface):
    def run(self, pressed):
        pass

    def stop(self):
        pass

    index = 1
    description = "Disable"
    can_raise_dialog = False

    def __init__(self):
        self._activated = False

    def __str__(self):
        return "Disable"

    def to_json(self) -> dict:
        pass


@MappingFactory.register_subclass('simulatedKeystrokes')
@MappingFactory.register_subclass(2)
class SimulatedKeystrokesMapping(MappingInterface):
    index = 2
    description = "Simulated Keys (undefined)"
    can_raise_dialog = True

    def __init__(self, kwargs):
        self.keys = None
        self.action_type = None
        if kwargs is not None and len(kwargs) > 0:
            if 'keys' in kwargs:
                self.keys = kwargs['keys']
            if 'action_type' in kwargs:
                self.action_type = kwargs['action_type']

    def __str__(self):
        my_str = "Simulated Keys: ({})"
        if self.action_type is not None:
            my_str = my_str.format(self.action_type.short_description)
        else:
            my_str = my_str.format("undefined")
        if self.keys is not None:
            my_str += f"[{self.keys}]"
        return my_str

    def to_json(self) -> dict:
        return {
            "simulatedKeystrokes": {
                "keys": self.keys,
                "type": self.action_type.index
            }
        }

    def run(self, pressed: bool):
        self.action_type.run(pressed, self.keys)

    def stop(self):
        self.action_type.stop(self.keys)
