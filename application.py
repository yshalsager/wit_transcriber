import tkinter as tk
from tkinter import messagebox
from tkinter import StringVar, filedialog
from Preferences import Preferences
import constants  
from pathlib import Path
from settings import Setting_Window
import wit_transcriber
import asyncio
import sys 
import tkinter.font as tkFont


class IORedirector(object):
    #https://stackoverflow.com/a/3333386
    '''A general class for redirecting I/O to this Text widget.'''
    def __init__(self,text_area):
        self.text_area = text_area

class StdoutRedirector(IORedirector):
    '''A class for redirecting stdout to this Text widget.'''
    def write(self,string):
        self.text_area.insert('end', string)
        self.text_area.see('end')

        
"""
Idea for connecting asyncio loop_event with tkinter main_loop from:
https://www.loekvandenouweland.com/content/python-asyncio-and-tkinter.html
"""

class GUI(tk.Tk):
    
    def __init__(self,loop):
        self.loop = loop
        self.parent = tk.Tk()
        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.parent.title("أداة التفريغ الصوتي")
        self.output_path = StringVar()
        self.input_path = StringVar()
        self.init_settings()
        self.preference = Preferences(str(Path().absolute()))
        self.default_font = tkFont.nametofont("TkDefaultFont")
        self.default_font.configure(family='Tajawal',size=10)
        
        self.menu = tk.Menu(self.parent)
        filemenu = tk.Menu(self.menu, tearoff=0)
        filemenu.add_command(label=constants.MENU_BAR_FILE_NEW, command=self.askForInputPath)
        filemenu.add_command(label=constants.MENU_BAR_FILE_SETTINGS, command=self.open_win)
        filemenu.add_separator()
        filemenu.add_command(label=constants.MENU_BAR_FILE_EXIT, command=self.on_closing)
        helpmenu = tk.Menu(self.menu, tearoff=0)
        helpmenu.add_command(label=constants.MENU_BAR_ABOUT, command='')
        self.menu.add_cascade(label=constants.MENU_BAR_FILE, menu=filemenu)
        self.menu.add_cascade(label=constants.MENU_BAR_HELP, menu=helpmenu)
        self.parent.config(menu=self.menu)

        self.label = tk.Label(self.parent, text="wit.ai أداة للتفريغ الصوتي باستخدام    ")
        self.label.grid(row=0, column=0, pady=10,sticky='w,e')

        self.intput_entry = tk.Entry(self.parent,textvariable = self.input_path,width=60)
        self.intput_entry.grid(row=1, column=0, pady=10,padx=10)

        self.output_entry = tk.Entry(self.parent,textvariable = self.output_path,width=60)
        self.output_entry.grid(row=3, column=0, pady=10,padx=10)


        tk.Button(self.parent,text=constants.INPUT_BUTTON_TITLE,command=self.askForInputPath).grid(row=1, column=1, pady=10,padx=10)

        tk.Button(self.parent,text=constants.OUTPUT_BUTTON_TITLE,command=self.askForOutputPath).grid(row=3, column=1, pady=10,padx=10)

        
        self.startTranscribe  = tk.Button(self.parent,text=constants.SUBMIT_BUTTON,command=lambda: self.loop.create_task(self.getTranscribe()))
        self.startTranscribe.grid(row=4, column=0, pady=10,padx=10,columnspan=2)

        self.scrollbar = tk.Scrollbar(self.parent,orient=tk.VERTICAL)       
        self.output_area =  tk.Text(self.parent, height = 5,width = 25, bg = "light gray",yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.output_area.yview)
        self.output_area.grid(row=5,column=0,sticky="wes",padx=10,pady=10)
        self.scrollbar.grid(row=5,column=0,sticky="nse",padx=10,pady=10)

        sys.stdout = StdoutRedirector( self.output_area )

        self.verbose_checkbox_var = tk.IntVar()
        # print(self.verbose_checkbox_var)
        verbose_checkbox=tk.Checkbutton(self.parent,variable=self.verbose_checkbox_var)
        verbose_checkbox["justify"] = "center"
        verbose_checkbox["text"] = "اظهار النتائج"
        verbose_checkbox.grid(row=6,column=0,sticky="w",padx=10,pady=10)
        verbose_checkbox["offvalue"] = 0
        verbose_checkbox["onvalue"] = 1

        
            
    def init_settings(self):
        self.output_path.set(Path().absolute())

    # [Improvment] edit to handle onClosing and stop asyncio loop    
    async def show(self):
        while True:
            self.parent.update()
            await asyncio.sleep(.1)

    def askForOutputPath(self):
        output_path = filedialog.askdirectory()
        self.output_path.set(output_path)
    
    def askForInputPath(self):
        input_path=filedialog.askopenfilename(initialdir = "/",title = constants.INPUT_DIALOG_TITLE,filetypes = (("Audio files","*.mp3 *.wav *.m4a *.ogg"),("all files","*.*")))
        self.input_path.set(input_path)

    def on_error_occurs(self,error_msg):
        messagebox.showerror('خطا',error_msg)

    def open_win(self):
        Setting_Window(self.parent,self.preference)

    def on_closing(self):
        self.parent.destroy()
        asyncio.get_event_loop().stop()

    async def getTranscribe(self):
        if not self.preference.checkIfArKeyExists():
            self.on_error_occurs(constants.ERROR_API_KEY)

        self.disableEntries()
        self.output_area.insert(tk.INSERT,"Please wait....")
        file_path = Path(self.input_path.get())
        output_path = Path(self.output_path.get()+ f"\\{file_path.stem}.txt")
        config_path = Path(self.preference.getConfigFile())
        try:
            await wit_transcriber.transcribe(
                            file_path=file_path,
                            output=output_path,
                            semaphore = 5,
                            config_file=config_path,
                            verbose= True&self.verbose_checkbox_var.get(),
                            lang="ar")
        except:
            self.output_area.insert(tk.INSERT,"Error occurs! Please try again!") 
            self.enableEntries()
        self.enableEntries()
        
    def disableEntries(self):
        self.intput_entry.config(state= "disabled")
        self.output_entry.config(state= "disabled")
        self.startTranscribe['state'] = tk.DISABLED
    
    def enableEntries(self):
        self.intput_entry.config(state= "normal")
        self.output_entry.config(state= "normal")
        self.startTranscribe['state'] = tk.NORMAL

class App:
    async def exec(self):
        self.window = GUI(asyncio.get_event_loop())
        await self.window.show()


if __name__ == "__main__":
    asyncio.run(App().exec())
