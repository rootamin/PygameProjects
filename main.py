import pygame, sys

class Ship(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups) # we have to init the parent class
        self.image = pygame.image.load('graphics/ship.png').convert_alpha()  # has to be image
        self.rect = self.image.get_rect(center=(WINDOWS_WIDTH/2, WINDOWS_HEIGHT/2)) # has to be rect

    def input_position(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

    def laser_shoot(self):
        def laser_timer(can_shoot, duration=500):
            if not can_shoot:
                current_time = pygame.time.get_ticks()
                if current_time - sh
        if pygame.mouse.get_pressed()[0]:
            print('shoot laser')

    def update(self):
        self.input_position()
        self.laser_shoot()

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/laser.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)

# basic setup
pygame.init()
WINDOWS_WIDTH, WINDOWS_HEIGHT = 1280, 720
screen = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HEIGHT))
pygame.display.set_caption('Asteroid shooter')
clock = pygame.time.Clock()

# background
bg_surf = pygame.image.load('graphics/background.png').convert()

# sprite groups
spaceship_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()

# sprite creation
ship = Ship(spaceship_group)
ship.update()
laser = Laser((100, 300), laser_group)

# game loop
while True:

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # delta time
        dt = clock.tick() / 1000

        # background
        screen.blit(bg_surf, (0, 0))

        # update
        spaceship_group.update()

        # graphics
        spaceship_group.draw(screen)
        laser_group.draw(screen)

        # draw the frame
        pygame.display.update()
