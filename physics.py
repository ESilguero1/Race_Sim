import pygame as pg
import math                        

DIST_SCALE = 60
TIRE_FRIC_COEFF = 1.7
MECH_FRIC = 100 # N
DRAG_COEFF = 0.7
DRAG_AREA = 1.43 # m^2
CAR_MASS = 800 # kg
ENGINE_TORQUE = 1200 # N*m
TIRE_RAD = 0.36 # m
GRAVITY = 9.8 # m/s^2
WHEELBASE = 1.6 # m
STEER_ANGLE_MAX = 30 # deg
WALL_ELASTICITY_COEF = 0.4
dt = 1/60

def Car_Physics(Car, map):
    if dt == 0:
        return

    # Normalize velocity vector to see if we're sliding
    vel_mag = Car.vel.magnitude()

    # Stabilize small velocity by setting to 0
    if vel_mag < 0.5 and Car.throttle == 0:
        Car.vel = pg.math.Vector2(0,0)
        vel_mag = 0

    vel_normalized = Car.vel.normalize() if vel_mag > 0 else Car.vel

    # Forces acting on car:
    # Normal force, between car and ground
    f_n = GRAVITY * CAR_MASS + (DRAG_COEFF * vel_mag**2) # gravity + downforce

    # Engine torque / tire radius, in direction of car
    f_eng = Car.throttle * (min(ENGINE_TORQUE / TIRE_RAD, f_n)) * Car.dir

    # Drag, opposing car velocity
    f_drag = vel_mag**2*DRAG_COEFF*DRAG_AREA*-vel_normalized

    # Mechanical friction, opposing car
    f_mech = pg.math.Vector2(0,0)
    if vel_mag > 0:
        f_mech = -vel_normalized*MECH_FRIC

    # Friction, opposing the car's sliding (lateral velocity)
    dir_perp = Car.dir.rotate(90) # Vector for the car's side direction
    vel_lat = Car.vel.project(dir_perp) # How much of our velocity vector is lateral to the car
    force_needed = (CAR_MASS*vel_lat/dt).magnitude() # The force that will stop our sliding
    f_fric_max = TIRE_FRIC_COEFF * f_n
    f_fric = min(f_fric_max, force_needed)*-vel_lat.normalize() if vel_lat.magnitude() > 0 else pg.math.Vector2(0,0) # friction will oppose sliding until it can't

    # Net force
    f_net = f_eng + f_drag + f_mech + f_fric

    # f = ma
    a_net = f_net/CAR_MASS

    # Integrate acceleration to get velocity
    new_vel = Car.vel + a_net*dt

    # Apply steering to heading of car
    turn_rad = math.inf
    if not Car.steer == 0:
        turn_rad = WHEELBASE/math.sin(math.radians(Car.steer*STEER_ANGLE_MAX))

    # Determine if we're moving forward or backward
    vector_dot_prod = Car.dir.dot(vel_normalized)if vel_mag > 0 else 1
    if vector_dot_prod < 0:
        turn_rad = -turn_rad # negate turn radius if we're going backwards

    w = (vel_mag/turn_rad)

    # Change in angle
    delta_theta = -w*dt
    new_dir = Car.dir.rotate(math.degrees(delta_theta))


    # Check for collisions 
    wall_hit_list = pg.sprite.spritecollide(Car, map, False)
    for wall in wall_hit_list:
        if pg.sprite.collide_mask(Car, wall):
            while pg.sprite.collide_mask(Car, wall):
                Car.rect.move_ip(wall.normal.x*2, -wall.normal.y*2)

            # Reflect car off wall
            new_vel.update(new_vel.reflect(wall.normal)*WALL_ELASTICITY_COEF)

            # Turn car
            # new_dir.update((new_dir + wall.normal/2).normalize())

    # Move
    Car.rect.move_ip(new_vel.x*dt*DIST_SCALE, -new_vel.y*dt*DIST_SCALE)

    Car.vel.update(new_vel)
    Car.dir.update(new_dir)