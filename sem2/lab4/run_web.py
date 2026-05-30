from web.app import app
import os

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    print("Запуск веб-интерфейса отеля...")
    print("Открыть в браузере: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)