import tkinter as tk

root = tk.Tk()
btn_text = tk.StringVar()

c = 0
def update_btn_text():
    global c
    if c == 0:
        btn_text.set("b")
        c = 1
    else:
        btn_text.set("a")
        c = 0


btn = tk.Button(root, textvariable=btn_text, command=update_btn_text)
btn_text.set("a")

btn.pack()

root.mainloop()