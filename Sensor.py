import pygame as pg
import physics

SENSOR_RESOLUTION = 1
SENSOR_COLOR = (255, 145, 145)

class Sensor:
    def __init__(self, Car, rel_pos, rel_angle, max_dist):
        self.Car = Car
        self.rel_pos = rel_pos
        self.rel_angle = rel_angle
        self.distance = 0
        self.max_dist = max_dist*physics.DIST_SCALE
    
    def sense(self, map, screen):
        rel_place_x = pg.math.Vector2(self.Car.dir*pg.math.Vector2(1, -1).elementwise()*self.rel_pos[0])
        rel_place_y = pg.math.Vector2(self.Car.dir.rotate(90)*pg.math.Vector2(1,-1).elementwise()*self.rel_pos[1])
        sensor_pos = pg.math.Vector2(self.Car.rect.center) + rel_place_x + rel_place_y
        sensor_angle = self.Car.dir.rotate(self.rel_angle) * pg.math.Vector2(1, -1).elementwise()
        sensed_pos = sensor_pos + sensor_angle*SENSOR_RESOLUTION
        self.distance = sensed_pos.distance_to(sensor_pos)
        hit = False
        while not hit and self.distance < self.max_dist:
            sensed_pos += sensor_angle*SENSOR_RESOLUTION
            self.distance = sensed_pos.distance_to(sensor_pos)
            for wall in map:
                if wall.rect.collidepoint(sensed_pos):
                    # get relative position of ray
                    x, y = sensed_pos.x - wall.rect.x, sensed_pos.y - wall.rect.y
                    if wall.mask.get_at((x, y)): # Ray hit a wall
                        hit = True

        pg.draw.line(screen, SENSOR_COLOR, sensor_pos, sensed_pos, 2)
    
    def get_dist(self):
        return self.distance/physics.DIST_SCALE
    
MAX_DIST_FAR = 5 # meters
class Sensor_Far(Sensor):
    def __init__(self, Car, rel_pos, rel_angle):
        super().__init__(Car, rel_pos, rel_angle, MAX_DIST_FAR)
 
MAX_DIST_SHORT = 2 # meters
class Sensor_Short(Sensor):
    def __init__(self, Car, rel_pos, rel_angle):
        super().__init__(Car, rel_pos, rel_angle, MAX_DIST_SHORT)