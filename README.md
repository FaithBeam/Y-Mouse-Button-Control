# Y-Mouse Button Control

*This is alpha software. There will be bugs and things will not behave like you expect them to.*

This is an attempt to clone the excellent [X-Mouse Button Control](https://www.highrez.co.uk/downloads/xmousebuttoncontrol.htm) for Linux/Windows/Mac.

![](https://i.imgur.com/4PeiT2q.png)

## Requirements

* At least Python 3.10

**Windows**

* At least Windows 10 (QT6 doesn't support < Windows 10)

**Linux**

* X11 (Sorry, pynput doesn't support Wayland yet)

**Mac**

* ?

## Run from Source

```
pip -r requirements.txt
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