import numpy as np
import pygame

def main():
    # pygame setup
    pygame.init()
    size = width, height = 1280, 720
    screen = pygame.display.set_mode(size, flags=pygame.SCALED, vsync=1)
    clock = pygame.time.Clock()
    running = True
    dt = 0
    
    player = pygame.image.load('assets/F1.png')
    player = player.convert_alpha()
    player = pygame.transform.scale_by(player, .15)
    playerrect = player.get_rect()

    SPEED = 300

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("white")

        # draw player on screen
        screen.blit(player, playerrect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and playerrect.top > 0:
            playerrect = playerrect.move(0,-SPEED * dt)
        if keys[pygame.K_s] and playerrect.bottom < height:
            playerrect = playerrect.move(0,SPEED * dt)
        if keys[pygame.K_a] and playerrect.left > 0:
            playerrect = playerrect.move(-SPEED * dt, 0)
        if keys[pygame.K_d] and playerrect.right < width:
            playerrect = playerrect.move(SPEED * dt, 0)


        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()

if __name__ == "__main__":
    main()