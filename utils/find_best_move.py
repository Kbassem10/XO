from .minimax import minimax

def find_best_move(board):
    best_score = -2
    best_move = None
    for row in range(3):
            for column in range(3):
                if board[row][column] == ' ':
                    board[row][column] = 'O'
                    score = minimax(board, is_ai_turn = False)
                    board[row][column] = ' '

                    if score > best_score:
                         best_score = score
                         best_move = (row, column)
    return best_move