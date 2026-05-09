import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, startx, starty, endx, endy, normal):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((endx-startx, endy-starty))
        self.rect = self.image.get_rect()
        self.rect.center = ((endx+startx)/2, (endy+starty)/2)
        self.normal = normal