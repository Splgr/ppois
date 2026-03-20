"""
Tournament Management System
Main entry point
"""
import tkinter as tk
from tkinter import messagebox
import sys
import traceback
import os


def main():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, "tournaments.db")
        
        print(f"📁 Путь к базе: {db_path}") 
        print(f"📁 Текущая папка: {os.getcwd()}")  
        
        root = tk.Tk()
        root.title("Система управления турнирами")
        root.geometry("1200x700")
        
        print("🔧 Инициализация базы данных...")
        from database import Database
        db = Database(db_path)  
        db.create_tables()
        
        count = db.get_tournaments_count()
        print(f"📊 Записей в базе: {count}")
        
        if count == 0:
            print("⚠️ База пустая! Запусти data_generator.py для создания данных")
        
        print("✅ База данных готова")
        
        print("🔧 Создание MVC компонентов...")
        from model import TournamentModel
        from view import TournamentView
        from controller import TournamentController
        
        model = TournamentModel(db)
        view = TournamentView(root)
        controller = TournamentController(model, view)
        
        print("✅ Все компоненты созданы")
        print("🚀 Запуск главного цикла...")
        
        # Обработка закрытия окна
        def on_closing():
            print("👋 Закрытие приложения...")
            db.close()
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)

        root.mainloop()
        
        print("✅ Приложение закрыто")
        
    except Exception as e:
        print(f"\n❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        print("\nТрассировка:")
        traceback.print_exc()
        
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Критическая ошибка", 
            f"Произошла ошибка при запуске:\n\n{e}\n\nСмотрите консоль для деталей.")
        root.destroy()
        sys.exit(1)


if __name__ == "__main__":
    main()