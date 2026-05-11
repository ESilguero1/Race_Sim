import pygame as pg
import math   
import Car                     

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
STEER_ANGLE_MAX = 45 # deg
WALL_ELASTICITY_COEF = 0.4
CAR_ELASTICITY_COEF = 0.7
COLLISION_PUSHBACK = 5 # to avoid feedback collisions
dt = 1/60

def Car_Physics(Car_Moving, map, cars, skids):
    # Normalize velocity vector to see if we're sliding
    vel_mag = Car_Moving.vel.magnitude()

    # Stabilize small velocity by setting to 0
    if vel_mag < 0.5 and Car_Moving.throttle == 0:
        Car_Moving.vel = pg.math.Vector2(0,0)
        vel_mag = 0

    vel_normalized = Car_Moving.vel.normalize() if vel_mag > 0 else Car_Moving.vel

    # Forces acting on car:
    # Normal force, between car and ground
    f_n = GRAVITY * CAR_MASS + (DRAG_COEFF * vel_mag**2) # gravity + downforce

    # Engine torque / tire radius, in direction of car
    f_eng = Car_Moving.throttle * (min(ENGINE_TORQUE / TIRE_RAD, f_n)) * Car_Moving.dir

    # Drag, opposing car velocity
    f_drag = vel_mag**2*DRAG_COEFF*DRAG_AREA*-vel_normalized

    # Mechanical friction, opposing car
    f_mech = pg.math.Vector2(0,0)
    if vel_mag > 0:
        f_mech = -vel_normalized*MECH_FRIC

    # Friction, opposing the car's sliding (lateral velocity)
    dir_perp = Car_Moving.dir.rotate(90) # Vector for the car's side direction
    vel_lat = Car_Moving.vel.project(dir_perp) # How much of our velocity vector is lateral to the car
    force_needed = (CAR_MASS*vel_lat/dt).magnitude() # The force that will stop our sliding
    f_fric_max = TIRE_FRIC_COEFF * f_n
    f_fric = min(f_fric_max, force_needed)*-vel_lat.normalize() if vel_lat.magnitude() > 0 else pg.math.Vector2(0,0) # friction will oppose sliding until it can't

    if force_needed > f_fric_max:
        skids.add(Car.Skid(Car_Moving.rect.centerx, Car_Moving.rect.centery, Car_Moving.dir))

    # Net force
    f_net = f_eng + f_drag + f_mech + f_fric

    # f = ma
    a_net = f_net/CAR_MASS

    # Integrate acceleration to get velocity
    new_vel = Car_Moving.vel + a_net*dt

    # Apply steering to heading of car
    turn_rad = math.inf
    if not Car_Moving.steer == 0:
        turn_rad = WHEELBASE/math.sin(math.radians(Car_Moving.steer*STEER_ANGLE_MAX))

    # Determine if we're moving forward or backward
    vector_dot_prod = Car_Moving.dir.dot(vel_normalized)if vel_mag > 0 else 1
    if vector_dot_prod < 0:
        turn_rad = -turn_rad # negate turn radius if we're going backwards

    w = (vel_mag/turn_rad)

    # Change in angle
    delta_theta = -w*dt
    new_dir = Car_Moving.dir.rotate(math.degrees(delta_theta))


    # Check for collisions 
    wall_hit_list = pg.sprite.spritecollide(Car_Moving, map, False)
    for wall in wall_hit_list:
        if pg.sprite.collide_mask(Car_Moving, wall):
            while pg.sprite.collide_mask(Car_Moving, wall):
                Car_Moving.rect.move_ip(wall.normal.x*COLLISION_PUSHBACK, -wall.normal.y*COLLISION_PUSHBACK)

            # Reflect car off wall
            new_vel.update(new_vel.reflect(wall.normal)*WALL_ELASTICITY_COEF)

            # Turn car
            # new_dir.update((new_dir + wall.normal/2).normalize())
    
    car_hit_list = pg.sprite.spritecollide(Car_Moving, cars, False)
    for other_car in car_hit_list:
        if not other_car == Car_Moving:
            if pg.sprite.collide_mask(Car_Moving, other_car):
                # Get vector between cars
                collision_normal = pg.math.Vector2(Car_Moving.rect.centerx - other_car.rect.centerx, Car_Moving.rect.centery-other_car.rect.centery).normalize()
                while pg.sprite.collide_mask(Car_Moving, other_car):
                    Car_Moving.rect.move_ip(collision_normal.x*COLLISION_PUSHBACK, collision_normal.y*COLLISION_PUSHBACK)
                
                # Conservation of momentum, trivial solution (equal masses)
                temp_vel = new_vel
                new_vel = other_car.vel * CAR_ELASTICITY_COEF
                other_car.vel = temp_vel * CAR_ELASTICITY_COEF

    # Move
    Car_Moving.rect.move_ip(new_vel.x*dt*DIST_SCALE, -new_vel.y*dt*DIST_SCALE)

    Car_Moving.vel.update(new_vel)
    Car_Moving.dir.update(new_dir)