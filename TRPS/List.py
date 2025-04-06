try:
    from tkinter import *
    from tkinter import ttk
except ImportError:
    from Tkinter import *
    import ttk

import encode
import json
#import pyperclip #Library for double click copy

NORM_FONT = ("Helvetica", 10)
LARGE_FONT = ("Verdana", 13)

class PasswordInfoWindow(Toplevel):
    def __init__(self, parent, password_info):
        super().__init__(parent)
        self.title("Password Information")
        self.geometry("300x200")

        #Password info display
        for key, value in password_info.items():
            label = Label(self, text=f"{key}: {value}")
            label.pack(pady=5)

class ListWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Stored Passwords")
        self.listbox = Listbox(self)
        self.listbox.pack(fill=BOTH, expand=True)
        
        self.passwords = self.load_passwords()
        self.updateList()

        self.listbox.bind('<Double-1>', self.on_double_click)

    def updateList(self):
        self.listbox.delete(0, END)  
        seen_names = set()      
        for password in self.passwords:
            if password['name'] not in seen_names: #Add password only with unique name
                seen_names.add(password['name'])
                self.listbox.insert(END, password['name']) #Insert unique password names

    def load_passwords(self):
        try:
            with open(".data", "r") as outfile:
                data = json.load(outfile)
                return [{'name': service, 'username': details[0], 'password': details[1]} for service, details in data.items()]
        except (IOError, json.JSONDecodeError):
            return []  #Return empty list if there is an error in loading

    def on_double_click(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            password_info = self.passwords[selected_index[0]] #Get password info based on selection
            PasswordInfoWindow(self, password_info)


def addConfigBtn(self, login):
    btnCmdList = [lambda: Add.AddWindow(self, lambda: self.updateList()),
                  lambda: List.ListWindow(self), 
                  lambda: Search.SearchWindow(self)]
#Lots of Awesomeness
class getTreeFrame(Frame):

    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.addLists()

    def addLists(self, *arg):
        dataList = self.getData()
        headings = ["Service", "Username"]

        if dataList:
            Label(self, text="Double Click to copy password",
                  bd=2, font=LARGE_FONT).pack(side="top")
            scroll = ttk.Scrollbar(self, orient=VERTICAL, takefocus=True)
            self.tree = ttk.Treeview(self, columns=headings, show="headings")
            scroll.config(command=self.tree.yview)
            self.tree.configure(yscroll=scroll.set)
            scroll.pack(side=RIGHT, fill=Y)
            self.tree.pack(side=LEFT, fill='both', expand=1)
            for heading in headings:
                self.tree.heading(
                    heading, text=heading,
                    command=lambda c=heading: self.sortby(self.tree, c, 0))
                self.tree.column(heading, width=200)
            for data in dataList:
                self.tree.insert("", "end", values=data)
            self.tree.bind("<Double-1>", self.OnDoubleClick)
        else:
            self.errorMsg()

    def getData(self, *arg):
        fileName = ".data"
        self.data = None
        try:
            with open(fileName, "r") as outfile:
                self.data = outfile.read()
        except IOError:
            return ""
        if not self.data:
            return ""
        self.data = json.loads(self.data)
        dataList = []
        for service, details in self.data.items():
            usr = details[0] if details[0] else "NO ENTRY"
            dataList.append((service, usr))
        return dataList

    def errorMsg(self, *args):
        msg = "There is no data yet!"
        label = Label(self, text=msg, font=NORM_FONT, bd=3, width=30)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(self, text="Okay", command=self.master.destroy)
        B1.pack(pady=10)

    def OnDoubleClick(self, event):
        item = self.tree.focus()
        service = self.tree.item(item, "values")[0]
        var = self.data[service][1]
        var = encode.decode(var)
        #pyperclip.copy(var) #Copies the password

    def updateList(self, regStr, *args):
        for x in self.tree.get_children(''):
            self.tree.delete(x)
        for data in self.getData():
            if re.search(regStr, data[0]) or re.search(regStr, data[1]):
                self.tree.insert("", "end", values=data)

    def sortby(self, tree, col, descending):
        data = [(tree.set(child, col), child)
                for child in tree.get_children('')]
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            tree.move(item[1], '', ix)
        tree.heading(col,
                     command=lambda col=col: self.sortby(tree, col,
                                                         int(not descending)))


if __name__ == "__main__":
    root = Tk()
    Tk.iconbitmap(root, default='icon.ico')
    Tk.wm_title(root, "Test")
    Label(root, text="Root window").pack()
    new = ListWindow(root)
    root.mainloop()
