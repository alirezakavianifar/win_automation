import pywinauto
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from pywinauto import keyboard as kb

app = Application().start(cmd_line=r"C:\Program Files\Notepad++\notepad++.exe")
