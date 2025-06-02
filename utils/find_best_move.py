from .minimax import minimax
import time

def find_best_move(board):
    best_score = -2 #initialize the best score to less than the minimum possible score
    best_move = None #initialize the best move to None
    memo = {} #create a memo dictionary for dynamic programming

    for row in range(3): #loop for the range of the XO game rows
            for column in range(3): #loop for the range of the XO game columns
                if board[row][column] == ' ': #check the not played yet cells
                    board[row][column] = 'O' #set it as O played for now

                    score = minimax(board, is_ai_turn=False, memo=memo) #calculate the score using minimax algorithm

                    board[row][column] = ' ' #unset again what we have done

                    if score > best_score: #if this move gives a better score
                         best_score = score #update the best score
                         best_move = (row, column) #update the best move coordinates
    return best_move #return the best move found