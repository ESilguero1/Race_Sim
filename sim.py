import numpy as np
import pygame as pg
import physics
from Car import Car
from Wall import Wall

def main():
    # pg setup
    pg.init()
    screen = pg.display.set_mode((0,0), vsync=1)
    clock = pg.time.Clock()
    running = True
    dt = 0
    
    f1 = pg.image.load('assets/F1.png')
    f1 = f1.convert_alpha()
    f1 = pg.transform.scale_by(f1, .075)

    cars = pg.sprite.Group()
    
    screen_width, screen_height = screen.get_width(), screen.get_height()
    p1 = Car(f1, screen_width/2, screen_height/2)
    cars.add(p1)

    w1 = pg.image.load('assets/Wall_straight.png')
    w1 = w1.convert_alpha()
    test_wall = Wall(w1, screen_width/2 + 80, screen_height/2, 180+45)
    map = pg.sprite.Group()
    map.add(test_wall)

    reset = pg.image.load('assets/reset.png')
    reset = reset.convert_alpha()
    reset = pg.transform.scale_by(reset, 0.1)
    reset_rect = reset.get_rect()
    reset_rect.top = 5
    reset_rect.right = screen_width-5

    Play = True

    while running:

        # pg.QUIT event means the user clicked X to close your window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        keys = pg.key.get_pressed()

        if keys[pg.K_p] and Play:
            Play = not Play

        click = pg.mouse.get_pressed()[0]

        if click:
            mouse_pos = pg.mouse.get_pos()
            if test_wall.rect.collidepoint(mouse_pos):
                test_wall.update(mouse_pos, keys)
            if reset_rect.collidepoint(mouse_pos):
                p1.rect.center = (screen_width/2, screen_height/2)
                p1.vel = pg.math.Vector2(0,0)

        # fill the screen with a color to wipe away anything from last frame
        screen.fill((227, 227, 227))

        # update car group
        if Play:
            cars.update(keys, map)

        # draw car group
        cars.draw(screen)

        # draw wall group
        map.draw(screen)

        # draw reset button
        screen.blit(reset, reset_rect)

        font = pg.font.Font(None, 32)
        text = font.render(f"Speed: {int(p1.vel.magnitude()* 5)} mph", True, "black")
        textpos = text.get_rect(centerx=screen.get_width()/2, y=10)
        screen.blit(text, textpos)

        # flip() the display to put your work on screen
        pg.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        physics.dt = clock.tick(60) / 1000

    pg.quit()

if __name__ == "__main__":
    main()