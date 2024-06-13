import time
import sys
import pygame
from ai.display import Button, Draw
from ai.othello_game import AiPlayerInterface, Player, InvalidMoveError, AiTimeoutError
from ai.othello_shared import get_possible_moves, get_score


WHITE = (255, 255, 255)
BTN_COLOR = (34, 139, 34)
BTN_HOVER_COLOR = (50, 205, 50)


class OthelloGui:
    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.game = gameStateManager
        self.playing = False
        self.black_player = None
        self.white_player = None


    def set_players(self, player1, player2):
        self.players = [None, player1, player2]
        self.black_player = player1.name
        self.white_player = player2.name
        self.playing = True

    def run(self):
        self.screen.blit(self.game.img.game_bg, (0, 0))
        pygame.display.set_caption("Othello AI | Game")

        if isinstance(self.players[self.game.current_player], AiPlayerInterface):  
            self.ai_move()
        else:
            self.game.set_state('over')

        pygame.display.update()


    def shutdown(self, text, time):
        print(text)
        print("Total calculation time:", time)

        if isinstance(self.players[1], AiPlayerInterface):
            self.players[1].kill(self.game)
        if isinstance(self.players[2], AiPlayerInterface):
            self.players[2].kill(self.game)
        
        self.draw_board()
        self.game.draw.text(f"{text}", self.game.font.medium, WHITE, (370, self.screen.get_height() // 2 + 220))
        self.game.draw.text(f"Total calculation time: {time}", self.game.font.medium, WHITE, (370, self.screen.get_height() // 2 + 270))
        self.game.draw.text("Click anywhere to continue...", self.game.font.small, WHITE, (370, self.screen.get_height() // 2 + 320))
        pygame.display.update()

        while self.playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.game.set_state('menu')
                    self.playing = False

        
    def check_game_over(self):
        if not get_possible_moves(self.game.board, 1) and not get_possible_moves(self.game.board, 2):
            black_score, white_score = get_score(self.game.board)
            self.game.set_scores(black_score, white_score)

            print("Dark Score:", black_score)    
            print("Light Score:", white_score)
            if black_score > white_score:
                time = f"{self.players[1].get_accumulated_time():.2f} seconds"
                self.shutdown(f"Game Over, {self.black_player} wins!", time)
            elif white_score > black_score:
                time = f"{self.players[2].get_accumulated_time():.2f} seconds"
                self.shutdown(f"Game Over, {self.white_player} wins!", time)
            else:
                self.shutdown("Game Over, It's a draw!", "")
            

    def ai_move(self):
        opposing_player = 3 - self.game.current_player
        player_obj = self.players[self.game.current_player]
        player_opp = self.players[opposing_player]
        try:
            player_obj.start_turn()
            i, j = player_obj.get_move(self.game)
            player_obj.end_turn()

            player = "Black" if self.game.current_player == 1 else "White"
            print(f"{player_obj.name} ({player}) move: {i},{j}\n")

            self.game.play(i, j)
            self.draw_board()
            self.game.draw.text(f"{player_obj.name} ({player}) move to ({i}, {j})", self.game.font.medium, WHITE, (370, self.screen.get_height() // 2 + 220))
            self.game.draw.text(f"Accumulated time: {player_obj.get_accumulated_time():.2f} seconds", self.game.font.small, WHITE, (370, self.screen.get_height() // 2 + 260))
            self.game.draw.text(f"{player_opp.name}'s turn...", self.game.font.medium, WHITE, (370, self.screen.get_height() // 2 + 320))
            
            pygame.time.delay(100)
            pygame.display.update()

            if not get_possible_moves(self.game.board, self.game.current_player):
                self.check_game_over()
        except AiTimeoutError:
            self.shutdown(f"Game Over, {player_obj.name} lost (timeout)")

    def draw_board(self):
        self.screen.blit(self.game.img.game_bg, (0, 0))
        
        board_size = 700
        self.cell_size  = board_size // self.game.dimension

        start_x = self.screen.get_width() - board_size - 100  
        start_y = (self.screen.get_height() - board_size) // 2

        self.draw_grid(start_x, start_y)
        self.draw_disks(start_x, start_y)
        self.draw_scores()

    def draw_scores(self):
        score_middle_y = self.screen.get_height() // 2
        x_position = 370 
        black_score, white_score = get_score(self.game.board)
        
        left, right = ("BLACK", "WHITE") if self.game.first_player == 'mcts' else ("WHITE", "BLACK")
        left_score, right_score = (black_score, white_score) if left == "BLACK" else (white_score, black_score)

        self.game.draw.text(left, self.game.font.large, WHITE, (x_position - 170, score_middle_y - 180))
        self.game.draw.text(right, self.game.font.large, WHITE, (x_position + 150, score_middle_y - 180))
        self.game.draw.text(f"{left_score}", self.game.font.larger, WHITE, (x_position - 170, score_middle_y))
        self.game.draw.text(f"{right_score}", self.game.font.larger, WHITE, (x_position + 150, score_middle_y))

    def draw_grid(self, start_x, start_y):
        for i in range(self.game.dimension):
            for j in range(self.game.dimension):
                pygame.draw.rect(self.screen, WHITE, 
                                (start_x + i * self.cell_size, start_y + j * self.cell_size,  
                                self.cell_size, self.cell_size), 1)

    def draw_disk(self, i, j, color_image, start_x, start_y):
        x = start_x + i * self.cell_size + (self.cell_size - color_image.get_width()) // 2
        y = start_y + j * self.cell_size + (self.cell_size - color_image.get_height()) // 2
        self.screen.blit(color_image, (x, y))

    def draw_disks(self, start_x, start_y):
        for i in range(self.game.dimension):
            for j in range(self.game.dimension):
                if self.game.board[i][j] == 1:
                    self.draw_disk(j, i, self.game.img.black_piece, start_x, start_y)
                elif self.game.board[i][j] == 2:
                    self.draw_disk(j, i, self.game.img.white_piece, start_x, start_y)

    
    # UNCOMMENT TO DRAW DISK USING PYGAME CIRCLE

    # def draw_disks(self, start_x, start_y):
    #     for i in range(self.game.dimension):
    #         for j in range(self.game.dimension):
    #             if self.game.board[i][j] != 0:
    #                 color = (255, 255, 255) if self.game.board[i][j] == 1 else (0, 0, 0)
    #                 pygame.draw.circle(self.screen, color, 
    #                                 (start_x + i * self.cell_size + self.cell_size // 2, 
    #                                 start_y + j * self.cell_size + self.cell_size // 2), 
    #                                 self.cell_size // 2 - 5)


class Menu:
    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.game = gameStateManager

    def run(self):
        self.screen.blit(self.game.img.menu_bg, (0, 0))
        pygame.display.set_caption("Othello AI | Menu")

        MOUSE_POS = pygame.mouse.get_pos()

        play_btn = Button(self.game.img.play, (self.screen.get_width() // 2, self.screen.get_height() // 1 - 120), 
                        None, BTN_COLOR, BTN_HOVER_COLOR)
        
        play_btn.update_color(MOUSE_POS)
        play_btn.draw_button(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.click_button(MOUSE_POS):
                    self.game.set_state('setup')
                    
        pygame.display.update()


class Setup:
    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.game = gameStateManager

    def run(self):
        self.screen.blit(self.game.img.setup_bg, (0, 0))
        pygame.display.set_caption("Monte Carlo Search Tree vs Minimax")
        MOUSE_POS = pygame.mouse.get_pos()

        mcts_btn = Button(self.game.img.mcts, (self.screen.get_width() // 2 - 300, self.screen.get_height() // 2 + 250), 
                        None, BTN_COLOR, BTN_HOVER_COLOR)
        ab_btn = Button(self.game.img.minimax, (self.screen.get_width() // 2 + 300, self.screen.get_height() // 2 + 250), 
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

