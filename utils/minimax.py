from .game_instructions import game_finish, check_winner
def minimax(board, is_ai_turn):

    if game_finish(board):
        winner = check_winner(board)
        
        if winner == 'O':  # AI wins
            return 1
        elif winner == 'X':  # Human wins
            return -1
        else:  # Draw or ongoing
            return 0
        
    if is_ai_turn:
        best_score = -2
        for row in range(3):
            for column in range(3):
                if board[row][column] == ' ':
                    board[row][column] = 'O'
                    score = minimax(board, is_ai_turn = False)
                    board[row][column] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = 2
        for row in range(3):
            for column in range(3):
                if board[row][column] == ' ':
                    board[row][column] = 'X'
                    score = minimax(board, is_ai_turn = True)
                    board[row][column] = ' '
                    best_score = min(score, best_score)
        return best_score