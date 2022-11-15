
import datetime


def log(func):
    def log_it(*args, **kwargs):
        if kwargs['coin'] == kwargs['last_coin']:
            print('The price of coin has not changed compared to last time %s ' %
                  datetime.datetime.now())
        else:
            print('The price has changed %s ' % datetime.datetime.now())

        result = func(*args, **kwargs)

        return result
    return log_it


def log_internet(func):
    def log_it(*args, **kwargs):
        result = func(*args, **kwargs)

        if result:
            return result
        else:
            print('The internet connection is lost. Trying again...')
            return result
    return log_it
