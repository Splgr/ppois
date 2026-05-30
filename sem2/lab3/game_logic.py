# game_logic.py
BOARD_SIZE = 8
DIRECTIONS = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)] # куда можно передвинуть пешку относительно текущего положения

def new_board():
    b = [[0]*BOARD_SIZE for _ in range(BOARD_SIZE)]
    b[3][3] = b[4][4] = 2
    b[3][4] = b[4][3] = 1
    return b

def is_valid_move(board, player, x, y):
    if board[y][x] != 0: return False #если игрок хочет поставить не на пустую клетку, то ложь
    opponent = 3 - player  # если был игрок 2, то оппонент 3-2=1, а если был 1, то оппонент 3-1=2
    for dx, dy in DIRECTIONS:
        nx, ny = x+dx, y+dy
        if not (0<=nx<BOARD_SIZE and 0<=ny<BOARD_SIZE): continue # если рядом граница поля, то мало что можем сказать о валидности хода
        if board[ny][nx] != opponent: continue # если рядом не оппонент, то есть своя фишка или пустота, то не можем ничего сказать о валидности хода
        # оставшиеся случа скажут о валидности хода
        while 0<=nx<BOARD_SIZE and 0<=ny<BOARD_SIZE and board[ny][nx]==opponent:  # пока клетка рядом содержит фишку противника, двигаемся в том же направлении, пока не встретим свою либо пустую
            nx+=dx; ny+=dy
        if 0<=nx<BOARD_SIZE and 0<=ny<BOARD_SIZE and board[ny][nx]==player:   # встретили свою фишку, значит исходная позиция (x, y) валидна
            return True
    return False   # если не дошли до цикла while, то есть рядом пустые клетки и края поля, либо дошли до цикла while но рядом пустота, чужие фишки, не обрамленные своей, и может быть конец поля

def get_flips(board, player, x, y):
    flips = []
    opponent = 3 - player
    for dx, dy in DIRECTIONS:
        line = []
        nx, ny = x+dx, y+dy
        while 0<=nx<BOARD_SIZE and 0<=ny<BOARD_SIZE and board[ny][nx]==opponent:
            line.append((nx,ny))
            nx+=dx; ny+=dy
        if 0<=nx<BOARD_SIZE and 0<=ny<BOARD_SIZE and board[ny][nx]==player and line:
            flips.extend(line)   # в отличие от append добавит не список line а его объекты
    return flips

def make_move(board, player, x, y):
    board[y][x] = player
    flips = get_flips(board, player, x, y)
    for fx, fy in flips:
        board[fy][fx] = player
    return flips

def get_valid_moves(board, player):
    return [(x,y) for y in range(BOARD_SIZE) for x in range(BOARD_SIZE) if is_valid_move(board, player, x, y)]

def count_scores(board):
    s = {1:0, 2:0}
    for row in board:
        for c in row:
            if c in s: s[c] += 1
    return s

def check_game_over(board):
    return not get_valid_moves(board, 1) and not get_valid_moves(board, 2)