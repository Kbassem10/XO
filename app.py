from flask import Flask, render_template, redirect, json, jsonify, request
from utils.find_best_move import find_best_move
from utils.game_instructions import *

app = Flask(__name__)

@app.route("/")
def index():
    board = create_empty_board() #create an empty 3x3 board
    return render_template("index.html", board=board) #render the HTML template with the board

@app.route("/play", methods=["POST"]) #define the route for playing moves via POST request
def play():
    try: #try to execute the game logic
        data = request.get_json() #get the JSON data from the request
        if not data or 'board' not in data: #check if the request contains valid board data
            return jsonify({'error': 'Invalid request - board data required'}), 400 #return error if invalid
            
        board = parse_board(data['board']) #parse the board data from the request

        if game_finish(board): #check if the game is finished
            result = get_game_result(board) #get the game result
            return jsonify({ #return the finished game status
                'game_status': 'finished',
                'result': result,
                'board': board
            })
        
        best_move = find_best_move(board) #find the best move for AI using minimax
        if best_move is None: #check if no valid moves are available
            return jsonify({'error': 'No valid moves available'}), 400 #return error if no moves
            
        board[best_move[0]][best_move[1]] = "O" #make the AI move on the board

        # Check game status after AI move
        if game_finish(board): #check if the game is finished after AI move
            result = get_game_result(board) #get the game result
            return jsonify({ #return the finished game status
                'game_status': 'finished',
                'result': result,
                'board': board
            })
        else: #if the game is still ongoing
            return jsonify({ #return the ongoing game status
                'game_status': 'ongoing',
                'result': 'ONGOING',
                'board': board
            })
        
    except Exception as e: #catch any exceptions that occur
        return jsonify({'error': f'Server error: {str(e)}'}), 500 #return server error

@app.route("/reset", methods=['POST']) #define the route for resetting the game via POST request
def reset_game():
    board = create_empty_board() #create a new empty board
    return jsonify({ #return the reset game status
        'game_status': 'reset',
        'result': 'ONGOING',
        'board': board
    })

if __name__ == '__main__': #check if the script is run directly
    app.run(debug=True) #run the Flask app in debug mode
else: #if the script is imported as a module
    application = app #assign the app to application variable for deployment