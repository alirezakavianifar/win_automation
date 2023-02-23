import multiprocess
import os
import psutil

IND = 0
ALL_PROCESSES = {}


def kill_proc_tree(pid, including_parent=False):
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    for child in children:
        child.kill()
    gone, still_alive = psutil.wait_procs(children, timeout=5)
    if including_parent:
        parent.kill()
        parent.wait(5)


def thread_start(task, name):
    global ALL_PROCESSES
    p1 = multiprocess.Process(target=task, daemon=True)
    p1.start()
    ALL_PROCESSES[name] = p1


def thread_kill():

    if 'tgju_start' in ALL_PROCESSES.keys():
        pid = os.getpid()
        kill_proc_tree(pid, False)
        # ALL_PROCESSES['tgju_start'].terminate()
        ALL_PROCESSES.pop('tgju_start', None)


def run_task(task, name):
    global IND
    global ALL_PROCESSES

    if IND == 0:
        IND = 1
        thread_start(task, name)
        IND = 0
    else:
        thread_kill()
        IND = 0
