import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox

from awesometkinter.bidirender import render_text

from preferences import PreferencesManager


class SettingWindow:
    """
    Window is designed by using https://visualtk.com/
    """

    def __init__(self, parent: tk.Tk, preferences: PreferencesManager) -> None:
        self.parent: tk.Tk = parent
        self.preferences: PreferencesManager = preferences

        self.window = tk.Toplevel(self.parent)
        # window.geometry("400x250")
        # setting window size
        width = 400
        height = 300
        screenwidth = self.window.winfo_screenwidth()
        screenheight = self.window.winfo_screenheight()
        align_str = f"{width:.0f}x{height:.0f}+{(screenwidth - width) / 2:.0f}+{(screenheight - height) / 2:.0f}"
        self.window.geometry(align_str)
        self.window.resizable(width=False, height=False)
        self.window.title("الإعدادات")
        ft = tkFont.Font(family="Tajawal", size=10)

        setting_main_title = tk.Label(
            self.window,
            font=ft,
            fg="#333333",
            justify="center",
            text=render_text("إعدادات البرنامج"),
        )
        setting_main_title.place(x=140, y=20, width=200, height=25)

        self.ar_lang_entry_str_var = tk.StringVar()
        self.ar_lang_entry_str_var.set("ar")
        ar_lang_entry = tk.Entry(
            self.window,
            textvariable=self.ar_lang_entry_str_var,
            borderwidth="1px",
            font=ft,
            justify="left",
            state="disabled",
        )
        ar_lang_entry.place(x=30, y=80, width=109, height=32)

        self.ar_api_key_entry_str_var = tk.StringVar()
        self.ar_api_key_entry_str_var.set(self.preferences.get("ar"))
        ar_api_key_entry = tk.Entry(
            self.window,
            textvariable=self.ar_api_key_entry_str_var,
            borderwidth="1px",
            font=ft,
            justify="left",
        )
        ar_api_key_entry.place(x=170, y=80, width=213, height=30)

        ar_lang_label = tk.Label(
            self.window,
            font=ft,
            fg="#333333",
            justify="left",
            text=render_text("اللغة العربية"),
        )
        ar_lang_label.place(x=30, y=50, width=70, height=25)

        ar_api_key_label = tk.Label(
            self.window,
            font=ft,
            fg="#333333",
            justify="center",
            text=render_text("مفتاح التفعيل"),
        )
        ar_api_key_label.place(x=170, y=50, width=100, height=25)

        save_btn = tk.Button(
            self.window,
            bg="#f0f0f0",
            fg="#000000",
            font=ft,
            justify="center",
            text=render_text("حفظ"),
            command=self.save_settings,
        )
        save_btn.place(x=160, y=250, width=70, height=25)

    def save_settings(self) -> None:
        self.preferences.put("ar", self.ar_api_key_entry_str_var.get())
        self.show_info(render_text("تم حفظ الإعدادات بنجاح!"))

    @staticmethod
    def show_info(msg: str) -> None:
        messagebox.showinfo(render_text("إعدادات"), msg)

    def load_preference_settings(self) -> None:
        self.ar_api_key_entry_str_var.set(self.preferences.get("ar"))
