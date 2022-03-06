import pygame, os, sys, configparser
from pygame.locals import *
wall_list = pygame.sprite.Group()

class Wall(pygame.sprite.Sprite): 
    def __init__(self, x, y, width, height, color):
        """Args:
            x,y - coordinates
            width, height - scale of the Wall
            color - color of the wall
        """
        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
 
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

class Level():
    pass

class Level1(Level):
    pass

wall_list.add(Wall(0, 0, 20, 250, (255, 0, 0)))

