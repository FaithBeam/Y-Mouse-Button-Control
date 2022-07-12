import os.path

from globals import app_author, app_version, app_name
from appdirs import user_config_dir, user_data_dir
from pathlib import Path

import logging


class Config:
    def __init__(self):
        self.config_dir = user_config_dir(app_name, app_author)
        self.data_dir = user_data_dir(app_name, app_author)
        self.profile_location = Path(os.path.join(self.data_dir, 'profile.json'))
        self._check_directories()
        self._check_profile()

    def _check_directories(self):
        for d in [self.config_dir, self.data_dir]:
            if not os.path.exists(d):
                logging.info(f"Creating config directory {d}")
                Path(d).mkdir(parents=True, exist_ok=True)

    def _check_profile(self):
        if not self.profile_location.exists():
            logging.info(f"Creating default profiles.json file at {self.profile_location}")
            with open(self.profile_location, 'w') as f:
                f.write("""{
    "Default": {
        "layer1": {
            "layerName": "Layer 1 Name",
            "leftButton": null,
            "rightButton": null,
            "middleButton": null,
            "mouseButton4": null,
            "mouseButton5": null,
            "scrollUp": null,
            "scrollDown": null
        },
        "layer2": {
            "layerName": null,
            "leftButton": null,
            "rightButton": null,
            "middleButton": null,
            "mouseButton4": null,
            "mouseButton5": null,
            "scrollUp": null,
            "scrollDown": null
        },
        "description": "Default",
        "windowCaption": "N/A",
        "process": "*",
        "windowClass": "N/A",
        "parentClass": "N/A",
        "matchType": "N/A",
        "checked": 2
    }
}""")
