import platform
import sys
from multiprocessing import Process
from threading import Thread
from time import sleep

from psutil import process_iter
if sys.platform.startswith('win'):
    import wmi
    c = wmi.WMI()


def get_processes() -> list[str]:
    procs = set()
    for proc in process_iter(['name']):
        with proc.oneshot():
            if proc.name():
                procs.add(proc.name())
    return sorted(procs)


class ProcessMonitor:
    def __init__(self, mutex, running_processes):
        if platform.system().lower().startswith('win'):
            # Create processes because wmi won't work from a thread
            t1 = Thread(target=update_processes, args=(mutex, running_processes,), daemon=True)
            t1.start()
            p2 = Process(target=self._win_monitor_process_creation, args=(mutex, running_processes,), daemon=True)
            p2.start()
            p3 = Process(target=self._win_monitor_process_deletion, args=(mutex, running_processes,), daemon=True)
            p3.start()
        else:
            t1 = Thread(target=lin_update_processes, args=(mutex, running_processes,), daemon=True)
            t1.start()


    def _win_monitor_process_creation(self, mutex, running_processes):
        global c
        process_watcher = c.Win32_Process.watch_for("creation")
        while True:
            new_proc = process_watcher()
            with mutex:
                running_processes[new_proc.Name] = None

    def _win_monitor_process_deletion(self, mutex, running_processes):
        global c
        process_watcher = c.Win32_Process.watch_for("deletion")
        while True:
            deleted_proc = process_watcher()
            with mutex:
                running_processes.pop(deleted_proc.Name, None)


def update_processes(mutex, running_processes):
    with mutex:
        running_processes.clear()
        for proc in process_iter(['name']):
            with proc.oneshot():
                if proc.name():
                    running_processes[proc.name()] = None


def lin_update_processes(mutex, running_processes):
    while True:
        sleep(5)
        update_processes(mutex, running_processes)
