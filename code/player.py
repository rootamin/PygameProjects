import pygame
from pygame.math import Vector2 as vector
from os import walk

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, path, collision_sprites):
        super().__init__(groups)

        self.import_assets(path)
        self.frame_index = 0
        self.status = 'down'

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # float based movement
        self.pos = vector(self.rect.center)
        self.direction = vector()
        self.speed = 200

        # collisions
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)
        self.collision_sprites = collision_sprites

        # attack
        self.attacking = False

    def get_status(self):
        # idle
        if self.direction.x == 0 and self.direction.y == 0:
            self.status = self.status.split('_')[0] + '_idle'  # fuck python again 6:40  111  => this one could cause "_idle" to get added multiple time in front of the self.status.. so in the next loop we are splitting it to get us a list and choose the first item of the list

        #attacking
        if self.attacking == True:
            self.status = self.status.split('_')[0] + '_attack' # //

    def import_assets(self, path):
        self.animations = {}   # practice on this shit

        for index, folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:

                for file_name in sorted(folder[2], key=lambda string: int(string.split('.')[0])):   # bruuuuuh fuck python
                    path = folder[0].replace('\\', "/") + '/' + file_name
                    surf = pygame.image.load(path).convert_alpha()
                    key = folder[0].split('\\')[1]
                    self.animations[key].append(surf)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.attacking:  # player is able to move if we are NOT attacking
            # horizontal input
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # vertical input
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.direction = vector()  # stops the player movement while attacking
                self.frame_index = 0

    def move(self, dt):
        # normalize a vector -> the length of the vector is going to be 1
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        # horiznontal collision

        # vertical movement + collision
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery

    def animate(self, dt):  # very fucking confusing mind wobbles, just pay enough attentions to variables
        current_animation = self.animations[self.status]

        self.frame_index += 7 * dt
        if self.frame_index >= len(current_animation): # fucked my mind before I realized about self.attacking: it will check how many animation one status have and if the frames of attack finishes, it will set back self.attacking to false and player will able to move again
            self.frame_index = 0
            if self.attacking:
                self.attacking = False

        self.image = current_animation[int(self.frame_index)]

    def update(self, dt):
        self.input()
        self.get_status()
        self.move(dt)
        self.animate(dt)