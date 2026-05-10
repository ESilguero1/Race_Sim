import pygame as pg
import physics

class Car(pg.sprite.Sprite):
    def __init__(self, image, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.original_image = image
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        # direction vector
        self.dir = pg.math.Vector2(1,0)

        # velocity vctor
        self.vel = pg.math.Vector2(0,0)

        # steering angle [-1, 1]
        self.steer = 0

        # rotational velocity
        self.w = 0

        # engine throttle [-1, 1]
        self.throttle = 0

    def update(self, keys, map):
        self.steer = 0
        self.throttle = 0

        if keys[pg.K_a]:
            self.steer = -1
        if keys[pg.K_d]:
            self.steer = 1
        if keys[pg.K_w]:
            self.throttle = 1
        if keys[pg.K_s]:
            self.throttle = -0.5

        physics.Car_Physics(self, map)

        # Update image orientation
        self.image = pg.transform.rotate(self.original_image, self.dir.as_polar()[1])
        self.rect = self.image.get_rect(center = self.rect.center)
        self.mask = pg.mask.from_surface(self.image)