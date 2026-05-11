import pygame as pg
import physics
import Sensor
import Controller

CAR_WIDTH_PX = 372 * .075
CAR_LENGTH_PX = 961 * .075
BACK_WHEEL_DIST = 20
SKID_FADE_RATE = 1
SKID_LENGTH = 5
SKID_WIDTH = 3
BACKGROUND = (227, 227, 227)

class Skid(pg.sprite.Sprite):
    def __init__(self, x, y, dir):
        super().__init__()
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
    def __init__(self, color, x, y, controller):
        super().__init__()
        f1 = pg.image.load(f"assets/F1_{color}.png")
        f1 = f1.convert_alpha()
        f1 = pg.transform.scale_by(f1, .075)
        self.image = f1
        self.original_image = f1
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

        # controller
        self.controller = controller

        # sensors
        front_sensor = Sensor.Sensor_Far(self, (CAR_LENGTH_PX/2, 0), 0)
        front_right_sensor = Sensor.Sensor_Far(self, (CAR_LENGTH_PX/2 - 2, CAR_WIDTH_PX/2 - 2), 45)
        front_left_sensor = Sensor.Sensor_Far(self, (CAR_LENGTH_PX/2 - 2, -CAR_WIDTH_PX/2 + 2), -45)
        right_sensor = Sensor.Sensor_Short(self, (0, CAR_WIDTH_PX/2 - 2), 90)
        left_sensor = Sensor.Sensor_Short(self, (0, -CAR_WIDTH_PX/2 + 2), -90)
        self.sensors = [front_sensor, front_right_sensor, front_left_sensor, left_sensor, right_sensor]

    def update(self, map, cars, skids, screen):
        self.controller.output(self)

        physics.Car_Physics(self, map, cars, skids)

        # Update image orientation
        self.image = pg.transform.rotate(self.original_image, self.dir.as_polar()[1])
        self.rect = self.image.get_rect(center = self.rect.center)
        self.mask = pg.mask.from_surface(self.image)

        # Update sensor distances
        for sensor in self.sensors:
            sensor.sense(map, screen)

    def set_pos(self, pos):
        self.rect.center = pos

class Car_User(Car):
    def __init__(self, color, x, y):
        controller = Controller.User_Controller(pg.K_w, pg.K_s, pg.K_a, pg.K_d)
        super().__init__(color, x, y, controller)

class Car_Auto(Car):
    def __init__(self, color, x, y):
        controller = Controller.Controller_5Sensor()
        super().__init__(color, x, y, self.controller)