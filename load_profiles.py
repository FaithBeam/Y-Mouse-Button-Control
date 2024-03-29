import json

from UI.models.mapping_commands import MappingFactory
from UI.models.action_type import ActionTypeFactory
from UI.models.layer import Layer
from UI.models.profile import Profiles, Profile


def get_profiles(path) -> Profiles:
    with open(path, "r") as f:
        profiles_dict = json.load(f)
        profiles = Profiles()
        for key, value in profiles_dict.items():
            profiles.add(Profile(
                name=key,
                layer_1=get_layer(value['layer1']),
                layer_2=get_layer(value['layer2']),
                description=value['description'],
                window_caption=value['windowCaption'],
                process=value['process'],
                window_class=value['windowClass'],
                parent_class=value['parentClass'],
                match_type=value['matchType'],
                checked_value=value['checked']
            ))
        return profiles


def get_layer(layer: dict):
    if layer:
        return Layer(
            name=layer['layerName'],
            left_mouse_button=get_mapping(layer['leftButton']),
            right_mouse_button=get_mapping(layer['rightButton']),
            middle_mouse_button=get_mapping(layer['middleButton']),
            mouse_button_4=get_mapping(layer['mouseButton4']),
            mouse_button_5=get_mapping(layer['mouseButton5']),
            scroll_up=get_mapping(layer['scrollUp']),
            scroll_down=get_mapping(layer['scrollDown']),
            tilt_wheel_left=get_mapping(layer['tiltWheelLeft']),
            tilt_wheel_right=get_mapping(layer['tiltWheelRight'])
        )
    else:
        return Layer()


def get_mapping(mapping: dict):
    if mapping is None:
        return None
    key, value = next(iter(mapping.items()))
    return MappingFactory.create(key, keys=value['keys'], action_type=ActionTypeFactory.create(value['type']))
