import pygame

class Menu:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.image = pygame.image.load('assets/bg.jpg')
        self.image = pygame.transform.scale(self.image, (self.display.get_width(), self.display.get_height()))
        self.font = pygame.font.Font(None, 36) 

    def run(self):
        pygame.display.set_caption('Menu')

        self.display.fill((0, 0, 0))
        self.display.blit(self.image, (0, 0))

        text = self.font.render("Hello, World!", True, (255, 255, 255)) 
        text_rect = text.get_rect(center=(self.display.get_width() // 2, self.display.get_height() // 2))

        self.display.blit(text, text_rect)

        pygame.display.update()
