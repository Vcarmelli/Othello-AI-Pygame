# from states.game import Game

# if __name__ == "__main__":
#     game = Game()
#     game.run()

import sys
import getopt
import pygame
from ai.othello_game import OthelloGameManager, AiPlayerInterface, Player, InvalidMoveError, AiTimeoutError
from ai.othello_shared import get_possible_moves
from ai.othello_gui import OthelloGui

def main(argv=None):
    # Default values
    size = 8
    limit = 5
    ordering = True
    caching = True
    minimax = False
    agent1 = "agent_mcts.py"
    agent2 = "agent.py"

    if argv is None:
        argv = []

    try:
        opts, args = getopt.getopt(argv, "hcmol:d:a:b:", ["limit=", "dimension=", "agent1=", "agent2="])
    except getopt.GetoptError:
        print('main.py -d <dimension> [-a <agentA> -b <agentB> -l <depth-limit> -c -o -m]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -d <dimension> -a <agentA> [-b <agentB> -l <depth-limit> -c -o]')
            sys.exit()
        elif opt in ("-d", "--dimension"):
            size = int(arg)
        elif opt in ("-a", "--agentA"):
            agent1 = arg
        elif opt in ("-b", "--agentB"):
            agent2 = arg
        elif opt in ("-c", "--caching"):
            caching = True
        elif opt in ("-m", "--minimax"):
            minimax = True
        elif opt in ("-o", "--ordering"):
            ordering = True
        elif opt in ("-l", "--limit"):
            limit = int(arg)

    if size <= 0:  # if no dimension provided
        print('Please provide a board size.')
        print('othello_gui.py -d <dimension> [-a <agentA> -b <agentB> -l <depth-limit> -c -o]')
        sys.exit(2)

    if agent1 is not None and agent2 is not None and size > 0:
        p1 = AiPlayerInterface(agent1, 1, limit, minimax, caching, ordering)
        p2 = AiPlayerInterface(agent2, 2, limit, minimax, caching, ordering)
    elif agent1 is not None and size > 0:
        p1 = Player(1)
        p2 = AiPlayerInterface(agent1, 2, limit, minimax, caching, ordering)
    else:
        p1 = Player(1)
        p2 = Player(2)

    game = OthelloGameManager(size)
    gui = OthelloGui(game, p1, p2)
    gui.run()

if __name__ == "__main__":
    main()
