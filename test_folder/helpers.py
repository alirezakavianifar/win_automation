# import pywinauto
# from pywinauto.application import Application
# from pywinauto.keyboard import send_keys
# from pywinauto import keyboard as kb
import os
import json
import time
from observer.observer_pattern import Observer

# app = Application().start(cmd_line=r"C:\Program Files\Notepad++\notepad++.exe")


LOG_DIR = r'D:\projects\win_automation\saved_dir\logs'
FILE_NAME = 'log.txt'
LOG_NAME = os.path.join(LOG_DIR, FILE_NAME)


class DataSource(Observer):
    def __init__(self) -> None:
        self.value = 0
        self.obs = []

    def set_value(self, value):
        self.value = value
        self.notify_observers()

    def get_value(self):
        return self.value

    # @log_it(LOG_NAME)
    # @json_it
    def convert_tojson(self):
        return 'Hello World'


def log_it(logname):
    def wrapper(func):
        def inner_func(*args, **kwargs):
            print('The function is called')
            with open(logname, 'a') as f:
                f.write('The function is called \n')
                result = func(*args, **kwargs)
                f.write('The function finished execution \n')
            print('The function is done!!')
            return result
        return inner_func
    return wrapper


def json_it(func):
    def try_it(*args, **kwargs):
        result = func(*args, **kwargs)
        dict_obj = {'result': result}
        dict_obj = json.dumps(dict_obj)
        final_dict = json.loads(dict_obj)
        print(str(final_dict))
        return final_dict
    return try_it


# if __name__ == '__main__':
#     convert_tojson()
