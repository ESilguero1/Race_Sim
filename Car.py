import pygame
import physics

class Car(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.original_image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        # direction vector
        self.dir = pygame.math.Vector2(1,0)

        # velocity vctor
        self.vel = pygame.math.Vector2(0,0)

        # steering angle [-1, 1]
        self.steer = 0

        # engine throttle [-1, 1]
        self.throttle = 0

    def update(self):
        keys = pygame.key.get_pressed()
        self.steer = 0
        self.throttle = 0

        if keys[pygame.K_a]:
            self.steer = -1
        if keys[pygame.K_d]:
            self.steer = 1
        if keys[pygame.K_w]:
            self.throttle = 1
        if keys[pygame.K_s]:
            self.throttle = -0.5

        physics.Car_Physics(self)

        self.rect.move_ip(self.vel[0], -self.vel[1])
        self.image = pygame.transform.rotozoom(self.original_image, self.dir.as_polar()[1], 1)
        self.rect = self.image.get_rect(center = self.rect.center)