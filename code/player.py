import pygame, os
from spritesheet import Spritesheet

class Player:
    def __init__(self):
        self.player_sprites = Spritesheet("assets/Characters/trainer_POKEMONTRAINER_Red.png")
        self.image = self.player_sprites.load_image(0,0)
        self.scaled_image = pygame.transform.scale_by(self.image, 1.3)
        self.rect = self.scaled_image.get_rect()
        self.rect.center = 640,360
