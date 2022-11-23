import sys
sys.path.append(r'D:\projects\win_automation\tgju')
import threading
from tgju import run_tgju
import tkinter as tk
from tgju_tkinter_constants import set_shared_var

def exit_tgju():
    print('run')
    set_shared_var(True)


def thread_tgju_start():
    t1 = threading.Thread(target=run_tgju)
    t1.start()


def thread_tgju_end():
    t2 = threading.Thread(target=exit_tgju)
    t2.start()
    


root = tk.Tk()

root.geometry('500x500')
root.title('My First GUI')

label = tk.Label(root, text='Hello World!', font=('Arial', 18))
label.pack(padx=20, pady=20)

button = tk.Button(root, text='Click Me!', command=lambda:thread_tgju_start())
button.pack(padx=10, pady=10)

button = tk.Button(root, text='exit!', command=lambda: thread_tgju_end())
button.pack(padx=10, pady=10)
root.mainloop()
