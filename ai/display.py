import pygame

class Fonts:
	def __init__(self):
		self.default = pygame.font.Font(None, 36)
		

class Images:
    def __init__(self, screen):
        cell_size = 60

        self.black_piece = pygame.image.load('assets/piece1.png')
        self.black_piece = pygame.transform.scale(self.black_piece, (int(cell_size / 1.2), int(cell_size / 1.2)))
        self.white_piece = pygame.image.load('assets/piece2.png')
        self.white_piece = pygame.transform.scale(self.white_piece, (int(cell_size / 1.2), int(cell_size / 1.2)))

        self.menu_bg = pygame.image.load('assets/index.png')
        self.menu_bg = pygame.transform.scale(self.menu_bg, (screen.get_width(), screen.get_height()))
        self.setup_bg = pygame.image.load('assets/boardbg.png')
        self.setup_bg = pygame.transform.scale(self.setup_bg, (screen.get_width(), screen.get_height()))


class Draw:
    def __init__(self, screen):
        self.screen = screen
        self.font = Fonts()

    def text(self, fill_color, text, font_color, pos):
        if fill_color is not None:
            text_bg = pygame.Surface(pos)
            text_bg.fill(fill_color)
            bg_rect = text_bg.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

            output = self.font.default.render(text, True, font_color)
            text_rect = output.get_rect(center=(bg_rect.centerx, bg_rect.centery))
            
            self.screen.blit(text_bg, bg_rect)
        else:
            output = self.font.default.render(text, True, font_color)
            text_rect = output.get_rect(center=pos)

        self.screen.blit(output, text_rect)
		

class Button:
	def __init__(self, image, pos, text_input, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = Fonts()
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.default.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def draw_button(self, screen):
		if self.image is not None:
			pygame.draw.rect(screen, (255 ,255, 255), pygame.Rect.inflate(self.text_rect, 30, 25))
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def click_button(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def update_color(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.default.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.default.render(self.text_input, True, self.base_color)