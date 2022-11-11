import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


is_downloaded = False


class Handler(FileSystemEventHandler):

    def on_created(self, event):
        global is_downloaded
        is_downloaded = True
        print('file was created')


def watch_over(path=r'E:\automating_reports_V2\saved_dir\arzeshafzoodeh_sonati'):
    global is_downloaded

    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            if is_downloaded == True:
                raise Exception

            time.sleep(1)
            print('waiting')

    except:
        is_downloaded = False

    finally:
        observer.stop()
        observer.join()
