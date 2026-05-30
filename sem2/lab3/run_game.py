# run_game.py
import subprocess
import sys
import os
import time

# === ВАЖНОЕ ИСПРАВЛЕНИЕ ===
# Находим папку, где лежит этот файл, и запоминаем путь
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"📁 Скрипт работает из: {SCRIPT_DIR}")

def run_command(cmd, title):
    print(f"🚀 Запуск: {title}")
    # Добавляем cwd=SCRIPT_DIR, чтобы процессы запускались из нужной папки
    return subprocess.Popen([sys.executable] + cmd, cwd=SCRIPT_DIR)

if __name__ == "__main__":
    print("=== 🎮 LAUNCHER REVERSI ONLINE ===")
    print("1. Только СЕРВЕР")
    print("2. Только КЛИЕНТ")
    print("3. СЕРВЕР + 2 КЛИЕНТА (всё сразу)")
    print("4. Выход")
    
    choice = input("\nВаш выбор (1-4): ").strip()
    
    if choice == "1":
        proc = run_command(["server.py"], "Сервер")
        proc.wait()
        
    elif choice == "2":
        proc = run_command(["client.py"], "Клиент")
        proc.wait()
        
    elif choice == "3":
        # 1. Сервер
        server = run_command(["server.py"], "Сервер")
        time.sleep(1.5) 
        
        # 2. Два клиента
        client1 = run_command(["client.py"], "Клиент 1")
        time.sleep(0.5)
        client2 = run_command(["client.py"], "Клиент 2")
        
        print("✅ Игра запущена! Закройте окна клиентов для завершения.")
        
        client1.wait()
        client2.wait()
        
        print("🛑 Клиенты закрыты. Остановка сервера...")
        server.terminate()
        server.wait()
        print("✅ Готово.")
        
    elif choice == "4":
        print("👋 Выход.")
        
    else:
        print("❌ Неверный выбор.")