# Add.py
try:
    from tkinter import *
    from tkinter import ttk
    from tkinter import messagebox
except ImportError:
    from Tkinter import *
    import ttk
    import tkMessageBox as messagebox

import json
import encode
import os

LABEL_FONT = ("Segoe UI", 11)
BUTTON_FONT = ("Segoe UI", 11, "bold")
ENTRY_FONT = ("Segoe UI", 11)

class AddWindow(Toplevel):
    """Окно добавления нового пароля"""
    
    def __init__(self, parent, update_callback=None):
        Toplevel.__init__(self, parent)
        self.parent = parent
        self.update_callback = update_callback
        
        # Получаем текущего пользователя
        self.current_user = self.get_current_user()
        
        # Загружаем категории
        self.categories = self.load_categories()
        
        self.title("Добавление пароля")
        self.geometry("450x600")
        self.resizable(False, False)
        self.configure(bg="#FFFFFF")
        self.center_window()
        self.create_widgets()
    
    def get_current_user(self):
        """Получение текущего пользователя"""
        try:
            if hasattr(self.master, 'current_user'):
                return self.master.current_user
            elif hasattr(self.master, 'username'):
                return self.master.username
        except:
            pass
        return "default"
    
    def load_categories(self):
        """Загрузка категорий пользователя"""
        try:
            with open(".categories", "r", encoding='utf-8') as f:
                data = json.load(f)
                return data.get(self.current_user, ["Без категории"])
        except:
            return ["Без категории"]
    
    def save_categories(self):
        """Сохранение категорий"""
        try:
            data = {}
            if os.path.exists(".categories"):
                with open(".categories", "r", encoding='utf-8') as f:
                    data = json.load(f)
            data[self.current_user] = self.categories
            with open(".categories", "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка сохранения категорий: {e}")
    
    def center_window(self):
        self.update_idletasks()
        width = 450
        height = 600
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        # Основной фрейм
        main_frame = Frame(self, bg="#FFFFFF", padx=25, pady=20)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Заголовок
        title = Label(
            main_frame,
            text="Добавление пароля",
            font=("Segoe UI", 18, "bold"),
            bg="#FFFFFF",
            fg="#5C0071"
        )
        title.pack(pady=(0, 15))
        
        # Поле: Пароль
        Label(
            main_frame,
            text="Пароль *",
            font=LABEL_FONT,
            bg="#FFFFFF",
            fg="#666666",
            anchor="w"
        ).pack(fill=X, pady=(0, 3))
        
        # Фрейм для поля пароля и кнопки генерации
        pwd_frame = Frame(main_frame, bg="#FFFFFF")
        pwd_frame.pack(fill=X, pady=(0, 12))
        
        self.password_entry = ttk.Entry(pwd_frame, font=ENTRY_FONT, show="*")
        self.password_entry.pack(side=LEFT, fill=X, expand=True)
        
        # Кнопка генерации
        gen_btn = Button(
            pwd_frame,
            text="⚡",
            font=("Segoe UI", 14),
            bg="#FFD700",
            fg="#333333",
            relief="flat",
            cursor="hand2",
            width=3,
            command=self.open_generator
        )
        gen_btn.pack(side=RIGHT, padx=(5, 0))
        
        # Поле: Псевдоним
        Label(
            main_frame,
            text="Псевдоним",
            font=LABEL_FONT,
            bg="#FFFFFF",
            fg="#666666",
            anchor="w"
        ).pack(fill=X, pady=(0, 3))
        
        self.alias_entry = ttk.Entry(main_frame, font=ENTRY_FONT)
        self.alias_entry.pack(fill=X, pady=(0, 12))
        
        # Поле: Сайт
        Label(
            main_frame,
            text="Сайт",
            font=LABEL_FONT,
            bg="#FFFFFF",
            fg="#666666",
            anchor="w"
        ).pack(fill=X, pady=(0, 3))
        
        self.site_entry = ttk.Entry(main_frame, font=ENTRY_FONT)
        self.site_entry.pack(fill=X, pady=(0, 12))
        
        # Поле: Логин
        Label(
            main_frame,
            text="Логин",
            font=LABEL_FONT,
            bg="#FFFFFF",
            fg="#666666",
            anchor="w"
        ).pack(fill=X, pady=(0, 3))
        
        self.login_entry = ttk.Entry(main_frame, font=ENTRY_FONT)
        self.login_entry.pack(fill=X, pady=(0, 12))
        
        # Поле: Категория
        Label(
            main_frame,
            text="Категория",
            font=LABEL_FONT,
            bg="#FFFFFF",
            fg="#666666",
            anchor="w"
        ).pack(fill=X, pady=(0, 3))
        
        # Фрейм для выпадающего списка
        cat_frame = Frame(main_frame, bg="#FFFFFF")
        cat_frame.pack(fill=X, pady=(0, 15))
        
        self.category_var = StringVar()
        self.category_var.set(self.categories[0] if self.categories else "Без категории")
        
        self.category_combo = ttk.Combobox(
            cat_frame,
            textvariable=self.category_var,
            values=self.categories,
            font=ENTRY_FONT,
            state="readonly"
        )
        self.category_combo.pack(side=LEFT, fill=X, expand=True)
        
        # Кнопка добавления категории
        add_cat_btn = Button(
            cat_frame,
            text="+",
            font=("Segoe UI", 14, "bold"),
            bg="#E4CCFF",
            fg="#5C0071",
            relief="flat",
            cursor="hand2",
            width=3,
            command=self.add_category
        )
        add_cat_btn.pack(side=RIGHT, padx=(5, 0))
        
        # Кнопки действий
        btn_frame = Frame(main_frame, bg="#FFFFFF")
        btn_frame.pack(fill=X, pady=(10, 0))
        
        # Стереть все
        clear_btn = Button(
            btn_frame,
            text="Стереть все",
            font=BUTTON_FONT,
            bg="#FF6B6B",
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.clear_all
        )
        clear_btn.pack(side=LEFT, padx=5, ipadx=10, ipady=8, expand=True)
        
        # Сохранить
        save_btn = Button(
            btn_frame,
            text="Сохранить пароль",
            font=BUTTON_FONT,
            bg="#4CAF50",
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.save_password
        )
        save_btn.pack(side=LEFT, padx=5, ipadx=10, ipady=8, expand=True)
        
        # Сгенерировать (открывает генератор)
        generate_btn = Button(
            btn_frame,
            text="Сгенерировать",
            font=BUTTON_FONT,
            bg="#FFD700",
            fg="#333333",
            relief="flat",
            cursor="hand2",
            command=self.open_generator
        )
        generate_btn.pack(side=LEFT, padx=5, ipadx=10, ipady=8, expand=True)
        
        # Информационное сообщение
        self.info_label = Label(
            main_frame,
            text="",
            font=LABEL_FONT,
            bg="#FFFFFF",
            fg="#4CAF50",
            anchor="w"
        )
        self.info_label.pack(fill=X, pady=(10, 0))
        
        # Привязка Enter
        self.password_entry.bind('<Return>', lambda e: self.save_password())
        self.alias_entry.bind('<Return>', lambda e: self.save_password())
        self.site_entry.bind('<Return>', lambda e: self.save_password())
        self.login_entry.bind('<Return>', lambda e: self.save_password())
    
    def open_generator(self):
        """Открытие генератора паролей"""
        try:
            if hasattr(self.master, 'open_generator_from_add'):
                self.master.open_generator_from_add(self)
            else:
                # Если метод не найден в родителе, создаем генератор напрямую
                from manager import GeneratorWindow
                generator = GeneratorWindow(self.master, return_to_add=True, add_window=self)
                self.withdraw()
                self.wait_window(generator)
                self.deiconify()
                self.lift()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть генератор: {e}")
    
    def add_category(self):
        """Добавление новой категории"""
        dialog = Toplevel(self)
        dialog.title("Новая категория")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.configure(bg="#FFFFFF")
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (300 // 2)
        y = (dialog.winfo_screenheight() // 2) - (150 // 2)
        dialog.geometry(f'300x150+{x}+{y}')
        
        main_frame = Frame(dialog, bg="#FFFFFF", padx=20, pady=20)
        main_frame.pack(fill=BOTH, expand=True)
        
        Label(
            main_frame,
            text="Название категории:",
            font=LABEL_FONT,
            bg="#FFFFFF",
            fg="#666666"
        ).pack(anchor=W, pady=(0, 5))
        
        entry = ttk.Entry(main_frame, font=ENTRY_FONT)
        entry.pack(fill=X, pady=(0, 15))
        entry.focus_set()
        
        def add():
            name = entry.get().strip()
            if name and name not in self.categories:
                self.categories.append(name)
                self.category_combo['values'] = self.categories
                self.category_var.set(name)
                self.save_categories()
                if self.update_callback:
                    self.update_callback()
                dialog.destroy()
                self.info_label.config(text=f"✅ Категория '{name}' добавлена", fg="#4CAF50")
            elif name in self.categories:
                messagebox.showwarning("Ошибка", "Такая категория уже существует")
            else:
                messagebox.showwarning("Ошибка", "Введите название категории")
        
        btn_frame = Frame(main_frame, bg="#FFFFFF")
        btn_frame.pack(fill=X)
        
        Button(
            btn_frame,
            text="Добавить",
            font=BUTTON_FONT,
            bg="#4CAF50",
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=add
        ).pack(side=LEFT, padx=5, ipadx=10, ipady=5, expand=True)
        
        Button(
            btn_frame,
            text="Отмена",
            font=BUTTON_FONT,
            bg="#CCCCCC",
            fg="#333333",
            relief="flat",
            cursor="hand2",
            command=dialog.destroy
        ).pack(side=LEFT, padx=5, ipadx=10, ipady=5, expand=True)
        
        entry.bind('<Return>', lambda e: add())
    
    def clear_all(self):
        """Очистка всех полей"""
        self.password_entry.delete(0, END)
        self.alias_entry.delete(0, END)
        self.site_entry.delete(0, END)
        self.login_entry.delete(0, END)
        self.category_var.set(self.categories[0] if self.categories else "Без категории")
        self.info_label.config(text="")
        self.password_entry.focus_set()
    
    def save_password(self):
        """Сохранение пароля"""
        password = self.password_entry.get()
        alias = self.alias_entry.get().strip()
        site = self.site_entry.get().strip()
        login = self.login_entry.get().strip()
        category = self.category_var.get()
        
        if not password:
            self.info_label.config(text="❌ Введите пароль!", fg="red")
            return
        
        if not alias:
            alias = site if site else "Без названия"
        
        data = {}
        try:
            with open(".data", "r", encoding='utf-8') as f:
                data = json.load(f)
        except:
            pass
        
        import time
        password_id = f"{self.current_user}_{int(time.time() * 1000)}"
        
        data[password_id] = {
            "password": encode.encode(password),
            "alias": alias,
            "site": site,
            "login": login,
            "category": category,
            "owner": self.current_user,
            "favorite": False,
            "notes": "",
            "created": time.time()
        }
        
        try:
            with open(".data", "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            self.info_label.config(text="✅ Пароль сохранен!", fg="#4CAF50")
            
            if self.update_callback:
                self.update_callback()
            
            self.after(1500, self.destroy)
        except Exception as e:
            self.info_label.config(text=f"❌ Ошибка: {e}", fg="red")

if __name__ == '__main__':
    root = Tk()
    root.withdraw()
    new = AddWindow(root)
    root.mainloop()
