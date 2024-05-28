import random
import sys
import time
import math
from ai.othello_shared import find_lines, get_possible_moves, get_score, play_move

state_action = {}    # {(board, color, move) : score}

class MCTS_state():
    """
            This sample code gives you a idea of how to store records for each node
            in the tree. However, you are welcome to modify this part or define your own
            class.
    """
    def __init__(self, ID , parent, children, direct_child, reward, total, move, board):
        self.ID = ID
        self.parent = parent    # a list of states
        self.children = children      # a list of states
        self.reward = reward    # number of win
        self.total = total      # number of simulation for self and (grand*)children
        self.board = board
        self.visited = 0        # 0 -> not visited yet, 1 -> already visited
        self.direct_child = direct_child
        self.move = move
        self.end = False

    def add_child(self, new_child):
        self.children.append(new_child)

    def display(self):
        print("-----MCTS node info------")
        print("reward:", self.reward)
        print("total:", self.total)
        print("move:", self.move)
        print("-----------END-----------")

    
def select_move_MCTS(board , color, limit):
    """
    You can add additional help functions as long as this function will return a position tuple
    """
    
    initial_state = MCTS_state(0, [], [], [], 0, 0, None, board)
    move = get_possible_moves(board, color)
    expand(initial_state,color,0)
    
    if limit > 0: #Step 1: Compute all Simulations
        ucb_of_children = []
        for i in range(limit):        
            state_to_go = select_best_grandchild(initial_state, color)
            if state_to_go.visited == 0:
                 state_to_go.visited = 1
                 winner = simulation(state_to_go , color, limit)
                 if winner == color:
                     backpropagation(state_to_go, 1) 
                 if winner != color:
                     backpropagation(state_to_go, 0)
            elif state_to_go.end == False and len(state_to_go.direct_child) == 0:
                expand(state_to_go, color, len(initial_state.children))
            elif state_to_go.end == True:
                break
            
    if not limit > 0: #Step 2: See if we've reached a conclusion after all simulations are finished
        ucb_of_children = []
        for child in initial_state.children:
            ucb_of_children.append(UCB_cal(child, color))
        state_to_go = initial_state.children[ucb_of_children.index(max(ucb_of_children))]
        if state_to_go.visited == 0:
            state_to_go.visited = 1
            winner = simulation(state_to_go , color, limit)
            if winner == color:
                backpropagation(state_to_go, 1) 
            if winner != color:
                backpropagation(state_to_go, 0)
        else:
            if state_to_go.end == False:
                expand(state_to_go, color, len(initial_state.children))
    
    if len(initial_state.direct_child) > 0:  #Step 3: Pick the best move, once we've reached an end to every simulation
        best_child = select_best_grandchild(initial_state, color)
        if best_child in initial_state.direct_child:
            best_move = move[initial_state.direct_child.index(best_child)]
        else:
            grand_parent = best_child.parent[1]
            best_move = move[initial_state.direct_child.index(grand_parent)]
            
        initial_state.move = best_move
        return best_move #Return Case #1

    
    if len(move) == 0 or len(initial_state.direct_child) == 0: #Edge case: We're out of moves, game over
        return None #Return Case #2

############################## UCB/HEURISTIC CALCULATIONS START HERE ##################################

def UCB_cal(state, color, bias = 100):

    #Used reinforcement learning w/Q Learning-> random exploration (f(n) = UCB + k/n)
    
    #Compute_heuristic takes up a majority of the time, so if you want to reduce time drastically,
    #replace compute_heuristic with compute_utility.

    if state.total > 0:
        k = state.reward*1000 + compute_heuristic(state.board, color)
        ucb = (k / state.total) + bias*math.sqrt(math.log(state.parent[-1].total)/state.total)
    else:
        k = state.reward*100 + compute_heuristic(state.board, color)
        ucb = (k / 1) 

    return ucb


def UCB_with_History(state, initial_state, color, state_action_knowledge, bias = math.sqrt(2)):
    
    move = get_possible_moves(state.board, color)
    
    if len(initial_state.direct_child) > 0:
        best_move = move[initial_state.direct_child.index(select_best_child(initial_state, color))]
        return best_move
    if len(move) == 0 or len(initial_state.direct_child) == 0:
        return None
        eprint('NOT POSSIBLE MOVE FOUND!')
 
    if state.total > 0:
        ucb = (state.reward / state.total) + bias*math.sqrt(math.log(state.parent[-1].total)/state.total)
    else:
        ucb = math.inf

    return ucb

def compute_utility(board, color):
    score = get_score(board)
    utility = 0

    if(color == 1):
        utility = score[0]- score[1]

    else:
        utility = score[1] - score[0]

    return utility

def compute_heuristic(board, color):
    
    #1. Compute Utility
    score = get_score(board)
    dim = len(board)
    utilityScore = 0

    if(color == 1):
        utilityScore = score[0]- score[1]

    else:
        utilityScore = score[1] - score[0]
        
    #2. Compute Mobility
    opposingColor = 3 - color
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
                subCornerScore = subCornerScore - 50
                
        elif(board[a[0]][a[1]] == opposingColor):
            if(board[0][0] == color):
                subCornerScore = subCornerScore + 10
            else:
                subCornerScore = subCornerScore - 50

        else:
            subCornerScore = subCornerScore - 6
                
    for b in sc2:

        if(board[b[0]][b[1]] == color):
            if(board[-1][0] == color):
                subCornerScore = subCornerScore + 10
            else:
                subCornerScore = subCornerScore - 50
                
        elif(board[b[0]][b[1]] == opposingColor):
            if(board[-1][0] == color):
                subCornerScore = subCornerScore + 10
            else:
                subCornerScore = subCornerScore - 50

        else:
            subCornerScore = subCornerScore - 6

    for c in sc3:
        if(board[c[0]][c[1]] == color):
            if(board[0][-1] == color):
                subCornerScore = subCornerScore + 10
            else:
                subCornerScore = subCornerScore - 50
                
        elif(board[c[0]][c[1]] == opposingColor):
            if(board[0][-1] == color):
                subCornerScore = subCornerScore + 10
            else:
                subCornerScore = subCornerScore - 50

        else:
            subCornerScore = subCornerScore - 6


    for d in sc4:
        if(board[d[0]][d[1]] == color):
            if(board[-1][-1] == color):
                subCornerScore = subCornerScore + 10
            else:
                subCornerScore = subCornerScore - 50
                
        elif(board[d[0]][d[1]] == opposingColor):
            if(board[-1][-1] == color):
                subCornerScore = subCornerScore + 10
            else:
                subCornerScore = subCornerScore - 50

        else:
            subCornerScore = subCornerScore - 6

    #5: Compute Edges
    edgeScore = 0

    for x in range(2,dim-2):
        if(board[x][0] == color or board[x][dim-2] == color):
            edgeScore = edgeScore + 2

    for y in range(2,dim-2):
        if(board[0][y] == color or board[dim-2][y] == color):
            edgeScore = edgeScore + 2

    #GRAND TOTAL

    # Case 1: If I get to take the first turn
    if(color == 1):
        total = 10*utilityScore + 10*mobilityScore + cornerScore + subCornerScore + 5*edgeScore

    #Case 2: If I have to take the 2nd turn
    else:
        total = 10*utilityScore + 5*mobilityScore + cornerScore + 0.5*subCornerScore + 2*edgeScore

    return total

#################################### POST SELECTION FOR MCTS STARTS HERE ########################################
def get_player_turn(n):
    if n % 2 == 1:
        return 1
    else:
        return 2

def simulation(state, color, limit):
    board_simulated = state.board

    while True:
        possible_moves = get_possible_moves(board_simulated , get_player_turn(color))
        if len(possible_moves) == 0:
            p1, p2 = get_score(board_simulated)
            if p1 > p2:
                return 1
            else:
                return 2                
            break
        random_move = random.choice(possible_moves)
        board_simulated = play_move(board_simulated , get_player_turn(color) , random_move[0] , random_move[1])

        color += 1

def expand(state, color, max_id):
     posssible_moves = get_possible_moves(state.board, color)
     if len(posssible_moves) > 0:
         for move in posssible_moves:
             max_id += 1
             new_board = play_move(state.board, get_player_turn(color), move[0] , move[1])
             parents = state.parent + [state]
             new_state = MCTS_state(max_id , parents , [], [] , 0, 0, None, new_board)
             state.direct_child.append(new_state)
             for grand_parent in parents:
                 grand_parent.children.append(new_state)
     if len(posssible_moves) == 0:
         state.end = True

def select_best_child(state, color):
    ucb_of_children = []
    for child in state.direct_child:
        ucb_of_children.append(UCB_cal(child,color))
    best_child = state.direct_child[ucb_of_children.index(max(ucb_of_children))]
    return best_child

def select_best_grandchild(state, color):
    ucb_of_children = []
    for child in state.children:
        ucb_of_children.append(UCB_cal(child,color))
    best_child = state.children[ucb_of_children.index(max(ucb_of_children))]
    return best_child

def backpropagation(state , winner):
    state.total = 1
    state.reward = winner
    for grand_parent in state.parent:
        grand_parent.total += 1
        grand_parent.reward += winner
        

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)


def run_mcts():
    """
        Please do not modify this part.
        """
    print("MCTS AI")  # First line is the name of this AI
    arguments = input().split(",")

    color = int(arguments[0])  # Player color: 1 for dark (goes first), 2 for light.
    limit = 700  # Iteration limit
    minimax = int(arguments[2])  # not used here
    caching = int(arguments[3])  # not used here
    ordering = int(arguments[4])  # not used here

    if (limit == -1):
        eprint("Iteration Limit is OFF")
    else:
        eprint("Iteration Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True:  # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL":  # Game is over.
            print
        else:
            board = eval(input())  # Read in the input and turn it into a Python
            # object. The format is a list of rows. The
            # squares in each row are represented by
            # 0 : empty square
            # 1 : dark disk (player 1)
            # 2 : light disk (player 2)

            # Select the move and send it to the manager
            movei, movej = select_move_MCTS(board, color, limit)

            print("{} {}".format(movei, movej))
            
            
if __name__ == "__main__":
    run_mcts()
