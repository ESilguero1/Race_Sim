import pygame as pg

class Controller:
    def __init__(self, Car):
        self.Car = Car

class User_Controller(Controller):
    def __init__(self, Car, forward, backward, left, right):
        Controller.__init__(self, Car)
        self.forward = forward
        self.backward = backward
        self.left = left
        self.right = right

    def output(self):
        keys = pg.key.get_pressed()

        self.Car.steer = 0
        self.Car.throttle = 0

        if keys[self.left]:
            self.Car.steer = -1
        if keys[self.right]:
            self.Car.steer = 1
        if keys[self.forward]:
            self.Car.throttle = 1
        if keys[self.backward]:
            self.Car.throttle = -0.5