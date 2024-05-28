"""
An AI player for Othello. 
"""

import random
import sys
import time

#Board -> A tuple of tuples
#Color -> Integer (0 = Blank, 1 = Black, 2 = White)

# You can use the functions in othello_shared to write your AI
from ai.othello_shared import find_lines, get_possible_moves, get_score, play_move

#The Data Structures I will be using
visited = {}

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)
    
# Method to compute utility value of terminal state
def compute_utility(board, color):
    #IMPLEMENT
    score = get_score(board)
    utility = 0

    if(color == 1):
        utility = score[0]- score[1]

    else:
        utility = score[1] - score[0]

    return utility

#################### HELPERS FOR NEW HEURISTIC END HERE ######################

# Better heuristic value of board
def compute_heuristic(board, color):
    #IMPLEMENT
    
    #1. Compute Utility
    score = get_score(board)
    dim = len(board)
    utilityScore = 0

    if(color == 1):
        utilityScore = score[0]- score[1]

    else:
        utilityScore = score[1] - score[0]
        
    #2. Compute Mobility
    opposingColor = 4 - (color+1)
    mobilityScore = 0 

    points1 = len(get_possible_moves(board,color))
    points2 = len(get_possible_moves(board,opposingColor))
    mobilityScore = points1 - points2
    
    #3. Compute Corners
    topLeft = board[0][0]
    topRight = board[-1][0]
    bottomLeft = board[0][-1]
    bottomRight = board[-1][-1]
    cornerScore = 0
    
    for corner in [topLeft, topRight, bottomLeft, bottomRight]:
        if (corner == color):
            cornerScore = cornerScore + 1000 
        elif (corner == opposingColor):
            cornerScore = cornerScore - 1000
            
    #4. Compute Traps
    sc1 = [(1,0), (0,1), (1,1)] #Top Left
    sc2 = [(-1,1), (-2,0), (-2,1)] #Top Right
    sc3 = [(1,-1), (0, -2), (1,-2)] #Bottom Left
    sc4 = [(-2, -1), (-1, -2),(-2, -2)] #Bottom Right
    subCornerScore = 0

    for a in sc1:
        if(board[a[0]][a[1]] == color):
            if(board[0][0] == color):
                subCornerScore = subCornerScore + 10
            else:
                subCornerScore = subCornerScore - 10
                
        elif(board[a[0]][a[1]] == opposingColor):
            if(board[0][0] == color):
                subCornerScore = subCornerScore + 10
            else:
                subCornerScore = subCornerScore - 10

        else:
            subCornerScore = subCornerScore - 6
                
    for b in sc2:
        if(board[b[0]][b[1]] == color):
            if(board[-1][0] == color):
                subCornerScore = subCornerScore + 10
            else:
                subCornerScore = subCornerScore - 10
                
        elif(board[b[0]][b[1]] == opposingColor):
            if(board[-1][0] == color):
                subCornerScore = subCornerScore + 10
            else:
                subCornerScore = subCornerScore - 10

        else:
            subCornerScore = subCornerScore - 6

    for c in sc3:
        if(board[c[0]][c[1]] == color):
            if(board[0][-1] == color):
                subCornerScore = subCornerScore + 10
            else:
                subCornerScore = subCornerScore - 10
                
        elif(board[c[0]][c[1]] == opposingColor):
            if(board[0][-1] == color):
                subCornerScore = subCornerScore + 10
            else:
                subCornerScore = subCornerScore - 10

        else:
            subCornerScore = subCornerScore - 6


    for d in sc4:
        if(board[d[0]][d[1]] == color):
            if(board[-1][-1] == color):
                subCornerScore = subCornerScore + 10
            else:
                subCornerScore = subCornerScore - 10
                
        elif(board[d[0]][d[1]] == opposingColor):
            if(board[-1][-1] == color):
                subCornerScore = subCornerScore + 10
            else:
                subCornerScore = subCornerScore - 10

        else:
            subCornerScore = subCornerScore - 6

    #GRAND TOTAL
    total = 3*utilityScore + mobilityScore + cornerScore + subCornerScore
    
    return total

############ MINIMAX, we wanna play around w/utility points ###############################
def minimax_min_node(board, color, limit, caching = 0):
    #IMPLEMENT

    global visited
    curState = color, board
    opposingColor = 4 - (color+1)
    
    ##Caching case #1: Trying to visit a state we've already visited
    if(caching == 1 and curState in visited):
        return visited[curState]

    if(limit == 0):
        result = (None, compute_utility(board,color))
        return result

    allMoves = get_possible_moves(board, opposingColor)
        
    minUtility = float("inf")
    worstMove = None

    if(allMoves == []):
        result = (None, compute_utility(board,color))
    ##Caching case #2: We reached the end, so we should put a "visited tag" on it.
        if(caching == 1):
            visited[curState] = result
        return result

    for moves in allMoves:
        nextState = play_move(board, opposingColor, moves[0], moves[1])

        #We want to see the opposing players' moves, then pick a move that minimizes
        #such. We want to move player, NOT the computer (hence why I don't adjust colour
        #when I call the utility function. 
        utility = minimax_max_node(nextState, color, limit-1, caching)[1]

        if(utility < minUtility):
            worstMove = moves
            minUtility = utility

    result = worstMove, minUtility

    ##Caching Case #3: Done searching a node that's not a leaf node.
    if(caching == 1):
        visited[curState] = result

    return result

def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility
    #IMPLEMENT
    
    global visited
    curState = color, board

    ##Caching case #1: Trying to visit a state we've already visited
    if(caching == 1 and curState in visited):
        return visited[curState]
    
    if(limit == 0):
        result = (None, compute_utility(board,color))
        return result
    
    allMoves = get_possible_moves(board, color)
    maxUtility = float("-inf")
    bestMove = None

    #Step 1: Check if you've bottomed out of the tree, or the depth (BASE CASE)
    if(allMoves == []):
        result = (None, compute_utility(board,color))
        
        ##Caching case #2: We reached the end, so we should put a "visited tag" on it.
        if(caching == 1):
            visited[curState] = result
        return result

    #Step 2: Check all the branches of a node
    for moves in allMoves:
        nextState = play_move(board, color, moves[0], moves[1])

        #Determining the color of the other player, and traversing accordingly
        #We only care about the utility value, hence the [1]
        utility = minimax_min_node(nextState, color, limit-1, caching)[1]

    #Step 3: Update max value
        if(utility > maxUtility):
            bestMove = moves
            maxUtility = utility

    result = bestMove, maxUtility

    ##Caching Case #3: Done searching a node that's not a leaf node.
    if(caching == 1):
        visited[curState] = result

    return result

def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    """

    #TLDR: Just make a function that returns a max-valued pair of coordinates
    ##We start mini-max search @ a max node (player). Min Node = Computer/other player. 
    maxTuple = minimax_max_node(board,color,limit,caching)[0]
    
    #IMPLEMENT
    return maxTuple #change this!

############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    #IMPLEMENT
    global visited
    curState = color, board
    allMoves = []

    sortedList = {}
    unsortedList = {}
    opposingColor = 4 - (color+1)
    
    ##Caching case #1: Trying to visit a state we've already visited
    if(caching == 1 and curState in visited):
        return visited[curState]

    if(limit == 0):
        result = (None, compute_utility(board,color))
        return result

    ##Ordering case #1: We deal with Node Ordering here
    if(ordering == 1):
        allMoves = sorted(get_possible_moves(board, opposingColor), key = lambda s:
                          compute_utility(play_move(board,opposingColor,s[0],s[1]),
                                            opposingColor), reverse = False)

    else:
        allMoves = get_possible_moves(board, opposingColor)

    minUtility = float("inf")
    worstMove = None

    if(allMoves == []):
        result = (None, compute_utility(board,color))
        ##Caching case #2: We reached the end, so we should put a "visited tag" on it.
        if(caching == 1):
            visited[curState] = result
        return result

    for moves in allMoves:
        nextState = play_move(board, opposingColor, moves[0], moves[1])

        utility = minimax_max_node(nextState, color, limit-1, caching)[1]

        if(utility < minUtility):
            worstMove = moves
            minUtility = utility

        beta = min(minUtility, beta)
        if(alpha >= beta):
            break

    result = worstMove, minUtility

    ##Caching Case #3: Done searching a node that's not a leaf node.
    if(caching == 1):
        visited[curState] = result

    return result

def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    #IMPLEMENT
    global visited
    curState = color, board
    allMoves = []
    unsortedList = {}
    sortedList = {}

    ##Caching case #1: Trying to visit a state we've already visited
    if(caching == 1 and curState in visited):
        return visited[curState]

    if(limit == 0):
        result = (None, compute_utility(board,color))
        return result

    ##Ordering case #1: We deal with Node Ordering here
    if(ordering == 1):
        allMoves = sorted(get_possible_moves(board, color),
                          key = lambda s: compute_utility(play_move(board,color,s[0],s[1]),
                                                            color), reverse = True)
        
    else:
        allMoves = get_possible_moves(board, color)

    maxUtility = float("-inf")
    bestMove = None

    #Step 1: Check if you've bottomed out of the tree, or the depth (BASE CASE)
    if(allMoves == []):
        result = None, compute_utility(board,color)
        ##Caching case #2: We reached the end, so we should put a "visited tag" on it.
        if(caching == 1):
            visited[curState] = result
        return result

    #Step 2: Check all the branches of a node
    for moves in allMoves:
        nextState = play_move(board, color, moves[0], moves[1])

        #Determining the color of the other player, and traversing accordingly
        #We only care about the utility value, hence the [1]
        utility = minimax_min_node(nextState, color, limit-1, caching)[1]

    #Step 3: Update max value
        if(utility > maxUtility):
            bestMove = moves
            maxUtility = utility

        alpha = max(maxUtility, alpha)
        if(alpha >= beta):
            break

    result = bestMove, maxUtility

    ##Caching Case #3: Done searching a node that's not a leaf node.
    if(caching == 1):
        visited[curState] = result

    return result

def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    """
    #IMPLEMENT
    alpha = float("-inf")
    beta = float("+inf")
    maxTuple = alphabeta_max_node(board, color, alpha, beta, limit, caching, ordering)
    
    return maxTuple[0] 

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("ALPHA-BETA AI") # First line is the name of this AI
    arguments = input().split(",")
    
    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light. 
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching 
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)
            
            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
