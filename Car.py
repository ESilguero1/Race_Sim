import pygame as pg
import physics

CAR_WIDTH_PX = 372 * .075
CAR_LENGTH_PX = 961 * .075
BACK_WHEEL_DIST = 20
SKID_FADE_RATE = 1
SKID_LENGTH = 5
SKID_WIDTH = 3
BACKGROUND = (227, 227, 227)

class Skid(pg.sprite.Sprite):
    def __init__(self, x, y, dir):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((CAR_WIDTH_PX, SKID_LENGTH))
        self.image.fill(BACKGROUND)
        pg.draw.line(self.image, "black", (2, 0), (2, SKID_LENGTH), SKID_WIDTH)
        pg.draw.line(self.image, "black", (CAR_WIDTH_PX - 3, 0), (CAR_WIDTH_PX - 3, SKID_LENGTH), SKID_WIDTH)
        self.alpha = 255
        self.rect = self.image.get_rect()
        self.rect.center = (x - dir[0]*(CAR_LENGTH_PX-BACK_WHEEL_DIST)/2, y + dir[1]*(CAR_LENGTH_PX-BACK_WHEEL_DIST)/2)
        # Rotate skid to face in set direction
        self.dir = dir
        self.image = pg.transform.rotate(self.image, self.dir.as_polar()[1] + 90)
        self.rect = self.image.get_rect(center = self.rect.center)
    
    def update(self, screen):
        self.image.set_alpha(self.alpha)
        screen.blit(self.image, self.rect)
        self.alpha -= 1
        if self.alpha == 0:
            self.kill()

class Car(pg.sprite.Sprite):
    def __init__(self, image, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.original_image = image
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        # direction vector
        self.dir = pg.math.Vector2(-1,0)

        # velocity vctor
        self.vel = pg.math.Vector2(0,0)

        # steering angle [-1, 1]
        self.steer = 0

        # rotational velocity
        self.w = 0

        # engine throttle [-1, 1]
        self.throttle = 0

    def update(self, map, cars, skids):
        physics.Car_Physics(self, map, cars, skids)

        # Update image orientation
        self.image = pg.transform.rotate(self.original_image, self.dir.as_polar()[1])
        self.rect = self.image.get_rect(center = self.rect.center)
        self.mask = pg.mask.from_surface(self.image)

    def set_pos(self, pos):
        self.rect.center = pos

class Car_Green(Car):
    def __init__(self, x, y):
        f1 = pg.image.load('assets/F1_Green.png')
        f1 = f1.convert_alpha()
        f1 = pg.transform.scale_by(f1, .075)
        Car.__init__(self, f1, x, y)

class Car_Blue(Car):
    def __init__(self, x, y):
        f1 = pg.image.load('assets/F1_Blue.png')
        f1 = f1.convert_alpha()
        f1 = pg.transform.scale_by(f1, .075)
        Car.__init__(self, f1, x, y)