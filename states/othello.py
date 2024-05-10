import pygame
from pygame.locals import *

class Othello:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.grid = Grid(self.display)

        self.board = [[0 for _ in range(8)] for _ in range(8)]
        self.board[3][3] = self.board[4][4] = 1  # White pieces
        self.board[3][4] = self.board[4][3] = -1  # Black pieces

        self.current_player = 1  #track turns
        self.game_over = False

        self.RUNNING = True
    
    def run(self):
        while self.RUNNING:
            self.input()
            self.update()
            self.render()

    def input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.RUNNING = False
            
            if event.type == MOUSEBUTTONDOWN and not self.game_over:
                if event.button == 1:
                    x, y = event.pos
                    row = y // self.grid.CELL_SIZE
                    col = x // self.grid.CELL_SIZE
                    if self.is_valid_move(row, col):
                        self.drop_piece(row, col)
                        self.switch_player()

    def update(self):
        pass

    def render(self):
        self.display.fill((0, 128, 0))  # Green background
        self.grid.draw_board(self.board)
        pygame.display.flip()

    def is_valid_move(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8 and self.board[row][col] == 0

    def drop_piece(self, row, col):
        self.board[row][col] = self.current_player

    def switch_player(self):
        self.current_player *= -1  # Switch player


class Grid:
    def __init__(self, display):
        # Constants
        self.display = display
        self.CELL_SIZE = 100
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.bgimage = pygame.image.load('assets/boardbg.png')

        # Load piece images
        self.black_piece_image = pygame.image.load('assets/piece1.png').convert_alpha()
        self.black_piece_image = pygame.transform.scale(self.black_piece_image, (self.CELL_SIZE / 1.2, self.CELL_SIZE / 1.2))
        self.white_piece_image = pygame.image.load('assets/piece2.png').convert_alpha()
        self.white_piece_image = pygame.transform.scale(self.white_piece_image, (self.CELL_SIZE / 1.2, self.CELL_SIZE / 1.2 ))


    def draw_board(self, board):
        self.display.fill(self.WHITE)
        self.display.blit(self.bgimage, (0, 0))
        for row in range(8):
            for col in range(8):
                rect = pygame.Rect(col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
                pygame.draw.rect(self.display, self.BLACK, rect, 1)
                if board[row][col] == 1:
                    # Calculate position to center the piece
                    x_pos = col * self.CELL_SIZE + (self.CELL_SIZE - self.black_piece_image.get_width()) // 2
                    y_pos = row * self.CELL_SIZE + (self.CELL_SIZE - self.black_piece_image.get_height()) // 2
                    self.display.blit(self.black_piece_image, (x_pos, y_pos))
                elif board[row][col] == -1:
                    # Calculate position to center the piece
                    x_pos = col * self.CELL_SIZE + (self.CELL_SIZE - self.white_piece_image.get_width()) // 2
                    y_pos = row * self.CELL_SIZE + (self.CELL_SIZE - self.white_piece_image.get_height()) // 2
                    self.display.blit(self.white_piece_image, (x_pos, y_pos))