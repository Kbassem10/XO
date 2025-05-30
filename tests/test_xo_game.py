import sys
sys.path.append('/home/kbassem/code/XO')

# Use direct imports from the utils directory
from utils.game_instructions import game_finish, check_winner, is_draw, get_game_result
from utils.minimax import minimax
from utils.find_best_move import find_best_move

def create_board(layout):
    """Helper function to create a board from a string layout"""
    return [list(layout[i:i+3]) for i in range(0, 9, 3)]

def print_board(board):
    """Helper function to print the board"""
    for row in board:
        print('|'.join(row))
        print('-----')

def test_check_winner():
    print("Testing check_winner function...")
    
    # Test X wins (row)
    board1 = create_board("XXX      ")
    result1 = check_winner(board1)
    print(f"Board1 (X row win): {board1}")
    print(f"Result: {result1}")
    assert result1 == 'X', "X should win in row 1"
    
    # Test O wins (column)
    board2 = create_board("O  O  O  ")
    result2 = check_winner(board2)
    print(f"Board2 (O column win): {board2}")
    print(f"Result: {result2}")
    assert result2 == 'O', "O should win in column 1"
    
    # Test X wins (diagonal)
    board3 = create_board("X   X   X")
    result3 = check_winner(board3)
    print(f"Board3 (X diagonal win): {board3}")
    print(f"Result: {result3}")
    assert result3 == 'X', "X should win in diagonal"
    
    # Test no winner - FIXED: This board truly has no winning lines
    board4 = create_board("XO OXX O ")  # Changed to have no winners
    result4 = check_winner(board4)
    print(f"Board4 (no winner): {board4}")
    print(f"Result: {result4}")
    assert result4 is None, "No winner in this board"
    
    print("✅ check_winner tests passed!")

def test_is_draw():
    print("Testing is_draw function...")
    
    # Test draw - create a proper draw scenario
    board1 = create_board("XOXXOXOXO")  # This is a real draw
    result1 = is_draw(board1)
    print(f"Board1 (draw): {board1}")
    print(f"Is draw: {result1}")
    assert result1 == True, "Should be a draw"
    
    # Test not draw (game ongoing)
    board2 = create_board("XO X     ")
    assert is_draw(board2) == False, "Should not be a draw"
    
    # Test not draw (winner exists)
    board3 = create_board("XXX      ")
    assert is_draw(board3) == False, "Should not be a draw when there's a winner"
    
    print("✅ is_draw tests passed!")

def test_game_finish():
    print("Testing game_finish function...")
    
    # Test finished game (winner)
    board1 = create_board("XXX      ")
    assert game_finish(board1) == True, "Game should be finished"
    
    # Test finished game (draw)
    board2 = create_board("XOXXOXOXO")  # Use proper draw board
    assert game_finish(board2) == True, "Game should be finished (draw)"
    
    # Test ongoing game
    board3 = create_board("X O   O X")
    assert game_finish(board3) == False, "Game should be ongoing"
    
    print("✅ game_finish tests passed!")

def test_get_game_result():
    print("Testing get_game_result function...")
    
    # Test X wins
    board1 = create_board("XXX      ")
    assert get_game_result(board1) == 'X_WINS', "Should return X_WINS"
    
    # Test O wins
    board2 = create_board("OOO      ")
    assert get_game_result(board2) == 'O_WINS', "Should return O_WINS"
    
    # Test draw
    board3 = create_board("XOXXOXOXO")  # Use proper draw board
    assert get_game_result(board3) == 'DRAW', "Should return DRAW"
    
    # Test ongoing
    board4 = create_board("X O   O X")
    assert get_game_result(board4) == 'ONGOING', "Should return ONGOING"
    
    print("✅ get_game_result tests passed!")

def test_minimax():
    print("Testing minimax function...")
    
    # Test AI winning position
    board1 = create_board("OO       ")
    score = minimax(board1, True)
    print(f"AI winning position score: {score}")
    assert score == 1, f"AI should see winning move, got {score}"
    
    # Test AI losing position
    board2 = create_board("XX       ")
    score = minimax(board2, False)
    print(f"AI losing position score: {score}")
    assert score == -1, f"AI should see losing position, got {score}"
    
    # Test finished game
    board3 = create_board("XXX      ")
    score = minimax(board3, True)
    print(f"Finished game score: {score}")
    assert score == -1, f"Should return -1 for X win, got {score}"
    
    print("✅ minimax tests passed!")

def test_find_best_move():
    print("Testing find_best_move function...")
    
    # Test obvious winning move
    board1 = create_board("OO       ")
    move = find_best_move(board1)
    print(f"Best move for OO_: {move}")
    expected_move = (0, 2)  # Should complete the row
    assert move == expected_move, f"Expected {expected_move}, got {move}"
    
    print("✅ find_best_move tests passed!")

def test_integration():
    print("Testing integration - Full game scenario...")
    
    # Simulate a game
    board = [[' ' for _ in range(3)] for _ in range(3)]
    
    # Human move
    board[0][0] = 'X'
    print("After human move:")
    print_board(board)
    
    # Check game state
    print(f"Game finished: {game_finish(board)}")
    print(f"Game result: {get_game_result(board)}")
    
    # AI move
    ai_move = find_best_move(board)
    if ai_move:
        board[ai_move[0]][ai_move[1]] = 'O'
        print("After AI move:")
        print_board(board)
    
    print("✅ Integration test works!")

def run_all_tests():
    print("🎮 Testing XO Game Functions\n")
    print("=" * 40)
    
    try:
        test_check_winner()
        test_is_draw()
        test_game_finish()
        test_get_game_result()
        test_minimax()
        test_find_best_move()
        test_integration()
        
        print("\n" + "=" * 40)
        print("🎉 All tests passed!")
        
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
    except Exception as e:
        print(f"💥 Error running tests: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()