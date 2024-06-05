import sys
import pygame
from states.display import Button, Draw
from ai.othello_game import AiPlayerInterface, Player, InvalidMoveError, AiTimeoutError
from ai.othello_shared import get_possible_moves, get_score

FPS = 60
WHITE = (255, 255, 255)
BTN_COLOR = (34, 139, 34)
BTN_HOVER_COLOR = (50, 205, 50)


class OthelloGui:
    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.game = gameStateManager
        self.cell_size = 60
        self.playing = False


    def set_players(self, player1, player2):
        self.players = [None, player1, player2]
        self.playing = True

    def run(self):
        self.screen.blit(self.game.img.setup_bg, (0, 0))
        
        # FOR HUMAN PLAYER
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         sys.exit()
        #     elif event.type == pygame.MOUSEBUTTONDOWN:
        #         if event.button == 1:  
        #             self.mouse_pressed(event.pos[0], event.pos[1])

        if isinstance(self.players[self.game.current_player], AiPlayerInterface):
            self.ai_move()
        else:
            self.game.set_state('over')
            #break

        pygame.display.update()


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
            print("FROM SHUTDOWN P1")
            self.players[1].kill(self.game)
        if isinstance(self.players[2], AiPlayerInterface):
            print("FROM SHUTDOWN P2")
            self.players[2].kill(self.game)

        input("======= PAUSE =======")
        

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
            self.playing = False


    def ai_move(self):
        player_obj = self.players[self.game.current_player]
        try:
            i, j = player_obj.get_move(self.game)

            player = "Dark" if self.game.current_player == 1 else "Light"
            player = f"{player_obj.name} {player}"
            print(f"{player} MOVE: {i},{j}")

            self.game.play(i, j)
            self.draw_board()
            pygame.display.flip()

            if not get_possible_moves(self.game.board, self.game.current_player):
                self.check_game_over()
        except AiTimeoutError:
            self.shutdown(f"Game Over, {player_obj.name} lost (timeout)")
        
    def draw_board(self):
        self.screen.blit(self.game.img.setup_bg, (0, 0))
        self.draw_grid()
        self.draw_disks()

    def draw_grid(self):
        for i in range(self.game.dimension):
            for j in range(self.game.dimension):
                pygame.draw.rect(self.screen, (0, 0, 0), (i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size), 1)

    def draw_disk(self, i, j, color_image):
        x = i * self.cell_size + (self.cell_size - color_image.get_width()) // 2
        y = j * self.cell_size + (self.cell_size - color_image.get_height()) // 2
        self.screen.blit(color_image, (x, y))

    def draw_disks(self):
        for i in range(self.game.dimension):
            for j in range(self.game.dimension):
                if self.game.board[i][j] == 1:
                    self.draw_disk(j, i, self.game.img.black_piece)
                elif self.game.board[i][j] == 2:
                    self.draw_disk(j, i, self.game.img.white_piece)




class Menu:
    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.game = gameStateManager

    def run(self):
        self.screen.blit(self.game.img.menu_bg, (0, 0))
        pygame.display.set_caption("Othello Menu")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.game.set_state('setup')
                    
        pygame.display.update()


class Setup:
    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.game = gameStateManager

    def run(self):
        self.screen.blit(self.game.img.setup_bg, (0, 0))
        pygame.display.set_caption("MCTS vs Alpha Beta")

        self.game.draw.text(None, "This is the simulation of two AI", WHITE, (self.screen.get_width() // 2, self.screen.get_height() // 4))
        self.game.draw.text(None, "The Monte Carlo vs Alpha Beta", WHITE, (self.screen.get_width() // 2, self.screen.get_height() // 3))

        MOUSE_POS = pygame.mouse.get_pos()

        setup_btn = Button(None, (self.screen.get_width() // 2, self.screen.get_height() // 2), 
                            "AI vs AI", BTN_COLOR, BTN_HOVER_COLOR)
        
        setup_btn.update_color(MOUSE_POS)
        setup_btn.draw_button(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if setup_btn.click_button(MOUSE_POS):
                    self.game.set_state('game')
                    
        pygame.display.update()


class GameOver:
    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.game = gameStateManager
    
    def run(self):
        self.screen.blit(self.game.img.setup_bg, (0, 0))

        self.game.draw.text(None, f"MCTS Score: {self.game.black_score}", (255, 255, 255), (self.screen.get_width() // 2, self.screen.get_height() // 6 + 50))
        self.game.draw.text(None, f"MINIMAX Score: {self.game.white_score}", (255, 255, 255), (self.screen.get_width() // 2, self.screen.get_height() // 5))

        MOUSE_POS = pygame.mouse.get_pos()

        menu_btn = Button(None, (self.screen.get_width() // 2, self.screen.get_height() // 2), 
                            "Back to Menu", BTN_COLOR, BTN_HOVER_COLOR)
        exit_btn = Button(None, (self.screen.get_width() // 2, self.screen.get_height() // 2 + 70), 
                            "Exit", BTN_COLOR, BTN_HOVER_COLOR)

        for button in [menu_btn, exit_btn]:
            button.update_color(MOUSE_POS)
            button.draw_button(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.set_state('menu')
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menu_btn.click_button(MOUSE_POS):
                    self.game.set_state('menu')
                elif exit_btn.click_button(MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

