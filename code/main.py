import pygame, sys
from pygame.math import Vector2 as vector
from settings import *
from player import Player
from pytmx.util_pygame import load_pygame
from sprite import Sprite

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = vector()
        self.display_surface = pygame.display.get_surface()
        self.bg = pygame.image.load('graphics/other/bg.png').convert()

    def customized_draw(self, player):
        # change the offset vector
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        # blit the surfaces
        self.display_surface.blit(self.bg, -self.offset)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):  # sorted(key=lambda): for creating overlap between sprites(player and objects)
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Western Shooter')
        self.clock = pygame.time.Clock()

        # groups
        self.all_sprites = AllSprites()
        self.obstacles = pygame.sprite.Group()

        self.setup()

    def setup(self):        # importing from tiles
        tmx_map = load_pygame('data/map.tmx')

        # tiles
        for x, y, surf in tmx_map.get_layer_by_name('Fence').tiles():
            Sprite((x * 64, y * 64), surf, [self.all_sprites, self.obstacles])

        # objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            Sprite((obj.x, obj.y), obj.image, [self.all_sprites, self.obstacles])

        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, PATHS['player'], self.obstacles)  # player itself is not in the obstacle sprites group

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            dt = self.clock.tick() / 1000

            # update groups
            self.all_sprites.update(dt)

            # draw groups
            self.display_surface.fill('black')
            self.all_sprites.customized_draw(self.player)

            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()