import sys
import pygame
from ai.othello_game import OthelloGameManager, AiPlayerInterface, Player, InvalidMoveError, AiTimeoutError
from ai.othello_shared import get_possible_moves
from ai.othello_gui import OthelloGui, Images, Menu, Setup, GameOver


class Game:
    def __init__(self):
        self.screenwidth = 600
        self.screenheight = 600
        self.gameStateManager = OthelloGameManager('menu')
        self.menu = None

        self.init_players()

    def init_display(self):
        self.img = Images(self.screen)
        self.menu = Menu(self.screen, self.gameStateManager)
        self.setup = Setup(self.screen, self.gameStateManager)
        self.game = OthelloGui(self.screen, self.gameStateManager)
        self.over = GameOver(self.screen, self.gameStateManager)

        self.state = {
            'menu': self.menu,
            'setup': self.setup,
            'game': self.game,
            'over': self.over
        }
        

    def init_players(self):
        size = 8
        limit = 5
        ordering = True
        caching = False
        minimax = False
        agent1 = "agent_mcts.py"
        agent2 = "agent.py"
        self.p1 = AiPlayerInterface(agent1, 1, limit, minimax, caching, ordering)
        self.p2 = AiPlayerInterface(agent2, 2, limit, minimax, caching, ordering)
        

    def run(self):   
        pygame.init()
        self.screen = pygame.display.set_mode((self.screenwidth, self.screenheight))
        if  self.menu is None:
            self.init_display()
        
        self.screen.blit(self.img.setup_bg, (0, 0))

        while True:
            print("self.gameStateManager.get_state(): ", self.gameStateManager.get_state())
            if self.gameStateManager.get_state() == 'menu':
                self.gameStateManager.clear_game()
            elif self.gameStateManager.get_state() == 'game':
                self.init_players()
                self.game.set_players(self.p1, self.p2)
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            self.state[self.gameStateManager.get_state()].run()

            pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
