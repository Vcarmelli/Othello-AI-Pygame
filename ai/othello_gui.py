import sys
import getopt
import pygame
from states.button import Button
from ai.othello_game import OthelloGameManager, AiPlayerInterface, Player, InvalidMoveError, AiTimeoutError
from ai.othello_shared import get_possible_moves, get_score

FPS = 60

class Images:
    def __init__(self, screen, cell_size = 50):
        self.screen = screen
        
        self.black_piece = pygame.image.load('assets/piece1.png')
        self.black_piece = pygame.transform.scale(self.black_piece, (int(cell_size / 1.2), int(cell_size / 1.2)))
        self.white_piece = pygame.image.load('assets/piece2.png')
        self.white_piece = pygame.transform.scale(self.white_piece, (int(cell_size / 1.2), int(cell_size / 1.2)))

        self.menu_bg = pygame.image.load('assets/index.png')
        self.menu_bg = pygame.transform.scale(self.menu_bg, (self.screen.get_width(), self.screen.get_height()))
        self.setup_bg = pygame.image.load('assets/boardbg.png')
        self.setup_bg = pygame.transform.scale(self.setup_bg, (self.screen.get_width(), self.screen.get_height()))
        

class OthelloGui:
    def __init__(self, screen, game_manager):
        self.game = game_manager
        self.height = self.game.dimension
        self.width = self.game.dimension
        self.cell_size = 60

        self.screen = screen
        self.img = Images(self.screen)
        self.draw = Draw(self.screen)

        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()

        self.button_color = (34, 139, 34)
        self.button_hover_color = (50, 205, 50)

    def set_players(self, player1, player2):
        self.players = [None, player1, player2]


    def run(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.img.setup_bg, (0, 0))
        
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    self.mouse_pressed(event.pos[0], event.pos[1])

        if isinstance(self.players[self.game.current_player], AiPlayerInterface):
            self.ai_move()
        else:
            self.game.set_state('over')
            #break

        pygame.display.flip()


    def get_position(self, x, y):
        i = x // self.cell_size
        j = y // self.cell_size
        return i, j

    def mouse_pressed(self, x, y):
        i, j = self.get_position(x, y)

        try:
            player = "Dark" if self.game.current_player == 1 else "Light"
            print(f"{player}: {i},{j}")
            self.game.play(i, j)
            self.draw_board()
            pygame.display.flip()
            if not get_possible_moves(self.game.board, self.game.current_player):
                self.shutdown("Game Over")
            elif isinstance(self.players[self.game.current_player], AiPlayerInterface):
                pygame.time.set_timer(pygame.USEREVENT, 100)
        except InvalidMoveError:
            print(f"Invalid move. {i},{j}")

    def shutdown(self, text):
        print(text)

        if isinstance(self.players[1], AiPlayerInterface):
            self.players[1].kill(self.game)
        if isinstance(self.players[2], AiPlayerInterface):
            self.players[2].kill(self.game)
        

    def check_game_over(self):
        if not get_possible_moves(self.game.board, 1) and not get_possible_moves(self.game.board, 2):
            light_score, dark_score = get_score(self.game.board)
            print("Dark Score:", dark_score)    
            print("Light Score:", light_score)
            if dark_score > light_score:
                self.shutdown("Game Over, Dark wins! (MCTS)")
            elif light_score > dark_score:
                self.shutdown("Game Over, Light wins! (MNM)")
            else:
                self.shutdown("Game Over, It's a draw!")

            self.game.set_scores(dark_score, light_score)
            self.game.set_state('over')


    def ai_move(self):
        player_obj = self.players[self.game.current_player]
        try:
            i, j = player_obj.get_move(self.game)
            player = "Dark" if self.game.current_player == 1 else "Light"
            player = f"{player_obj.name} {player}"
            print(f"{player}: {i},{j}")
            self.game.play(i, j)
            self.draw_board()
            pygame.display.flip()
            if not get_possible_moves(self.game.board, self.game.current_player):
                self.check_game_over()
        except AiTimeoutError:
            self.shutdown(f"Game Over, {player_obj.name} lost (timeout)")
        
    def draw_board(self):
        self.screen.blit(self.img.setup_bg, (0, 0))
        self.draw_grid()
        self.draw_disks()

    def draw_grid(self):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(self.screen, (0, 0, 0), (i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size), 1)

    def draw_disk(self, i, j, color_image):
        x = i * self.cell_size + (self.cell_size - color_image.get_width()) // 2
        y = j * self.cell_size + (self.cell_size - color_image.get_height()) // 2
        self.screen.blit(color_image, (x, y))

    def draw_disks(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.game.board[i][j] == 1:
                    self.draw_disk(j, i, self.img.black_piece)
                elif self.game.board[i][j] == 2:
                    self.draw_disk(j, i, self.img.white_piece)


class Draw:
    def __init__(self, screen):
        self.screen = screen
        self.img = Images(self.screen)
        self.font = pygame.font.Font(None, 36)


    def text(self, fill_color, text, font_color, pos):
        if fill_color is not None:
            text_bg = pygame.Surface(pos)
            text_bg.fill(fill_color)
            bg_rect = text_bg.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

            output = self.font.render(text, True, font_color)
            text_rect = output.get_rect(center=(bg_rect.centerx, bg_rect.centery))
            
            self.screen.blit(text_bg, bg_rect)
        else:
            output = self.font.render(text, True, font_color)
            text_rect = output.get_rect(center=pos)

        self.screen.blit(output, text_rect)


class Menu:
    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.gameStateManager = gameStateManager
        self.img = Images(self.screen)

    def run(self):
        self.screen.blit(self.img.menu_bg, (0, 0))
        pygame.display.set_caption("Othello Menu")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.gameStateManager.set_state('setup')
                    
        pygame.display.update()


class Setup:
    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.gameStateManager = gameStateManager
        self.img = Images(self.screen)
        self.draw = Draw(self.screen)
        self.font = pygame.font.Font(None, 36)
        self.button_color = (34, 139, 34)
        self.button_hover_color = (50, 205, 50)

    def run(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.img.setup_bg, (0, 0))
        pygame.display.set_caption("MCTS vs Alpha Beta")

        self.draw.text(None, "This is the simulation of two AI", (255, 255, 255), (self.screen.get_width() // 2, self.screen.get_height() // 4))
        self.draw.text(None, "The Monte Carlo vs Alpha Beta", (255, 255, 255), (self.screen.get_width() // 2, self.screen.get_height() // 3))

        MOUSE_POS = pygame.mouse.get_pos()

        setup_btn = Button(None, (self.screen.get_width() // 2, self.screen.get_height() // 2), 
                            "AI vs AI", self.font, self.button_color, self.button_hover_color)
        setup_btn.update_color(MOUSE_POS)
        setup_btn.draw_button(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if setup_btn.click_button(MOUSE_POS):
                    self.gameStateManager.set_state('game')
                    
        pygame.display.update()

class GameOver:
    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.gameStateManager = gameStateManager
        self.img = Images(self.screen)
        self.draw = Draw(self.screen)
        self.font = pygame.font.Font(None, 36)
        self.button_color = (34, 139, 34)
        self.button_hover_color = (50, 205, 50)
    

    def run(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.img.setup_bg, (0, 0))

        self.draw.text(None, f"MCTS Score: {self.gameStateManager.black_score}", (255, 255, 255), (self.screen.get_width() // 2, self.screen.get_height() // 6 + 50))
        self.draw.text(None, f"MINIMAX Score: {self.gameStateManager.white_score}", (255, 255, 255), (self.screen.get_width() // 2, self.screen.get_height() // 5))

        MOUSE_POS = pygame.mouse.get_pos()

        menu_btn = Button(None, (self.screen.get_width() // 2, self.screen.get_height() // 2), 
                            "Back to Menu", self.font, self.button_color, self.button_hover_color)
        exit_btn = Button(None, (self.screen.get_width() // 2, self.screen.get_height() // 2 + 70), 
                            "Exit", self.font, self.button_color, self.button_hover_color)

        for button in [menu_btn, exit_btn]:
            button.update_color(MOUSE_POS)
            button.draw_button(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.gameStateManager.set_state('menu')
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menu_btn.click_button(MOUSE_POS):
                    self.gameStateManager.set_state('menu')
                elif exit_btn.click_button(MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

