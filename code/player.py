import pygame, sys
from pygame.math import Vector2 as vector
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, path, collision_sprites, create_bullet):
        super().__init__(pos, groups, path, collision_sprites)

        self.create_bullet = create_bullet
        self.bullet_shot = False

    def get_status(self):
        # idle
        if self.direction.x == 0 and self.direction.y == 0:
            self.status = self.status.split('_')[0] + '_idle'  # fuck python again 6:40  111  => this one could cause "_idle" to get added multiple time in front of the self.status.. so in the next loop we are splitting it to get us a list and choose the first item of the list

        #attacking
        if self.attacking == True:
            self.status = self.status.split('_')[0] + '_attack' # //

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
                self.bullet_shot = False

                match self.status.split('_')[0]:
                    case 'left': self.bullet_direction = vector(-1, 0)
                    case 'right': self.bullet_direction = vector(1, 0)
                    case 'up': self.bullet_direction = vector(0, -1)
                    case 'down': self.bullet_direction = vector(0, 1)

    def animate(self, dt):  # very fucking confusing mind wobbles, just pay enough attentions to variables
        current_animation = self.animations[self.status]

        self.frame_index += 7 * dt

        if int(self.frame_index) == 2 and self.attacking and not self.bullet_shot:
            bullet_start_pos = self.rect.center + self.bullet_direction * 80
            self.create_bullet(bullet_start_pos, self.bullet_direction)  # this one is addresed multiple times throgh variables and it is a function from main.py that we are passing parameters on
            self.bullet_shot = True
            self.shoot_sound.play()

        if self.frame_index >= len(current_animation): # fucked my mind before I realized about self.attacking: it will check how many animation one status have and if the frames of attack finishes, it will set back self.attacking to false and player will able to move again
            self.frame_index = 0
            if self.attacking:
                self.attacking = False

        self.image = current_animation[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)

    def check_death(self):
        if self.health <= 0:
            pygame.quit()
            sys.exit()

    def update(self, dt):
        self.input()
        self.get_status()
        self.move(dt)
        self.animate(dt)
        self.blink()

        self.vulnerability_timer()
        self.check_death()