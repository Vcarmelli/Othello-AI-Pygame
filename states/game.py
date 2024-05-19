import pygame
import sys
from states.game_state_manager import GameStateManager
from states.menu import Menu
from states.othello import Othello
from states.agent_ab import AlphaBeta

Screenwidth = 800
Screenheight = 800
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((Screenwidth, Screenheight))
        self.clock = pygame.time.Clock()

        self.gameStateManager = GameStateManager('alphabeta')   # GameStateManager('menu')
        self.menu = Menu(self.display, self.gameStateManager)
        self.game = Othello(self.display, self.gameStateManager)
        self.agentAB = AlphaBeta(self.display, self.gameStateManager)

        self.state = {
            'menu': self.menu,
            'game': self.game,
            'alphabeta': self.agentAB,
        }

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        print("self.gameStateManager.get_state(): ", self.gameStateManager.get_state())
                        if self.gameStateManager.get_state() == 'menu':
                            self.gameStateManager.set_state('game')
                        elif self.gameStateManager.get_state() == 'game':
                            self.gameStateManager.set_state('menu')
                        elif self.gameStateManager.get_state() == 'alphabeta':
                            self.gameStateManager.set_state('menu')

            self.state[self.gameStateManager.get_state()].run()

            pygame.display.update()
            self.clock.tick(FPS)
