"""
Скрипт удаления дубликатов из базы данных
Оставляет только одну запись с уникальным сочетанием Название + Дата
"""
import sqlite3

def remove_duplicates():
    db_path = "tournaments.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Считаем сколько было записей
    cursor.execute("SELECT COUNT(*) FROM tournaments")
    count_before = cursor.fetchone()[0]
    print(f"📊 Записей ДО очистки: {count_before}")
    
    # 2. Находим дубликаты и удаляем их
    # Оставляем запись с минимальным ID, остальные удаляем
    cursor.execute('''
        DELETE FROM tournaments
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM tournaments
            GROUP BY name, date
        )
    ''')
    
    conn.commit()
    
    # 3. Считаем сколько осталось
    cursor.execute("SELECT COUNT(*) FROM tournaments")
    count_after = cursor.fetchone()[0]
    deleted = count_before - count_after
    
    print(f"📊 Записей ПОСЛЕ очистки: {count_after}")
    print(f"🗑️ Удалено дубликатов: {deleted}")
    
    if deleted > 0:
        print("✅ Дубликаты успешно удалены!")
    else:
        print("✨ Дубликатов не найдено, база чистая!")
    
    conn.close()

if __name__ == "__main__":
    remove_duplicates()
    input("\nНажмите Enter для выхода...")
