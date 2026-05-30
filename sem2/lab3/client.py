# client.py
import pygame
import json
import os
import sys
import math
import socket
import threading
from pygame import mixer
from game_logic import is_valid_move, make_move, get_valid_moves as logic_get_valid_moves

# ====================== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ======================
sock = None
MY_ROLE = 0
current_turn = 1
is_my_turn = False
game_state = "menu"
input_ip = "127.0.0.1"
ip_active = False
error_msg = ""
error_timer = 0
board = [[0]*8 for _ in range(8)]
flipped_pieces = []
anim_progress = 0.0
running = True
input_name = ""
menu_buttons = []
show_help = False
show_scores = False
record_saved = False
GAME_MODE = None  # "online" или "offline"

# ====================== РЕКОРДЫ ======================
SCORES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'highscores.json')
highscores = []

def load_highscores():
    global highscores
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'r', encoding='utf-8') as f: 
            highscores = json.load(f)
    else: 
        highscores = []

def save_highscores():
    with open(SCORES_FILE, 'w', encoding='utf-8') as f:
        json.dump(highscores, f, indent=4, ensure_ascii=False)

# ====================== PYGAME ИНИЦИАЛИЗАЦИЯ (ПЕРВЫМ ДЕЛОМ!) ======================
pygame.init()
mixer.init()  # ✅ Инициализируем звук сразу

# Создаём окно
W, H = 1280, 720
screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
pygame.display.set_caption("Reversi")
clock = pygame.time.Clock()

# Считаем размеры доски
BOARD_SIZE = 8
CELL_SIZE = min((W-120)//BOARD_SIZE, (H-180)//BOARD_SIZE, 80)
CELL_SIZE = max(CELL_SIZE, 40)
BOARD_WIDTH = BOARD_SIZE * CELL_SIZE
BOARD_HEIGHT = BOARD_SIZE * CELL_SIZE
OFFSET_X = (W - BOARD_WIDTH) // 2
OFFSET_Y = 80

# ✅ Теперь создаём шрифты (после pygame.init())
def get_font(size):
    # Пробуем Arial, если нет — берём дефолтный
    f = pygame.font.SysFont("arial", int(size * CELL_SIZE / 60))
    return f if f else pygame.font.Font(None, int(size * CELL_SIZE / 60))

font = get_font(32)
small_font = get_font(22)
medium_font = get_font(26)

# ✅ Инициализируем звуки (после mixer.init())
SOUNDS = {}
def init_sounds():
    global SOUNDS
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'sounds')
    try:
        SOUNDS["place"] = mixer.Sound(os.path.join(base, "place.wav"))
        SOUNDS["flip"] = mixer.Sound(os.path.join(base, "flip.wav"))
        SOUNDS["place"].set_volume(0.7)
        SOUNDS["flip"].set_volume(0.7)
    except Exception as e: 
        print(f"🔇 Звуки не найдены: {e}")

def play_sound(name):
    if name in SOUNDS:
        try: SOUNDS[name].play()
        except: pass

init_sounds()

# Пробуем загрузить музыку
try:
    music_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'sounds', 'background_music.mp3')
    if os.path.exists(music_path):
        mixer.music.load(music_path)
        mixer.music.set_volume(0.4)
        mixer.music.play(-1)
except: 
    pass

# Загружаем рекорды (в конце, когда всё стабильно)
load_highscores()

# ====================== СЕТЬ ======================
def connect_to_server(ip, port):
    global sock
    print(f"🔌 Подключение к {ip}:{port}...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((ip, port))
        sock.settimeout(None)
        print("✅ Подключено!")
        threading.Thread(target=recv_loop, daemon=True).start()
        return True
    except Exception as e:
        show_error(f"Ошибка подключения: {e}")
        return False

def recv_loop():
    global MY_ROLE, current_turn, is_my_turn, board, game_state, flipped_pieces, anim_progress
    buf = b""
    while running and sock:
        try:
            data = sock.recv(4096)
            if not data:
                show_error("Сервер отключился")
                game_state = "menu"
                break
            buf += data
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                try: process_message(json.loads(line.decode('utf-8')))
                except: pass
        except Exception as e:
            show_error(f"Потеря связи: {e}")
            game_state = "menu"
            break

def process_message(msg):
    global MY_ROLE, current_turn, is_my_turn, board, game_state, flipped_pieces, anim_progress, record_saved
    cmd = msg.get("cmd")
    if cmd == "welcome":
        MY_ROLE = msg.get("role")
        game_state = "playing"
        record_saved = False
        print(f"✅ Вы игрок {MY_ROLE}")
    elif cmd == "update":
        old_board = [row[:] for row in board]
        board = msg.get("board", [[0]*8 for _ in range(8)])
        current_turn = msg.get("turn", 1)
        is_my_turn = (current_turn == MY_ROLE)
        if msg.get("game_over"): 
            game_state = "game_over"
            record_saved = False
        
        flips = []
        for y in range(8):
            for x in range(8):
                if old_board[y][x] != 0 and board[y][x] != 0 and old_board[y][x] != board[y][x]:
                    flips.append({'x': x, 'y': y, 'progress': 0.0})
        if flips:
            flipped_pieces = flips
            anim_progress = 0.0
            play_sound("flip")
    elif cmd == "invalid": show_error("⛔ Недопустимый ход!")
    elif cmd == "disconnect": 
        show_error("🔌 Противник отключился")
        game_state = "menu"

def send_move(x, y):
    if sock and game_state == "playing":
        try:
            sock.sendall((json.dumps({"cmd": "move", "x": x, "y": y}) + "\n").encode('utf-8'))
            play_sound("place")
        except: show_error("Ошибка отправки")

def show_error(text):
    global error_msg, error_timer
    error_msg = text
    error_timer = 120

# ====================== ЛОГИКА ======================
def count_scores():
    s = {1: 0, 2: 0}
    for row in board:
        for c in row:
            if c in s: s[c] += 1
    return s

def get_valid_moves(player):
    return logic_get_valid_moves(board, player)

def start_offline_game():
    """Запуск оффлайн-режима: доска сбрасывается, ходят чёрные"""
    global board, current_turn, is_my_turn, game_state, flipped_pieces, anim_progress, record_saved
    board = [[0]*8 for _ in range(8)]
    board[3][3], board[3][4] = 2, 1
    board[4][3], board[4][4] = 1, 2
    current_turn = 1
    is_my_turn = True
    game_state = "playing"
    flipped_pieces = []
    anim_progress = 0.0
    record_saved = False
    print("🎮 Оффлайн режим запущен. Ходят чёрные (1)")

def make_offline_move(x, y, player):
    """Локальный ход без сервера"""
    if is_valid_move(board, player, x, y):
        make_move(board, player, x, y)
        return True
    return False

def switch_turn_offline():
    """Переключает ход и проверяет конец игры / пропуски"""
    global current_turn, is_my_turn, game_state
    
    if not get_valid_moves(1) and not get_valid_moves(2):
        game_state = "game_over"
        return
    
    next_player = 3 - current_turn
    if get_valid_moves(next_player):
        current_turn = next_player
        is_my_turn = True
    else:
        if get_valid_moves(current_turn):
            show_error(f"⏭️ Игрок {next_player} пропускает ход!")
            is_my_turn = True
            pygame.time.set_timer(pygame.USEREVENT, 1500)
        else:
            game_state = "game_over"

# ====================== ОТРИСОВКА ======================
def draw_menu():
    global menu_buttons
    overlay = pygame.Surface((W, H)); overlay.set_alpha(180); overlay.fill((0,0,0)); screen.blit(overlay, (0,0))
    mw, mh = 500, 500
    mx, my = (W-mw)//2, (H-mh)//2
    pygame.draw.rect(screen, (0, 60, 0), (mx, my, mw, mh))
    pygame.draw.rect(screen, (0, 150, 0), (mx, my, mw, mh), 3)
    screen.blit(font.render("REVERSI", True, (0, 255, 100)), (W//2 - 80, my + 30))
    
    menu_buttons = []
    labels = ["ОНЛАЙН (2 игрока)", "ОФФЛАЙН (на одном ПК)", "РЕКОРДЫ", "СПРАВКА", "ВЫХОД"]
    for i, label in enumerate(labels):
        by = my + 90 + i * 70
        btn = pygame.Rect(mx + (mw-300)//2, by, 300, 50)
        pygame.draw.rect(screen, (0, 100, 0), btn)
        pygame.draw.rect(screen, (0, 200, 0), btn, 3)
        surf = medium_font.render(label, True, (0, 255, 100))
        screen.blit(surf, (btn.centerx - surf.get_width()//2, btn.centery - surf.get_height()//2))
        menu_buttons.append(btn)
    screen.blit(small_font.render("Нажми 1-5 или клик", True, (100,255,100)), (W//2-100, my+mh-40))

def draw_connect_screen():
    overlay = pygame.Surface((W, H)); overlay.set_alpha(160); overlay.fill((0,0,0)); screen.blit(overlay, (0,0))
    screen.blit(font.render("ПОДКЛЮЧЕНИЕ", True, (0,255,100)), (W//2-120, 150))
    box = pygame.Rect(W//2-200, 220, 400, 50)
    pygame.draw.rect(screen, (30,40,50), box)
    pygame.draw.rect(screen, (0,150,100), box, 3)
    cur = "▮" if ip_active else ""
    screen.blit(medium_font.render(f"IP: {input_ip}{cur}", True, (200,255,200)), (box.x+15, box.y+12))
    btn = pygame.Rect(W//2-80, 290, 160, 45)
    pygame.draw.rect(screen, (0,100,80), btn)
    pygame.draw.rect(screen, (0,200,150), btn, 3)
    screen.blit(medium_font.render("ПОДКЛЮЧИТЬСЯ", True, (0,255,100)), (btn.centerx-70, btn.centery-10))
    if error_msg: screen.blit(small_font.render(error_msg, True, (255,80,80)), (W//2-100, 350))
    screen.blit(small_font.render("ESC - назад", True, (150,150,150)), (W//2-60, 420))
    return btn

def draw_help():
    overlay = pygame.Surface((W,H)); overlay.set_alpha(200); overlay.fill((0,0,0)); screen.blit(overlay,(0,0))
    w,h = 600,400; x,y = (W-w)//2, (H-h)//2
    pygame.draw.rect(screen, (30,30,50), (x,y,w,h))
    pygame.draw.rect(screen, (100,200,100), (x,y,w,h), 3)
    screen.blit(font.render("ПРАВИЛА", True, (255,215,0)), (W//2-60, y+20))
    rules = ["1. Ходите по очереди.", "2. Окружайте фишки врага.", "3. Окружённые переворачиваются.",
             "4. Побеждает тот, у кого больше.", "Клик = ход. ESC = меню."]
    for i, r in enumerate(rules): screen.blit(small_font.render(r, True, (220,220,220)), (x+30, y+80+i*40))
    screen.blit(small_font.render("Клик/клавиша для закрытия", True, (150,150,150)), (W//2-120, y+h-30))

def draw_highscores():
    load_highscores()
    overlay = pygame.Surface((W,H)); overlay.set_alpha(200); overlay.fill((0,0,0)); screen.blit(overlay,(0,0))
    w,h = 400,400; x,y = (W-w)//2, (H-h)//2
    pygame.draw.rect(screen, (30,30,50), (x,y,w,h))
    pygame.draw.rect(screen, (100,200,100), (x,y,w,h), 3)
    screen.blit(font.render("РЕКОРДЫ", True, (255,215,0)), (W//2-70, y+20))
    if highscores:
        for i, rec in enumerate(highscores[:8]):
            screen.blit(medium_font.render(f"{i+1}. {rec['name']} — {rec['score']}", True, (200,255,200)), (x+40, y+80+i*35))
    else:
        screen.blit(medium_font.render("Пусто", True, (200,200,200)), (W//2-30, y+150))
    screen.blit(small_font.render("Клик/клавиша для закрытия", True, (150,150,150)), (W//2-120, y+h-30))

def draw_board():
    global flipped_pieces, anim_progress
    if flipped_pieces:
        anim_progress += 0.08
        for p in flipped_pieces: p['progress'] = min(anim_progress, 1.0)
        if anim_progress >= 1.0: flipped_pieces = []; anim_progress = 0.0

    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            rect = pygame.Rect(OFFSET_X + x*CELL_SIZE, OFFSET_Y + y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (0, 100, 0), rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)
            
            view_player = current_turn if GAME_MODE == "offline" else MY_ROLE
            dx = (BOARD_SIZE-1-x) if view_player == 2 else x
            dy = (BOARD_SIZE-1-y) if view_player == 2 else y
            
            val = board[dy][dx] if 0 <= dy < 8 and 0 <= dx < 8 else 0
            if val == 0: continue
            
            prog = 1.0
            for fp in flipped_pieces:
                if fp['x']==dx and fp['y']==dy: prog = fp['progress']; break
            cx = OFFSET_X + x*CELL_SIZE + CELL_SIZE//2
            cy = OFFSET_Y + y*CELL_SIZE + CELL_SIZE//2
            scale = abs(math.cos(prog*math.pi)) if prog < 1 else 1.0
            r = int((CELL_SIZE//2 - 5) * scale)
            col = (20,20,20) if val==1 else (240,240,240)
            pygame.draw.circle(screen, col, (cx,cy), r)

def draw_ui():
    if game_state == "playing":
        # 🔹 Текст статуса зависит от режима
        if GAME_MODE == "offline":
            status = f"ХОД ИГРОКА {current_turn} ({'ЧЁРНЫЕ' if current_turn==1 else 'БЕЛЫЕ'})"
            col = (0,255,0)
        else:
            # ✅ ЗАЩИТА: не рисуем статус, пока роль не назначена
            if MY_ROLE not in [1, 2]:
                status = "ПОДКЛЮЧЕНИЕ..."
                col = (255, 255, 0)
            else:
                status = "ВАШ ХОД" if is_my_turn else "ХОД ПРОТИВНИКА..."
                col = (0,255,0) if is_my_turn else (255,100,100)
        screen.blit(font.render(status, True, col), (W//2 - 150, OFFSET_Y-40))
        
        sc = count_scores()
        # 🔹 Отрисовка счёта с защитой от KeyError
        if GAME_MODE == "offline":
            screen.blit(small_font.render(f"Чёрные: {sc[1]}  Белые: {sc[2]}", True, (200,255,200)), (20, OFFSET_Y-40))
        elif MY_ROLE in [1, 2]:  # ✅ Только если роль назначена
            screen.blit(small_font.render(f"Вы: {sc[MY_ROLE]}  Соперник: {sc[3-MY_ROLE]}", True, (200,255,200)), (20, OFFSET_Y-40))
        
        screen.blit(small_font.render("ESC - в меню", True, (150,150,150)), (W//2 - 50, H-25))
        
    if error_msg and error_timer > 0:
        screen.blit(small_font.render(error_msg, True, (255,100,100)), (W//2 - 100, OFFSET_Y + BOARD_HEIGHT + 10))

def draw_game_over():
    overlay = pygame.Surface((W,H)); overlay.set_alpha(180); overlay.fill((0,0,0)); screen.blit(overlay,(0,0))
    sc = count_scores()
    
    if GAME_MODE == "offline":
        my_score = sc[current_turn]
        opp_score = sc[3-current_turn]
        display_my = sc[1] if current_turn == 1 else sc[2]
        display_opp = sc[2] if current_turn == 1 else sc[1]
    else:
        my_score = sc.get(MY_ROLE, 0)
        opp_score = sc.get(3-MY_ROLE, 0)
        display_my = my_score
        display_opp = opp_score
    
    if my_score > opp_score: res, col = "ПОБЕДА!", (0,255,0)
    elif opp_score > my_score: res, col = "ПОРАЖЕНИЕ", (255,100,100)
    else: res, col = "НИЧЬЯ", (255,215,0)
    
    screen.blit(font.render(res, True, col), (W//2 - 80, H//2 - 60))
    screen.blit(medium_font.render(f"{display_my} - {display_opp}", True, (200,200,200)), (W//2 - 40, H//2 - 10))
    
    if GAME_MODE == "offline" or (MY_ROLE in [1,2] and my_score > opp_score):
        is_rec = my_score > 0 and (not highscores or my_score > highscores[0].get("score",0))
        if record_saved:
            screen.blit(small_font.render("✅ РЕКОРД СОХРАНЁН! ESC - меню", True, (0,255,0)), (W//2 - 130, H//2 + 40))
        elif is_rec:
            screen.blit(small_font.render("НОВЫЙ РЕКОРД! Имя + Enter:", True, (255,255,100)), (W//2 - 140, H//2 + 20))
            screen.blit(medium_font.render(input_name + "▮", True, (255,255,255)), (W//2 - 50, H//2 + 50))
        else:
            screen.blit(small_font.render("ESC - в меню", True, (150,150,150)), (W//2 - 50, H//2 + 40))
    else:
        screen.blit(small_font.render("ESC - в меню", True, (150,150,150)), (W//2 - 50, H//2 + 40))

# ====================== ГЛАВНЫЙ ЦИКЛ ======================
connect_btn = None
print("🎮 Клиент запущен. Окно: 1280x720")

while running:
    clock.tick(60)
    if error_timer > 0: error_timer -= 1
    if error_timer <= 0: error_msg = ""
    
    W, H = screen.get_size()
    OFFSET_X = (W - BOARD_WIDTH) // 2

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if game_state in ["playing","game_over","connect","help","scores"]:
                if GAME_MODE == "online" and sock:
                    try: sock.close()
                    except: pass
                    sock = None
                game_state = "menu"
                input_name = ""; record_saved = False
                MY_ROLE = 0; is_my_turn = False; board = [[0]*8 for _ in range(8)]
            elif game_state == "menu":
                running = False
            continue

        if event.type == pygame.USEREVENT:
            pygame.time.set_timer(pygame.USEREVENT, 0)
            continue

        if game_state == "menu" and not show_help and not show_scores:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, btn in enumerate(menu_buttons):
                    if btn.collidepoint(event.pos):
                        if i == 0:
                            GAME_MODE = "online"
                            game_state = "connect"
                        elif i == 1:
                            GAME_MODE = "offline"
                            start_offline_game()
                        elif i == 2: show_scores = True
                        elif i == 3: show_help = True
                        elif i == 4: running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: GAME_MODE = "online"; game_state = "connect"
                elif event.key == pygame.K_2: GAME_MODE = "offline"; start_offline_game()
                elif event.key == pygame.K_3: show_scores = True
                elif event.key == pygame.K_4: show_help = True

        elif show_help or show_scores:
            if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                show_help = False; show_scores = False

        elif game_state == "connect":
            if event.type == pygame.MOUSEBUTTONDOWN and connect_btn and connect_btn.collidepoint(event.pos):
                if connect_to_server(input_ip, 5555): error_msg=""; game_state="playing"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if connect_to_server(input_ip, 5555): error_msg=""; game_state="playing"
                elif event.key == pygame.K_BACKSPACE: input_ip = input_ip[:-1]
                elif event.unicode.isdigit() or event.unicode in ".:": input_ip += event.unicode

        elif game_state == "playing" and event.type == pygame.MOUSEBUTTONDOWN and not flipped_pieces:
            # 🔹 В оффлайне ходит тот, чей сейчас current_turn; в онлайне — только если is_my_turn
            can_move = (GAME_MODE == "offline") or (GAME_MODE == "online" and is_my_turn)
            if can_move:
                mx, my = event.pos
                if OFFSET_X <= mx < OFFSET_X+BOARD_WIDTH and OFFSET_Y <= my < OFFSET_Y+BOARD_HEIGHT:
                    bx = (mx-OFFSET_X)//CELL_SIZE  # Экранная координата (0..7 слева направо)
                    by = (my-OFFSET_Y)//CELL_SIZE  # Экранная координата (0..7 сверху вниз)
                    
                    # 🔹 ПРЕОБРАЗОВАНИЕ КООРДИНАТ: экран → доска
                    if GAME_MODE == "offline":
                        # В оффлайне доска переворачивается для игрока 2 (белых)
                        if current_turn == 2:
                            bx = BOARD_SIZE - 1 - bx
                            by = BOARD_SIZE - 1 - by
                        player = current_turn
                    else:  # online
                        if MY_ROLE == 2:
                            bx = BOARD_SIZE - 1 - bx
                            by = BOARD_SIZE - 1 - by
                        player = MY_ROLE
                    
                    if GAME_MODE == "online":
                        send_move(bx, by)
                    else:  # 🔹 ОФФЛАЙН: локальный ход
                        if make_offline_move(bx, by, player):
                            play_sound("place")
                            # Анимация: помечаем поставленную фишку
                            flipped_pieces = [{'x': bx, 'y': by, 'progress': 0.0}]
                            anim_progress = 0.0
                            play_sound("flip")
                            switch_turn_offline()
                        else:
                            show_error("⛔ Недопустимый ход!")

        elif game_state == "game_over" and event.type == pygame.KEYDOWN:
            sc = count_scores()
            if GAME_MODE == "offline":
                my_score = sc[current_turn]
            else:
                my_score = sc.get(MY_ROLE, 0)
            is_rec = my_score > 0 and (not highscores or my_score > highscores[0].get("score",0))
            
            if event.key == pygame.K_RETURN and is_rec and input_name.strip() and not record_saved:
                name = input_name.strip()
                idx = next((i for i,r in enumerate(highscores) if r["name"].lower()==name.lower()), None)
                if idx is not None:
                    if my_score > highscores[idx]["score"]: highscores[idx]["score"] = my_score
                else:
                    highscores.append({"name": name, "score": my_score})
                highscores.sort(key=lambda x: x["score"], reverse=True)
                highscores = highscores[:10]
                save_highscores()
                input_name = ""; record_saved = True
                print("🏆 Рекорд сохранён!")
            elif event.key == pygame.K_BACKSPACE and is_rec and not record_saved:
                input_name = input_name[:-1]
            elif is_rec and not record_saved and event.unicode.isprintable() and len(input_name) < 12:
                input_name += event.unicode

    screen.fill((0, 40, 0))
    if game_state == "menu": draw_menu()
    elif game_state == "connect": connect_btn = draw_connect_screen()
    else:
        draw_board()
        if game_state == "playing" and (GAME_MODE == "offline" or is_my_turn):
            player = current_turn if GAME_MODE == "offline" else MY_ROLE
            for vx, vy in get_valid_moves(player):
                dx = (BOARD_SIZE-1-vx) if (current_turn if GAME_MODE=="offline" else MY_ROLE)==2 else vx
                dy = (BOARD_SIZE-1-vy) if (current_turn if GAME_MODE=="offline" else MY_ROLE)==2 else vy
                pygame.draw.rect(screen, (255,255,0) if player==1 else (0,255,255),
                                pygame.Rect(OFFSET_X+dx*CELL_SIZE+4, OFFSET_Y+dy*CELL_SIZE+4, CELL_SIZE-8, CELL_SIZE-8), 2)
        draw_ui()
        if game_state == "game_over": draw_game_over()
        
    if show_help: draw_help()
    if show_scores: draw_highscores()
    pygame.display.flip()

if sock: 
    try: sock.close()
    except: pass
pygame.quit()
sys.exit()