from flask import Flask, render_template, redirect, json, jsonify, request
from utils.find_best_move import find_best_move
from utils.game_instructions import *

app = Flask(__name__)

@app.route("/")
def index():
    board = create_empty_board()
    return render_template("index.html", board=board)

@app.route("/play", methods=["POST"])
def play():
    try:
        data = request.get_json()
        if not data or 'board' not in data:
            return jsonify({'error': 'Invalid request - board data required'}), 400
            
        board = parse_board(data['board'])

        if game_finish(board): #the game is finished
            result = get_game_result(board)
            return jsonify({
                'game_status': 'finished',
                'result': result,
                'board': board
            })
        
        best_move = find_best_move(board)
        if best_move is None:
            return jsonify({'error': 'No valid moves available'}), 400
            
        board[best_move[0]][best_move[1]] = "O"

        # Check game status after AI move
        if game_finish(board):
            result = get_game_result(board)
            return jsonify({
                'game_status': 'finished',
                'result': result,
                'board': board
            })
        else:
            return jsonify({
                'game_status': 'ongoing',
                'result': 'ONGOING',
                'board': board
            })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route("/reset", methods=['POST'])
def reset_game():
    board = create_empty_board()
    return jsonify({
        'game_status': 'reset',
        'result': 'ONGOING',
        'board': board
    })

# For Vercel deployment
app.config['ENV'] = 'production'

if __name__ == '__main__':
    app.run(debug=True)
