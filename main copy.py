import sys
import pygame
from ai.othello_game import OthelloGameManager, AiPlayerInterface, Player, InvalidMoveError, AiTimeoutError
from ai.othello_gui import OthelloGui, Menu, Setup, GameOver


class Game:
    def __init__(self):
        screenwidth = 600
        screenheight = 600

        pygame.init()
        self.screen = pygame.display.set_mode((screenwidth, screenheight))
        self.gameStateManager = OthelloGameManager(self.screen, 'menu')

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
        
        self.menu = None

        self.init_players()


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
        self.screen.blit(self.gameStateManager.img.setup_bg, (0, 0))

        while True:
            curr_state = self.gameStateManager.get_state()           

            if curr_state == 'menu':
                self.gameStateManager.clear_game()
            elif curr_state == 'game':
                if not self.game.playing:
                    self.init_players()
                    self.game.set_players(self.p1, self.p2)
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.state[curr_state].run()
            print("curr_state: ", curr_state)

            pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
