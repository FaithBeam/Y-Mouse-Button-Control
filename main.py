import sys
import multiprocessing

from PySide6.QtWidgets import QApplication, QStyleFactory

from config import Config
from mkb.mkb_controller import MKBController
from process_monitor import ProcessMonitor
from load_profiles import get_profiles
from UI.views.main_view import MainView
from globals import mouse_handler


class App(QApplication):
    def __init__(self, app_config, sys_argv):
        super(App, self).__init__(sys_argv)

        self._mutex = multiprocessing.Lock()
        self._running_processes = multiprocessing.Manager().dict()
        ProcessMonitor(self._mutex, self._running_processes)
        self._profiles = get_profiles(app_config.profile_location)
        self._profiles.current_profile = self._profiles.profiles[0]
        MKBController(mouse_handler, self._profiles, self._mutex, self._running_processes)
        self.main_view = MainView(app_config, self._profiles)
        self.setQuitOnLastWindowClosed(False)
        self.setStyle(QStyleFactory.create('Fusion'))
        self.main_view.show()


if __name__ == "__main__":
    if sys.platform.startswith('win'):
        multiprocessing.freeze_support()

    config = Config()

    app = App(config, sys.argv)
    sys.exit(app.exec())
