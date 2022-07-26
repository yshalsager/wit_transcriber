import tkinter as tk
import tkinter.font as tkFont

class Setting_Window():
    def __init__(self,parent,preference) :
        self.parent = parent
        self.preference = preference

        self.window= tk.Toplevel(self.parent)
        #window.geometry("400x250")
        #setting window size
        width=400
        height=300
        screenwidth = self.window.winfo_screenwidth()
        screenheight = self.window.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.window.geometry(alignstr)
        self.window.resizable(width=False, height=False)
        self.window.title("Settings")
        ft = tkFont.Font(family='Tajawal',size=10)

        setting_main_title=tk.Label(self.window)
        setting_main_title["font"] = ft
        setting_main_title["fg"] = "#333333"
        setting_main_title["justify"] = "center"
        setting_main_title["text"] = "اعدادات البرنامج"
        setting_main_title.place(x=140,y=20,width=100,height=25)

        self.ar_lang_entry_strvar = tk.StringVar()
        self.ar_lang_entry_strvar.set("ar")
        ar_lang_entry=tk.Entry(self.window,textvariable=self.ar_lang_entry_strvar)
        ar_lang_entry["borderwidth"] = "1px"
        ar_lang_entry["font"] = ft
        ar_lang_entry["justify"] = "left"
        ar_lang_entry["state"] = "disabled"
        ar_lang_entry.place(x=30,y=80,width=109,height=32)

        self.ar_apiKey_entry_strvar = tk.StringVar()
        self.ar_apiKey_entry_strvar.set(self.preference.get("ar"))
        ar_apiKey_entry=tk.Entry(self.window,textvariable=self.ar_apiKey_entry_strvar)
        ar_apiKey_entry["borderwidth"] = "1px"
        ar_apiKey_entry["font"] = ft
        ar_apiKey_entry["justify"] = "left"
        ar_apiKey_entry.place(x=170,y=80,width=213,height=30)

        
        ar_lang_label=tk.Label(self.window)
        ar_lang_label["font"] = ft
        ar_lang_label["fg"] = "#333333"
        ar_lang_label["justify"] = "left"
        ar_lang_label["text"] = "اللغة العربية"
        ar_lang_label.place(x=30,y=50,width=70,height=25)

        ar_apiKey_label=tk.Label(self.window)
        ar_apiKey_label["font"] = ft
        ar_apiKey_label["fg"] = "#333333"
        ar_apiKey_label["justify"] = "center"
        ar_apiKey_label["text"] = "مفتاح التفعيل"
        ar_apiKey_label.place(x=170,y=50,width=100,height=25)

        save_btn=tk.Button(self.window)
        save_btn["bg"] = "#f0f0f0"
        save_btn["font"] = ft
        save_btn["fg"] = "#000000"
        save_btn["justify"] = "center"
        save_btn["text"] = "حفظ"
        save_btn.place(x=160,y=250,width=70,height=25)
        save_btn["command"] = self.save_settings

       
    def save_settings(self):
        self.preference.put("ar",self.ar_apiKey_entry_strvar.get())
        self.show_info("تم حفظ الاعدادات بنجاح!")

    def show_info(self,msg):
        tk.messagebox.showinfo('اعدادات',msg)

    def load_preference_settings(self):
        self.ar_apiKey_entry_strvar.set(self.preference.get("ar"))

    

        
        

        

    


