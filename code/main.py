import pygame, sys
from settings import *
from player import Player
from car import Car

# basic setup
pygame.init()
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Frogger')
clock = pygame.time.Clock()

# groups
all_sprites = pygame.sprite.Group()

# sprites
player = Player((600, 400), all_sprites)
car = Car((700, 200), all_sprites)

# game loop
while True:

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # delta time
    dt = clock.tick() / 1000

    # draw a bg
    display_surface.fill('black')

    # update
    all_sprites.update(dt)

    # draw
    all_sprites.draw(display_surface)

    # update the display surface => draw the frame
    pygame.display.update()