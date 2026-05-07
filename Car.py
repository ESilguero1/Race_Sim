import pygame
import physics
import math

width, height = 1280, 720



# Source - https://stackoverflow.com/a/54714144
# Posted by Rabbid76, modified by community. See post 'Timeline' for change history
# Retrieved 2026-05-07, License - CC BY-SA 4.0

def rot_center(image, angle, x, y):
    
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect



class Car(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.original_image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        # direction vectors
        self.dir_x = 1
        self.dir_y = 0

        self.angle = 0

    def update(self):
        keys = pygame.key.get_pressed()
        self.angle = math.atan2(-self.dir_y, self.dir_x)

        vel = 0
        if keys[pygame.K_w]:
            vel = 1 # moving forward
        if keys[pygame.K_s]:
            vel = -1 # moving backward
        if keys[pygame.K_a]:
            self.angle += physics.ROT_SPEED*physics.dt
        if keys[pygame.K_d]:
            self.angle -= physics.ROT_SPEED*physics.dt

        self.dir_x = math.cos(self.angle)
        self.dir_y = math.sin(-self.angle)

        self.rect.move_ip(physics.SPEED * physics.dt * self.dir_x * vel, physics.SPEED * physics.dt * self.dir_y * vel)

        self.image = pygame.transform.rotozoom(self.original_image, math.degrees(self.angle), 1)
        self.rect = self.image.get_rect(center = self.rect.center)