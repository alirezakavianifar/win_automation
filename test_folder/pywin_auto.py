# import pywinauto 
# import win32api
# import pyautogui
# from pywinauto.application import Application
# from pywinauto.keyboard import send_keys
# from pywinauto import keyboard as kb

# pywin.mouse.double_click(button='left', coords=(25, 25))

# print(win32api.GetCursorPos())

import pyautogui, sys
import time
print('Press Ctrl-C to quit.')
try:
    while True:
        x, y = pyautogui.position()
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
except KeyboardInterrupt:
    print('\n')

pyautogui.doubleClick(x=42, y=667)
time.sleep(5)
pyautogui.doubleClick(x=39, y=86)
time.sleep(5)
pyautogui.doubleClick(x=1043, y=549)