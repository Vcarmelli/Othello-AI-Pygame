import sys
import getopt
import pygame
from ai.othello_game import OthelloGameManager, AiPlayerInterface, Player, InvalidMoveError, AiTimeoutError
from ai.othello_shared import get_possible_moves

FPS = 60

class OthelloGui:
    def __init__(self, game_manager, player1, player2):
        self.game = game_manager
        self.players = [None, player1, player2]
        self.height = self.game.dimension
        self.width = self.game.dimension
        
        self.cell_size = 50

        pygame.init()
        self.screen = pygame.display.set_mode((self.cell_size * self.width, self.cell_size * self.height))
        pygame.display.set_caption("Othello")

        self.bgimage = pygame.image.load('assets/boardbg.png').convert_alpha()
        self.bgimage = pygame.transform.scale(self.bgimage, (self.cell_size * self.width, self.cell_size * self.height))
        
        self.black_piece_image = pygame.image.load('assets/piece1.png').convert_alpha()
        self.black_piece_image = pygame.transform.scale(self.black_piece_image, (int(self.cell_size / 1.2), int(self.cell_size / 1.2)))
        self.white_piece_image = pygame.image.load('assets/piece2.png').convert_alpha()
        self.white_piece_image = pygame.transform.scale(self.white_piece_image, (int(self.cell_size / 1.2), int(self.cell_size / 1.2)))

        self.menu_bg_image = pygame.image.load('assets/index.png')
        self.menu_bg_image = pygame.transform.scale(self.menu_bg_image, (self.screen.get_width(), self.screen.get_height()))
        self.setup_bg_image = pygame.image.load('assets/boardbg.png')
        self.setup_bg_image = pygame.transform.scale(self.setup_bg_image, (self.screen.get_width(), self.screen.get_height()))
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        
        self.state = 'menu'

        self.setup_button_color = (34, 139, 34)
        self.setup_button_hover_color = (50, 205, 50)
        self.setup_button_rect = pygame.Rect(self.screen.get_width() // 2 - 100, self.screen.get_height() // 50, 200, 50 )


    def draw_menu(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.menu_bg_image, (0, 0))
    
    def draw_game_over(self):
        self.screen.fill((0, 0, 0))
        game_over_text = self.font.render(self.game_over_text, True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        prompt_text = self.font.render("Press Enter to return to menu or Q to exit", True, (255, 255, 255))
        prompt_rect = prompt_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(prompt_text, prompt_rect)

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.state = 'menu'
                        return
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

    def draw_setup(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.setup_bg_image, (0, 0))

        title_text = self.font.render("This is the simulation of two AI. The Monte Carlo vs Alpha Beta", True, (255, 255, 255)) 
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 3))
        prompt_text = self.font.render("Othello AI", True, (255, 255, 255)) 
        prompt_rect = prompt_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 8))

        self.screen.blit(title_text, title_rect)
        self.screen.blit(prompt_text, prompt_rect)
        
        self.draw_setup_button()


    def draw_setup_button(self):
        button_rect1 = pygame.Rect(self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 - 40, 200, 50)

        mouse_pos = pygame.mouse.get_pos()

        color1 = self.setup_button_hover_color if button_rect1.collidepoint(mouse_pos) else self.setup_button_color
        pygame.draw.rect(self.screen, color1, button_rect1)
        text_surface1 = self.font.render("AI vs AI", True, (255, 255, 255))
        text_rect1 = text_surface1.get_rect(center=button_rect1.center)
        self.screen.blit(text_surface1, text_rect1)

        self.setup_button_rect = button_rect1

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: 
                        if self.state == 'menu':
                            self.state = 'setup'
                        elif self.state == 'setup' and self.setup_button_rect.collidepoint(event.pos):
                            self.state = 'game'
                        

            if self.state == 'menu':
                self.draw_menu()
            elif self.state == 'setup':
                self.draw_setup()
            elif self.state == 'game':
                self.game_loop()

            pygame.display.update()
            self.clock.tick(FPS)

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
        
        pygame.quit()
        sys.exit()

    def check_game_over(self):
        if not get_possible_moves(self.game.board, 1) and not get_possible_moves(self.game.board, 2):
            dark_score = sum(row.count(1) for row in self.game.board)
            light_score = sum(row.count(2) for row in self.game.board)
            print("Dark Score:", dark_score)
            print("Light Score:", light_score)
            if dark_score > light_score:
                self.shutdown("Game Over, Dark wins!")
            elif light_score > dark_score:
                self.shutdown("Game Over, Light wins!")
            else:
                self.shutdown("Game Over, It's a draw!")

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

    def game_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  
                        self.mouse_pressed(event.pos[0], event.pos[1])

            if isinstance(self.players[self.game.current_player], AiPlayerInterface):
                self.ai_move()

        pygame.display.flip()
        #pygame.quit()

    def draw_board(self):
        self.screen.blit(self.bgimage, (0, 0))
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
                    self.draw_disk(j, i, self.black_piece_image)
                elif self.game.board[i][j] == 2:
                    self.draw_disk(j, i, self.white_piece_image)
