import pygame, configparser
from pygame.locals import *

config = configparser.ConfigParser()
config.read('config.ini')
SCALE = int(config['config']['scale'])

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

class Level(object):
    wall_list = None

    def __init__(self):
        self.wall_list = pygame.sprite.Group()

class Level1(Level):
    def __init__(self):
        super().__init__()
        walls = [   [0, 0, SCALE, SCALE * 7, (255, 0, 0)], # Wall top left corner, down
                    [0, 0, SCALE * 7, SCALE, (255, 0, 0)] # Wall top left corner, right
                ]

        for parameter in walls:
            wall = Wall(parameter[0], parameter[1], parameter[2], parameter[3], parameter[4])
            self.wall_list.add(wall)
