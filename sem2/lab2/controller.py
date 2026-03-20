"""
Controller component for Tournament Management System
"""

from model import Tournament, TournamentModel
from view import TournamentView
from dialogs import (
    AddTournamentDialog,
    EditTournamentDialog,
    SearchDialog,
    DeleteDialog
)


class TournamentController:
    """Controller for managing tournaments"""
    
    def __init__(self, model: TournamentModel, view: TournamentView):
        self.model = model
        self.view = view
        
        print("🔧 Контроллер инициализируется...")
        
        self.view.set_controller(self)
        
        self.current_page = 1
        self.page_size = 10
        self.search_results = None
        
        print("🔧 Загрузка данных...")
        self.refresh_display()
        print("✅ Контроллер готов!")
    
    def refresh_display(self):
        """Refresh the display with current data"""
        print(f"🔄 Обновление display (страница {self.current_page})")
        
        if self.search_results is not None:
            total = len(self.search_results)
            total_pages = max(1, (total + self.page_size - 1) // self.page_size)
            self.current_page = max(1, min(self.current_page, total_pages))
            
            start_idx = (self.current_page - 1) * self.page_size
            end_idx = start_idx + self.page_size
            page_data = self.search_results[start_idx:end_idx]
            
            self.view.display_tournaments(page_data)
            self.view.update_pagination(self.current_page, total_pages, total)
        else:
            tournaments, total = self.model.get_tournaments_paginated(
                self.current_page, self.page_size
            )
            total_pages = max(1, (total + self.page_size - 1) // self.page_size)
            
            self.view.display_tournaments(tournaments)
            self.view.update_pagination(self.current_page, total_pages, total)
        
        self.view.set_status("Готово")
        print(f"✅ Отображено записей: {total}")
    
    def on_add_tournament(self):
        print("\n➕ [DEBUG] on_add_tournament ВЫЗВАН!")
        try:
            sports = self.model.get_unique_sports()
            print(f"   Виды спорта: {sports[:3]}...")
            
            dialog = AddTournamentDialog(self.view.root, sports)
            print(f"   Диалог закрыт, result={dialog.result}")
            
            if dialog.result:
                tournament = Tournament(
                    id=None,
                    name=dialog.result['name'],
                    date=dialog.result['date'],
                    sport=dialog.result['sport'],
                    winner_name=dialog.result['winner_name'],
                    prize_pool=dialog.result['prize_pool'],
                    winner_earnings=dialog.result['prize_pool'] * 0.6
                )
                
                self.model.add_tournament(tournament)
                self.view.show_message(f"Турнир '{tournament.name}' добавлен!", "Успех")
                self.refresh_display()
        except Exception as e:
            print(f"   ❌ ОШИБКА: {e}")
            import traceback
            traceback.print_exc()
            self.view.show_error(f"Ошибка при добавлении: {e}", "Ошибка")
    
    def on_edit_tournament(self):
        print("\n✏️ [DEBUG] on_edit_tournament ВЫЗВАН!")
        try:
            if self.view.current_view == 'table':
                tournament_id = self.view.table_frame.get_selected_id()
                print(f"   Выбранный ID: {tournament_id}")
            else:
                self.view.show_warning("Редактирование доступно только в режиме таблицы")
                return
            
            if not tournament_id:
                self.view.show_warning("Выберите турнир для редактирования")
                return
            
            tournament = self.model.get_tournament_by_id(tournament_id)
            if not tournament:
                self.view.show_error("Турнир не найден")
                return
            
            dialog = EditTournamentDialog(self.view.root, tournament, self.model.get_unique_sports())
            
            if dialog.result:
                tournament.name = dialog.result['name']
                tournament.date = dialog.result['date']
                tournament.sport = dialog.result['sport']
                tournament.winner_name = dialog.result['winner_name']
                tournament.prize_pool = dialog.result['prize_pool']
                tournament.winner_earnings = dialog.result['prize_pool'] * 0.6
                
                self.model.update_tournament(tournament)
                self.view.show_message(f"Турнир '{tournament.name}' обновлён!", "Успех")
                self.refresh_display()
        except Exception as e:
            print(f"   ❌ ОШИБКА: {e}")
            import traceback
            traceback.print_exc()
            self.view.show_error(f"Ошибка при редактировании: {e}", "Ошибка")
    
    def on_delete_tournament(self):  # ← ИСПРАВЛЕННЫЙ МЕТОД
        print("\n🗑️ [DEBUG] on_delete_tournament ВЫЗВАН!")
        try:
            dialog = DeleteDialog(self.view.root, self.model.get_unique_sports())
            
            if dialog.result:
                count = self.model.delete_tournaments_by_criteria(dialog.result)
                
                # ← УБРАЛ messagebox — всё видно в консоли
                print(f"🗑️ Удалено: {count} записей")
                
                self.search_results = None
                self.current_page = 1
                self.refresh_display()
        except Exception as e:
            print(f"   ❌ ОШИБКА: {e}")
            import traceback
            traceback.print_exc()
            self.view.show_error(f"Ошибка при удалении: {e}", "Ошибка")
    
    def on_search_tournaments(self):
        print("\n🔍 [DEBUG] on_search_tournaments ВЫЗВАН!")
        try:
            dialog = SearchDialog(self.view.root, self.model.get_unique_sports())
            
            if dialog.result:
                self.search_results = self.model.search_tournaments(dialog.result)
                self.current_page = 1
                
                if len(self.search_results) > 0:
                    self.view.show_message(f"Найдено записей: {len(self.search_results)}", "Поиск завершён")
                else:
                    self.view.show_warning("Записи не найдены", "Результат поиска")
                
                self.refresh_display()
        except Exception as e:
            print(f"   ❌ ОШИБКА: {e}")
            import traceback
            traceback.print_exc()
            self.view.show_error(f"Ошибка при поиске: {e}", "Ошибка")
    
    def on_save_xml(self):
        print("\n💾 [DEBUG] on_save_xml ВЫЗВАН!")
        try:
            filepath = self.view.get_save_filename()
            if filepath:
                success = self.model.export_to_xml(filepath)
                if success:
                    self.view.show_message(f"Данные сохранены в {filepath}", "Сохранение")
                else:
                    self.view.show_error("Ошибка при сохранении", "Ошибка")
        except Exception as e:
            print(f"   ❌ ОШИБКА: {e}")
            import traceback
            traceback.print_exc()
    
    def on_load_xml(self):
        print("\n📂 [DEBUG] on_load_xml ВЫЗВАН!")
        try:
            filepath = self.view.get_load_filename()
            if filepath:
                count = self.model.import_from_xml(filepath)
                if count > 0:
                    self.view.show_message(f"Загружено записей: {count}", "Загрузка завершена")
                    self.search_results = None
                    self.current_page = 1
                    self.refresh_display()
                else:
                    self.view.show_warning("Не удалось загрузить данные", "Ошибка загрузки")
        except Exception as e:
            print(f"   ❌ ОШИБКА: {e}")
            import traceback
            traceback.print_exc()
    
    def on_show_table(self):
        print("\n📊 [DEBUG] on_show_table ВЫЗВАН!")
        self.view.show_table_view()
        self.refresh_display()
    
    def on_show_tree(self):
        print("\n🌳 [DEBUG] on_show_tree ВЫЗВАН!")
        self.view.show_tree_view()
        if self.search_results is not None:
            self.view.tree_frame.populate(self.search_results)
        else:
            self.view.tree_frame.populate(self.model.get_all_tournaments())
    
    def on_refresh(self):
        print("\n🔄 [DEBUG] on_refresh ВЫЗВАН!")
        self.search_results = None
        self.current_page = 1
        self.refresh_display()
    
    def on_page_change(self, page: int):
        print(f"\n📄 [DEBUG] on_page_change: страница {page}")
        self.current_page = page
        self.refresh_display()
    
    def on_page_size_change(self, size: int):
        print(f"\n📊 [DEBUG] on_page_size_change: размер {size}")
        self.page_size = size
        self.current_page = 1
        self.refresh_display()