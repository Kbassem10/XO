from .game_instructions import game_finish, check_winner

def minimax(board, is_ai_turn, memo=None):

    #using a memo for DP
    if memo==None:
        memo={}

    #convert the list of lists to a tuple and each list of them to tuple too
    #lists in python can't be used as a key of a dict because they are mutable
    board_key = tuple(tuple(row) for row in board)

    #create a key of that it's AI turn and the tuple of tuples
    key = (board_key, is_ai_turn)

    #check if this key we have calculated before or not
    if key in memo:
        return memo[key] #if it's calculated before then return it directly

    if game_finish(board): #check if the game is finished or not
        winner = check_winner(board) #call the function of check_winner to return the winner
        
        if winner == 'O':  #AI wins
            result = 1
        elif winner == 'X':  #human wins
            result = -1
        else:  #draw or ongoing
            result = 0

        return result
        
    if is_ai_turn: #if the game is still going and it's AI turn

        best_score = -2 #set the score to less than the least number
        for row in range(3): #loop for the range of the XO game rows
            for column in range(3):#loop for the range of the XO game columns
                if board[row][column] == ' ': #check the not played yet cells
                    board[row][column] = 'O' #set it as O played for now
                    score = minimax(board, is_ai_turn = False, memo=memo) #try to minimax again for the rest of the options of this recursivly
                    board[row][column] = ' ' #unset again what we have done
                    best_score = max(score, best_score) #calculate the best score till now

        memo[key] = best_score #save the best score on the memo
        return best_score
    
    else: #if the game is still going and it's human turn
        best_score = 2 #set the score to more than the highest number
        for row in range(3): #loop for the range of the XO game rows
            for column in range(3): #loop for the range of the XO game columns
                if board[row][column] == ' ': #check the not played yet cells
                    board[row][column] = 'X' #set it as X played for now
                    score = minimax(board, is_ai_turn = True, memo=memo) #try to minimax again for the rest of the options of this recursively
                    board[row][column] = ' ' #unset again what we have done
                    best_score = min(score, best_score) #calculate the best score till now (minimum for human)

        memo[key] = best_score #save the best score on the memo
        return best_score