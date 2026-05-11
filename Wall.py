import pygame as pg

WALL_SCALE = 5

class Wall(pg.sprite.Sprite):
    def __init__(self, image, centerx, centery, norm_angle):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale_by(image,WALL_SCALE)
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (centerx, centery)
        # Rotate wall to face in set direction
        self.normal = pg.math.Vector2.from_polar((1, norm_angle))
        self.image = pg.transform.rotate(self.image, self.normal.as_polar()[1]+90)
        self.rect = self.image.get_rect(center = self.rect.center)
        self.mask = pg.mask.from_surface(self.image)
        self.rotating = False

    def update(self, mouse_pos, keys):
        self.rect.center = mouse_pos

        if keys[pg.K_r] and self.rotating == False:
            self.normal.update(self.normal.rotate(45))
            self.image = pg.transform.rotate(self.original_image, self.normal.as_polar()[1]+90)
            self.rect = self.image.get_rect(center = self.rect.center)
            self.mask = pg.mask.from_surface(self.image)
            self.rotating = True
        elif not keys[pg.K_r]:
            self.rotating = False
        if keys[pg.K_x]:
            self.kill()

class Wall_Straight(Wall):
    def __init__(self, centerx, centery, norm_angle):
        straight = pg.image.load('assets/Wall_straight.png')
        straight = straight.convert_alpha()
        Wall.__init__(self, straight, centerx, centery, norm_angle)