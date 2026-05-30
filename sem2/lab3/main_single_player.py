import pygame
import json
import os
import sys
import math
from pygame import mixer

# ====================== ЗАГРУЗКА КОНФИГУРАЦИИ ======================
def load_config():
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        config = {
            "board_size": 8,
            "fps": 60,
            "bg_music_volume": 0.5,
            "sound_volume": 0.8
        }
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
        return config

CONFIG = load_config()

# ====================== ИНИЦИАЛИЗАЦИЯ ======================
pygame.init()

# === СНАЧАЛА пути, потом микшер ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUNDS_DIR = os.path.join(BASE_DIR, 'assets', 'sounds')

if not mixer.get_init():
    mixer.init()

info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# Адаптивные размеры
BOARD_SIZE = CONFIG["board_size"]
MIN_CELL_SIZE = 50
MAX_CELL_SIZE = 90

available_width = SCREEN_WIDTH - 120
available_height = SCREEN_HEIGHT - 180

max_cell_by_width = available_width // BOARD_SIZE
max_cell_by_height = available_height // BOARD_SIZE

CELL_SIZE = min(max_cell_by_width, max_cell_by_height, MAX_CELL_SIZE)
CELL_SIZE = max(CELL_SIZE, MIN_CELL_SIZE)

BOARD_WIDTH = BOARD_SIZE * CELL_SIZE
BOARD_HEIGHT = BOARD_SIZE * CELL_SIZE
OFFSET_X = (SCREEN_WIDTH - BOARD_WIDTH) // 2
OFFSET_Y = 100

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Reversi (Отелло) — Игра на двоих")
clock = pygame.time.Clock()

# Адаптивные шрифты
def get_font(size):
    return pygame.font.SysFont("arial", int(size * CELL_SIZE / 70))

font = get_font(36)
small_font = get_font(24)
medium_font = get_font(28)

# ====================== ЗВУКИ И МУЗЫКА ======================
def load_sounds():
    sounds = {}
    try:
        sounds["place"] = mixer.Sound(os.path.join(SOUNDS_DIR, "place.wav"))
        sounds["flip"] = mixer.Sound(os.path.join(SOUNDS_DIR, "flip.wav"))
        sounds["place"].set_volume(CONFIG["sound_volume"])
        sounds["flip"].set_volume(CONFIG["sound_volume"])
        print("✅ Звуки загружены")
    except Exception as e:
        print(f"❌ Ошибка звуков: {e}")
        sounds["place"] = None
        sounds["flip"] = None
    return sounds

sounds = load_sounds()

try:
    mixer.music.load(os.path.join(SOUNDS_DIR, "background_music.mp3"))
    mixer.music.set_volume(CONFIG["bg_music_volume"])
    mixer.music.play(-1)
    print("🎵 Музыка запущена")
except Exception as e:
    print(f"❌ Ошибка музыки: {e}")

# ====================== ЛОГИКА ИГРЫ ======================
DIRECTIONS = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

def new_board():
    b = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    b[3][3] = b[4][4] = 2
    b[3][4] = b[4][3] = 1
    return b

def is_valid_move(board, player, x, y):
    if board[y][x] != 0: return False
    opponent = 3 - player
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        if not (0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE): continue
        if board[ny][nx] != opponent: continue
        while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[ny][nx] == opponent:
            nx += dx
            ny += dy
        if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[ny][nx] == player:
            return True
    return False

def get_valid_moves(board, player):
    return [(x, y) for y in range(BOARD_SIZE) for x in range(BOARD_SIZE) if is_valid_move(board, player, x, y)]

def get_flips(board, player, x, y):
    flips = []
    opponent = 3 - player
    for dx, dy in DIRECTIONS:
        line = []
        nx, ny = x + dx, y + dy
        while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[ny][nx] == opponent:
            line.append((nx, ny))
            nx += dx
            ny += dy
        if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[ny][nx] == player and line:
            flips.extend(line)
    return flips

def make_move(board, player, x, y):
    board[y][x] = player
    flips = get_flips(board, player, x, y)
    for fx, fy in flips:
        board[fy][fx] = player
    return flips

def rotate_board_180(board):
    return [row[::-1] for row in board[::-1]]

# ✅ НОВАЯ ФУНКЦИЯ: считаем фишки напрямую на доске
def get_board_scores(board):
    """Возвращает актуальный счёт, пересчитывая все фишки на поле"""
    s = {1: 0, 2: 0}
    for row in board:
        for cell in row:
            if cell == 1:
                s[1] += 1
            elif cell == 2:
                s[2] += 1
    return s

# ====================== HIGHSCORES ======================
def load_highscores():
    if os.path.exists('highscores.json'):
        with open('highscores.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_highscores(scores):
    with open('highscores.json', 'w', encoding='utf-8') as f:
        json.dump(scores, f, indent=4, ensure_ascii=False)

highscores = load_highscores()

# ====================== ПЕРЕМЕННЫЕ ======================
board = new_board()
current_player = 1
game_state = "menu"
flipped_pieces = []
anim_progress = 0.0
is_flipped_view = False
input_name = ""
show_help = False
show_scores = False
menu_buttons = []

# ====================== ОТРИСОВКА ======================
def draw_board():
    if game_state == "game_over":
        screen.fill((20, 20, 40))
    else:
        screen.fill((0, 40, 0))
    
    if game_state != "game_over":
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                rect = pygame.Rect(OFFSET_X + x*CELL_SIZE, OFFSET_Y + y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, (0, 100, 0), rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, max(2, CELL_SIZE//35))

                draw_x = (BOARD_SIZE - 1 - x) if is_flipped_view else x
                draw_y = (BOARD_SIZE - 1 - y) if is_flipped_view else y
                value = board[draw_y][draw_x]

                if value == 0: continue

                progress = 1.0
                for fp in flipped_pieces:
                    if fp['x'] == draw_x and fp['y'] == draw_y:
                        progress = fp['progress']
                        break

                cx = OFFSET_X + x * CELL_SIZE + CELL_SIZE // 2
                cy = OFFSET_Y + y * CELL_SIZE + CELL_SIZE // 2

                scale = abs(math.cos(progress * math.pi)) if progress < 1 else 1.0
                radius = int((CELL_SIZE // 2 - 5) * scale)

                color = (20, 20, 20) if value == 1 else (240, 240, 240)
                pygame.draw.circle(screen, color, (cx, cy), radius)

                if scale > 0.7:
                    pygame.draw.circle(screen, (255, 255, 255, 80), (cx - radius//3, cy - radius//3), radius//3)

        if game_state == "playing":
            valid = get_valid_moves(board, current_player)
            color = (255, 255, 0) if current_player == 1 else (0, 255, 255)
            border = max(3, CELL_SIZE // 20)
            for vx, vy in valid:
                dx = (BOARD_SIZE - 1 - vx) if is_flipped_view else vx
                dy = (BOARD_SIZE - 1 - vy) if is_flipped_view else vy
                r = pygame.Rect(OFFSET_X + dx*CELL_SIZE + border, 
                               OFFSET_Y + dy*CELL_SIZE + border, 
                               CELL_SIZE - border*2, 
                               CELL_SIZE - border*2)
                pygame.draw.rect(screen, color, r, border)

def draw_ui():
    title_size = int(36 * CELL_SIZE / 70)
    title_font = pygame.font.SysFont("arial", title_size)
    title = title_font.render("REVERSI", True, (0, 255, 100))
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 10))

    if game_state == "playing":
        # ✅ Считаем очки напрямую с доски
        current_scores = get_board_scores(board)
        
        txt = font.render(f"Ход {'ЧЁРНЫХ' if current_player==1 else 'БЕЛЫХ'}", True, (255, 255, 100))
        screen.blit(txt, (SCREEN_WIDTH//2 - txt.get_width()//2, OFFSET_Y - 45))

        s1 = small_font.render(f"● Чёрные: {current_scores[1]}", True, (20, 20, 20))
        s2 = small_font.render(f"○ Белые: {current_scores[2]}", True, (240, 240, 240))
        screen.blit(s1, (20, OFFSET_Y - 45))
        screen.blit(s2, (SCREEN_WIDTH - s2.get_width() - 20, OFFSET_Y - 45))
        
        exit_text = small_font.render("ESC - выход в меню", True, (200, 200, 100))
        screen.blit(exit_text, (SCREEN_WIDTH//2 - exit_text.get_width()//2, SCREEN_HEIGHT - 30))

def draw_menu():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    menu_w = 500
    menu_h = 450
    menu_x = (SCREEN_WIDTH - menu_w) // 2
    menu_y = (SCREEN_HEIGHT - menu_h) // 2
    
    pygame.draw.rect(screen, (0, 60, 0), (menu_x, menu_y, menu_w, menu_h))
    pygame.draw.rect(screen, (0, 150, 0), (menu_x, menu_y, menu_w, menu_h), 3)
    
    title = font.render("REVERSI", True, (0, 255, 100))
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, menu_y + 30))
    
    btn_w = 300
    btn_h = 50
    
    btn1 = pygame.Rect(menu_x + (menu_w - btn_w)//2, menu_y + 100, btn_w, btn_h)
    pygame.draw.rect(screen, (0, 100, 0), btn1)
    pygame.draw.rect(screen, (0, 200, 0), btn1, 3)
    surf1 = medium_font.render("НАЧАТЬ ИГРУ", True, (0, 255, 100))
    screen.blit(surf1, (btn1.centerx - surf1.get_width()//2, btn1.centery - surf1.get_height()//2))
    
    btn2 = pygame.Rect(menu_x + (menu_w - btn_w)//2, menu_y + 170, btn_w, btn_h)
    pygame.draw.rect(screen, (0, 100, 0), btn2)
    pygame.draw.rect(screen, (0, 200, 0), btn2, 3)
    surf2 = medium_font.render("ТАБЛИЦА РЕКОРДОВ", True, (0, 255, 100))
    screen.blit(surf2, (btn2.centerx - surf2.get_width()//2, btn2.centery - surf2.get_height()//2))
    
    btn3 = pygame.Rect(menu_x + (menu_w - btn_w)//2, menu_y + 240, btn_w, btn_h)
    pygame.draw.rect(screen, (0, 100, 0), btn3)
    pygame.draw.rect(screen, (0, 200, 0), btn3, 3)
    surf3 = medium_font.render("СПРАВКА", True, (0, 255, 100))
    screen.blit(surf3, (btn3.centerx - surf3.get_width()//2, btn3.centery - surf3.get_height()//2))
    
    btn4 = pygame.Rect(menu_x + (menu_w - btn_w)//2, menu_y + 310, btn_w, btn_h)
    pygame.draw.rect(screen, (0, 100, 0), btn4)
    pygame.draw.rect(screen, (0, 200, 0), btn4, 3)
    surf4 = medium_font.render("ВЫХОД", True, (0, 255, 100))
    screen.blit(surf4, (btn4.centerx - surf4.get_width()//2, btn4.centery - surf4.get_height()//2))
    
    global menu_buttons
    menu_buttons = [btn1, btn2, btn3, btn4]
    
    tip = small_font.render("Или нажмите 1, 2, 3, Esc", True, (100, 255, 100))
    screen.blit(tip, (SCREEN_WIDTH//2 - tip.get_width()//2, menu_y + menu_h - 40))

def draw_help():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    w, h = 700, 550
    x = (SCREEN_WIDTH - w) // 2
    y = (SCREEN_HEIGHT - h) // 2
    
    pygame.draw.rect(screen, (30, 30, 50), (x, y, w, h))
    pygame.draw.rect(screen, (100, 200, 100), (x, y, w, h), 3)
    
    title = font.render("ПРАВИЛА ИГРЫ REVERSI", True, (255, 215, 0))
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, y + 20))
    
    rules = [
        "1. Игроки по очереди ставят фишки на доску 8x8.",
        "2. Фишка ставится так, чтобы окружить фишки противника.",
        "3. Все окружённые фишки переворачиваются.",
        "4. Если ходов нет — игрок пропускает ход.",
        "5. Игра заканчивается, когда доска заполнена.",
        "6. Побеждает игрок с большим количеством фишек.",
        "",
        "УПРАВЛЕНИЕ:",
        "• Клик мышью по клетке — сделать ход",
        "• ESC — выйти в меню (во время игры)",
        "",
        "Нажмите любую клавишу или кликните для закрытия"
    ]
    
    for i, rule in enumerate(rules):
        surf = small_font.render(rule, True, (220, 220, 220))
        screen.blit(surf, (x + 50, y + 80 + i * 35))

def draw_highscores():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    w, h = 500, 450
    x = (SCREEN_WIDTH - w) // 2
    y = (SCREEN_HEIGHT - h) // 2
    
    pygame.draw.rect(screen, (30, 30, 50), (x, y, w, h))
    pygame.draw.rect(screen, (100, 200, 100), (x, y, w, h), 3)
    
    title = font.render("ТАБЛИЦА РЕКОРДОВ", True, (255, 215, 0))
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, y + 20))
    
    if highscores:
        y_pos = y + 80
        for i, rec in enumerate(highscores[:10]):
            text = f"{i+1}. {rec['name']} — {rec['score']} очков"
            surf = medium_font.render(text, True, (200, 255, 200))
            screen.blit(surf, (x + 80, y_pos))
            y_pos += 40
    else:
        surf = font.render("Нет рекордов", True, (200, 200, 200))
        screen.blit(surf, (SCREEN_WIDTH//2 - surf.get_width()//2, y + 200))
    
    tip = small_font.render("Нажмите любую клавишу или кликните для выхода", True, (150, 150, 100))
    screen.blit(tip, (SCREEN_WIDTH//2 - tip.get_width()//2, y + h - 40))

def draw_game_over():
    screen.fill((20, 20, 40))
    
    # ✅ Финальный пересчёт очков с доски
    final_scores = get_board_scores(board)
    black_score = final_scores[1]
    white_score = final_scores[2]
    
    if black_score > white_score:
        winner = "ПОБЕДИЛИ ЧЁРНЫЕ!"
        winner_color = (200, 200, 200)
    elif white_score > black_score:
        winner = "ПОБЕДИЛИ БЕЛЫЕ!"
        winner_color = (255, 255, 255)
    else:
        winner = "НИЧЬЯ!"
        winner_color = (255, 215, 0)
    
    res = font.render(winner, True, winner_color)
    screen.blit(res, (SCREEN_WIDTH//2 - res.get_width()//2, SCREEN_HEIGHT//2 - 150))
    
    sc = font.render(f"Чёрные: {black_score}    Белые: {white_score}", True, (200, 255, 200))
    screen.blit(sc, (SCREEN_WIDTH//2 - sc.get_width()//2, SCREEN_HEIGHT//2 - 80))
    
    max_score = max(black_score, white_score)
    is_record = False
    if black_score != white_score:
        if not highscores or max_score > highscores[0].get("score", 0):
            is_record = True
    
    if is_record:
        prompt = medium_font.render("НОВЫЙ РЕКОРД! Введите имя и нажмите Enter:", True, (255, 255, 100))
        screen.blit(prompt, (SCREEN_WIDTH//2 - prompt.get_width()//2, SCREEN_HEIGHT//2))
        name_surf = font.render(input_name + "_", True, (255, 255, 255))
        screen.blit(name_surf, (SCREEN_WIDTH//2 - name_surf.get_width()//2, SCREEN_HEIGHT//2 + 60))
    else:
        prompt = medium_font.render("Нажмите любую клавишу для выхода в меню", True, (150, 150, 100))
        screen.blit(prompt, (SCREEN_WIDTH//2 - prompt.get_width()//2, SCREEN_HEIGHT//2 + 40))

# ====================== ОСНОВНОЙ ЦИКЛ ======================
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # ========== ГЛОБАЛЬНЫЙ ESC ==========
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if game_state == "playing":
                game_state = "menu"
                show_help = False
                show_scores = False
            elif show_help or show_scores:
                show_help = False
                show_scores = False
            elif game_state == "menu":
                running = False
            continue
        
        # ========== ОБРАБОТКА СОСТОЯНИЙ ==========
        
        # --- МЕНЮ ---
        if game_state == "menu":
            if show_help:
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    show_help = False
            elif show_scores:
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    show_scores = False
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    for i, btn in enumerate(menu_buttons):
                        if btn.collidepoint(mx, my):
                            if i == 0:  # Начать игру
                                game_state = "playing"
                                board = new_board()
                                current_player = 1
                                is_flipped_view = False
                                flipped_pieces = []
                                anim_progress = 0.0
                            elif i == 1:  # Рекорды
                                show_scores = True
                            elif i == 2:  # Справка
                                show_help = True
                            elif i == 3:  # Выход
                                running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        game_state = "playing"
                        board = new_board()
                        current_player = 1
                        is_flipped_view = False
                        flipped_pieces = []
                        anim_progress = 0.0
                    elif event.key == pygame.K_2:
                        show_scores = True
                    elif event.key == pygame.K_3:
                        show_help = True
        
        # --- ИГРА ---
        elif game_state == "playing":
            if event.type == pygame.MOUSEBUTTONDOWN and not flipped_pieces:
                mx, my = event.pos
                if OFFSET_X <= mx < OFFSET_X + BOARD_WIDTH and OFFSET_Y <= my < OFFSET_Y + BOARD_HEIGHT:
                    bx = (mx - OFFSET_X) // CELL_SIZE
                    by = (my - OFFSET_Y) // CELL_SIZE

                    if is_flipped_view:
                        bx = BOARD_SIZE - 1 - bx
                        by = BOARD_SIZE - 1 - by

                    if is_valid_move(board, current_player, bx, by):
                        flips = make_move(board, current_player, bx, by)
                        # ✅ УБРАНО ручное начисление очков — теперь считаем с доски

                        flipped_pieces = [{'x': fx, 'y': fy, 'progress': 0.0} for fx, fy in flips]
                        anim_progress = 0.0

                        if sounds.get("place"):
                            sounds["place"].play()
                        if sounds.get("flip") and flips:
                            sounds["flip"].play()
        
        # --- GAME OVER ---
        elif game_state == "game_over":
            if event.type == pygame.KEYDOWN:
                final_scores = get_board_scores(board)  # ✅ Пересчитываем
                max_score = max(final_scores[1], final_scores[2])
                is_record = (final_scores[1] != final_scores[2]) and (not highscores or max_score > highscores[0].get("score", 0))
                
                if is_record and event.key == pygame.K_RETURN and input_name.strip():
                    highscores.append({"name": input_name.strip(), "score": max_score})
                    highscores.sort(key=lambda x: x["score"], reverse=True)
                    highscores = highscores[:10]
                    save_highscores(highscores)
                    game_state = "menu"
                    input_name = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_name = input_name[:-1]
                elif event.key == pygame.K_ESCAPE:
                    game_state = "menu"
                    input_name = ""
                elif not is_record:
                    game_state = "menu"
                else:
                    if event.unicode.isprintable() and len(input_name) < 12:
                        input_name += event.unicode
    
    # ========== АНИМАЦИЯ ==========
    if flipped_pieces:
        anim_progress += 0.08
        for p in flipped_pieces:
            p['progress'] = min(anim_progress, 1.0)

        if anim_progress >= 1.0:
            board = rotate_board_180(board)
            is_flipped_view = not is_flipped_view
            current_player = 3 - current_player
            flipped_pieces = []

            if not get_valid_moves(board, current_player):
                current_player = 3 - current_player
                if not get_valid_moves(board, current_player):
                    game_state = "game_over"
    
    # ========== ОТРИСОВКА ==========
    if game_state == "game_over":
        draw_game_over()
    else:
        draw_board()
        draw_ui()
        
        if game_state == "menu" and not show_help and not show_scores:
            draw_menu()
        
        if show_help:
            draw_help()
        
        if show_scores:
            draw_highscores()
    
    pygame.display.flip()
    clock.tick(CONFIG["fps"])

pygame.quit()
sys.exit()