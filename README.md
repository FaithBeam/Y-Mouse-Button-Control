# Y-Mouse Button Control

*This is alpha software. There will be bugs and things will not behave like you expect them to.*

This is an attempt to clone the excellent [X-Mouse Button Control](https://www.highrez.co.uk/downloads/xmousebuttoncontrol.htm) for Linux/Windows/Mac.

![](https://i.imgur.com/3522t4u.png)

## Requirements

* Python <3.11, >=3.6

**Windows**

* Windows 10 and newer

**Linux**

* X11 (Sorry, pynput doesn't support Wayland yet)
* Ubuntu 20.04, CentOS 8.1, OpenSuSE 15.1 and newer

**Mac**

* macOS 10.14 and newer

## Run from Source

```
git clone https://github.com/FaithBeam/Y-Mouse-Button-Control
cd Y-Mouse-Button-Control
pip install -r requirements.txt
python main.py
```

## Gotchas

* No blocking original mouse input
* Unable to recognize if a window is visible (It can tell if it is running right now)
* Opening and closing the program too many times on Windows will cause WMI to spew errors which will cause the program to not function. Usually not an issue if you're not developing this but a restart will fix it
* Does not handle dark themes well with respect to highlighting the mouse button combo boxes

## Credits

* PySide6
* pynput
* psutil
* wmi
* Python GUIs
* PyInstaller
* Mouse icon by [Yusuke Kamiyamane](https://p.yusukekamiyamane.com/)
