import numpy as np
import pygame
import physics
from Car import Car

def main():
    # pygame setup
    pygame.init()
    size = width, height = 1280, 720
    screen = pygame.display.set_mode(size, flags=pygame.SCALED, vsync=1)
    clock = pygame.time.Clock()
    running = True
    dt = 0
    
    f1 = pygame.image.load('assets/F1.png')
    f1 = f1.convert_alpha()
    f1 = pygame.transform.scale_by(f1, .075)

    cars = pygame.sprite.Group()
    
    p1 = Car(f1, width/2, height/2)
    cars.add(p1)

    while running:

        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("white")

        # update car group
        cars.update()

        # draw car group
        cars.draw(screen)

        font = pygame.font.Font(None, 32)
        text = font.render(f"Speed: {int(p1.vel.magnitude()* 5)} mph", True, "black")
        textpos = text.get_rect(centerx=screen.get_width()/2, y=10)
        screen.blit(text, textpos)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        physics.dt = clock.tick(60) / 1000

    pygame.quit()

if __name__ == "__main__":
    main()