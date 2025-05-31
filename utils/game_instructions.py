import json
def game_finish(board):
    return check_winner(board) is not None or is_draw(board)

def check_winner(board):
    """
    Check if there's a winner on the board.
    
    Args:
        board: 3x3 list representing the game board
        
    Returns:
        str: 'X' if human wins, 'O' if AI wins, None if no winner
    """
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != ' ':
            return row[0]
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != ' ':
            return board[0][col]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]
    
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]
    
    return None

def is_draw(board):
    """
    Check if the game is a draw (board is full with no winner).
    
    Args:
        board: 3x3 list representing the game board
        
    Returns:
        bool: True if it's a draw, False otherwise
    """
    if check_winner(board) is not None:
        return False
    
    # Check if board is full
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    
    return True

def get_game_result(board):
    """
    Get the final result of the game.
    
    Args:
        board: 3x3 list representing the game board
        
    Returns:
        str: 'X_WINS', 'O_WINS', 'DRAW', or 'ONGOING'
    """
    winner = check_winner(board)
    
    if winner == 'X':
        return 'X_WINS'
    elif winner == 'O':
        return 'O_WINS'
    elif is_draw(board):
        return 'DRAW'
    else:
        return 'ONGOING'

def create_empty_board():
    """Create a new empty board"""
    return [[" " for _ in range(3)] for _ in range(3)]

def parse_board(board_string):
    """Parse board from string format to 2D list"""
    try:
        if isinstance(board_string, str):
            # If it's a JSON string, parse it
            board = json.loads(board_string)
        else:
            board = board_string
        
        # Ensure it's a proper 3x3 board
        if len(board) == 3 and all(len(row) == 3 for row in board):
            return board
        else:
            return create_empty_board()
    except:
        return create_empty_board()
