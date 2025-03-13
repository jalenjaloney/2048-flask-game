from flask import Flask, render_template, request, jsonify
from app import *
from waitress import serve

app = Flask(__name__)

# Global game state
board = None
score = 0
win_acknowledged = False

@app.route('/')
def index():
    global board, score, win_acknowledged
    return render_template('index.html', board=board, score=score, win=False, game_over=False)

@app.route('/new_game', methods=['POST'])
def new_game():
    global board, score, win_acknowledged
    board = init_board()
    score = 0
    win_acknowledged = False
    return jsonify({'board': board, 'score': score, 'win': False, 'game_over': False})

@app.route('/move', methods=['POST'])
def move_board():
    global board, score, win_acknowledged
    direction = request.json.get('direction')
    board, moved, score = move(board, direction, score)
    win = check_win(board) and not win_acknowledged
    game_over = check_game_over(board) if not win else False
    return jsonify({'board': board, 'score': score, 'win': win, 'game_over': game_over})

@app.route('/continue', methods=['POST'])
def continue_game():
    global win_acknowledged
    win_acknowledged = True
    return jsonify({'success': True})

if __name__ == '__main__':
    board = init_board()
    score = 0
    win_acknowledged = False
    serve(app, host = "0.0.0.0", port = 8000)