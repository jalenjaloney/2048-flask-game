import random

def init_board():
    board = [[0] * 4 for _ in range(4)]
    add_new_tile(board)
    add_new_tile(board)
    return board

def add_new_tile(board):
    empty_cells = [(r, c) for r in range(4) for c in range(4) if board[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        board[r][c] = 2 if random.random() < 0.9 else 4

def move_left(board, score):
    def compress(row):
        new_row = [num for num in row if num != 0]
        new_row += [0] * (4 - len(new_row))
        return new_row

    def merge(row):
        local_score = 0
        for i in range(3):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                local_score += row[i]
                row[i + 1] = 0
        return row, local_score

    moved = False
    for r in range(4):
        compressed = compress(board[r])
        merged, gained = merge(compressed)
        new_row = compress(merged)
        if board[r] != new_row:
            moved = True
        board[r] = new_row
        score += gained
    return moved, score

def rotate_board(board):
    return [list(row) for row in zip(*board[::-1])]

def move(board, direction, score):
    rotated_times = {'up': 3, 'right': 2, 'down': 1, 'left': 0}[direction]
    for _ in range(rotated_times):
        board = rotate_board(board)
    moved, score = move_left(board, score)
    for _ in range((4 - rotated_times) % 4):
        board = rotate_board(board)
    if moved:
        add_new_tile(board)
    return board, moved, score

def check_win(board):
    for row in board:
        if 2048 in row:
            return True
    return False

def check_game_over(board):
    for r in range(4):
        for c in range(4):
            if board[r][c] == 0:
                return False
            if r < 3 and board[r][c] == board[r + 1][c]:
                return False
            if c < 3 and board[r][c] == board[r][c + 1]:
                return False
    return True