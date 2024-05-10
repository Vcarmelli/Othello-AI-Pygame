import pygame,os
#loading images
def load_images():
    images = {}
    # Load board image
    images['board'] = pygame.image.load(os.path.join('assets/boardbg.png'))
    # Load player pieces images
    images['black_piece'] = pygame.image.load(os.path.join('assets/piece2.png'))
    images['white_piece'] = pygame.image.load(os.path.join('assets/piece1.png'))
    return images