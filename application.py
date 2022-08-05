import asyncio
import sys
import tkinter as tk
import tkinter.font as tkFont
from pathlib import Path
from tkinter import StringVar, filedialog, messagebox
from webbrowser import open_new_tab

from awesometkinter.bidirender import render_text

import constants
import wit_transcriber
from preferences import PreferencesManager
from settings import SettingWindow


class IORedirector:
    # https://stackoverflow.com/a/3333386
    """A general class for redirecting I/O to this Text widget."""

    def __init__(self, text_area: tk.Text) -> None:
        self.text_area = text_area


class StdoutRedirector(IORedirector):
    """A class for redirecting stdout to this Text widget."""

    def __init__(self, text_area: tk.Text):
        super().__init__(text_area)

    def write(self, string: str) -> None:
        self.text_area.insert("end", render_text(string))
        self.text_area.see("end")

    def flush(self) -> None:
        pass


"""
Idea for connecting asyncio loop_event with tkinter main_loop from:
https://www.loekvandenouweland.com/content/python-asyncio-and-tkinter.html
"""


class App:
    def __init__(self) -> None:
        self.parent: tk.Tk = tk.Tk()
        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.parent.title("أداة التفريغ الصوتي")
        self.output_path = StringVar()
        self.input_path = StringVar()
        self.init_settings()
        self.preference = PreferencesManager(Path().absolute())
        self.default_font = tkFont.nametofont("TkDefaultFont")
        self.default_font.configure(family="Tajawal", size=10)

        self.menu = tk.Menu(self.parent)
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(
            label=render_text(constants.MENU_BAR_FILE_NEW),
            command=self.ask_for_input_path,
        )
        file_menu.add_command(
            label=render_text(constants.MENU_BAR_FILE_SETTINGS), command=self.open_win
        )
        file_menu.add_separator()
        file_menu.add_command(
            label=render_text(constants.MENU_BAR_FILE_EXIT), command=self.on_closing
        )
        help_menu = tk.Menu(self.menu, tearoff=0)
        help_menu.add_command(
            label=render_text(constants.MENU_BAR_ABOUT),
            command=lambda: open_new_tab(
                "https://github.com/yshalsager/wit_transcriber"
            ),
        )
        self.menu.add_cascade(
            label=render_text(constants.MENU_BAR_FILE), menu=file_menu
        )
        self.menu.add_cascade(
            label=render_text(constants.MENU_BAR_HELP), menu=help_menu
        )
        self.parent.config(menu=self.menu)

        self.label = tk.Label(
            self.parent, text=render_text("wit.ai أداة للتفريغ الصوتي باستخدام")
        )
        self.label.grid(row=0, column=0, pady=10, sticky="w,e")

        self.input_entry = tk.Entry(self.parent, textvariable=self.input_path, width=60)
        self.input_entry.grid(row=1, column=0, pady=10, padx=10)

        self.output_entry = tk.Entry(
            self.parent, textvariable=self.output_path, width=60
        )
        self.output_entry.grid(row=3, column=0, pady=10, padx=10)

        tk.Button(
            self.parent,
            text=render_text(constants.INPUT_BUTTON_TITLE),
            command=self.ask_for_input_path,
        ).grid(row=1, column=1, pady=10, padx=10)

        tk.Button(
            self.parent,
            text=render_text(constants.OUTPUT_BUTTON_TITLE),
            command=self.ask_for_output_path,
        ).grid(row=3, column=1, pady=10, padx=10)

        self.startTranscribe = tk.Button(
            self.parent,
            text=render_text(constants.SUBMIT_BUTTON),
            command=lambda: asyncio.create_task(self.get_transcribe()),
        )
        self.startTranscribe.grid(row=4, column=0, pady=10, padx=10, columnspan=2)

        self.scrollbar = tk.Scrollbar(self.parent, orient=tk.VERTICAL)
        self.output_area = tk.Text(
            self.parent,
            height=5,
            width=25,
            bg="light gray",
            yscrollcommand=self.scrollbar.set,
        )
        self.scrollbar.config(command=self.output_area.yview)
        self.output_area.grid(row=5, column=0, sticky="wes", padx=10, pady=10)
        self.scrollbar.grid(row=5, column=0, sticky="nse", padx=10, pady=10)

        sys.stdout = StdoutRedirector(self.output_area)  # type: ignore

        self.verbose_checkbox_var = tk.IntVar()
        # print(self.verbose_checkbox_var)
        verbose_checkbox = tk.Checkbutton(
            self.parent,
            variable=self.verbose_checkbox_var,
            justify="center",
            text=render_text("إظهار النتائج"),
            offvalue=0,
            onvalue=1,
        )
        verbose_checkbox.grid(row=6, column=0, sticky="w", padx=10, pady=10)

    def init_settings(self) -> None:
        self.output_path.set(str(Path().absolute()))

    # TODO [Improvement] edit to handle onClosing and stop asyncio loop
    async def show(self) -> None:
        while True:
            self.parent.update()
            await asyncio.sleep(0.1)

    def ask_for_output_path(self) -> None:
        output_path = filedialog.askdirectory()
        self.output_path.set(output_path)

    def ask_for_input_path(self) -> None:
        input_path = filedialog.askopenfilename(
            initialdir="./",
            title=render_text(constants.INPUT_DIALOG_TITLE),
            filetypes=(
                ("Audio files", "*.mp3 *.wav *.m4a *.ogg"),
                ("all files", "*.*"),
            ),
        )
        self.input_path.set(input_path)

    @staticmethod
    def on_error_occurs(error_msg: str) -> None:
        messagebox.showerror("خطأ", error_msg)

    def open_win(self) -> None:
        SettingWindow(self.parent, self.preference)

    def on_closing(self) -> None:
        self.parent.destroy()
        asyncio.get_event_loop().stop()

    async def get_transcribe(self) -> None:
        if not self.preference.check_if_ar_key_exists():
            self.on_error_occurs(render_text(constants.ERROR_API_KEY))

        self.disable_entries()
        self.output_area.insert(tk.INSERT, "Please wait....\n")
        file_path = Path(self.input_path.get())
        output_path = Path(self.output_path.get() + f"/{file_path.stem}.txt")
        config_path = Path(self.preference.get_config_file())
        try:
            await wit_transcriber.transcribe(
                file_path=file_path,
                output=output_path,
                semaphore=5,
                config_file=config_path,
                verbose=True and bool(self.verbose_checkbox_var.get()),
                lang="ar",
            )
        except:
            self.output_area.insert(tk.INSERT, "Error occurs! Please try again!")
            self.enable_entries()
        self.enable_entries()

    def disable_entries(self) -> None:
        self.input_entry.config(state="disabled")
        self.output_entry.config(state="disabled")
        self.startTranscribe["state"] = tk.DISABLED

    def enable_entries(self) -> None:
        self.input_entry.config(state="normal")
        self.output_entry.config(state="normal")
        self.startTranscribe["state"] = tk.NORMAL

    async def exec(self) -> None:
        await self.show()


def main() -> None:
    asyncio.run(App().exec())


if __name__ == "__main__":
    main()
