"""
Data generator for Tournament Management System
Generates test data for demonstration (DATABASE ONLY)
"""
import os
import random
from datetime import datetime, timedelta
from model import Tournament
from database import Database

# ← Абсолютные пути (чтобы файлы всегда создавались в нужной папке)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "tournaments.db")

SPORTS = [
    "Футбол", "Баскетбол", "Теннис", "Хоккей", "Волейбол",
    "Плавание", "Лёгкая атлетика", "Бокс", "ММА", "Киберспорт",
    "Шахматы", "Гимнастика", "Фигурное катание", "Бадминтон", "Настольный теннис"
]

TOURNAMENT_PREFIXES = [
    "Чемпионат", "Кубок", "Турнир", "Первенство", "Открытый чемпионат",
    "Международный турнир", "Национальный кубок", "Гран-при", "Мастерс", "Серия"
]

TOURNAMENT_SUFFIXES = [
    "мира", "Европы", "России", "Москвы", "Санкт-Петербурга",
    "по региону", "среди профессионалов", "среди любителей", "2024", "2025",
    "Winter Cup", "Summer Open", "Spring Championship", "Autumn League"
]

FIRST_NAMES_MALE = [
    "Александр", "Дмитрий", "Максим", "Сергей", "Андрей", "Алексей", "Артём",
    "Илья", "Кирилл", "Михаил", "Иван", "Павел", "Егор", "Никита", "Владимир"
]

FIRST_NAMES_FEMALE = [
    "Анастасия", "Мария", "Анна", "Елена", "Дарья", "Алина", "Ирина",
    "Екатерина", "Арина", "Полина", "Ольга", "Юлия", "Татьяна", "Ксения", "Виктория"
]

LAST_NAMES = [
    "Иванов", "Смирнов", "Кузнецов", "Попов", "Васильев", "Петров", "Соколов",
    "Михайлов", "Новиков", "Фёдоров", "Морозов", "Волков", "Алексеев", "Лебедев",
    "Семёнов", "Егоров", "Павлов", "Козлов", "Степанов", "Николаев"
]


def generate_random_name(is_male=None):
    """Generate random full name"""
    if is_male is None:
        is_male = random.choice([True, False])
    
    last_name = random.choice(LAST_NAMES)
    
    if is_male:
        first_name = random.choice(FIRST_NAMES_MALE)
        patronymic = random.choice(["Александрович", "Дмитриевич", "Максимович", "Сергеевич", "Андреевич"])
    else:
        first_name = random.choice(FIRST_NAMES_FEMALE)
        patronymic = random.choice(["Александровна", "Дмитриевна", "Максимовна", "Сергеевна", "Андреевна"])
        
        # ← ИСПРАВЛЕНО: Правильное склонение фамилий
        if last_name.endswith("ова") or last_name.endswith("ева"):
            pass  # Уже женская фамилия
        elif last_name.endswith("ов"):
            last_name = last_name + "а"
        elif last_name.endswith("ев"):
            last_name = last_name + "а"
    
    return f"{last_name} {first_name} {patronymic}"


def generate_tournament_name():
    """Generate realistic tournament name"""
    prefix = random.choice(TOURNAMENT_PREFIXES)
    suffix = random.choice(TOURNAMENT_SUFFIXES)
    sport = random.choice(SPORTS)
    
    return f"{prefix} по {sport} {suffix}"


def generate_random_date(start_year=2020, end_year=2026):
    """Generate random date"""
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)


def generate_tournaments(count=60):
    """Generate multiple tournaments"""
    tournaments = []
    unique_keys = set()
    
    attempts = 0
    max_attempts = count * 3
    
    while len(tournaments) < count and attempts < max_attempts:
        attempts += 1
        
        sport = random.choice(SPORTS)
        prize_pool = random.choice([
            50000, 100000, 250000, 500000, 1000000,
            2000000, 5000000, 10000000, 15000000
        ])
        
        name = generate_tournament_name()
        date = generate_random_date()
        
        # Проверка на дубликаты (название + дата)
        unique_key = f"{name}|{date.strftime('%Y-%m-%d')}"
        
        if unique_key in unique_keys:
            continue
        
        unique_keys.add(unique_key)
        
        tournament = Tournament(
            id=None,
            name=name,
            date=date,
            sport=sport,
            winner_name=generate_random_name(),
            prize_pool=prize_pool,
            winner_earnings=prize_pool * 0.6
        )
        tournaments.append(tournament)
    
    print(f"✅ Сгенерировано {len(tournaments)} уникальных турниров за {attempts} попыток")
    return tournaments


def populate_database(db_path=None, count=60):
    """Populate database with generated tournaments"""
    if db_path is None:
        db_path = DB_PATH
    
    print(f"📁 Путь к базе: {db_path}")
    
    db = Database(db_path)
    db.create_tables()
    
    # Очистить базу перед заполнением (чтобы не было дубликатов)
    print("🗑️ Очистка базы данных...")
    db.cursor.execute("DELETE FROM tournaments")
    db.conn.commit()
    
    count_before = db.get_tournaments_count()
    print(f"📊 Записей до генерации: {count_before}")
    
    tournaments = generate_tournaments(count)
    
    for tournament in tournaments:
        db.insert_tournament(tournament)
    
    count_after = db.get_tournaments_count()
    print(f"📊 Записей после генерации: {count_after}")
    
    print(f"✅ Добавлено {count} турниров в базу данных {db_path}")
    db.close()


if __name__ == "__main__":
    print("🔧 Генерация тестовых данных...")
    print("=" * 60)
    
    # ← ТОЛЬКО генерация в базу данных (XML больше не создаётся!)
    populate_database(DB_PATH, 60)
