import numpy as np
import pygame as pg
import physics
import Car
import Wall
import Controller
import json

START_DIR = (-1,0)
BACKGROUND = (227, 227, 227)

def Save_Map(map):
    data = []
    for wall in map:
        wall_info = {
            'type': wall.__class__.__name__,
            'centerx': wall.rect.centerx,
            'centery': wall.rect.centery,
            'norm_angle': wall.normal.as_polar()[1]
        }
        data.append(wall_info)
    
    with open('assets/map.json', 'w') as f:
        json.dump(data, f)

def Load_Map(map, wall_types):
    with open('assets/map.json') as f:
        data = json.load(f)

    for wall in data:
        wall_type = wall_types[wall['type']]
        new_wall = wall_type(wall['centerx'], wall['centery'], wall['norm_angle'])
        map.add(new_wall)

def Add_Wall(map, screen_width, screen_height):
    new_wall = Wall.Wall_Straight(screen_width - 40, screen_height/2, 180)
    map.add(new_wall)

def main():
    # pg setup
    pg.init()
    screen = pg.display.set_mode((0,0), vsync=1)
    clock = pg.time.Clock()
    running = True

    cars = pg.sprite.Group()
    
    screen_width, screen_height = screen.get_width(), screen.get_height()
    p1 = Car.Car_Green(screen_width/2, screen_height/2)
    p1_controls = Controller.User_Controller(p1, pg.K_w, pg.K_s, pg.K_a, pg.K_d)
    p2 = Car.Car_Blue(screen_width/2, screen_height/2+30)
    p2_controls = Controller.User_Controller(p2, pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT)
    cars.add(p1, p2)

    map = pg.sprite.Group()
    Load_Map(map, {"Wall_Straight" : Wall.Wall_Straight})

    skids = pg.sprite.Group()

    reset = pg.image.load('assets/reset.png')
    reset = reset.convert_alpha()
    reset = pg.transform.scale_by(reset, 0.1)
    reset_rect = reset.get_rect()
    reset_rect.top = 5
    reset_rect.right = screen_width-5

    pause = pg.image.load('assets/Pause.png')
    pause = pause.convert_alpha()
    pause = pg.transform.scale_by(pause, .65)
    pause_rect = pause.get_rect()
    pause_rect.top = reset_rect.bottom + 10
    pause_rect.right = screen_width-5

    Play = True

    while running:
        mouse_pos = pg.mouse.get_pos()

        # pg.QUIT event means the user clicked X to close your window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if pause_rect.collidepoint(mouse_pos):
                    Play = not Play

        keys = pg.key.get_pressed()

        click = pg.mouse.get_pressed()[0]

        if click:
            for wall in map:
                if wall.rect.collidepoint(mouse_pos):
                    x, y = mouse_pos[0] - wall.rect.x, mouse_pos[1] - wall.rect.y
                    if wall.mask.get_at((x, y)):
                        if wall.rect.center == (screen_width - 40, screen_height/2):
                            Add_Wall(map, screen_width, screen_height)
                        wall.update(mouse_pos, keys)
                        break # Don't want to move multiple walls at once
            if reset_rect.collidepoint(mouse_pos):
                p1.rect.center = (screen_width/2, screen_height/2)
                p1.vel.update(0,0)
                p1.dir.update(START_DIR)
                p2.rect.center = (screen_width/2, screen_height/2+30)
                p2.vel.update(0,0)
                p2.dir.update(START_DIR)
            for car in cars:
                if car.rect.collidepoint(mouse_pos):
                    car.set_pos(mouse_pos)

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(BACKGROUND)

        # update player1 controller
        p1_controls.output()

        # update player2 controller
        p2_controls.output()

        # update/draw skids
        skids.update(screen)

        # update car group
        if Play:
            cars.update(map, cars, skids)

        # draw car group
        cars.draw(screen)

        # draw wall group
        map.draw(screen)

        # draw reset button
        screen.blit(reset, reset_rect)

        # draw pause button
        screen.blit(pause, pause_rect)

        font = pg.font.Font(None, 32)
        text = font.render(f"P1 Speed: {int(p1.vel.magnitude()* 5)} mph P2 Speed: {int(p2.vel.magnitude()* 5)} mph", True, "black")
        textpos = text.get_rect(centerx=screen.get_width()/2, y=10)
        screen.blit(text, textpos)

        # flip() the display to put your work on screen
        pg.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        physics.dt = clock.tick(60) / 1000

    Save_Map(map)
    pg.quit()

if __name__ == "__main__":
    main()