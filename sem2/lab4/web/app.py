from flask import Flask
from core.storage import HotelStorage
from core.reception import Reception
import os

app = Flask(__name__)
app.secret_key = "hotel_lab4_super_secret_key"

storage = HotelStorage(filepath="data/hotel_data.json")
reception = Reception(storage)

app.config['RECEPTION'] = reception
app.config['STORAGE'] = storage

from web.routes import *

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    app.run(debug=True, port=5000)