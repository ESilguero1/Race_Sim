import pygame as pg

class Controller:
    def __init__(self):
        self.steer = 0
        self.throttle = 0

    def output(self, Car):
        Car.steer = self.steer
        Car.throttle = self.throttle

class User_Controller(Controller):
    def __init__(self, forward, backward, left, right):
        super().__init__()
        self.forward = forward
        self.backward = backward
        self.left = left
        self.right = right

    def output(self, Car):
        keys = pg.key.get_pressed()

        self.steer = 0
        self.throttle = 0

        if keys[self.left]:
            self.steer = -1
        if keys[self.right]:
            self.steer = 1
        if keys[self.forward]:
            self.throttle = 1
        if keys[self.backward]:
            self.throttle = -0.5

        super().output(Car)

class Controller_5Sensor(Controller):
    def __init__(self):
        super().__init__()

    