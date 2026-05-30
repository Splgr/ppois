# server.py
import socket
import json
import threading
import queue
import time
from game_logic import new_board, is_valid_move, make_move, get_valid_moves, count_scores

HOST = "0.0.0.0"
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(2)

clients = {}
board = new_board()
current_turn = 1
game_over = False
cmd_queue = queue.Queue()

def broadcast(msg):
    data = (json.dumps(msg) + "\n").encode('utf-8')
    for conn in list(clients.values()):
        try: conn.sendall(data)
        except: pass

def send_state():
    broadcast({
        "cmd": "update",
        "board": board,
        "turn": current_turn,
        "scores": count_scores(board),
        "game_over": game_over
    })

def client_handler(conn, role):
    global game_over
    print(f"✅ Игрок {role} подключился")
    conn.sendall((json.dumps({"cmd": "welcome", "role": role}) + "\n").encode('utf-8'))
    send_state()
    
    buffer = b""
    try:
        while True:  # Сервер держит соединение, даже если игра закончилась
            try:
                data = conn.recv(4096)
                if not data:
                    print(f"⚠️ Игрок {role} разорвал соединение")
                    break
                buffer += data
                while b"\n" in buffer:
                    line, buffer = buffer.split(b"\n", 1)
                    try:
                        msg = json.loads(line.decode('utf-8'))
                        cmd_queue.put((role, msg))
                    except json.JSONDecodeError:
                        pass
            except Exception as e:
                print(f"❌ Ошибка игрока {role}: {e}")
                break
    finally:
        if role in clients: del clients[role]
        conn.close()
        print(f"🔌 Игрок {role} отключился")
        if not clients:
            game_over = True
        else:
            broadcast({"cmd": "disconnect"})

print(f"🟢 Сервер запущен на {HOST}:{PORT}")
print("Ожидание 2 игроков...")

for role in [1, 2]:
    conn, addr = server.accept()
    clients[role] = conn
    print(f"👤 Игрок {role} из {addr}")
    threading.Thread(target=client_handler, args=(conn, role), daemon=True).start()

print("🎮 Игра началась!")

try:
    while True:  # ✅ ИЗМЕНЕНО: сервер работает постоянно
        if game_over:
            time.sleep(1)  # Ждем, пока игроки нажмут ESC
            continue
            
        if not cmd_queue.empty():
            role, msg = cmd_queue.get()
            if msg.get("cmd") == "move" and role == current_turn and not game_over:
                x, y = msg.get("x"), msg.get("y")
                if is_valid_move(board, current_turn, x, y):
                    make_move(board, current_turn, x, y)
                    next_p = 3 - current_turn
                    if not get_valid_moves(board, next_p):
                        if get_valid_moves(board, current_turn):
                            broadcast({"cmd": "skip", "player": next_p})
                        else:
                            game_over = True
                    else:
                        current_turn = next_p
                    send_state()
                else:
                    try: clients[role].sendall((json.dumps({"cmd": "invalid"}) + "\n").encode('utf-8'))
                    except: pass
except KeyboardInterrupt:
    print("🛑 Сервер остановлен")
finally:
    server.close()