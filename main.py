import random

import pygame, sys
from random import randint, uniform

class Ship(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups) # we have to init the parent class
        self.image = pygame.image.load('graphics/ship.png').convert_alpha()  # has to be image
        self.rect = self.image.get_rect(center=(WINDOWS_WIDTH/2, WINDOWS_HEIGHT/2)) # has to be rect

        self.audio = pygame.mixer.Sound('sounds/laser.ogg')
        self.audio.set_volume(0.1)

        # add a mask
        self.mask = pygame.mask.from_surface(self.image)  # has to be mask


        # timer
        self.can_shoot = True
        self.shoot_time = None

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > 500:
                self.can_shoot = True

    def input_position(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

    def laser_shoot(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            self.audio.play()

            Laser(self.rect.midtop, laser_group)

    def meteor_collisions(self):
        if pygame.sprite.spritecollide(self, meteor_group, False, pygame.sprite.collide_mask):
            pygame.quit()
            sys.exit()

    def update(self):
        self.laser_timer()
        self.input_position()
        self.laser_shoot()

        self.meteor_collisions()

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/laser.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.audio = pygame.mixer.Sound('sounds/explosion.wav')
        self.audio.set_volume(0.1)

        # float based postition
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0, -1)
        self.speed = 600

    def meteor_collision(self):
        if pygame.sprite.spritecollide(self, meteor_group, True, pygame.sprite.collide_mask):
            self.audio.play()
            self.kill()

    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        if self.rect.bottom < 0:
            self.kill()

        self.meteor_collision()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, pos, groups):

        # basic setup
        super().__init__(groups)
        # randomizing the meteor size
        meteor_surf = pygame.image.load('graphics/meteor.png').convert_alpha()
        meteor_size = pygame.math.Vector2(meteor_surf.get_size()) * uniform(0.5, 1.5) # 101x84 original
        self.scaled_surf = pygame.transform.scale(meteor_surf, meteor_size)
        self.image = self.scaled_surf
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)


        # float based positioning
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 600)

        # rotation logic
        self.rotation = 0
        self.rotation_speed = randint(20, 50)

    def rotate(self):
        self.rotation += self.rotation_speed * dt
        rotated_surf = pygame.transform.rotozoom(self.scaled_surf, self.rotation, 1)
        self.image = rotated_surf
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        self.rotate()

        if self.rect.top > WINDOWS_HEIGHT:
            self.kill()

class Score:
    def __init__(self):
        self.font = pygame.font.Font('graphics/subatomic.ttf', 50)

    def display(self):
        score_text = f'Score: {pygame.time.get_ticks() // 1000}'
        text_surf = self.font.render(score_text, True, 'white')
        text_rect = text_surf.get_rect(midbottom=(WINDOWS_WIDTH / 2, WINDOWS_HEIGHT - 80))
        screen.blit(text_surf, text_rect)
        pygame.draw.rect(screen, 'white', text_rect.inflate(30, 30), width=8, border_radius=5)

# basic setup
pygame.init()
WINDOWS_WIDTH, WINDOWS_HEIGHT = 1280, 720
screen = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HEIGHT))
pygame.display.set_caption('Asteroid shooter')
clock = pygame.time.Clock()

# background
bg_surf = pygame.image.load('graphics/background.png').convert()
bg_music = pygame.mixer.Sound('sounds/music.wav')
bg_music.set_volume(0.05)
bg_music.play(loops=-1)

# sprite groups
spaceship_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()

# sprite creation
ship = Ship(spaceship_group)

# timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 300)

# score
score = Score()

# game loop
while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == meteor_timer:
            meteor_x_pos = randint(-100, WINDOWS_WIDTH + 100)
            meteor_y_pos = randint(-150, -50)
            Meteor((meteor_x_pos, meteor_y_pos), meteor_group)

    # delta time
    dt = clock.tick() / 1000

    # background
    screen.blit(bg_surf, (0, 0))

    # update
    spaceship_group.update()
    laser_group.update()
    meteor_group.update()

    # score
    score.display()

    # graphics
    spaceship_group.draw(screen)
    laser_group.draw(screen)
    meteor_group.draw(screen)

    # draw the frame
    pygame.display.update()
