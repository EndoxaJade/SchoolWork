# manager.py
try:
    from tkinter import *
    from tkinter import ttk
    from tkinter import messagebox
except ImportError:
    from Tkinter import *
    import ttk
    import tkMessageBox as messagebox

import Add
import hashlib
import os
import encode
import List
import Search
import json
import re
import random
import string
from datetime import datetime

try:
    import pyperclip
except ImportError:
    pyperclip = None

# Настройка шрифтов
TITLE_FONT = ("Segoe UI", 20, "bold")
HEADER_FONT = ("Segoe UI", 14, "bold")
LABEL_FONT = ("Segoe UI", 10)
FIELD_FONT = ("Segoe UI", 11)
BUTTON_FONT = ("Segoe UI", 11, "bold")
LINK_FONT = ("Segoe UI", 10)
SMALL_FONT = ("Segoe UI", 9)

# Цвета
BG_COLOR = "#E6E6E6"
WHITE = "#FFFFFF"
TEXT_DARK = "#000000"
TEXT_GRAY = "#666666"
BUTTON_BG = "#E4CCFF"
BUTTON_TEXT = "#5C0071"
BORDER_COLOR = "#CE04F3"
ENTRY_BG = "#FFFFFF"
FAVORITE_COLOR = "#FFD700"
CATEGORY_SELECTED = "#E4CCFF"

# Файлы для хранения данных
USERS_FILE = ".users"
ORGANIZATIONS_FILE = ".organizations"
CATEGORIES_FILE = ".categories"

class RoundedFrame(Frame):
    """Фрейм со скругленными углами"""
    def __init__(self, parent, corner_radius=15, border_color=BORDER_COLOR, border_width=2, bg=WHITE, **kwargs):
        super().__init__(parent, bg=bg, **kwargs)
        self.corner_radius = corner_radius
        self.border_color = border_color
        self.border_width = border_width
        self.bg_color = bg

        self.canvas = Canvas(self, bg=bg, highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=True)

        self.inner_frame = Frame(self.canvas, bg=bg)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.bind("<Configure>", self._on_configure)
        self.canvas.bind("<Configure>", self._draw_rounded_rect)

    def _draw_rounded_rect(self, event=None):
        self.canvas.delete("border")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        r = self.corner_radius

        if width < 2 or height < 2:
            return

        self.canvas.create_oval(0, 0, r*2, r*2, fill=self.bg_color, outline=self.bg_color, tags="border")
        self.canvas.create_oval(width-r*2, 0, width, r*2, fill=self.bg_color, outline=self.bg_color, tags="border")
        self.canvas.create_oval(0, height-r*2, r*2, height, fill=self.bg_color, outline=self.bg_color, tags="border")
        self.canvas.create_oval(width-r*2, height-r*2, width, height, fill=self.bg_color, outline=self.bg_color, tags="border")
        self.canvas.create_rectangle(r, 0, width-r, height, fill=self.bg_color, outline=self.bg_color, tags="border")
        self.canvas.create_rectangle(0, r, width, height-r, fill=self.bg_color, outline=self.bg_color, tags="border")

        bw = self.border_width
        self.canvas.create_arc(r, r, r*3, r*3, start=90, extent=90, outline=self.border_color, width=bw, tags="border")
        self.canvas.create_arc(width-r*3, r, width-r, r*3, start=0, extent=90, outline=self.border_color, width=bw, tags="border")
        self.canvas.create_arc(r, height-r*3, r*3, height-r, start=180, extent=90, outline=self.border_color, width=bw, tags="border")
        self.canvas.create_arc(width-r*3, height-r*3, width-r, height-r, start=270, extent=90, outline=self.border_color, width=bw, tags="border")
        self.canvas.create_line(r, 0, width-r, 0, fill=self.border_color, width=bw, tags="border")
        self.canvas.create_line(r, height, width-r, height, fill=self.border_color, width=bw, tags="border")
        self.canvas.create_line(0, r, 0, height-r, fill=self.border_color, width=bw, tags="border")
        self.canvas.create_line(width, r, width, height-r, fill=self.border_color, width=bw, tags="border")

    def _on_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width, height=event.height)
        self._draw_rounded_rect()

class RoundedEntry(Frame):
    """Поле ввода со скругленными углами"""
    def __init__(self, parent, corner_radius=10, show="", font=FIELD_FONT, fg=TEXT_DARK, **kwargs):
        bg_color = parent.cget('bg') if hasattr(parent, 'cget') else WHITE
        super().__init__(parent, bg=bg_color, height=40)
        self.pack(fill=X, pady=(0, 5))
        self.corner_radius = corner_radius
        self.border_color = BORDER_COLOR
        self.bg_color = WHITE
        self.fg_color = fg

        self.canvas = Canvas(self, bg=bg_color, highlightthickness=0, height=40)
        self.canvas.pack(fill=X, expand=True)

        self.entry_widget = Entry(self.canvas, font=font, fg=fg, show=show,
                                  bg=WHITE, relief="flat", bd=0, highlightthickness=0,
                                  insertbackground=TEXT_DARK)
        self.entry_window = self.canvas.create_window((15, 20), window=self.entry_widget, anchor="w")

        self.canvas.bind("<Configure>", self._on_configure)
        self.entry_widget.bind("<FocusIn>", self._on_focus_in)
        self.entry_widget.bind("<FocusOut>", self._on_focus_out)

        self._draw_entry()

    def _draw_entry(self, focused=False):
        self.canvas.delete("entry_bg")
        w = self.canvas.winfo_width() or 400
        h = 40
        r = self.corner_radius

        if w < 2:
            return

        color = self.bg_color if not focused else "#F5F0FF"
        border = self.border_color

        self.canvas.create_oval(0, 0, r*2, r*2, fill=color, outline=color, tags="entry_bg")
        self.canvas.create_oval(w-r*2, 0, w, r*2, fill=color, outline=color, tags="entry_bg")
        self.canvas.create_oval(0, h-r*2, r*2, h, fill=color, outline=color, tags="entry_bg")
        self.canvas.create_oval(w-r*2, h-r*2, w, h, fill=color, outline=color, tags="entry_bg")
        self.canvas.create_rectangle(r, 0, w-r, h, fill=color, outline=color, tags="entry_bg")
        self.canvas.create_rectangle(0, r, w, h-r, fill=color, outline=color, tags="entry_bg")

        bw = 2
        self.canvas.create_arc(r, r, r*3, r*3, start=90, extent=90, outline=border, width=bw, tags="entry_bg")
        self.canvas.create_arc(w-r*3, r, w-r, r*3, start=0, extent=90, outline=border, width=bw, tags="entry_bg")
        self.canvas.create_arc(r, h-r*3, r*3, h-r, start=180, extent=90, outline=border, width=bw, tags="entry_bg")
        self.canvas.create_arc(w-r*3, h-r*3, w-r, h-r, start=270, extent=90, outline=border, width=bw, tags="entry_bg")
        self.canvas.create_line(r, 0, w-r, 0, fill=border, width=bw, tags="entry_bg")
        self.canvas.create_line(r, h, w-r, h, fill=border, width=bw, tags="entry_bg")
        self.canvas.create_line(0, r, 0, h-r, fill=border, width=bw, tags="entry_bg")
        self.canvas.create_line(w, r, w, h-r, fill=border, width=bw, tags="entry_bg")

    def _on_configure(self, event):
        if event.width > 30:
            self.canvas.itemconfig(self.entry_window, width=event.width-30)
        self._draw_entry()

    def _on_focus_in(self, event):
        self._draw_entry(focused=True)

    def _on_focus_out(self, event):
        self._draw_entry(focused=False)

    def get(self):
        return self.entry_widget.get()

    def delete(self, first, last=None):
        self.entry_widget.delete(first, last)

    def insert(self, index, string):
        self.entry_widget.insert(index, string)

    def focus_set(self):
        self.entry_widget.focus_set()

    def bind(self, sequence, func, add=None):
        self.entry_widget.bind(sequence, func, add)

    def config(self, **kwargs):
        if 'justify' in kwargs:
            self.entry_widget.config(justify=kwargs['justify'])
        if 'show' in kwargs:
            self.entry_widget.config(show=kwargs['show'])


class FavoritesWindow(Toplevel):
    """Окно с избранными паролями"""
    def __init__(self, parent, favorites):
        super().__init__(parent)
        self.parent = parent
        self.favorites = favorites
        
        self.title("Избранные пароли")
        self.geometry("400x450")
        self.resizable(False, False)
        self.configure(bg="#FFFFFF")
        
        self.center_window()
        self.create_widgets()
    
    def center_window(self):
        self.update_idletasks()
        width = 400
        height = 450
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        main_frame = Frame(self, bg="#FFFFFF", padx=20, pady=15)
        main_frame.pack(fill=BOTH, expand=True)
        
        title = Label(
            main_frame,
            text="★ Избранные пароли",
            font=("Segoe UI", 16, "bold"),
            bg="#FFFFFF",
            fg="#5C0071"
        )
        title.pack(pady=(0, 10))
        
        list_frame = Frame(main_frame, bg="#FFFFFF")
        list_frame.pack(fill=BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.listbox = Listbox(
            list_frame,
            font=("Segoe UI", 11),
            bg="#FFFFFF",
            fg="#333333",
            selectbackground="#E4CCFF",
            selectforeground="#333333",
            yscrollcommand=scrollbar.set,
            height=12
        )
        scrollbar.config(command=self.listbox.yview)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)
        
        self.update_list()
        self.listbox.bind("<Double-1>", self.on_double_click)
        
        back_btn = Button(
            main_frame,
            text="Назад",
            font=("Segoe UI", 11, "bold"),
            bg="#E4CCFF",
            fg="#5C0071",
            relief="flat",
            cursor="hand2",
            command=self.destroy
        )
        back_btn.pack(pady=(10, 0), fill=X, ipady=6)
    
    def update_list(self):
        self.listbox.delete(0, END)
        self.favorites.sort(key=lambda x: x.get('created', 0), reverse=True)
        for idx, pwd in enumerate(self.favorites, 1):
            display_name = pwd.get('alias') if pwd.get('alias') else pwd.get('site', 'Без названия')
            self.listbox.insert(END, f"{idx}. {display_name}")
    
    def on_double_click(self, event):
        selected = self.listbox.curselection()
        if not selected:
            return
        idx = selected[0]
        if 0 <= idx < len(self.favorites):
            pwd = self.favorites[idx]
            self.destroy()
            self.parent.show_password_view(pwd)


class GeneratorWindow(Toplevel):
    """Окно генерации паролей"""
    
    def __init__(self, parent, return_to_add=False, add_window=None):
        super().__init__(parent)
        self.parent = parent
        self.return_to_add = return_to_add
        self.add_window = add_window
        self.generated_passwords = []
        
        self.title("Генератор паролей")
        self.geometry("500x550")
        self.resizable(False, False)
        self.configure(bg="#FFFFFF")
        self.center_window()
        self.create_widgets()
    
    def center_window(self):
        self.update_idletasks()
        width = 500
        height = 550
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        # Основной контейнер
        main_frame = Frame(self, bg="#FFFFFF", padx=25, pady=20)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Заголовок
        title = Label(
            main_frame,
            text="🔐 Генератор паролей",
            font=("Segoe UI", 18, "bold"),
            bg="#FFFFFF",
            fg="#5C0071"
        )
        title.pack(pady=(0, 15))
        
        # === Параметры ===
        params_frame = Frame(main_frame, bg="#FFFFFF")
        params_frame.pack(fill=X, pady=(0, 15))
        
        # Количество знаков
        Label(
            params_frame,
            text="Количество знаков",
            font=("Segoe UI", 11, "bold"),
            bg="#FFFFFF",
            fg="#333333",
            anchor="w"
        ).pack(fill=X, pady=(0, 3))
        
        self.length_var = StringVar(value="8")
        length_entry = ttk.Entry(
            params_frame,
            textvariable=self.length_var,
            font=("Segoe UI", 11),
            width=10
        )
        length_entry.pack(anchor=W, pady=(0, 10))
        
        # Обязательные знаки
        Label(
            params_frame,
            text="Обязательные знаки",
            font=("Segoe UI", 11, "bold"),
            bg="#FFFFFF",
            fg="#333333",
            anchor="w"
        ).pack(fill=X, pady=(0, 3))
        
        self.mandatory_var = StringVar()
        mandatory_entry = ttk.Entry(
            params_frame,
            textvariable=self.mandatory_var,
            font=("Segoe UI", 11)
        )
        mandatory_entry.pack(fill=X, pady=(0, 10))
        mandatory_entry.insert(0, "")
        
        # Количество паролей
        Label(
            params_frame,
            text="Количество паролей",
            font=("Segoe UI", 11, "bold"),
            bg="#FFFFFF",
            fg="#333333",
            anchor="w"
        ).pack(fill=X, pady=(0, 3))
        
        self.count_var = StringVar(value="1")
        count_entry = ttk.Entry(
            params_frame,
            textvariable=self.count_var,
            font=("Segoe UI", 11),
            width=10
        )
        count_entry.pack(anchor=W, pady=(0, 10))
        
        # Кнопка генерации
        generate_btn = Button(
            params_frame,
            text="Сгенерировать пароли",
            font=BUTTON_FONT,
            bg="#E4CCFF",
            fg="#5C0071",
            relief="flat",
            cursor="hand2",
            command=self.generate_passwords
        )
        generate_btn.pack(fill=X, ipady=8, pady=(0, 10))
        
        # === Список сгенерированных паролей ===
        list_label = Label(
            main_frame,
            text="Сгенерированные пароли",
            font=("Segoe UI", 11, "bold"),
            bg="#FFFFFF",
            fg="#333333",
            anchor="w"
        )
        list_label.pack(fill=X, pady=(0, 5))
        
        # Фрейм для списка с прокруткой
        list_container = Frame(main_frame, bg="#FFFFFF")
        list_container.pack(fill=BOTH, expand=True, pady=(0, 10))
        
        # Канвас для прокрутки
        self.canvas = Canvas(list_container, bg="#FFFFFF", highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg="#FFFFFF")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # === Нижние кнопки ===
        bottom_frame = Frame(main_frame, bg="#FFFFFF")
        bottom_frame.pack(fill=X, pady=(10, 0))
        
        # Кнопка "Повторно сгенерировать"
        regen_btn = Button(
            bottom_frame,
            text="Повторно сгенерировать",
            font=BUTTON_FONT,
            bg="#E4CCFF",
            fg="#5C0071",
            relief="flat",
            cursor="hand2",
            command=self.generate_passwords
        )
        regen_btn.pack(side=LEFT, padx=5, ipadx=10, ipady=8, expand=True)
        
        # Кнопка "Перейти в создание пароля" или "Вернуться"
        if self.return_to_add:
            btn_text = "Вернуться к созданию пароля"
        else:
            btn_text = "Перейти в создание пароля"
        
        go_to_add_btn = Button(
            bottom_frame,
            text=btn_text,
            font=BUTTON_FONT,
            bg="#4CAF50",
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.go_to_add_password
        )
        go_to_add_btn.pack(side=RIGHT, padx=5, ipadx=10, ipady=8, expand=True)
    
    def generate_passwords(self):
        """Генерация паролей"""
        # Получаем параметры
        try:
            length = int(self.length_var.get().strip())
            if length < 1:
                messagebox.showwarning("Ошибка", "Количество знаков должно быть больше 0")
                return
            if length > 100:
                length = 100
                self.length_var.set("100")
        except ValueError:
            messagebox.showwarning("Ошибка", "Введите корректное количество знаков")
            return
        
        # Обязательные знаки
        mandatory = self.mandatory_var.get().strip()
        if mandatory:
            mandatory_chars = [c.strip() for c in mandatory.split(",")]
        else:
            mandatory_chars = []
        
        # Количество паролей
        try:
            count = int(self.count_var.get().strip())
            if count < 1:
                messagebox.showwarning("Ошибка", "Количество паролей должно быть больше 0")
                return
            if count > 50:
                count = 50
                self.count_var.set("50")
        except ValueError:
            messagebox.showwarning("Ошибка", "Введите корректное количество паролей")
            return
        
        # Генерируем пароли
        new_passwords = []
        for i in range(count):
            password = self.generate_single_password(length, mandatory_chars)
            new_passwords.append(password)
        
        # Добавляем к существующим
        self.generated_passwords.extend(new_passwords)
        
        # Отображаем
        self.display_passwords()
    
    def generate_single_password(self, length, mandatory_chars):
        """Генерация одного пароля"""
        # Набор символов
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        punctuation = "!@#$%^&*()-_=+[]{}|;:,.<>?/~"
        
        all_chars = lowercase + uppercase + digits + punctuation
        
        # Если есть обязательные символы
        if mandatory_chars:
            # Проверяем, что все обязательные символы есть в наборе
            valid_mandatory = []
            for char in mandatory_chars:
                if char in all_chars:
                    valid_mandatory.append(char)
                else:
                    # Если символ не найден, добавляем его в набор
                    all_chars += char
                    valid_mandatory.append(char)
            
            # Строим пароль с обязательными символами
            if length < len(valid_mandatory):
                length = len(valid_mandatory) + 2
                self.length_var.set(str(length))
            
            # Сначала добавляем обязательные символы
            password_chars = valid_mandatory.copy()
            
            # Добавляем остальные случайные символы
            remaining = length - len(valid_mandatory)
            if remaining > 0:
                password_chars.extend(random.choices(all_chars, k=remaining))
            
            # Перемешиваем
            random.shuffle(password_chars)
            return ''.join(password_chars)
        else:
            # Простая генерация
            return ''.join(random.choices(all_chars, k=length))
    
    def display_passwords(self):
        """Отображение сгенерированных паролей"""
        # Очищаем старые виджеты
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Создаем строки для каждого пароля
        for idx, password in enumerate(self.generated_passwords, 1):
            pwd_frame = Frame(self.scrollable_frame, bg="#FFFFFF", pady=3)
            pwd_frame.pack(fill=X)
            
            # Номер
            num_label = Label(
                pwd_frame,
                text=f"{idx}.",
                font=("Segoe UI", 11),
                bg="#FFFFFF",
                fg="#666666",
                width=4,
                anchor="w"
            )
            num_label.pack(side=LEFT)
            
            # Пароль (скрытый по умолчанию)
            pwd_label = Label(
                pwd_frame,
                text="●" * len(password),
                font=("Segoe UI", 11, "bold"),
                bg="#FFFFFF",
                fg="#333333",
                anchor="w"
            )
            pwd_label.pack(side=LEFT, fill=X, expand=True, padx=(0, 5))
            
            # Сохраняем пароль в атрибуте
            pwd_label.real_password = password
            pwd_label.showing = False
            
            # Кнопка показа/скрытия
            show_btn = Button(
                pwd_frame,
                text="👁",
                font=("Segoe UI", 11),
                bg="#FFFFFF",
                fg="#666666",
                relief="flat",
                cursor="hand2",
                command=lambda lbl=pwd_label: self.toggle_show_password(lbl)
            )
            show_btn.pack(side=RIGHT, padx=(0, 5))
            
            # Кнопка копирования
            copy_btn = Button(
                pwd_frame,
                text="📋",
                font=("Segoe UI", 11),
                bg="#FFFFFF",
                fg="#666666",
                relief="flat",
                cursor="hand2",
                command=lambda p=password: self.copy_password(p)
            )
            copy_btn.pack(side=RIGHT, padx=(0, 5))
            
            # Кнопка перехода к добавлению (только если не возврат)
            if not self.return_to_add:
                add_btn = Button(
                    pwd_frame,
                    text="➕",
                    font=("Segoe UI", 11),
                    bg="#FFFFFF",
                    fg="#4CAF50",
                    relief="flat",
                    cursor="hand2",
                    command=lambda p=password: self.go_to_add_with_password(p)
                )
                add_btn.pack(side=RIGHT, padx=(0, 5))
        
        # Обновляем размер канваса
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def toggle_show_password(self, label):
        """Показать/скрыть пароль"""
        if label.showing:
            label.config(text="●" * len(label.real_password))
            label.showing = False
        else:
            label.config(text=label.real_password)
            label.showing = True
    
    def copy_password(self, password):
        """Копирование пароля в буфер обмена"""
        if pyperclip:
            try:
                pyperclip.copy(password)
                messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена")
            except:
                # Если pyperclip не работает, используем стандартный способ
                self.clipboard_clear()
                self.clipboard_append(password)
                self.update()
                messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена")
        else:
            self.clipboard_clear()
            self.clipboard_append(password)
            self.update()
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена")
    
    def go_to_add_with_password(self, password):
        """Переход к добавлению с выбранным паролем"""
        self.destroy()
        self.parent.open_add_password_with_password(password)
    
    def go_to_add_password(self):
        """Переход к добавлению пароля"""
        if self.return_to_add and self.add_window:
            # Возвращаемся к окну добавления
            self.destroy()
            self.add_window.deiconify()
            self.add_window.lift()
        else:
            # Открываем новое окно добавления
            last_password = self.generated_passwords[-1] if self.generated_passwords else ""
            self.destroy()
            self.parent.open_add_password_with_password(last_password)


class Login(Tk):
    def __init__(self, *args):
        Tk.__init__(self, *args)

        if os.name == 'nt':
            Tk.iconbitmap(self, default='icon.ico')

        self.title("Шифровалка")
        self.geometry("520x620")
        self.resizable(False, False)
        self.configure(bg=BG_COLOR)
        self.center_window()

        self.current_screen = "login"
        self.current_user = None
        self.users_data = self.load_users()
        self.organizations_data = self.load_organizations()
        self.categories_data = self.load_categories()
        
        self.selected_category = None
        self.filtered_passwords = []

        self.migrate_passwords()

        self.logo_image = None
        try:
            from PIL import Image, ImageTk
            img = Image.open("logo.png")
            img = img.resize((64, 64), Image.Resampling.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(img)
        except:
            self.logo_image = None

        self.show_login_screen()

    def center_window(self):
        self.update_idletasks()
        width = 520
        height = 620
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def load_users(self):
        try:
            with open(USERS_FILE, "r", encoding='utf-8') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError):
            return {}

    def save_users(self):
        try:
            with open(USERS_FILE, "w", encoding='utf-8') as f:
                json.dump(self.users_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка сохранения пользователей: {e}")

    def load_organizations(self):
        try:
            with open(ORGANIZATIONS_FILE, "r", encoding='utf-8') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError):
            return {}

    def save_organizations(self):
        try:
            with open(ORGANIZATIONS_FILE, "w", encoding='utf-8') as f:
                json.dump(self.organizations_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка сохранения организаций: {e}")

    def load_categories(self):
        try:
            with open(CATEGORIES_FILE, "r", encoding='utf-8') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError):
            return {}

    def save_categories(self):
        try:
            with open(CATEGORIES_FILE, "w", encoding='utf-8') as f:
                json.dump(self.categories_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка сохранения категорий: {e}")

    def migrate_passwords(self):
        try:
            with open(".data", "r", encoding='utf-8') as f:
                data = json.load(f)
            
            migrated = False
            new_data = {}
            
            for key, value in data.items():
                if isinstance(value, list) and len(value) >= 2:
                    owner = value[2] if len(value) >= 3 else "default"
                    import time
                    new_id = f"{owner}_{int(time.time() * 1000)}_{len(new_data)}"
                    new_data[new_id] = {
                        "password": value[1],
                        "alias": key,
                        "site": key,
                        "login": value[0],
                        "category": "Без категории",
                        "owner": owner,
                        "favorite": False,
                        "notes": "",
                        "created": time.time()
                    }
                    migrated = True
                elif isinstance(value, dict) and "password" in value:
                    new_data[key] = value
            
            if migrated:
                with open(".data", "w", encoding='utf-8') as f:
                    json.dump(new_data, f, indent=4, ensure_ascii=False)
        except (IOError, json.JSONDecodeError):
            pass

    def generate_organization_code(self, name):
        import random
        import string
        prefix = ''.join(word[0].upper() for word in name.split()[:3])
        if len(prefix) < 2:
            prefix = name[:2].upper()
        code = prefix + ''.join(random.choices(string.digits, k=6))
        return code

    def add_logo(self, parent):
        if self.logo_image:
            logo_label = Label(parent, image=self.logo_image, bg=WHITE)
            logo_label.image = self.logo_image
            logo_label.pack(pady=(10, 5))
        else:
            logo_label = Label(parent, text="🔒", font=("Segoe UI", 40), bg=WHITE, fg=TEXT_DARK)
            logo_label.pack(pady=(10, 5))
        return logo_label

    def create_separator(self, parent):
        sep = Frame(parent, height=1, bd=0, bg=BORDER_COLOR)
        sep.pack(fill=X, pady=(15, 15))
        return sep

    def create_entry(self, parent, show=""):
        entry = RoundedEntry(parent, show=show, font=FIELD_FONT, fg=TEXT_DARK)
        return entry

    def create_rounded_button(self, parent, text, command, **kwargs):
        btn = Button(parent, text=text,
                     font=BUTTON_FONT,
                     bg=BUTTON_BG,
                     fg=BUTTON_TEXT,
                     activebackground="#D4B8FF",
                     activeforeground=BUTTON_TEXT,
                     relief="solid",
                     bd=2,
                     highlightbackground=BORDER_COLOR,
                     highlightcolor=BORDER_COLOR,
                     cursor="hand2",
                     command=command,
                     **kwargs)
        return btn

    # ============================================================
    # ЭКРАН 1: ВХОД
    # ============================================================

    def show_login_screen(self):
        self.clear_window()
        self.title("Шифровалка - Вход")
        self.current_screen = "login"
        self.configure(bg=BG_COLOR)

        card = RoundedFrame(self, corner_radius=15, bg=WHITE, border_color=BORDER_COLOR, border_width=2)
        card.pack(fill=BOTH, expand=True, padx=40, pady=40)

        main_frame = card.inner_frame
        main_frame.configure(bg=WHITE)
        main_frame.pack(fill=BOTH, expand=True, padx=40, pady=20)

        self.add_logo(main_frame)

        title_label = Label(main_frame, text="Войти в аккаунт", font=TITLE_FONT, fg=TEXT_DARK, bg=WHITE)
        title_label.pack(pady=(5, 25))

        login_label = Label(main_frame, text="Логин", font=LABEL_FONT, fg=TEXT_GRAY, anchor="w", bg=WHITE)
        login_label.pack(fill=X, pady=(0, 5))
        self.login_entry = self.create_entry(main_frame)
        self.login_entry.pack(fill=X, pady=(0, 5))
        self.login_entry.focus_set()

        password_label = Label(main_frame, text="Пароль", font=LABEL_FONT, fg=TEXT_GRAY, anchor="w", bg=WHITE)
        password_label.pack(fill=X, pady=(0, 5))
        self.password_entry = self.create_entry(main_frame, show="*")
        self.password_entry.pack(fill=X, pady=(0, 15))
        self.password_entry.bind('<Return>', lambda e: self.login_action())

        login_btn = self.create_rounded_button(main_frame, text="Войти", command=self.login_action)
        login_btn.pack(fill=X, pady=(0, 20), ipady=8)

        links_frame = Frame(main_frame, bg=WHITE)
        links_frame.pack(pady=(10, 0))

        forgot_link = Label(links_frame, text="Забыли пароль?", font=LINK_FONT, fg=TEXT_GRAY, bg=WHITE, cursor="hand2")
        forgot_link.pack(side=LEFT, padx=(0, 20))
        forgot_link.bind('<Button-1>', lambda e: self.show_forgot_password_screen())
        forgot_link.bind('<Enter>', lambda e: forgot_link.config(fg=TEXT_DARK))
        forgot_link.bind('<Leave>', lambda e: forgot_link.config(fg=TEXT_GRAY))

        register_link = Label(links_frame, text="Зарегистрироваться", font=LINK_FONT, fg=BUTTON_TEXT, bg=WHITE, cursor="hand2")
        register_link.pack(side=LEFT)
        register_link.bind('<Button-1>', lambda e: self.show_register_type_screen())
        register_link.bind('<Enter>', lambda e: register_link.config(fg="#3D0050"))
        register_link.bind('<Leave>', lambda e: register_link.config(fg=BUTTON_TEXT))

    def login_action(self):
        login = self.login_entry.get().strip()
        password = self.password_entry.get()

        if not login or not password:
            messagebox.showwarning("Ошибка", "Введите логин и пароль")
            return

        if login not in self.users_data:
            messagebox.showerror("Ошибка", "Пользователь не найден")
            return

        hashed_password = hashlib.md5(password.encode()).hexdigest()
        if self.users_data[login]["password"] == hashed_password:
            self.current_user = login
            self.show_2fa_screen()
        else:
            messagebox.showerror("Ошибка", "Неверный пароль")

    # ============================================================
    # ЭКРАН 2: 2FA
    # ============================================================

    def show_2fa_screen(self):
        self.clear_window()
        self.title("Шифровалка - Код подтверждения")
        self.current_screen = "2fa"
        self.configure(bg=BG_COLOR)

        card = RoundedFrame(self, corner_radius=15, bg=WHITE, border_color=BORDER_COLOR, border_width=2)
        card.pack(fill=BOTH, expand=True, padx=40, pady=40)

        main_frame = card.inner_frame
        main_frame.configure(bg=WHITE)
        main_frame.pack(fill=BOTH, expand=True, padx=40, pady=30)

        self.add_logo(main_frame)

        title_label = Label(main_frame, text="Введите пришедший код", font=TITLE_FONT, fg=TEXT_DARK, bg=WHITE)
        title_label.pack(pady=(5, 25))

        self.code_entry = self.create_entry(main_frame)
        self.code_entry.config(justify="center")
        self.code_entry.pack(fill=X, pady=(0, 20))
        self.code_entry.bind('<Return>', lambda e: self.code_action())
        self.code_entry.focus_set()

        continue_btn = self.create_rounded_button(main_frame, text="Продолжить", command=self.code_action)
        continue_btn.pack(fill=X, pady=(0, 20), ipady=8)

        back_link = Label(main_frame, text="Назад", font=LINK_FONT, fg=TEXT_GRAY, bg=WHITE, cursor="hand2")
        back_link.pack()
        back_link.bind('<Button-1>', lambda e: self.show_login_screen())
        back_link.bind('<Enter>', lambda e: back_link.config(fg=TEXT_DARK))
        back_link.bind('<Leave>', lambda e: back_link.config(fg=TEXT_GRAY))

    def code_action(self):
        code = self.code_entry.get().strip()
        if code == "123456":
            # Получаем имя пользователя из данных
            user_data = self.users_data.get(self.current_user, {})
            user_name = user_data.get('name', self.current_user)  # Если имя не найдено, показываем логин
            messagebox.showinfo("Успех", f"Добро пожаловать, {user_name}!")
            self.show_main_app()
        else:
            messagebox.showerror("Ошибка", "Неверный код подтверждения")
            self.code_entry.delete(0, END)
            self.code_entry.focus_set()

    # ============================================================
    # ЭКРАН 3: ВОССТАНОВЛЕНИЕ ПАРОЛЯ
    # ============================================================

    def show_forgot_password_screen(self):
        self.clear_window()
        self.title("Шифровалка - Восстановление пароля")
        self.current_screen = "forgot"
        self.configure(bg=BG_COLOR)

        card = RoundedFrame(self, corner_radius=15, bg=WHITE, border_color=BORDER_COLOR, border_width=2)
        card.pack(fill=BOTH, expand=True, padx=40, pady=40)

        main_frame = card.inner_frame
        main_frame.configure(bg=WHITE)
        main_frame.pack(fill=BOTH, expand=True, padx=40, pady=30)

        self.add_logo(main_frame)

        step_label = Label(main_frame, text="Шаг 1.", font=TITLE_FONT, fg=TEXT_DARK, bg=WHITE)
        step_label.pack(pady=(5, 5))

        title_label = Label(main_frame, text="Введите адрес электронной почты", font=HEADER_FONT, fg=TEXT_GRAY, bg=WHITE)
        title_label.pack(pady=(0, 20))

        self.email_entry = self.create_entry(main_frame)
        self.email_entry.pack(fill=X, pady=(0, 20))
        self.email_entry.bind('<Return>', lambda e: self.forgot_password_action())
        self.email_entry.focus_set()

        send_btn = self.create_rounded_button(main_frame, text="Отправить", command=self.forgot_password_action)
        send_btn.pack(fill=X, pady=(0, 20), ipady=8)

        back_link = Label(main_frame, text="Назад", font=LINK_FONT, fg=TEXT_GRAY, bg=WHITE, cursor="hand2")
        back_link.pack()
        back_link.bind('<Button-1>', lambda e: self.show_login_screen())
        back_link.bind('<Enter>', lambda e: back_link.config(fg=TEXT_DARK))
        back_link.bind('<Leave>', lambda e: back_link.config(fg=TEXT_GRAY))

    def forgot_password_action(self):
        email = self.email_entry.get().strip()
        if not email:
            messagebox.showwarning("Ошибка", "Введите адрес электронной почты")
            return

        found = False
        for login, data in self.users_data.items():
            if data.get("email") == email:
                found = True
                break

        if found:
            messagebox.showinfo("Восстановление", f"Инструкции по восстановлению отправлены на {email}")
            self.show_login_screen()
        else:
            messagebox.showerror("Ошибка", "Пользователь с таким email не найден")

    # ============================================================
    # ЭКРАН 4: ВЫБОР ТИПА РЕГИСТРАЦИИ
    # ============================================================

    def show_register_type_screen(self):
        self.clear_window()
        self.title("Шифровалка - Регистрация")
        self.current_screen = "register_type"
        self.configure(bg=BG_COLOR)

        card = RoundedFrame(self, corner_radius=15, bg=WHITE, border_color=BORDER_COLOR, border_width=2)
        card.pack(fill=BOTH, expand=True, padx=40, pady=40)

        main_frame = card.inner_frame
        main_frame.configure(bg=WHITE)
        main_frame.pack(fill=BOTH, expand=True, padx=40, pady=20)

        self.add_logo(main_frame)

        title_label = Label(main_frame, text="Создание аккаунта", font=TITLE_FONT, fg=TEXT_DARK, bg=WHITE)
        title_label.pack(pady=(5, 25))

        btn_style = {
            "font": BUTTON_FONT,
            "pady": 14,
            "bd": 2,
            "relief": "solid",
            "cursor": "hand2",
            "bg": BUTTON_BG,
            "fg": BUTTON_TEXT,
            "activebackground": "#D4B8FF",
            "activeforeground": BUTTON_TEXT,
            "highlightbackground": BORDER_COLOR,
            "highlightcolor": BORDER_COLOR
        }

        personal_btn = Button(main_frame, text="Личный аккаунт", **btn_style, command=lambda: self.show_personal_register())
        personal_btn.pack(pady=(0, 10), fill=X)

        corporate_btn = Button(main_frame, text="Корпоративный аккаунт", **btn_style, command=lambda: self.show_corporate_register())
        corporate_btn.pack(pady=(0, 10), fill=X)

        org_btn = Button(main_frame, text="Зарегистрировать организацию", **btn_style, command=lambda: self.show_organization_register())
        org_btn.pack(pady=(0, 10), fill=X)

        back_link = Label(main_frame, text="Назад", font=LINK_FONT, fg=TEXT_GRAY, bg=WHITE, cursor="hand2")
        back_link.pack(pady=(20, 0))
        back_link.bind('<Button-1>', lambda e: self.show_login_screen())
        back_link.bind('<Enter>', lambda e: back_link.config(fg=TEXT_DARK))
        back_link.bind('<Leave>', lambda e: back_link.config(fg=TEXT_GRAY))

    # ============================================================
    # ЭКРАН 5: РЕГИСТРАЦИЯ ЛИЧНОГО АККАУНТА
    # ============================================================

    def show_personal_register(self):
        self.clear_window()
        self.title("Шифровалка - Регистрация личного аккаунта")
        self.current_screen = "personal_register"
        self.configure(bg=BG_COLOR)

        main_container = Frame(self, bg=BG_COLOR)
        main_container.pack(fill=BOTH, expand=True)

        canvas = Canvas(main_container, bg=BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg=BG_COLOR)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        card = RoundedFrame(scrollable_frame, corner_radius=15, bg=WHITE, border_color=BORDER_COLOR, border_width=2)
        card.pack(fill=BOTH, expand=True, padx=40, pady=30)

        main_frame = card.inner_frame
        main_frame.configure(bg=WHITE)
        main_frame.pack(fill=BOTH, expand=True, padx=40, pady=20)

        title_label = Label(main_frame, text="Регистрация личного аккаунта", font=TITLE_FONT, fg=TEXT_DARK, bg=WHITE)
        title_label.pack(pady=(20, 20))

        fields = [
            ("Фамилия", "surname"),
            ("Имя", "name"),
            ("Отчество", "patronymic"),
            ("Email", "email"),
            ("Логин", "login"),
            ("Пароль", "password", "*"),
            ("Повторный пароль", "confirm_password", "*")
        ]

        self.reg_fields = {}
        for field_info in fields:
            label_text = field_info[0]
            field_name = field_info[1]
            show_char = field_info[2] if len(field_info) > 2 else ""

            label = Label(main_frame, text=label_text, font=LABEL_FONT, fg=TEXT_GRAY, anchor="w", bg=WHITE)
            label.pack(fill=X, pady=(8, 3))
            entry = self.create_entry(main_frame, show=show_char)
            entry.pack(fill=X, pady=(0, 3))

            if field_name == "surname":
                entry.focus_set()
            self.reg_fields[field_name] = entry

        self.create_separator(main_frame)

        buttons_frame = Frame(main_frame, bg=WHITE)
        buttons_frame.pack(pady=(10, 5), fill=X)

        back_btn = Button(buttons_frame, text="Назад", font=BUTTON_FONT, bg=BUTTON_BG, fg=BUTTON_TEXT,
                         activebackground="#D4B8FF", activeforeground=BUTTON_TEXT, relief="solid", bd=2,
                         highlightbackground=BORDER_COLOR, highlightcolor=BORDER_COLOR, pady=10,
                         cursor="hand2", command=self.show_register_type_screen)
        back_btn.pack(side=LEFT, padx=(0, 10))

        continue_btn = Button(buttons_frame, text="Продолжить", font=BUTTON_FONT, bg=BUTTON_BG, fg=BUTTON_TEXT,
                             activebackground="#D4B8FF", activeforeground=BUTTON_TEXT, relief="solid", bd=2,
                             highlightbackground=BORDER_COLOR, highlightcolor=BORDER_COLOR, pady=10,
                             cursor="hand2", command=self.personal_register_action)
        continue_btn.pack(side=RIGHT)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def personal_register_action(self):
        surname = self.reg_fields["surname"].get().strip()
        name = self.reg_fields["name"].get().strip()
        patronymic = self.reg_fields["patronymic"].get().strip()
        email = self.reg_fields["email"].get().strip()
        login = self.reg_fields["login"].get().strip()
        password = self.reg_fields["password"].get()
        confirm = self.reg_fields["confirm_password"].get()

        if not all([surname, name, email, login, password, confirm]):
            messagebox.showwarning("Ошибка", "Все поля обязательны для заполнения")
            return

        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            messagebox.showwarning("Ошибка", "Введите корректный email")
            return

        if len(password) < 4:
            messagebox.showwarning("Ошибка", "Пароль должен содержать минимум 4 символа")
            return

        if password != confirm:
            messagebox.showerror("Ошибка", "Пароли не совпадают")
            return

        if login in self.users_data:
            messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует")
            return

        for user_data in self.users_data.values():
            if user_data.get("email") == email:
                messagebox.showerror("Ошибка", "Пользователь с таким email уже существует")
                return

        hashed_password = hashlib.md5(password.encode()).hexdigest()
        self.users_data[login] = {
            "password": hashed_password,
            "email": email,
            "account_type": "personal",
            "surname": surname,
            "name": name,
            "patronymic": patronymic,
            "created": datetime.now().isoformat()
        }
        self.save_users()

        if login not in self.categories_data:
            self.categories_data[login] = ["Без категории"]
            self.save_categories()

        messagebox.showinfo("Успех", "Регистрация выполнена успешно!")
        self.current_user = login
        self.show_main_app()

    # ============================================================
    # ЭКРАН 6: РЕГИСТРАЦИЯ КОРПОРАТИВНОГО АККАУНТА
    # ============================================================

    def show_corporate_register(self):
        self.clear_window()
        self.title("Шифровалка - Регистрация корпоративного аккаунта")
        self.current_screen = "corporate_register"
        self.configure(bg=BG_COLOR)

        main_container = Frame(self, bg=BG_COLOR)
        main_container.pack(fill=BOTH, expand=True)

        canvas = Canvas(main_container, bg=BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg=BG_COLOR)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        card = RoundedFrame(scrollable_frame, corner_radius=15, bg=WHITE, border_color=BORDER_COLOR, border_width=2)
        card.pack(fill=BOTH, expand=True, padx=40, pady=30)

        main_frame = card.inner_frame
        main_frame.configure(bg=WHITE)
        main_frame.pack(fill=BOTH, expand=True, padx=40, pady=20)

        title_label = Label(main_frame, text="Регистрация корпоративного аккаунта", font=TITLE_FONT, fg=TEXT_DARK, bg=WHITE)
        title_label.pack(pady=(20, 20))

        fields = [
            ("Код организации", "org_code"),
            ("Фамилия", "surname"),
            ("Имя", "name"),
            ("Отчество", "patronymic"),
            ("Должность", "position"),
            ("Отдел", "department"),
            ("Email", "email"),
            ("Логин", "login"),
            ("Пароль", "password", "*"),
            ("Повторный пароль", "confirm_password", "*")
        ]

        self.reg_fields = {}
        for field_info in fields:
            label_text = field_info[0]
            field_name = field_info[1]
            show_char = field_info[2] if len(field_info) > 2 else ""

            label = Label(main_frame, text=label_text, font=LABEL_FONT, fg=TEXT_GRAY, anchor="w", bg=WHITE)
            label.pack(fill=X, pady=(8, 3))
            entry = self.create_entry(main_frame, show=show_char)
            entry.pack(fill=X, pady=(0, 3))

            if field_name == "org_code":
                entry.focus_set()
            self.reg_fields[field_name] = entry

        self.create_separator(main_frame)

        buttons_frame = Frame(main_frame, bg=WHITE)
        buttons_frame.pack(pady=(10, 5), fill=X)

        back_btn = Button(buttons_frame, text="Назад", font=BUTTON_FONT, bg=BUTTON_BG, fg=BUTTON_TEXT,
                         activebackground="#D4B8FF", activeforeground=BUTTON_TEXT, relief="solid", bd=2,
                         highlightbackground=BORDER_COLOR, highlightcolor=BORDER_COLOR, pady=10,
                         cursor="hand2", command=self.show_register_type_screen)
        back_btn.pack(side=LEFT, padx=(0, 10))

        continue_btn = Button(buttons_frame, text="Продолжить", font=BUTTON_FONT, bg=BUTTON_BG, fg=BUTTON_TEXT,
                             activebackground="#D4B8FF", activeforeground=BUTTON_TEXT, relief="solid", bd=2,
                             highlightbackground=BORDER_COLOR, highlightcolor=BORDER_COLOR, pady=10,
                             cursor="hand2", command=self.corporate_register_action)
        continue_btn.pack(side=RIGHT)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def corporate_register_action(self):
        org_code = self.reg_fields["org_code"].get().strip()
        surname = self.reg_fields["surname"].get().strip()
        name = self.reg_fields["name"].get().strip()
        patronymic = self.reg_fields["patronymic"].get().strip()
        position = self.reg_fields["position"].get().strip()
        department = self.reg_fields["department"].get().strip()
        email = self.reg_fields["email"].get().strip()
        login = self.reg_fields["login"].get().strip()
        password = self.reg_fields["password"].get()
        confirm = self.reg_fields["confirm_password"].get()

        if not all([org_code, surname, name, position, email, login, password, confirm]):
            messagebox.showwarning("Ошибка", "Все поля обязательны для заполнения")
            return

        if org_code not in self.organizations_data:
            messagebox.showerror("Ошибка", "Организация с таким кодом не найдена. Пожалуйста, зарегистрируйте организацию.")
            return

        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            messagebox.showwarning("Ошибка", "Введите корректный email")
            return

        if len(password) < 4:
            messagebox.showwarning("Ошибка", "Пароль должен содержать минимум 4 символа")
            return

        if password != confirm:
            messagebox.showerror("Ошибка", "Пароли не совпадают")
            return

        if login in self.users_data:
            messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует")
            return

        for user_data in self.users_data.values():
            if user_data.get("email") == email:
                messagebox.showerror("Ошибка", "Пользователь с таким email уже существует")
                return

        hashed_password = hashlib.md5(password.encode()).hexdigest()
        self.users_data[login] = {
            "password": hashed_password,
            "email": email,
            "account_type": "corporate",
            "org_code": org_code,
            "surname": surname,
            "name": name,
            "patronymic": patronymic,
            "position": position,
            "department": department,
            "created": datetime.now().isoformat()
        }
        self.save_users()

        if login not in self.categories_data:
            self.categories_data[login] = ["Без категории"]
            self.save_categories()

        messagebox.showinfo("Успех", "Регистрация выполнена успешно!")
        self.current_user = login
        self.show_main_app()

    # ============================================================
    # ЭКРАН 7: РЕГИСТРАЦИЯ ОРГАНИЗАЦИИ
    # ============================================================

    def show_organization_register(self):
        self.clear_window()
        self.title("Шифровалка - Регистрация организации")
        self.current_screen = "organization_register"
        self.configure(bg=BG_COLOR)

        main_container = Frame(self, bg=BG_COLOR)
        main_container.pack(fill=BOTH, expand=True)

        canvas = Canvas(main_container, bg=BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg=BG_COLOR)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        card = RoundedFrame(scrollable_frame, corner_radius=15, bg=WHITE, border_color=BORDER_COLOR, border_width=2)
        card.pack(fill=BOTH, expand=True, padx=40, pady=30)

        main_frame = card.inner_frame
        main_frame.configure(bg=WHITE)
        main_frame.pack(fill=BOTH, expand=True, padx=40, pady=20)

        title_label = Label(main_frame, text="Регистрация организации", font=TITLE_FONT, fg=TEXT_DARK, bg=WHITE)
        title_label.pack(pady=(20, 20))

        fields = [
            ("Сокращенное наименование организации", "short_name"),
            ("ИНН", "inn"),
            ("Адрес организации", "address"),
            ("ФИО директора организации", "director"),
            ("Основной вид деятельности организации", "activity"),
            ("Субъект МСП", "msp"),
        ]

        self.reg_fields = {}
        for label_text, field_name in fields:
            label = Label(main_frame, text=label_text, font=LABEL_FONT, fg=TEXT_GRAY, anchor="w", bg=WHITE)
            label.pack(fill=X, pady=(8, 3))
            entry = self.create_entry(main_frame)
            entry.pack(fill=X, pady=(0, 3))

            if field_name == "short_name":
                entry.focus_set()
            self.reg_fields[field_name] = entry

        self.confirm_var = IntVar()
        confirm_check = Checkbutton(main_frame,
                                    text="Подтвердите, что вы являетесь лицом, имеющим право действовать от имени организации",
                                    font=LABEL_FONT, bg=WHITE, fg=TEXT_DARK,
                                    variable=self.confirm_var, wraplength=350,
                                    justify="left", selectcolor=WHITE)
        confirm_check.pack(pady=(10, 10), anchor="w")

        def generate_code():
            short_name = self.reg_fields["short_name"].get().strip()
            if short_name:
                code = self.generate_organization_code(short_name)
                messagebox.showinfo("Код организации", f"Код организации: {code}\n\nСохраните этот код для регистрации корпоративных аккаунтов.")
            else:
                messagebox.showwarning("Ошибка", "Введите сокращенное наименование организации")

        gen_btn = Button(main_frame, text="Генерация личного кода организации", font=LABEL_FONT,
                        bg=BUTTON_BG, fg=BUTTON_TEXT, activebackground="#D4B8FF",
                        activeforeground=BUTTON_TEXT, relief="solid", bd=2,
                        highlightbackground=BORDER_COLOR, highlightcolor=BORDER_COLOR,
                        pady=8, cursor="hand2", command=generate_code)
        gen_btn.pack(pady=(5, 10), fill=X)

        self.create_separator(main_frame)

        buttons_frame = Frame(main_frame, bg=WHITE)
        buttons_frame.pack(pady=(10, 5), fill=X)

        back_btn = Button(buttons_frame, text="Назад", font=BUTTON_FONT, bg=BUTTON_BG, fg=BUTTON_TEXT,
                         activebackground="#D4B8FF", activeforeground=BUTTON_TEXT, relief="solid", bd=2,
                         highlightbackground=BORDER_COLOR, highlightcolor=BORDER_COLOR, pady=10,
                         cursor="hand2", command=self.show_register_type_screen)
        back_btn.pack(side=LEFT, padx=(0, 10))

        continue_btn = Button(buttons_frame, text="Продолжить", font=BUTTON_FONT, bg=BUTTON_BG, fg=BUTTON_TEXT,
                             activebackground="#D4B8FF", activeforeground=BUTTON_TEXT, relief="solid", bd=2,
                             highlightbackground=BORDER_COLOR, highlightcolor=BORDER_COLOR, pady=10,
                             cursor="hand2", command=self.organization_register_action)
        continue_btn.pack(side=RIGHT)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def organization_register_action(self):
        short_name = self.reg_fields["short_name"].get().strip()
        inn = self.reg_fields["inn"].get().strip()
        address = self.reg_fields["address"].get().strip()
        director = self.reg_fields["director"].get().strip()
        activity = self.reg_fields["activity"].get().strip()
        msp = self.reg_fields["msp"].get().strip()

        if not all([short_name, inn, address, director, activity, msp]):
            messagebox.showwarning("Ошибка", "Все поля обязательны для заполнения")
            return

        if not self.confirm_var.get():
            messagebox.showwarning("Ошибка", "Подтвердите, что вы имеете право действовать от имени организации")
            return

        if not inn.isdigit() or len(inn) < 10:
            messagebox.showwarning("Ошибка", "Введите корректный ИНН (только цифры, минимум 10 символов)")
            return

        for org_data in self.organizations_data.values():
            if org_data.get("inn") == inn:
                messagebox.showerror("Ошибка", "Организация с таким ИНН уже зарегистрирована")
                return

        org_code = self.generate_organization_code(short_name)
        while org_code in self.organizations_data:
            import random
            import string
            org_code = org_code[:4] + ''.join(random.choices(string.digits, k=4))

        self.organizations_data[org_code] = {
            "short_name": short_name,
            "inn": inn,
            "address": address,
            "director": director,
            "activity": activity,
            "msp": msp,
            "created": datetime.now().isoformat()
        }
        self.save_organizations()

        messagebox.showinfo("Успех", f"Организация зарегистрирована!\n\nКод организации: {org_code}\nСохраните этот код для регистрации корпоративных аккаунтов.")
        self.show_register_type_screen()

    # ============================================================
    # ГЛАВНОЕ МЕНЮ
    # ============================================================

    def show_main_app(self):
        """Открытие главного окна приложения"""
        self.clear_window()
        self.title("Шифровалка")
        self.geometry("880x580")
        self.resizable(False, False)
        self.configure(bg="#FFFFFF")
        self.center_window_for_main()
        
        self.selected_category = None
        self.filtered_passwords = []
        
        self.load_user_passwords()
        self.load_user_categories()
        
        self.create_main_widgets()

    def center_window_for_main(self):
        self.update_idletasks()
        width = 880
        height = 580
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def load_user_passwords(self):
        """Загрузка паролей текущего пользователя"""
        self.passwords = []
        self.favorites = []
        try:
            with open(".data", "r", encoding='utf-8') as f:
                all_data = json.load(f)
                for pwd_id, details in all_data.items():
                    if details.get('owner') == self.current_user:
                        password_info = {
                            'id': pwd_id,
                            'password': details.get('password', ''),
                            'alias': details.get('alias', 'Без названия'),
                            'site': details.get('site', ''),
                            'login': details.get('login', ''),
                            'category': details.get('category', 'Без категории'),
                            'favorite': details.get('favorite', False),
                            'notes': details.get('notes', ''),
                            'created': details.get('created', 0)
                        }
                        self.passwords.append(password_info)
                        if password_info['favorite']:
                            self.favorites.append(password_info)
        except (IOError, json.JSONDecodeError):
            pass
        
        self.passwords.sort(key=lambda x: x.get('created', 0), reverse=True)
        self.favorites.sort(key=lambda x: x.get('created', 0), reverse=True)
        self.update_filtered_passwords()

    def update_filtered_passwords(self):
        """Обновление списка отфильтрованных паролей"""
        if self.selected_category:
            self.filtered_passwords = [p for p in self.passwords if p.get('category') == self.selected_category]
        else:
            self.filtered_passwords = self.passwords.copy()

    def load_user_categories(self):
        """Загрузка категорий пользователя"""
        try:
            with open(CATEGORIES_FILE, "r", encoding='utf-8') as f:
                data = json.load(f)
                self.user_categories = data.get(self.current_user, ["Без категории"])
        except:
            self.user_categories = ["Без категории"]

    def create_main_widgets(self):
        # Главный контейнер
        main_container = Frame(self, bg="#FFFFFF")
        main_container.pack(fill=BOTH, expand=True, padx=15, pady=10)

        # ====== ВЕРХНЯЯ ПАНЕЛЬ ======
        top_panel = Frame(main_container, bg="#FFFFFF", height=50)
        top_panel.pack(fill=X, pady=(0, 10))
        top_panel.pack_propagate(False)

        # Левый верх - звездочка (избранное)
        self.fav_btn = Button(
            top_panel,
            text="☆",
            font=("Segoe UI", 24),
            bg="#FFFFFF",
            fg="#CCCCCC",
            relief="flat",
            cursor="hand2",
            command=self.show_favorites_window
        )
        self.fav_btn.pack(side=LEFT, padx=3)
        self.update_fav_button()

        # Центр - логотип
        logo_frame = Frame(top_panel, bg="#FFFFFF")
        logo_frame.pack(side=LEFT, expand=True)

        self.category_title = Label(
            logo_frame,
            text="🔒 Шифровалка",
            font=("Segoe UI", 18, "bold"),
            bg="#FFFFFF",
            fg="#5C0071"
        )
        self.category_title.pack()

        # Правый верх - шестеренка (настройки)
        settings_btn = Button(
            top_panel,
            text="⚙",
            font=("Segoe UI", 20),
            bg="#FFFFFF",
            fg="#CCCCCC",
            relief="flat",
            cursor="hand2",
            command=self.show_settings
        )
        settings_btn.pack(side=RIGHT, padx=3)

        # ====== ОСНОВНАЯ ОБЛАСТЬ ======
        content_frame = Frame(main_container, bg="#FFFFFF")
        content_frame.pack(fill=BOTH, expand=True)

        # ----- ЛЕВАЯ ЧАСТЬ -----
        left_panel = Frame(content_frame, bg="#FFFFFF", width=230)
        left_panel.pack(side=LEFT, fill=BOTH, padx=(0, 10))
        left_panel.pack_propagate(False)

        # Недавние/частые пароли
        recent_frame = Frame(left_panel, bg="#FFFFFF")
        recent_frame.pack(fill=X, pady=(0, 10))

        recent_title = Label(
            recent_frame,
            text="Недавние/частые",
            font=("Segoe UI", 11, "bold"),
            bg="#FFFFFF",
            fg="#333333"
        )
        recent_title.pack(anchor=W, pady=(0, 5))

        recent_tree_frame = Frame(recent_frame, bg="#FFFFFF")
        recent_tree_frame.pack(fill=X)

        # Стиль для таблиц
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            "Custom.Treeview",
            background="#FFFFFF",
            foreground="#333333",
            rowheight=25,
            font=("Segoe UI", 9),
            fieldbackground="#FFFFFF"
        )
        style.map('Custom.Treeview', background=[('selected', '#E4CCFF')])

        style.configure(
            "Custom.Treeview.Heading",
            font=("Segoe UI", 9, "bold"),
            background="#F5F0FF",
            foreground="#5C0071"
        )

        self.recent_tree = ttk.Treeview(
            recent_tree_frame,
            columns=("№", "Пароль"),
            show="headings",
            height=2,
            style="Custom.Treeview"
        )

        self.recent_tree.heading("№", text="№")
        self.recent_tree.heading("Пароль", text="Пароль")
        self.recent_tree.column("№", width=30, anchor="center")
        self.recent_tree.column("Пароль", width=170)

        self.update_recent_list()
        self.recent_tree.pack(fill=X)

        # Категории
        categories_frame = Frame(left_panel, bg="#FFFFFF")
        categories_frame.pack(fill=BOTH, expand=True)

        categories_title = Label(
            categories_frame,
            text="Категории",
            font=("Segoe UI", 11, "bold"),
            bg="#FFFFFF",
            fg="#333333"
        )
        categories_title.pack(anchor=W, pady=(0, 5))

        categories_container = Frame(categories_frame, bg="#FFFFFF")
        categories_container.pack(fill=BOTH, expand=True)

        cat_scrollbar = ttk.Scrollbar(categories_container)
        cat_scrollbar.pack(side=RIGHT, fill=Y)

        self.categories_tree = ttk.Treeview(
            categories_container,
            columns=("Категория", "Кол-во"),
            show="headings",
            height=6,
            yscrollcommand=cat_scrollbar.set,
            style="Custom.Treeview"
        )
        cat_scrollbar.config(command=self.categories_tree.yview)

        self.categories_tree.heading("Категория", text="Категория")
        self.categories_tree.heading("Кол-во", text="Кол-во")
        self.categories_tree.column("Категория", width=160)
        self.categories_tree.column("Кол-во", width=40, anchor="center")

        self.update_categories()

        self.categories_tree.bind("<ButtonRelease-1>", self.on_category_click)
        self.categories_tree.pack(side=LEFT, fill=BOTH, expand=True)

        # ----- ПРАВАЯ ЧАСТЬ (список паролей) -----
        right_panel = Frame(content_frame, bg="#F3E9FF")
        right_panel.pack(side=RIGHT, fill=BOTH, expand=True)

        # Заголовок с кнопкой "Все пароли"
        header_frame = Frame(right_panel, bg="#F3E9FF")
        header_frame.pack(fill=X, padx=10, pady=(8, 5))

        # Кнопка "Домой" (показывает все пароли)
        self.home_btn = Button(
            header_frame,
            text="🏠",
            font=("Segoe UI", 14),
            bg="#F3E9FF",
            fg="#5C0071",
            relief="flat",
            cursor="hand2",
            command=self.show_all_passwords
        )
        self.home_btn.pack(side=LEFT, padx=(0, 8))

        self.list_title = Label(
            header_frame,
            text="Все пароли",
            font=("Segoe UI", 12, "bold"),
            bg="#F3E9FF",
            fg="#333333"
        )
        self.list_title.pack(side=LEFT)

        self.clear_filter_btn = Button(
            header_frame,
            text="✕ Очистить фильтр",
            font=("Segoe UI", 9),
            bg="#F3E9FF",
            fg="#FF6B6B",
            relief="flat",
            cursor="hand2",
            command=self.show_all_passwords
        )
        self.clear_filter_btn.pack(side=RIGHT, padx=(8, 0))
        self.clear_filter_btn.pack_forget()

        list_container = Frame(right_panel, bg="#F3E9FF")
        list_container.pack(fill=BOTH, expand=True, padx=8, pady=(0, 8))

        list_scrollbar = ttk.Scrollbar(list_container)
        list_scrollbar.pack(side=RIGHT, fill=Y)

        self.passwords_tree = ttk.Treeview(
            list_container,
            columns=("№", "Пароль"),
            show="headings",
            height=10,
            yscrollcommand=list_scrollbar.set,
            style="Custom.Treeview"
        )
        list_scrollbar.config(command=self.passwords_tree.yview)

        self.passwords_tree.heading("№", text="№")
        self.passwords_tree.heading("Пароль", text="Пароль")
        self.passwords_tree.column("№", width=35, anchor="center")
        self.passwords_tree.column("Пароль", width=280)

        self.update_password_list()

        self.passwords_tree.pack(side=LEFT, fill=BOTH, expand=True)

        self.passwords_tree.bind("<Double-1>", self.on_password_double_click)
        self.recent_tree.bind("<Double-1>", self.on_password_double_click)

        # ====== НИЖНЯЯ ПАНЕЛЬ ======
        bottom_panel = Frame(main_container, bg="#FFFFFF", height=50)
        bottom_panel.pack(fill=X, pady=(10, 0))
        bottom_panel.pack_propagate(False)

        # Левый нижний - зеленый плюс (добавить)
        add_btn = Button(
            bottom_panel,
            text="＋",
            font=("Segoe UI", 22),
            bg="#4CAF50",
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            width=3,
            command=self.open_add_password_main
        )
        add_btn.pack(side=LEFT, padx=3)

        # Центр - кнопка организации
        org_btn = Button(
            bottom_panel,
            text="🏢",
            font=("Segoe UI", 20),
            bg="#E4CCFF",
            fg="#5C0071",
            relief="flat",
            cursor="hand2",
            width=3,
            command=self.open_organization_main
        )
        org_btn.pack(side=LEFT, padx=3, expand=True)

        # Правый нижний - молния (генерация)
        gen_btn = Button(
            bottom_panel,
            text="⚡",
            font=("Segoe UI", 20),
            bg="#FFD700",
            fg="#333333",
            relief="flat",
            cursor="hand2",
            width=3,
            command=self.open_generator_main
        )
        gen_btn.pack(side=RIGHT, padx=3)

        self.protocol("WM_DELETE_WINDOW", self.on_main_closing)

    def update_recent_list(self):
        """Обновление списка недавних паролей"""
        for item in self.recent_tree.get_children():
            self.recent_tree.delete(item)
        
        recent_items = self.filtered_passwords[:3] if self.filtered_passwords else []
        for idx, pwd in enumerate(recent_items, 1):
            display_name = pwd['alias'] if pwd['alias'] else pwd['site']
            if not display_name:
                display_name = "Без названия"
            self.recent_tree.insert("", "end", values=(idx, display_name))

    def update_fav_button(self):
        """Обновление кнопки избранного"""
        if self.favorites:
            self.fav_btn.config(text="★", fg=FAVORITE_COLOR)
        else:
            self.fav_btn.config(text="☆", fg="#CCCCCC")

    def update_categories(self):
        """Обновление списка категорий"""
        for item in self.categories_tree.get_children():
            self.categories_tree.delete(item)

        all_cat_count = len(self.passwords)
        tags = ()
        if self.selected_category is None:
            tags = ('selected',)
        self.categories_tree.insert("", "end", values=("📋 Все категории", all_cat_count), tags=tags)

        category_counts = {}
        for pwd in self.passwords:
            cat = pwd.get('category', 'Без категории')
            category_counts[cat] = category_counts.get(cat, 0) + 1

        for cat in self.user_categories:
            count = category_counts.get(cat, 0)
            tags = ()
            if self.selected_category == cat:
                tags = ('selected',)
            self.categories_tree.insert("", "end", values=(cat, count), tags=tags)

        self.categories_tree.tag_configure('selected', background=CATEGORY_SELECTED)

    def on_category_click(self, event):
        """Обработка клика по категории"""
        selected = self.categories_tree.selection()
        if not selected:
            return
        
        item = self.categories_tree.item(selected[0])
        category = item['values'][0]
        
        if category == "📋 Все категории":
            self.show_all_passwords()
        elif category:
            self.filter_by_category(category)

    def filter_by_category(self, category):
        """Фильтрация паролей по категории"""
        self.selected_category = category
        self.update_filtered_passwords()
        
        self.list_title.config(text=f"📂 {category}")
        self.clear_filter_btn.pack(side=RIGHT, padx=(8, 0))
        self.home_btn.config(text="🏠")
        
        self.update_password_list()
        self.update_recent_list()
        self.update_categories()

    def show_all_passwords(self):
        """Показ всех паролей (сброс фильтра)"""
        self.selected_category = None
        self.update_filtered_passwords()
        
        self.list_title.config(text="Все пароли")
        self.clear_filter_btn.pack_forget()
        self.home_btn.config(text="🏠")
        
        self.update_password_list()
        self.update_recent_list()
        self.update_categories()

    def update_password_list(self):
        """Обновление списка паролей"""
        for item in self.passwords_tree.get_children():
            self.passwords_tree.delete(item)
        
        passwords_to_show = self.filtered_passwords
        
        for idx, pwd in enumerate(passwords_to_show, 1):
            display_name = pwd['alias'] if pwd['alias'] else pwd['site']
            if not display_name:
                display_name = "Без названия"
            if pwd.get('favorite', False):
                display_name = "★ " + display_name
            self.passwords_tree.insert("", "end", values=(idx, display_name))

    def on_password_double_click(self, event):
        """Показ окна просмотра пароля"""
        tree = event.widget
        selected = tree.selection()
        if not selected:
            return

        item = tree.item(selected[0])
        idx = item['values'][0] - 1
        
        if 0 <= idx < len(self.filtered_passwords):
            pwd = self.filtered_passwords[idx]
            self.show_password_view(pwd)

    def show_favorites_window(self):
        """Открытие окна с избранными паролями"""
        if not self.favorites:
            messagebox.showinfo("Избранное", "Нет избранных паролей")
            return
        
        self.load_user_passwords()
        
        if not self.favorites:
            messagebox.showinfo("Избранное", "Нет избранных паролей")
            return
        
        favorites_window = FavoritesWindow(self, self.favorites)
        self.wait_window(favorites_window)
        self.refresh_main()

    # ============================================================
    # МЕТОДЫ ГЕНЕРАТОРА
    # ============================================================

    def open_generator_main(self):
        """Открытие генератора с главного экрана"""
        generator = GeneratorWindow(self, return_to_add=False)
        self.wait_window(generator)

    def open_generator_from_add(self, add_window):
        """Открытие генератора из окна добавления"""
        generator = GeneratorWindow(self, return_to_add=True, add_window=add_window)
        # Скрываем окно добавления
        add_window.withdraw()
        self.wait_window(generator)
        # После закрытия генератора показываем окно добавления
        add_window.deiconify()
        add_window.lift()

    def open_add_password_with_password(self, password):
        """Открытие окна добавления с предустановленным паролем"""
        try:
            add_window = Add.AddWindow(self, update_callback=self.refresh_main)
            # Если есть пароль, вставляем его
            if password:
                add_window.password_entry.delete(0, END)
                add_window.password_entry.insert(0, password)
            self.wait_window(add_window)
            self.refresh_main()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть окно: {e}")

    # ============================================================
    # МЕТОДЫ ПРОСМОТРА ПАРОЛЕЙ
    # ============================================================

    def show_password_view(self, pwd):
        """Окно просмотра и редактирования пароля"""
        view_window = Toplevel(self)
        view_window.title("Просмотр пароля")
        view_window.geometry("420x600")
        view_window.resizable(False, False)
        view_window.configure(bg="#FFFFFF")
        
        view_window.update_idletasks()
        x = (view_window.winfo_screenwidth() // 2) - (420 // 2)
        y = (view_window.winfo_screenheight() // 2) - (600 // 2)
        view_window.geometry(f'420x600+{x}+{y}')

        try:
            decoded_password = encode.decode(pwd['password'])
        except:
            decoded_password = "Ошибка декодирования"

        main_frame = Frame(view_window, bg="#FFFFFF", padx=25, pady=15)
        main_frame.pack(fill=BOTH, expand=True)

        # Верхняя панель с кнопками
        top_actions = Frame(main_frame, bg="#FFFFFF")
        top_actions.pack(fill=X, pady=(0, 10))

        close_btn = Button(
            top_actions,
            text="✕",
            font=("Segoe UI", 16),
            bg="#FFFFFF",
            fg="#CCCCCC",
            relief="flat",
            cursor="hand2",
            command=view_window.destroy
        )
        close_btn.pack(side=LEFT)

        fav_btn = Button(
            top_actions,
            text="★" if pwd.get('favorite', False) else "☆",
            font=("Segoe UI", 18),
            bg="#FFFFFF",
            fg=FAVORITE_COLOR if pwd.get('favorite', False) else "#CCCCCC",
            relief="flat",
            cursor="hand2",
            command=lambda: self.toggle_favorite(pwd, fav_btn, view_window)
        )
        fav_btn.pack(side=LEFT, padx=(15, 0))

        delete_btn = Button(
            top_actions,
            text="🗑",
            font=("Segoe UI", 16),
            bg="#FFFFFF",
            fg="#FF6B6B",
            relief="flat",
            cursor="hand2",
            command=lambda: self.delete_password(pwd, view_window)
        )
        delete_btn.pack(side=RIGHT)

        # Поля ввода
        Label(main_frame, text="Псевдоним", font=LABEL_FONT, bg="#FFFFFF", fg="#666666", anchor="w").pack(fill=X, pady=(0, 3))
        alias_entry = ttk.Entry(main_frame, font=FIELD_FONT)
        alias_entry.insert(0, pwd.get('alias', ''))
        alias_entry.pack(fill=X, pady=(0, 10))
        
        Label(main_frame, text="Сайт", font=LABEL_FONT, bg="#FFFFFF", fg="#666666", anchor="w").pack(fill=X, pady=(0, 3))
        site_entry = ttk.Entry(main_frame, font=FIELD_FONT)
        site_entry.insert(0, pwd.get('site', ''))
        site_entry.pack(fill=X, pady=(0, 10))
        
        # Логин с кнопкой копирования
        login_frame = Frame(main_frame, bg="#FFFFFF")
        login_frame.pack(fill=X, pady=(0, 10))
        
        Label(login_frame, text="Логин", font=LABEL_FONT, bg="#FFFFFF", fg="#666666", anchor="w").pack(fill=X, pady=(0, 3))
        login_inner = Frame(login_frame, bg="#FFFFFF")
        login_inner.pack(fill=X)
        
        login_entry = ttk.Entry(login_inner, font=FIELD_FONT)
        login_entry.insert(0, pwd.get('login', ''))
        login_entry.pack(side=LEFT, fill=X, expand=True)
        
        copy_login_btn = Button(
            login_inner,
            text="📋",
            font=("Segoe UI", 11),
            bg="#FFFFFF",
            fg="#666666",
            relief="flat",
            cursor="hand2",
            command=lambda: self.copy_to_clipboard(login_entry.get())
        )
        copy_login_btn.pack(side=RIGHT, padx=(5, 0))
        
        # Пароль с кнопкой копирования
        pwd_frame = Frame(main_frame, bg="#FFFFFF")
        pwd_frame.pack(fill=X, pady=(0, 10))
        
        Label(pwd_frame, text="Пароль", font=LABEL_FONT, bg="#FFFFFF", fg="#666666", anchor="w").pack(fill=X, pady=(0, 3))
        pwd_inner = Frame(pwd_frame, bg="#FFFFFF")
        pwd_inner.pack(fill=X)
        
        pwd_entry = ttk.Entry(pwd_inner, font=FIELD_FONT, show="*")
        pwd_entry.insert(0, decoded_password)
        pwd_entry.pack(side=LEFT, fill=X, expand=True)
        
        show_pwd = False
        def toggle_show():
            nonlocal show_pwd
            show_pwd = not show_pwd
            pwd_entry.config(show="" if show_pwd else "*")
            show_pwd_btn.config(text="👁" if show_pwd else "👁‍🗨")
        
        show_pwd_btn = Button(
            pwd_inner,
            text="👁‍🗨",
            font=("Segoe UI", 11),
            bg="#FFFFFF",
            fg="#666666",
            relief="flat",
            cursor="hand2",
            command=toggle_show
        )
        show_pwd_btn.pack(side=RIGHT, padx=(5, 0))
        
        copy_pwd_btn = Button(
            pwd_inner,
            text="📋",
            font=("Segoe UI", 11),
            bg="#FFFFFF",
            fg="#666666",
            relief="flat",
            cursor="hand2",
            command=lambda: self.copy_to_clipboard(pwd_entry.get())
        )
        copy_pwd_btn.pack(side=RIGHT, padx=(5, 0))
        
        # Категория
        Label(main_frame, text="Категория", font=LABEL_FONT, bg="#FFFFFF", fg="#666666", anchor="w").pack(fill=X, pady=(0, 3))
        
        self.load_user_categories()
        category_var = StringVar()
        category_var.set(pwd.get('category', 'Без категории'))
        
        category_combo = ttk.Combobox(
            main_frame,
            textvariable=category_var,
            values=self.user_categories,
            font=FIELD_FONT,
            state="readonly"
        )
        category_combo.pack(fill=X, pady=(0, 8))
        
        add_cat_frame = Frame(main_frame, bg="#FFFFFF")
        add_cat_frame.pack(fill=X, pady=(0, 10))
        
        add_cat_btn = Button(
            add_cat_frame,
            text="+ Добавить категорию",
            font=LABEL_FONT,
            bg="#E4CCFF",
            fg="#5C0071",
            relief="flat",
            cursor="hand2",
            command=lambda: self.add_category_from_view(category_combo)
        )
        add_cat_btn.pack(side=LEFT)
        
        # Примечания
        Label(main_frame, text="Примечания", font=LABEL_FONT, bg="#FFFFFF", fg="#666666", anchor="w").pack(fill=X, pady=(0, 3))
        notes_text = Text(main_frame, font=FIELD_FONT, height=2, wrap=WORD)
        notes_text.insert("1.0", pwd.get('notes', ''))
        notes_text.pack(fill=X, pady=(0, 10))
        
        # Кнопки
        btn_frame = Frame(main_frame, bg="#FFFFFF")
        btn_frame.pack(fill=X, pady=(5, 0))
        
        save_btn = Button(
            btn_frame,
            text="Сохранить изменения",
            font=BUTTON_FONT,
            bg="#4CAF50",
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=lambda: self.save_password_changes(
                pwd, alias_entry.get(), site_entry.get(),
                login_entry.get(), pwd_entry.get(),
                category_var.get(), notes_text.get("1.0", "end-1c"),
                view_window
            )
        )
        save_btn.pack(side=LEFT, padx=5, ipadx=10, ipady=6, expand=True)
        
        cancel_btn = Button(
            btn_frame,
            text="Отменить изменения",
            font=BUTTON_FONT,
            bg="#CCCCCC",
            fg="#333333",
            relief="flat",
            cursor="hand2",
            command=view_window.destroy
        )
        cancel_btn.pack(side=LEFT, padx=5, ipadx=10, ipady=6, expand=True)

    def add_category_from_view(self, category_combo):
        """Добавление категории из окна просмотра"""
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
        
        entry = ttk.Entry(main_frame, font=FIELD_FONT)
        entry.pack(fill=X, pady=(0, 15))
        entry.focus_set()
        
        def add():
            name = entry.get().strip()
            if name and name not in self.user_categories:
                self.user_categories.append(name)
                self.categories_data[self.current_user] = self.user_categories
                self.save_categories()
                category_combo['values'] = self.user_categories
                category_combo.set(name)
                self.refresh_main()
                dialog.destroy()
                messagebox.showinfo("Успех", f"Категория '{name}' добавлена")
            elif name in self.user_categories:
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

    def toggle_favorite(self, pwd, fav_btn, window):
        """Переключение избранного"""
        try:
            with open(".data", "r", encoding='utf-8') as f:
                data = json.load(f)
            
            if pwd['id'] in data:
                data[pwd['id']]['favorite'] = not data[pwd['id']].get('favorite', False)
                
                with open(".data", "w", encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                
                pwd['favorite'] = data[pwd['id']]['favorite']
                if pwd['favorite']:
                    fav_btn.config(text="★", fg=FAVORITE_COLOR)
                else:
                    fav_btn.config(text="☆", fg="#CCCCCC")
                
                self.refresh_main()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось изменить избранное: {e}")

    def delete_password(self, pwd, window):
        """Удаление пароля"""
        display_name = pwd.get('alias') if pwd.get('alias') else pwd.get('site', 'Без названия')
        if messagebox.askyesno("Подтверждение удаления", f"Вы уверены, что хотите удалить пароль '{display_name}'?"):
            try:
                with open(".data", "r", encoding='utf-8') as f:
                    data = json.load(f)
                
                if pwd['id'] in data:
                    del data[pwd['id']]
                    
                    with open(".data", "w", encoding='utf-8') as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)
                    
                    window.destroy()
                    self.refresh_main()
                    messagebox.showinfo("Успех", "Пароль удален")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить пароль: {e}")

    def save_password_changes(self, pwd, alias, site, login, password, category, notes, window):
        """Сохранение изменений пароля"""
        try:
            with open(".data", "r", encoding='utf-8') as f:
                data = json.load(f)
            
            if pwd['id'] in data:
                data[pwd['id']]['alias'] = alias
                data[pwd['id']]['site'] = site
                data[pwd['id']]['login'] = login
                data[pwd['id']]['password'] = encode.encode(password)
                data[pwd['id']]['category'] = category
                data[pwd['id']]['notes'] = notes
                
                with open(".data", "w", encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                
                window.destroy()
                self.refresh_main()
                messagebox.showinfo("Успех", "Изменения сохранены")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить изменения: {e}")

    def copy_to_clipboard(self, text):
        """Копирование в буфер обмена"""
        if pyperclip:
            try:
                pyperclip.copy(text)
                messagebox.showinfo("Успех", "Скопировано в буфер обмена")
                return
            except:
                pass
        
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()
        messagebox.showinfo("Успех", "Скопировано в буфер обмена")

    def show_settings(self):
        messagebox.showinfo("Настройки", "Функция в разработке")

    def open_add_password_main(self):
        try:
            add_window = Add.AddWindow(self, update_callback=self.refresh_main)
            self.wait_window(add_window)
            self.refresh_main()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть окно: {e}")

    def refresh_main(self):
        """Обновление главного окна"""
        self.load_user_passwords()
        self.update_filtered_passwords()
        self.update_password_list()
        self.update_recent_list()
        self.update_categories()
        self.update_fav_button()
        
        if self.selected_category:
            self.list_title.config(text=f"📂 {self.selected_category}")
            self.clear_filter_btn.pack(side=RIGHT, padx=(8, 0))
        else:
            self.list_title.config(text="Все пароли")
            self.clear_filter_btn.pack_forget()

    def open_organization_main(self):
        messagebox.showinfo("Организация", "Функция в разработке")

    def open_generator_main(self):
        """Открытие генератора с главного экрана"""
        generator = GeneratorWindow(self, return_to_add=False)
        self.wait_window(generator)

    def on_main_closing(self):
        """Закрытие главного окна - завершение приложения"""
        self.quit()

    # ============================================================
    # МЕТОДЫ ДЛЯ СТАРОГО МЕНЮ (сохранены для совместимости)
    # ============================================================

    def open_add_window(self):
        try:
            Add.AddWindow(self)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть окно: {e}")

    def open_list_window(self):
        try:
            List.ListWindow(self)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть окно: {e}")

    def open_search_window(self):
        try:
            Search.SearchWindow(self)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть окно: {e}")

    def logout(self):
        if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?"):
            self.current_user = None
            self.show_login_screen()

if __name__ == '__main__':
    new = Login()
    new.mainloop()
