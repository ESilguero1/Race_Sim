import pygame  
import  math                          

TIRE_FRIC_COEFF = 1.7
MECH_FRIC = 50 # N
DRAG_COEFF = 0.7
DRAG_AREA = 1.43 # m^2
CAR_MASS = 800 # kg
ENGINE_TORQUE = 1200 # N*m
TIRE_RAD = 0.36 # m
GRAVITY = 9.8 # m/s^2
WHEELBASE = 1.6 # m
STEER_ANGLE_MAX = 30 # deg
dt = 1/60

def Car_Physics(Car):

    # Normalize velocity vector to see if we're sliding
    vel_mag = Car.vel.magnitude()

    # Stabilize small velocity by setting to 0
    if vel_mag < 0.5 and Car.throttle == 0:
        Car.vel = pygame.math.Vector2(0,0)
        vel_mag = 0

    vel_normalized = Car.vel.normalize() if vel_mag > 0 else Car.vel

    # Determine how sideways we are for frictional force
    dir_perp = Car.dir.rotate(90)
    slide = dir_perp.dot(Car.vel)

    # Forces acting on car:
    # Engine torque / tire radius in direction of car
    f_eng = Car.throttle * (ENGINE_TORQUE / TIRE_RAD) * Car.dir

    # Drag, opposing car velocity
    f_drag = vel_mag**2*DRAG_COEFF*DRAG_AREA*-vel_normalized

    # Mechanical friction, opposing car
    f_mech = pygame.math.Vector2(0,0)
    if vel_mag > 0:
        f_mech = -vel_normalized*MECH_FRIC

    # Friction, opposing the car's sliding
    f_n = GRAVITY * CAR_MASS + (DRAG_COEFF/4 * vel_mag**2) # gravity + downforce
    f_fric = TIRE_FRIC_COEFF * f_n * -dir_perp * slide

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

    w = vel_mag/turn_rad

    # Determine if we're moving forward or backward
    vector_dot_prod = Car.dir.dot(vel_normalized)if vel_mag > 0 else 1
    if vector_dot_prod < 0:
        w = -w # negate rotation if moving backward

    # Change in angle
    delta_theta = -w*dt
    new_dir = Car.dir.rotate(math.degrees(delta_theta))

    Car.vel.update(new_vel)
    Car.dir.update(new_dir)