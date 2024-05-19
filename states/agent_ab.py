import pygame
from pygame.locals import *
from states.othello import Othello


class GameTree:

    def __init__(self, board):
        self.parent = None
        # self.kids: {(i, j): node}
        self.kids = {}
        self.board = board

    def getScore(self):
        playerOneCount = self.countPieces(1)
        playerTwoCount = self.countPieces(-1) # AI

        pieceCountScore = 100 * (playerTwoCount - playerOneCount)

        positionalScore = 0
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == -1:
                    positionalScore += self.positionalValue(row, col)
                elif self.board[row][col] == 1:
                    positionalScore -= self.positionalValue(row, col)

        print("score:", pieceCountScore + positionalScore)
        return pieceCountScore + positionalScore

    def countPieces(self, player):
        count = 0
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == player:
                    count += 1
        return count        
    
    def positionalValue(self, i, j):
        # Assign higher values to corners and edges
        if (i == 0 or i == 7) and (j == 0 or j == 7):
            return 100  # Corner
        elif (i == 0 or i == 7) or (j == 0 or j == 7):
            return 10  # Edge
        else:
            return 1  # Other positions
        


class AlphaBeta:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.othello = Othello(display, gameStateManager)


    def run(self):
        while self.othello.RUNNING and not self.othello.check_game_over():
            self.othello.input()
            self.othello.render()
            if self.othello.current_player == -1:
                print("AI SHOULD MOVE: ", self.othello.current_player)

                continue
            print("CURR PLAYER: ", self.othello.current_player)

    


    
