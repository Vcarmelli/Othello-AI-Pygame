import sys
import pygame
from ai.display import Button, Draw
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
        self.screen.blit(self.game.img.game_bg, (0, 0))
        
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
                self.shutdown("Game Over, Dark wins!")
            elif light_score > dark_score:
                self.shutdown("Game Over, Light wins!")
            else:
                self.shutdown("Game Over, It's a draw!")

            self.game.set_scores(dark_score, light_score)
            self.game.set_state('over')
            self.playing = False


    def ai_move(self):
        meduim_font = pygame.font.Font(None, 40)  
        large_font = pygame.font.Font(None, 48)  
        larger_font = pygame.font.Font(None, 300)  
        player_obj = self.players[self.game.current_player]
        try:
            i, j = player_obj.get_move(self.game)

            player = "Black" if self.game.current_player == 1 else "White"
            print(f"{player_obj.name} ({player}): {i},{j}")

            self.game.play(i, j)
            self.draw_board()
            
            light_score, dark_score = get_score(self.game.board)

            self.screen.blit(meduim_font.render(f"{player_obj.name} ({player}) move to ({i}, {j})", True, WHITE), (45, self.screen.get_height() - 180))
            
            score_middle_y = (self.screen.get_height() - 50) // 2
            x_position = 50 
            self.screen.blit(large_font.render(f"BLACK", True, WHITE), (x_position + 35, score_middle_y - 245))
            self.screen.blit(larger_font.render(f"{dark_score}", True, WHITE), (x_position + 10, score_middle_y -140))
            self.screen.blit(large_font.render(f"WHITE", True, WHITE), (x_position + 375, score_middle_y - 245))
            self.screen.blit(larger_font.render(f"{light_score}", True, WHITE), (x_position + 350, score_middle_y -140))
            pygame.time.delay(900)
            pygame.display.update()

            if not get_possible_moves(self.game.board, self.game.current_player):
                self.check_game_over()
        except AiTimeoutError:
            self.shutdown(f"Game Over, {player_obj.name} lost (timeout)")
        
    def draw_board(self):
        self.screen.blit(self.game.img.game_bg, (0, 0))
        
        new_width = 700
        
        new_cell_size = new_width // self.game.dimension
        
        total_height = self.game.dimension * new_cell_size

        start_x = self.screen.get_width() - new_width - 100  
        
        start_y = (self.screen.get_height() - total_height) // 2

        self.draw_grid(start_x, start_y, self.game.dimension, new_cell_size)
        
        self.draw_disks(start_x, start_y, self.game.dimension, new_cell_size)

    def draw_grid(self, start_x, start_y, dimension, cell_size):
        for i in range(dimension):
            for j in range(dimension):
                pygame.draw.rect(self.screen, (0, 0, 0), 
                                (start_x + i * cell_size, start_y + j * cell_size, 
                                cell_size, cell_size), 1)

    def draw_disks(self, start_x, start_y, dimension, cell_size):
        # Example implementation of drawing disks
        for i in range(dimension):
            for j in range(dimension):
                if self.game.board[i][j] != 0:  # Assuming 0 means no disk
                    color = (255, 255, 255) if self.game.board[i][j] == 1 else (0, 0, 0)
                    pygame.draw.circle(self.screen, color, 
                                    (start_x + i * cell_size + cell_size // 2, 
                                        start_y + j * cell_size + cell_size // 2), 
                                    cell_size // 2 - 5)



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
        mcts_image = pygame.image.load("assets/MCTS.png")
        minimax_image = pygame.image.load("assets/MINIMAX.png")

        mcts_image = pygame.transform.scale(mcts_image, (290, 100))
        minimax_image = pygame.transform.scale(minimax_image, (290, 100))

        self.screen.blit(self.game.img.setup_bg, (0, 0))
        MOUSE_POS = pygame.mouse.get_pos()

        mcts_btn = Button(mcts_image, (self.screen.get_width() // 2 - 300, self.screen.get_height() // 2 + 200), 
                        None, BTN_COLOR, BTN_HOVER_COLOR)
        ab_btn = Button(minimax_image, (self.screen.get_width() // 2 + 300, self.screen.get_height() // 2 + 200), 
                        None, BTN_COLOR, BTN_HOVER_COLOR)
        

        for button in [mcts_btn, ab_btn]:
            button.update_color(MOUSE_POS)
            button.draw_button(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mcts_btn.click_button(MOUSE_POS):
                    self.game.first_player = 'mcts'                    
                    self.game.set_state('game')
                if ab_btn.click_button(MOUSE_POS):
                    self.game.first_player = 'ab'
                    self.game.set_state('game')
                    
        pygame.display.update()


class GameOver:
    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.game = gameStateManager
    
    def run(self):
        self.screen.blit(self.game.img.game_bg, (0, 0))

        mcts_score = self.game.black_score if self.game.first_player == 'mcts' else self.game.white_score
        ab_score = self.game.white_score if self.game.first_player == 'mcts' else self.game.black_score

        self.game.draw.text(None, f"MCTS Score: {mcts_score}", (255, 255, 255), (self.screen.get_width() // 2, self.screen.get_height() // 6 + 50))
        self.game.draw.text(None, f"MINIMAX Score: {ab_score}", (255, 255, 255), (self.screen.get_width() // 2, self.screen.get_height() // 5))

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

