import pygame, sys
from pygame.math import Vector2 as vector
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, path, collision_sprites, shoot):
        super().__init__(pos, path, groups, shoot)

        # collision
        self.collision_sprites = collision_sprites

        # vertical movement
        self.gravity = 15
        self.jump_speed = 1200
        self.on_floor = False
        self.moving_floor = None

        self.health = 10

    def get_status(self):
        # idle
        if self.direction.x == 0 and self.on_floor:
            self.status = self.status.split('_')[0] + '_idle'
        # jump
        if self.direction.y != 0 and not self.on_floor:  # second if is not necessary because it is gonna be false
            self.status = self.status.split('_')[0] + '_jump'

        # duck
        if self.on_floor and self.duck:
            self.status = self.status.split('_')[0] + '_duck'

    def check_contact(self): # here we create a rect below the player and check if its inside of an obstacle or not for the idle/moving/jumping animations
        bottom_rect = pygame.Rect(0, 0, self.rect.width, 5)
        bottom_rect.midtop = self.rect.midbottom
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(bottom_rect):
                if self.direction.y > 0:
                    self.on_floor = True
                if hasattr(sprite, 'direction'): # only a moving platform has a direction (pos and speed would also work as well)
                    self.moving_floor = sprite

    def input(self):
        keys = pygame.key.get_pressed()
        # horizontal input
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

        if keys[pygame.K_UP] and self.on_floor:
            self.direction.y = -self.jump_speed

        if keys[pygame.K_DOWN]:
            self.duck = True
        else:
            self.duck = False

        if keys[pygame.K_SPACE] and self.can_shoot:
            direction = vector(1, 0) if self.status.split('_')[0] == 'right' else vector(-1, 0)
            pos = self.rect.center + direction * 60
            y_offset = vector(0, -16) if not self.duck else vector(0, 10) # we can duck shoot while on air
            self.shoot(pos + y_offset, direction ,self)

            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            self.shoot_sound.play()

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):

                if direction == 'horizontal':
                    # left collision
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                    # right collision
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                    self.pos.x = self.rect.x
                else:
                    # vertical collision
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.on_floor = True
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                    self.pos.y = self.rect.y
                    self.direction.y = 0

        if self.on_floor and self.direction.y != 0:  # this switches on floor to false of player is floating
            self.on_floor = False

    def move(self, dt):
        if self.duck and self.on_floor:
            self.direction.x = 0

        # horizontal movement + collision
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.collision('horizontal') # this one is a function, dont get confused

        # vertical movement + collision
        # gravity
        self.direction.y += self.gravity
        self.pos.y += self.direction.y * dt

        # glue the player to the platform                              # if the player is not jumping
        if self.moving_floor and self.moving_floor.direction.y > 0 and self.direction.y > 0: # if platform is going up its fine but here we are checking if the platform is moving downwards to fix the glitching animation
            self.direction.y = 0
            self.rect.bottom = self.moving_floor.rect.top
            self.pos.y = self.rect.y
            self.on_floor = True

        self.rect.y = round(self.pos.y)
        self.collision('vertical')
        self.moving_floor = None # this gonna make the hasattr in check_contant() gone and we would't stick to the platform while jumping when its moving down

    def check_death(self):
        if self.health <= 0:
            pygame.quit()
            sys.exit()

    def update(self, dt):
        self.old_rect = self.rect.copy() # 129 -> 5:00
        self.input()
        self.get_status()
        self.move(dt)
        self.check_contact()

        self.animate(dt)
        self.blink()

        # timer
        self.shoot_timer()
        self.invul_timer()

        # death
        self.check_death()

        self.check_death()