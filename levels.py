import pygame, configparser
from pygame.locals import *

config = configparser.ConfigParser()
config.read('config.ini')
SCALE = int(config['config']['scale']) // 2 * 2

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
    background = 'desert.jpg'
    music = 'Tequila.mp3'

    def __init__(self):
        self.wall_list = pygame.sprite.Group()

class Level1(Level):
    def __init__(self, width, height):
        super().__init__()
        walls = [   [0, 0, SCALE, (height/5)*2, (255, 0, 0)], # Wall top left corner -> down
                    [0, 0, (width/5)*2, SCALE, (255, 0, 0)], # Wall top left corner -> right

                    [width - SCALE, 0, SCALE, (height/5)*2, (255, 255, 0)], # Wall top right corner -> down
                    [width - (width/5)*2, 0, (width/5)*2, SCALE, (255, 255, 0)], # Wall top right corner -> left

                    [0, height - (height/5)*2, SCALE, (height/5)*2, (0, 255, 0)], # Wall Bottom left corner -> up
                    [0, height - SCALE, (width/5)*2, SCALE, (0, 255, 0)], # Wall Bottom left corner -> right

                    [width - SCALE, height - (height/5)*2, SCALE, (height/5)*2, (0, 0, 255)], # Wall Bottom right corner -> up
                    [width - (width/5)*2, height - SCALE, (width/5)*2, SCALE, (0, 0, 255)] # Wall Bottom right corner -> left
                ]

        for parameter in walls:
            wall = Wall(parameter[0], parameter[1], parameter[2], parameter[3], parameter[4])
            self.wall_list.add(wall)
