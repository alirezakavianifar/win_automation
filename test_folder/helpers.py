# import pywinauto
# from pywinauto.application import Application
# from pywinauto.keyboard import send_keys
# from pywinauto import keyboard as kb
import os
import json
import time

# app = Application().start(cmd_line=r"C:\Program Files\Notepad++\notepad++.exe")


LOG_DIR = r'D:\projects\win_automation\saved_dir\logs'
FILE_NAME = 'log.txt'
LOG_NAME = os.path.join(LOG_DIR, FILE_NAME)



def log_it(logname):
    def wrapper(func):
        def inner_func(*args, **kwargs):
            print('The function is called')
            args[0].set_txt1_val('The function is called\n\n')
            time.sleep(1)
            with open(logname, 'a') as f:
                f.write('The function is called \n')
                result = func(*args, **kwargs)
                f.write('The function finished execution \n')
            print('The function is done!!')
            args[0].set_txt1_val('The function finished execution \n\n')
            return result
        return inner_func
    return wrapper


def json_it(func):
    def try_it(*args, **kwargs):
        result = func(*args, **kwargs)
        dict_obj = {'result': result}
        dict_obj = json.dumps(dict_obj)
        final_dict = json.loads(dict_obj)
        args[0].set_txt1_val('%s \n\n' % str(final_dict))
        print(str(final_dict))
        return final_dict
    return try_it

@log_it(LOG_NAME)
@json_it
def convert_tojson(data_source):
    return 'Hello World'


if __name__ == '__main__':
    convert_tojson()
