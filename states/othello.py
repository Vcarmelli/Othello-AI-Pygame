import pygame, random, copy, sys
from .utils import loadImages


class Othello:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        
        self.rows = 8
        self.columns = 8
        
        self.grid = Grid(self.rows, self.columns, (80,80), self)

        self.RUNNING = True
    
    def run(self):
        while self.RUNNING == True:
            self.input()
            self.update()
            self.render()


    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.RUNNING = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print('Left click')
                    self.grid.drawGrid()


    def update(self):
        pass

    def render(self):
        self.display.fill((0, 0, 0))
    
        pygame.display.flip()

class Grid:
    def __init__(self,rows, columns,size,main):
        self.rows = rows
        self.columns = columns
        self.size = size
        self.main = main

        self.logicGrid = self.emptyGrid(self.rows, self.columns)

    def emptyGrid(self, rows, columns): #class for empty grid
        grid = []
        for y in range(rows):
            line = []
            for x in range(columns):
                line.append(0)
            grid.append(line)

        return grid
    
    def drawGrid(self):
        print('  | A | B | C | D | E | F | G | H |')
        for i, row in enumerate(self.logicGrid):
            line = f'{i} |'.ljust(3, " ")
            for item in row:
                line += f"{item}".center(3, " ") + "|"
            print(line)
        print()