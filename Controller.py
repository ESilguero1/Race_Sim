import pygame as pg
import math

class Controller:
    def __init__(self):
        self.steer = 0
        self.throttle = 0

    def output(self, Car):
        if self.steer > 1: self.steer = 1
        if self.steer < -1: self.steer = -1
        if self.throttle > 1: self.throttle = 1
        if self.throttle < -0.5: self.throttle = -0.5
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
        self.front_dist = 0
        self.front_left_dist = 0
        self.front_right_dist = 0
        self.left_dist = 0
        self.right_dist = 0

    def get_distances(self, sensors):
        self.front_dist = sensors["front"].get_dist()
        self.front_left_dist = sensors["front_left"].get_dist()
        self.front_right_dist = sensors["front_right"].get_dist()
        self.left_dist = sensors["left"].get_dist()
        self.right_dist = sensors["right"].get_dist()

SENSORS_DIST = (961 * .075)/120# how far front right sensor is from right sensor
DIST_REF = 0
ANGLE_REF = 0
class Controller_Tweinstein(Controller_5Sensor):
    def __init__(self, kp_d, kd_d, kp_a, kd_a):
        self.kp_d = kp_d
        self.kd_d = kd_d
        self.kp_a = kp_a
        self.kd_a = kd_a
        self.prev_dist_error = 0
        self.prev_angle_error = 0
        super().__init__()

    # Solves for the angle to the wall given front angled and side sensor
    def get_angle(self, front_angled, side):
        a = front_angled + SENSORS_DIST*math.sqrt(2)
        b = side + SENSORS_DIST
        c_squared = math.pow(a, 2) + math.pow(b, 2) + - 2*a*b*math.cos(math.radians(45)) # Law of cosines
        c = math.sqrt(c_squared)
        angle = math.asin((math.sin(math.radians(45))/c)*a) # Law of sines
        return angle

    def output (self, Car, sensors):
        self.get_distances(sensors)
    
        # find angle to wall
        right_angle = self.get_angle(self.front_right_dist, self.right_dist)
        left_angle = self.get_angle(self.front_left_dist, self.left_dist)
        
        # use angle to find perpendicular distance to wall
        perp_dist_right = math.sin(right_angle)*self.right_dist
        perp_dist_left = math.sin(left_angle)*self.left_dist

        # distance error is difference between left and right - ref
        dist_error = perp_dist_right - perp_dist_left - DIST_REF

        # use distance error to produce intended heading angle
        intended_angle = self.kp_d*dist_error + self.kd_d*(dist_error - self.prev_dist_error)
        self.prev_dist_error = dist_error

        # angle error is intended - difference between angles on each side - ref
        angle_error = intended_angle - (right_angle - left_angle) - ANGLE_REF

        # use angle error to produce steering output
        self.steer = self.kp_a*angle_error + self.kd_a*(angle_error - self.prev_angle_error)
        self.prev_angle_error = angle_error

        self.throttle = 0.1

        super().output(Car)