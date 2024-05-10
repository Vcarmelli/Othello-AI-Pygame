import pygame
#loading images
def loadImages(path, size):
    img = pygame.image.load(f"{path}").convert_alpha()
    img = pygame.transform.scale(img, (32, 32))
    return img

def loadSpriteSheet(sheet, row, col, size, scale):
    image = pygame.Surface((32, 32)).convert_alpha()
    image.blit(sheet, (0, 0), (row * size[0], col * size[1], size[0], size[1]))
    image = pygame.transform.scale(image, scale)
    image.set_colorkey((0, 0, 0))
    return image