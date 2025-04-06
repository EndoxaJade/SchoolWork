try:
    from tkinter import *
    from tkinter import ttk
except ImportError:
    from Tkinter import *
    import ttk

import Add
import hashlib
import os
import encode
import List
import Search


LARGE_FONT = ("Verdana", 13)
BUTTON_FONT = ("Sans-Serif", 10, "bold")


class Login(Tk):
    def __init__(self, *args):
        Tk.__init__(self, *args)
        if os.name == 'nt':
            Tk.iconbitmap(self, default='icon.ico')
        Tk.wm_title(self, "Шифровалка")
        self.state = {
            "text": "Войти в аккаунт.", "val": False
        }
        if encode.password:
            self.addLoginFrame()
        else:
            self.addRegisterFrame()

    def addLoginFrame(self, *kwargs):
        login = Frame(self, padx=2, pady=2, bd=2)
        login.pack()

        loginLabel = Label(login, text=self.state['text'],
                           bd=10, font=LARGE_FONT, width=30)
        loginLabel.grid(row=0, columnspan=3)

        entry = ttk.Entry(login, show="*")
        entry.grid(row=1, column=1, pady=3)
        entry.bind('<Return>', lambda _: self.checkPwd(
            login, label=loginLabel, entry=entry, btn=submitBtn))
        entry.focus_set()
        s = ttk.Style()
        s.configure("Submit.TButton", font=BUTTON_FONT)
        submitBtn = ttk.Button(login, text="Sign in", style="Submit.TButton",
                               command=lambda: self.checkPwd(login, label=loginLabel, entry=entry, btn=submitBtn))
        submitBtn.grid(row=2, column=1, pady=3)

    def checkPwd(self, frame, **kwargs):
        chk = kwargs['entry'].get()
        # if passwords match
        #if hashlib.md5(chk).hexdigest() == encode.password:
        self.state['text'] = "Entry"
        self.state['val'] = True
        kwargs['label'].config(text=self.state['text'])
        kwargs['entry'].config(state=DISABLED)
        kwargs['btn'].config(state=DISABLED)
        self.addConfigBtn(frame)
        # If passwords don't match
        #else:
            #kwargs['label'].config(text=self.state['text'] + "\nTry Again!!!")

    def addConfigBtn(self, login):
        # configured buttons
        # btnList = (addBtn, listBtn, getBtn)
        btnList = ["Add", "List", "Search"]
        btnCmdList = [lambda: Add.AddWindow(self),
                      lambda: List.ListWindow(self),
                      lambda: Search.SearchWindow(self)]
        f = []  #Frames massive
        img = []  #Image massive
        self.temp = []  #Temp massive
        for i in range(3):
            f.append(Frame(login, padx=2, width=50, height=50))
            f[i].grid(row=3, column=i)
            img.append(PhotoImage(
                file=btnList[i] + ".gif", width=48, height=48))
            self.temp.append(img[i])
            ttk.Button(f[i], image=img[i], text=btnList[i], compound="top",
                       style="Submit.TButton",
                       command=btnCmdList[i]).grid(sticky="NWSE")

    def addRegisterFrame(self, *arg):
        register = Frame(self, padx=2, pady=2, bd=2)
        register.pack()

        info = "Зарегистрируйтесь\nДля начала работы"
        registerLabel = Label(register, text=info,
                              bd=10, font=LARGE_FONT, width=30)
        registerLabel.grid(row=0, columnspan=3)

        entry = ttk.Entry(register, show="*")
        entry.grid(row=1, column=1, pady=3)
        entry.focus_set()

        entryChk = ttk.Entry(register, show="*")
        entryChk.grid(row=2, column=1, pady=3)
        entryChk.bind('<Return>', lambda _: self.register(register,
                                                          entry, entryChk))

        s = ttk.Style()
        s.configure("Submit.TButton", font=BUTTON_FONT)
        submitBtn = ttk.Button(register, text="Зарегистрироваться",
                               style="Submit.TButton",
                               command=lambda: self.register(register,
                                                             entry, entryChk))
        submitBtn.grid(row=3, column=1, pady=3)

    def register(self, frame, *pwd):
        if pwd[0].get() == pwd[1].get(): #Pwd contains password inputs
            #encode.password = hashlib.md5(pwd[0].get()).hexdigest() #ERROR!! "Strings must be encoded before hashing" when registering
            #Saving password for future use.
            #open(".pwd", "w").write(encode.password)

            frame.destroy()
            self.addLoginFrame()
        else:
            error = "Пароли не совпадают!\nПопробуйте снова"
            errorLabel = Label(frame, text=error,
                               bd=10, font=("Verdana", 11), fg="red")
            errorLabel.grid(row=4, column=1, pady=3)
            for wid in pwd:
                wid.delete(0, 'end') #Removing previous password

if __name__ == '__main__':
    new = Login()
    new.mainloop()
