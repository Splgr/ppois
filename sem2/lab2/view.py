"""
View component for Tournament Management System
Implements the user interface using tkinter
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from typing import List, Callable, Optional
from model import Tournament


class PaginationFrame(ttk.Frame):
    """Кнопочки внизу страницы чтобы листать"""
    
    def __init__(self, parent, on_page_change: Callable, on_page_size_change: Callable):
        super().__init__(parent)
        self.on_page_change = on_page_change
        self.on_page_size_change = on_page_size_change
        self.current_page = 1
        self.total_pages = 1
        self.page_size = 10
        self.total_records = 0
        
        self._create_widgets()
    
    def _create_widgets(self):
        ttk.Button(self, text="|◄", command=lambda: self.on_page_change(1)).pack(side=tk.LEFT, padx=2)
        ttk.Button(self, text="◄", command=self._prev_page).pack(side=tk.LEFT, padx=2)
        
        self.page_label = ttk.Label(self, text="Страница 1 из 1")
        self.page_label.pack(side=tk.LEFT, padx=10)
        
        ttk.Button(self, text="►", command=self._next_page).pack(side=tk.LEFT, padx=2)
        ttk.Button(self, text="►|", command=lambda: self.on_page_change(self.total_pages)).pack(side=tk.LEFT, padx=2)
        
        ttk.Label(self, text="Записей на странице:").pack(side=tk.LEFT, padx=(20, 5))
        self.page_size_var = tk.StringVar(value="10")
        page_size_combo = ttk.Combobox(self, textvariable=self.page_size_var, 
                                        values=["5", "10", "20", "50", "100"], width=5)
        page_size_combo.pack(side=tk.LEFT, padx=2)
        page_size_combo.bind('<<ComboboxSelected>>', self._on_page_size_change)
        
        self.total_label = ttk.Label(self, text="Всего: 0")
        self.total_label.pack(side=tk.LEFT, padx=20)
    
    def _prev_page(self):
        if self.current_page > 1:
            self.on_page_change(self.current_page - 1)
    
    def _next_page(self):
        if self.current_page < self.total_pages:
            self.on_page_change(self.current_page + 1)
    
    def _on_page_size_change(self, event):
        try:
            new_size = int(self.page_size_var.get())
            self.on_page_size_change(new_size)
        except ValueError:
            pass
    
    def update_info(self, current_page: int, total_pages: int, total_records: int):
        self.current_page = current_page
        self.total_pages = total_pages if total_pages > 0 else 1
        self.total_records = total_records
        
        self.page_label.config(text=f"Страница {self.current_page} из {self.total_pages}")
        self.total_label.config(text=f"Всего: {self.total_records}")


class TournamentTableFrame(ttk.Frame):
    """Tournament table display widget"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self._create_widgets()
    
    def _create_widgets(self):
        columns = ('id', 'name', 'date', 'sport', 'winner', 'prize', 'earnings')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=15)
        
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='Название турнира')
        self.tree.heading('date', text='Дата проведения')
        self.tree.heading('sport', text='Вид спорта')
        self.tree.heading('winner', text='ФИО победителя')
        self.tree.heading('prize', text='Призовые (₽)')
        self.tree.heading('earnings', text='Заработок победителя (₽)')
        
        # ИСПРАВЛЕНО: используем строки 'center', 'e', 'w'
        self.tree.column('id', width=50, anchor='center')
        self.tree.column('name', width=200, anchor='w')
        self.tree.column('date', width=100, anchor='center')
        self.tree.column('sport', width=120, anchor='w')
        self.tree.column('winner', width=180, anchor='w')
        self.tree.column('prize', width=120, anchor='e')
        self.tree.column('earnings', width=140, anchor='e')
        
        vsb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def populate(self, tournaments: List[Tournament]):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for tour in tournaments:
            self.tree.insert('', tk.END, values=(
                tour.id,
                tour.name,
                tour.date.strftime('%d.%m.%Y') if isinstance(tour.date, datetime) else tour.date,
                tour.sport,
                tour.winner_name,
                f"{tour.prize_pool:,.2f}",
                f"{tour.winner_earnings:,.2f}"
            ))
    
    def get_selected_id(self) -> Optional[int]:
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            return item['values'][0]
        return None


class TournamentTreeView(ttk.Frame):
    """Tree view alternative display"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self._create_widgets()
    
    def _create_widgets(self):
        self.tree = ttk.Treeview(self, height=15)
        self.tree.heading('#0', text='Турниры')
        
        vsb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def populate(self, tournaments: List[Tournament]):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        sports = {}
        for tour in tournaments:
            if tour.sport not in sports:
                sports[tour.sport] = []
            sports[tour.sport].append(tour)
        
        for sport, tours in sports.items():
            sport_node = self.tree.insert('', tk.END, text=f"🏆 {sport}", open=True)
            for tour in tours:
                tour_node = self.tree.insert(sport_node, tk.END, 
                    text=f"📅 {tour.date.strftime('%d.%m.%Y') if isinstance(tour.date, datetime) else tour.date} - {tour.name}")
                
                self.tree.insert(tour_node, tk.END, text=f"👤 Победитель: {tour.winner_name}")
                self.tree.insert(tour_node, tk.END, text=f"💰 Призовые: {tour.prize_pool:,.2f} ₽")
                self.tree.insert(tour_node, tk.END, text=f"🏅 Заработок: {tour.winner_earnings:,.2f} ₽")


class TournamentView:
    """Main View class for the application"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Система управления турнирами")
        self.root.geometry("1200x700")
        
        self.current_view = 'table'
        self.controller = None  # Будет установлен позже
        
        self._create_menu()
        self._create_toolbar()
        self._create_main_area()
        self._create_status_bar()
    
    def _create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Сохранить в XML", command=self._on_save_xml)
        file_menu.add_command(label="Загрузить из XML", command=self._on_load_xml)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Редактирование", menu=edit_menu)
        edit_menu.add_command(label="Добавить турнир", command=self._on_add_tournament)
        edit_menu.add_command(label="Редактировать турнир", command=self._on_edit_tournament)
        edit_menu.add_command(label="Удалить турнир", command=self._on_delete_tournament)
        
        search_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Поиск", menu=search_menu)
        search_menu.add_command(label="Поиск турниров", command=self._on_search_tournaments)
        
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Вид", menu=view_menu)
        view_menu.add_command(label="Таблица", command=self._on_show_table)
        view_menu.add_command(label="Дерево", command=self._on_show_tree)
        view_menu.add_separator()
        view_menu.add_command(label="Обновить", command=self._on_refresh)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self._on_about)
    
    def _create_toolbar(self):
        """Create toolbar with buttons"""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # ИСПРАВЛЕНО: используем _on_* методы которые проверяют controller
        ttk.Button(toolbar, text="➕ Добавить", command=self._on_add_tournament).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="✏️ Редактировать", command=self._on_edit_tournament).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🗑️ Удалить", command=self._on_delete_tournament).pack(side=tk.LEFT, padx=2)
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=10, fill=tk.Y)
        ttk.Button(toolbar, text="🔍 Поиск", command=self._on_search_tournaments).pack(side=tk.LEFT, padx=2)
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=10, fill=tk.Y)
        ttk.Button(toolbar, text="💾 Сохранить XML", command=self._on_save_xml).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="📂 Загрузить XML", command=self._on_load_xml).pack(side=tk.LEFT, padx=2)
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=10, fill=tk.Y)
        ttk.Button(toolbar, text="📊 Таблица", command=self._on_show_table).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🌳 Дерево", command=self._on_show_tree).pack(side=tk.LEFT, padx=2)
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=10, fill=tk.Y)
        ttk.Button(toolbar, text="🔄 Обновить", command=self._on_refresh).pack(side=tk.LEFT, padx=2)
    
    def _create_main_area(self):
        """Create main content area"""
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.table_frame = TournamentTableFrame(self.main_frame)
        self.tree_frame = TournamentTreeView(self.main_frame)
        
        self.pagination = PaginationFrame(
            self.main_frame,
            on_page_change=self._on_page_change,
            on_page_size_change=self._on_page_size_change
        )
        
        self.table_frame.pack(fill=tk.BOTH, expand=True)
        self.pagination.pack(fill=tk.X, pady=5)
    
    def _create_status_bar(self):
        """Create status bar"""
        self.status_var = tk.StringVar(value="Готово")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    # ============ Внутренние обработчики (всегда вызывают controller) ============
    
    def _on_add_tournament(self):
        if self.controller:
            self.controller.on_add_tournament()
    
    def _on_edit_tournament(self):
        if self.controller:
            self.controller.on_edit_tournament()
    
    def _on_delete_tournament(self):
        if self.controller:
            self.controller.on_delete_tournament()
    
    def _on_search_tournaments(self):
        if self.controller:
            self.controller.on_search_tournaments()
    
    def _on_save_xml(self):
        if self.controller:
            self.controller.on_save_xml()
    
    def _on_load_xml(self):
        if self.controller:
            self.controller.on_load_xml()
    
    def _on_show_table(self):
        if self.controller:
            self.controller.on_show_table()
    
    def _on_show_tree(self):
        if self.controller:
            self.controller.on_show_tree()
    
    def _on_refresh(self):
        if self.controller:
            self.controller.on_refresh()
    
    def _on_page_change(self, page: int):
        if self.controller:
            self.controller.on_page_change(page)
    
    def _on_page_size_change(self, size: int):
        if self.controller:
            self.controller.on_page_size_change(size)
    
    def _on_about(self):
        messagebox.showinfo("О программе", 
            "Система управления турнирами\nВерсия 1.0\n\nИспользует шаблон MVC\nБаза данных: SQLite")
    
    # ============ Methods for Controller ============
    
    def set_controller(self, controller):
        """Set controller reference"""
        self.controller = controller
        print(f"✅ Контроллер установлен: {controller}")
    
    def display_tournaments(self, tournaments: List[Tournament]):
        if self.current_view == 'table':
            self.table_frame.populate(tournaments)
        else:
            self.tree_frame.populate(tournaments)
    
    def update_pagination(self, current_page: int, total_pages: int, total_records: int):
        self.pagination.update_info(current_page, total_pages, total_records)
    
    def show_table_view(self):
        self.current_view = 'table'
        self.tree_frame.pack_forget()
        self.pagination.pack_forget()
        self.table_frame.pack(fill=tk.BOTH, expand=True)
        self.pagination.pack(fill=tk.X, pady=5)
    
    def show_tree_view(self):
        self.current_view = 'tree'
        self.table_frame.pack_forget()
        self.pagination.pack_forget()
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
    
    def show_message(self, message: str, title: str = "Информация"):
        messagebox.showinfo(title, message)
    
    def show_error(self, message: str, title: str = "Ошибка"):
        messagebox.showerror(title, message)
    
    def show_warning(self, message: str, title: str = "Предупреждение"):
        messagebox.showwarning(title, message)
    
    def ask_yes_no(self, message: str, title: str = "Подтверждение") -> bool:
        return messagebox.askyesno(title, message)
    
    def get_save_filename(self) -> Optional[str]:
        return filedialog.asksaveasfilename(
            defaultextension=".xml",
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")],
            title="Сохранить в файл"
        )
    
    def get_load_filename(self) -> Optional[str]:
        return filedialog.askopenfilename(
            defaultextension=".xml",
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")],
            title="Загрузить из файла"
        )
    
    def set_status(self, message: str):
        self.status_var.set(message)