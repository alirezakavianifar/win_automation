import customtkinter
from multiprocess_test import run_task
from helpers import convert_tojson
import zope.interface
from observer.observer_pattern import IObserver


@zope.interface.implementer(IObserver)
class App(customtkinter.CTk):
    def __init__(self, data_source=None):
        super().__init__()
        self.data_source = data_source
        self.geometry("600x500")
        self.title("CTk example")

        # add widgets to app
        self.button_1 = customtkinter.CTkButton(
            self, command=lambda: btn_th(self.update_btn))
        self.button_1.grid(row=0, column=0, padx=20, pady=10)
        self.button_2 = customtkinter.CTkButton(
            self, command=lambda: btn_th(self.update_btn))
        self.button_2.grid(row=1, column=0, padx=20, pady=10)
        self.button_3 = customtkinter.CTkButton(
            self, command=lambda: btn_th(self.update_btn))
        self.button_3.grid(row=2, column=0, padx=20, pady=10)
        self.button_4 = customtkinter.CTkButton(
            self, command=lambda: btn_th(self.update_btn))
        self.button_4.grid(row=3, column=0, padx=20, pady=10)
        self.textbox_1 = customtkinter.CTkTextbox(self, width=250, height=100)
        self.textbox_1.grid(row=0, column=1, padx=(
            20, 0), pady=(20, 0), sticky="nsew")
        self.textbox_2 = customtkinter.CTkTextbox(self, width=250, height=100)
        self.textbox_2.grid(row=1, column=1, padx=(
            20, 0), pady=(20, 0), sticky="nsew")
        self.textbox_3 = customtkinter.CTkTextbox(self, width=250, height=100)
        self.textbox_3.grid(row=2, column=1, padx=(
            20, 0), pady=(20, 0), sticky="nsew")
        self.textbox_4 = customtkinter.CTkTextbox(self, width=250, height=100)
        self.textbox_4.grid(row=3, column=1, padx=(
            20, 0), pady=(20, 0), sticky="nsew")
        
        # Set default values
        self.textbox_1.insert("0.0", self.data_source.get_txt1_val())
        self.textbox_2.insert("0.0", self.data_source.get_txt2_val())
        self.textbox_3.insert("0.0", self.data_source.get_txt3_val())
        self.textbox_4.insert("0.0", self.data_source.get_txt4_val())
        
    def update(self):
        # self.value = self.data_source.get_value()
        self.textbox_1.insert("end", self.data_source.get_txt1_val())
        self.textbox_2.insert("end", self.data_source.get_txt2_val())
        self.textbox_3.insert("end", self.data_source.get_txt3_val())
        self.textbox_4.insert("end", self.data_source.get_txt4_val())

    # add methods to app
    def update_btn(self):
        convert_tojson(self.data_source)


def btn_th(task):
    import threading
    t1 = threading.Thread(target=task)
    t1.start()
    x = 12


if __name__ == "__main__":
    from observer.observer_pattern import DataSource
    data_source = DataSource()
    app = App(data_source)
    data_source.add_observer(app)

    app.mainloop()
