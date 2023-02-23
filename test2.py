import os
import json

LOG_DIR = r'D:\projects\win_automation\saved_dir\logs'
FILE_NAME = 'log.txt'
LOG_NAME = os.path.join(LOG_DIR, FILE_NAME)


def log_it(logname):
    def wrapper(func):
        def inner_func(*args, **kwargs):
            print('The function is called')
            with open(logname, 'a') as f:
                f.write('The function is called \n')
                result = func(*args, **kwargs)
                f.write('The function finished execution \n')
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


@log_it(LOG_NAME)
@json_it
def convert_tojson():
    return 'Hello World'


if __name__ == '__main__':
    convert_tojson()
