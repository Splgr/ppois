"""
Dialog windows for Tournament Management System
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from typing import List
import os


def get_db_path():
    """Get absolute path to database file"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "tournaments.db")
    return db_path


try:
    from tkcalendar import Calendar
    HAS_CALENDAR = True
    print("✅ tkcalendar загружен")
except ImportError:
    HAS_CALENDAR = False
    print("⚠️ tkcalendar не найден (будет использоваться ручной ввод даты)")


class AddTournamentDialog:
    """Dialog for adding new tournament"""
    
    def __init__(self, parent, sports_list: List[str]):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Добавить турнир")
        self.dialog.geometry("500x450")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.dialog.lift()
        self.dialog.focus_force()
        self.dialog.attributes('-topmost', True)
        self.dialog.after(100, lambda: self.dialog.attributes('-topmost', False))
        
        self.sports_list = sports_list
        self._create_widgets()
        
        print("📋 Диалог добавления открыт")
        self.dialog.wait_window()
        print("📋 Диалог добавления закрыт")
    
    def _create_widgets(self):
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Название турнира:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(main_frame, width=40)
        self.name_entry.grid(row=0, column=1, pady=5, padx=10)
        
        ttk.Label(main_frame, text="Дата проведения (ГГГГ-ММ-ДД):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.date_entry = ttk.Entry(main_frame, width=20)
        self.date_entry.grid(row=1, column=1, sticky=tk.W, pady=5, padx=10)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        if HAS_CALENDAR:
            ttk.Button(main_frame, text="📅 Календарь", command=self._select_date).grid(row=1, column=2, pady=5)
        
        ttk.Label(main_frame, text="Вид спорта:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.sport_var = tk.StringVar()
        self.sport_combo = ttk.Combobox(main_frame, textvariable=self.sport_var, 
                                         values=self.sports_list, width=37, state='readonly')
        self.sport_combo.grid(row=2, column=1, sticky=tk.W, pady=5, padx=10)
        if self.sports_list:
            self.sport_combo.current(0)
        
        ttk.Label(main_frame, text="ФИО победителя:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.winner_entry = ttk.Entry(main_frame, width=40)
        self.winner_entry.grid(row=3, column=1, pady=5, padx=10)
        
        ttk.Label(main_frame, text="Размер призовых (₽):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.prize_entry = ttk.Entry(main_frame, width=20)
        self.prize_entry.grid(row=4, column=1, sticky=tk.W, pady=5, padx=10)
        self.prize_entry.bind('<KeyRelease>', self._update_earnings)
        
        ttk.Label(main_frame, text="Заработок победителя (60%):").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.earnings_var = tk.StringVar(value="0.00")
        self.earnings_label = ttk.Label(main_frame, textvariable=self.earnings_var, width=20)
        self.earnings_label.grid(row=5, column=1, sticky=tk.W, pady=5, padx=10)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=6, column=0, columnspan=3, pady=20)
        
        ttk.Button(btn_frame, text="Сохранить", command=self._save).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Отмена", command=self.dialog.destroy).pack(side=tk.LEFT, padx=10)
    
    def _select_date(self):
        if not HAS_CALENDAR:
            messagebox.showwarning("Календарь", "Модуль tkcalendar не установлен.\nВведите дату вручную в формате ГГГГ-ММ-ДД")
            return
            
        def on_date_select():
            selected_date = cal.get_date()
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, selected_date)
            cal_dialog.destroy()
        
        cal_dialog = tk.Toplevel(self.dialog)
        cal_dialog.title("Выберите дату")
        cal_dialog.transient(self.dialog)
        cal_dialog.lift()
        
        cal = Calendar(cal_dialog, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack(padx=20, pady=20)
        
        ttk.Button(cal_dialog, text="OK", command=on_date_select).pack(pady=10)
    
    def _update_earnings(self, event=None):
        try:
            prize = float(self.prize_entry.get().replace(',', '.').replace(' ', ''))
            earnings = prize * 0.6
            self.earnings_var.set(f"{earnings:,.2f}")
        except ValueError:
            self.earnings_var.set("0.00")
    
    def _save(self):
        try:
            name = self.name_entry.get().strip()
            if not name:
                messagebox.showwarning("Ошибка", "Введите название турнира", parent=self.dialog)
                return
            
            date_str = self.date_entry.get().strip()
            date = datetime.strptime(date_str, '%Y-%m-%d')
            
            sport = self.sport_var.get().strip()
            if not sport:
                messagebox.showwarning("Ошибка", "Выберите вид спорта", parent=self.dialog)
                return
            
            winner_name = self.winner_entry.get().strip()
            if not winner_name:
                messagebox.showwarning("Ошибка", "Введите ФИО победителя", parent=self.dialog)
                return
            
            prize_pool = float(self.prize_entry.get().replace(',', '.').replace(' ', ''))
            if prize_pool <= 0:
                messagebox.showwarning("Ошибка", "Призовые должны быть больше 0", parent=self.dialog)
                return
            
            self.result = {
                'name': name,
                'date': date,
                'sport': sport,
                'winner_name': winner_name,
                'prize_pool': prize_pool
            }
            
            print(f"✅ Данные сохранены: {name}")
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Неверный формат данных: {e}", parent=self.dialog)


class EditTournamentDialog:
    """Dialog for editing tournament"""
    
    def __init__(self, parent, tournament, sports_list: List[str]):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Редактировать турнир")
        self.dialog.geometry("500x450")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.dialog.lift()
        self.dialog.focus_force()
        self.dialog.attributes('-topmost', True)
        self.dialog.after(100, lambda: self.dialog.attributes('-topmost', False))
        
        self.tournament = tournament
        self.sports_list = sports_list
        self._create_widgets()
        
        print("📋 Диалог редактирования открыт")
        self.dialog.wait_window()
        print("📋 Диалог редактирования закрыт")
    
    def _create_widgets(self):
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Название турнира:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(main_frame, width=40)
        self.name_entry.grid(row=0, column=1, pady=5, padx=10)
        self.name_entry.insert(0, self.tournament.name)
        
        ttk.Label(main_frame, text="Дата проведения (ГГГГ-ММ-ДД):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.date_entry = ttk.Entry(main_frame, width=20)
        self.date_entry.grid(row=1, column=1, sticky=tk.W, pady=5, padx=10)
        date_str = self.tournament.date.strftime('%Y-%m-%d') if isinstance(self.tournament.date, datetime) else self.tournament.date
        self.date_entry.insert(0, date_str)
        
        if HAS_CALENDAR:
            ttk.Button(main_frame, text="📅 Календарь", command=self._select_date).grid(row=1, column=2, pady=5)
        
        ttk.Label(main_frame, text="Вид спорта:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.sport_var = tk.StringVar(value=self.tournament.sport)
        self.sport_combo = ttk.Combobox(main_frame, textvariable=self.sport_var, 
                                         values=self.sports_list, width=37, state='readonly')
        self.sport_combo.grid(row=2, column=1, sticky=tk.W, pady=5, padx=10)
        
        ttk.Label(main_frame, text="ФИО победителя:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.winner_entry = ttk.Entry(main_frame, width=40)
        self.winner_entry.grid(row=3, column=1, pady=5, padx=10)
        self.winner_entry.insert(0, self.tournament.winner_name)
        
        ttk.Label(main_frame, text="Размер призовых (₽):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.prize_entry = ttk.Entry(main_frame, width=20)
        self.prize_entry.grid(row=4, column=1, sticky=tk.W, pady=5, padx=10)
        self.prize_entry.insert(0, str(self.tournament.prize_pool))
        self.prize_entry.bind('<KeyRelease>', self._update_earnings)
        
        ttk.Label(main_frame, text="Заработок победителя (60%):").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.earnings_var = tk.StringVar(value=f"{self.tournament.winner_earnings:,.2f}")
        self.earnings_label = ttk.Label(main_frame, textvariable=self.earnings_var, width=20)
        self.earnings_label.grid(row=5, column=1, sticky=tk.W, pady=5, padx=10)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=6, column=0, columnspan=3, pady=20)
        
        ttk.Button(btn_frame, text="Сохранить", command=self._save).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Отмена", command=self.dialog.destroy).pack(side=tk.LEFT, padx=10)
    
    def _select_date(self):
        if not HAS_CALENDAR:
            messagebox.showwarning("Календарь", "Модуль tkcalendar не установлен.", parent=self.dialog)
            return

        def on_date_select():
            selected_date = cal.get_date()
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, selected_date)
            cal_dialog.destroy()
        
        cal_dialog = tk.Toplevel(self.dialog)
        cal_dialog.title("Выберите дату")
        cal_dialog.transient(self.dialog)
        cal_dialog.lift()
        
        cal = Calendar(cal_dialog, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack(padx=20, pady=20)
        
        ttk.Button(cal_dialog, text="OK", command=on_date_select).pack(pady=10)
    
    def _update_earnings(self, event=None):
        try:
            prize = float(self.prize_entry.get().replace(',', '.').replace(' ', ''))
            earnings = prize * 0.6
            self.earnings_var.set(f"{earnings:,.2f}")
        except ValueError:
            self.earnings_var.set("0.00")
    
    def _save(self):
        try:
            name = self.name_entry.get().strip()
            if not name:
                messagebox.showwarning("Ошибка", "Введите название турнира", parent=self.dialog)
                return
            
            date_str = self.date_entry.get().strip()
            date = datetime.strptime(date_str, '%Y-%m-%d')
            
            sport = self.sport_var.get().strip()
            if not sport:
                messagebox.showwarning("Ошибка", "Выберите вид спорта", parent=self.dialog)
                return
            
            winner_name = self.winner_entry.get().strip()
            if not winner_name:
                messagebox.showwarning("Ошибка", "Введите ФИО победителя", parent=self.dialog)
                return
            
            prize_pool = float(self.prize_entry.get().replace(',', '.').replace(' ', ''))
            if prize_pool <= 0:
                messagebox.showwarning("Ошибка", "Призовые должны быть больше 0", parent=self.dialog)
                return
            
            self.result = {
                'name': name,
                'date': date,
                'sport': sport,
                'winner_name': winner_name,
                'prize_pool': prize_pool
            }
            
            print(f"✅ Данные обновлены: {name}")
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Неверный формат данных: {e}", parent=self.dialog)


class SearchDialog:
    """Dialog for searching tournaments"""
    
    def __init__(self, parent, sports_list: List[str]):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Поиск турниров")
        self.dialog.geometry("600x550")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.dialog.lift()
        self.dialog.focus_force()
        
        self.sports_list = sports_list
        self._create_widgets()
        
        print("🔍 Диалог поиска открыт")
        self.dialog.wait_window()
        print("🔍 Диалог поиска закрыт")
    
    def _create_widgets(self):
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        group1 = ttk.LabelFrame(main_frame, text="Название или дата", padding=10)
        group1.grid(row=0, column=0, columnspan=2, sticky=tk.EW, pady=5)
        
        self.name_or_date_entry = ttk.Entry(group1, width=50)
        self.name_or_date_entry.pack(fill=tk.X)
        
        group2 = ttk.LabelFrame(main_frame, text="Вид спорта или победитель", padding=10)
        group2.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=5)
        
        ttk.Label(group2, text="Вид спорта:").pack(anchor=tk.W)
        self.sport_var = tk.StringVar()
        self.sport_combo = ttk.Combobox(group2, textvariable=self.sport_var, 
                                         values=self.sports_list, width=47, state='readonly')
        self.sport_combo.pack(fill=tk.X, pady=5)
        
        ttk.Label(group2, text="ФИО победителя (можно частично):").pack(anchor=tk.W)
        self.winner_entry = ttk.Entry(group2, width=50)
        self.winner_entry.pack(fill=tk.X)
        
        group3 = ttk.LabelFrame(main_frame, text="Размер призовых (₽)", padding=10)
        group3.grid(row=2, column=0, sticky=tk.EW, pady=5)
        
        prize_frame = ttk.Frame(group3)
        prize_frame.pack(fill=tk.X)
        
        ttk.Label(prize_frame, text="От:").pack(side=tk.LEFT)
        self.prize_min_entry = ttk.Entry(prize_frame, width=15)
        self.prize_min_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(prize_frame, text="До:").pack(side=tk.LEFT, padx=(20, 0))
        self.prize_max_entry = ttk.Entry(prize_frame, width=15)
        self.prize_max_entry.pack(side=tk.LEFT, padx=5)
        
        group4 = ttk.LabelFrame(main_frame, text="Заработок победителя (₽)", padding=10)
        group4.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        
        earnings_frame = ttk.Frame(group4)
        earnings_frame.pack(fill=tk.X)
        
        ttk.Label(earnings_frame, text="От:").pack(side=tk.LEFT)
        self.earnings_min_entry = ttk.Entry(earnings_frame, width=15)
        self.earnings_min_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(earnings_frame, text="До:").pack(side=tk.LEFT, padx=(20, 0))
        self.earnings_max_entry = ttk.Entry(earnings_frame, width=15)
        self.earnings_max_entry.pack(side=tk.LEFT, padx=5)
        
        results_frame = ttk.LabelFrame(main_frame, text="Результаты поиска", padding=10)
        results_frame.grid(row=3, column=0, columnspan=2, sticky=tk.NSEW, pady=10)
        
        self.results_text = tk.Text(results_frame, height=8, width=70)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        main_frame.grid_rowconfigure(3, weight=1)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="🔍 Найти", command=self._search).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="ОК", command=self._ok).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Отмена", command=self.dialog.destroy).pack(side=tk.LEFT, padx=10)
    
    def _search(self):
        criteria = self._get_criteria()
        
        from model import TournamentModel
        from database import Database
        
        db = Database(get_db_path())
        model = TournamentModel(db)
        results = model.search_tournaments(criteria)
        db.close()
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Найдено записей: {len(results)}\n\n")
        
        if results:
            for i, tour in enumerate(results[:20], 1):
                date_str = tour.date.strftime('%d.%m.%Y') if isinstance(tour.date, datetime) else tour.date
                self.results_text.insert(tk.END, 
                    f"{i}. {tour.name} | {date_str} | {tour.sport}\n"
                    f"   Победитель: {tour.winner_name} | Призовые: {tour.prize_pool:,.2f} ₽\n\n"
                )
            
            if len(results) > 20:
                self.results_text.insert(tk.END, f"... и ещё {len(results) - 20} записей")
        else:
            self.results_text.insert(tk.END, "Записи не найдены")
    
    def _get_criteria(self) -> dict:
        criteria = {}
        
        name_or_date = self.name_or_date_entry.get().strip()
        if name_or_date:
            converted_date = None
            
            if name_or_date.count('.') == 2:
                try:
                    parsed_date = datetime.strptime(name_or_date, '%d.%m.%Y')
                    converted_date = parsed_date.strftime('%Y-%m-%d')
                except ValueError:
                    pass
            
            elif name_or_date.count('/') == 2:
                try:
                    parsed_date = datetime.strptime(name_or_date, '%d/%m/%Y')
                    converted_date = parsed_date.strftime('%Y-%m-%d')
                except ValueError:
                    pass
            
            criteria['name_or_date'] = converted_date if converted_date else name_or_date
        
        sport = self.sport_var.get().strip()
        if sport:
            criteria['sport'] = sport
        
        winner_name = self.winner_entry.get().strip()
        if winner_name:
            criteria['winner_name'] = winner_name
        
        try:
            prize_min = self.prize_min_entry.get().strip()
            if prize_min:
                criteria['prize_min'] = float(prize_min.replace(',', '.'))
            
            prize_max = self.prize_max_entry.get().strip()
            if prize_max:
                criteria['prize_max'] = float(prize_max.replace(',', '.'))
        except ValueError:
            pass
        
        try:
            earnings_min = self.earnings_min_entry.get().strip()
            if earnings_min:
                criteria['earnings_min'] = float(earnings_min.replace(',', '.'))
            
            earnings_max = self.earnings_max_entry.get().strip()
            if earnings_max:
                criteria['earnings_max'] = float(earnings_max.replace(',', '.'))
        except ValueError:
            pass
        
        return criteria
    
    def _ok(self):
        """Save criteria and close dialog"""
        self.result = self._get_criteria()
        self.dialog.destroy()


class DeleteDialog:
    """Dialog for deleting tournaments by criteria"""
    
    def __init__(self, parent, sports_list: List[str]):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Удаление турниров")
        self.dialog.geometry("750x800")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.dialog.lift()
        self.dialog.focus_force()
        
        self.sports_list = sports_list
        self._create_widgets()
        
        print("🗑️ Диалог удаления открыт")
        self.dialog.wait_window()
        print("🗑️ Диалог удаления закрыт")
    
    def _create_widgets(self):
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        warning_label = ttk.Label(main_frame, 
            text="⚠️ Внимание! Удаление необратимо!",
            foreground='red',
            font=('Arial', 10, 'bold'))
        warning_label.pack(pady=(0, 10))
        
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        group1 = ttk.LabelFrame(input_frame, text="Название или дата", padding=10)
        group1.pack(fill=tk.X, pady=5)
        
        self.name_or_date_entry = ttk.Entry(group1, width=50)
        self.name_or_date_entry.pack(fill=tk.X)
        
        hint_label = ttk.Label(group1, 
            text="💡 Формат даты: ГГГГ-ММ-ДД (2025-06-15) или ДД.ММ.ГГГГ (15.06.2025)",
            font=('Arial', 8),
            foreground='gray')
        hint_label.pack(anchor=tk.W, pady=(5, 0))
        
        group2 = ttk.LabelFrame(input_frame, text="Вид спорта или победитель", padding=10)
        group2.pack(fill=tk.X, pady=5)
        
        ttk.Label(group2, text="Вид спорта:").pack(anchor=tk.W)
        self.sport_var = tk.StringVar()
        self.sport_combo = ttk.Combobox(group2, textvariable=self.sport_var, 
                                         values=self.sports_list, width=47, state='readonly')
        self.sport_combo.pack(fill=tk.X, pady=5)
        
        ttk.Label(group2, text="ФИО победителя:").pack(anchor=tk.W)
        self.winner_entry = ttk.Entry(group2, width=50)
        self.winner_entry.pack(fill=tk.X)
        
        group3 = ttk.LabelFrame(input_frame, text="Размер призовых (₽)", padding=10)
        group3.pack(fill=tk.X, pady=5)
        
        prize_frame = ttk.Frame(group3)
        prize_frame.pack(fill=tk.X)
        
        ttk.Label(prize_frame, text="От:").pack(side=tk.LEFT)
        self.prize_min_entry = ttk.Entry(prize_frame, width=15)
        self.prize_min_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(prize_frame, text="До:").pack(side=tk.LEFT, padx=(20, 0))
        self.prize_max_entry = ttk.Entry(prize_frame, width=15)
        self.prize_max_entry.pack(side=tk.LEFT, padx=5)
        
        group4 = ttk.LabelFrame(input_frame, text="Заработок победителя (₽)", padding=10)
        group4.pack(fill=tk.X, pady=5)
        
        earnings_frame = ttk.Frame(group4)
        earnings_frame.pack(fill=tk.X)
        
        ttk.Label(earnings_frame, text="От:").pack(side=tk.LEFT)
        self.earnings_min_entry = ttk.Entry(earnings_frame, width=15)
        self.earnings_min_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(earnings_frame, text="До:").pack(side=tk.LEFT, padx=(20, 0))
        self.earnings_max_entry = ttk.Entry(earnings_frame, width=15)
        self.earnings_max_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(main_frame, text="👁️ Предварительный просмотр", 
                   command=self._preview).pack(pady=10)
        
        self.preview_text = tk.Text(main_frame, height=4, width=70)
        self.preview_text.pack(fill=tk.X, pady=10)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="🗑️ Удалить", command=self._delete, 
                   width=15).pack(side=tk.LEFT, padx=20)
        ttk.Button(btn_frame, text="Отмена", command=self.dialog.destroy, 
                   width=15).pack(side=tk.LEFT, padx=20)
    
    def _get_criteria(self) -> dict:
        criteria = {}
        
        name_or_date = self.name_or_date_entry.get().strip()
        if name_or_date:
            converted_date = None
            
            if name_or_date.count('.') == 2:
                try:
                    parsed_date = datetime.strptime(name_or_date, '%d.%m.%Y')
                    converted_date = parsed_date.strftime('%Y-%m-%d')
                except ValueError:
                    pass
            
            elif name_or_date.count('/') == 2:
                try:
                    parsed_date = datetime.strptime(name_or_date, '%d/%m/%Y')
                    converted_date = parsed_date.strftime('%Y-%m-%d')
                except ValueError:
                    pass
            
            criteria['name_or_date'] = converted_date if converted_date else name_or_date
        
        sport = self.sport_var.get().strip()
        if sport:
            criteria['sport'] = sport
        
        winner_name = self.winner_entry.get().strip()
        if winner_name:
            criteria['winner_name'] = winner_name
        
        try:
            prize_min = self.prize_min_entry.get().strip()
            if prize_min:
                criteria['prize_min'] = float(prize_min.replace(',', '.'))
            
            prize_max = self.prize_max_entry.get().strip()
            if prize_max:
                criteria['prize_max'] = float(prize_max.replace(',', '.'))
        except ValueError:
            pass
        
        try:
            earnings_min = self.earnings_min_entry.get().strip()
            if earnings_min:
                criteria['earnings_min'] = float(earnings_min.replace(',', '.'))
            
            earnings_max = self.earnings_max_entry.get().strip()
            if earnings_max:
                criteria['earnings_max'] = float(earnings_max.replace(',', '.'))
        except ValueError:
            pass
        
        return criteria
    
    def _preview(self):
        criteria = self._get_criteria()
        
        print(f"\n🔍 [PREVIEW] Критерии: {criteria}")
        
        from model import TournamentModel
        from database import Database
        
        db = Database(get_db_path())
        model = TournamentModel(db)
        results = model.search_tournaments(criteria)
        db.close()
        
        print(f"🔍 [PREVIEW] Найдено: {len(results)}")
        
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, f"Будет удалено записей: {len(results)}\n\n")
        
        if results:
            for i, tour in enumerate(results[:10], 1):
                date_str = tour.date.strftime('%d.%m.%Y') if isinstance(tour.date, datetime) else tour.date
                self.preview_text.insert(tk.END, f"{i}. {tour.name} ({date_str})\n")
            
            if len(results) > 10:
                self.preview_text.insert(tk.END, f"... и ещё {len(results) - 10}")
        else:
            self.preview_text.insert(tk.END, "Ничего не будет удалено")
    
    def _delete(self):
        criteria = self._get_criteria()
        
        print(f"\n🗑️ [DELETE] Критерии: {criteria}")
        
        if not any(criteria.values()):
            messagebox.showwarning("Ошибка", "Заполните хотя бы одно условие удаления", parent=self.dialog)
            return
        
        if messagebox.askyesno("Подтверждение", 
            "Вы уверены, что хотите удалить указанные записи?\nЭто действие нельзя отменить!",
            parent=self.dialog):
            
            from model import TournamentModel
            from database import Database
            
            db = Database(get_db_path())
            model = TournamentModel(db)
            
            count_before = db.get_tournaments_count()
            print(f"📊 ДО: {count_before}")
            
            count_deleted = model.delete_tournaments_by_criteria(criteria)
            print(f"🗑️ Удалено: {count_deleted}")
            
            count_after = db.get_tournaments_count()
            print(f"📊 ПОСЛЕ: {count_after}")
            
            db.close()
            
            self.result = criteria
            self.dialog.destroy()