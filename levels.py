import pygame, configparser, os
from pygame.locals import *

config = configparser.ConfigParser()
config.read(os.path.join('resources', 'config.ini'))
SCALE = int(config['config']['scale']) // 2 * 2

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        """ Args:
                x, y: int                       - pixel coordinates for the postion of the wall. relative to (0, 0) -> top left corner
                width, height: int              - scale of the Wall
                color: tuple of int rgb(r,g,b)  - color of the wall
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
    textcolor = 'Black'

    def __init__(self):
        self.wall_list = pygame.sprite.Group()      # Converts list into a pygame.spritegroup

class Level1(Level):
    def __init__(self, width, height):
        """ Args:
                widht, heigt: int   - scale of the window within the walls will be build in
        """
        super().__init__()
        self.background = 'pepe.png'
        self.music = 'EEEAAAOOO.mp3'
        walls = [   [0, 0, SCALE, (height/5)*2, (255, 0, 0)],                                   # Wall top left corner -> down
                    [0, 0, (width/5)*2, SCALE, (255, 0, 0)],                                    # Wall top left corner -> right

                    [width - SCALE, 0, SCALE, (height/5)*2, (255, 255, 0)],                     # Wall top right corner -> down
                    [width - (width/5)*2, 0, (width/5)*2, SCALE, (255, 255, 0)],                # Wall top right corner -> left

                    [0, height - (height/5)*2, SCALE, (height/5)*2, (0, 255, 0)],               # Wall Bottom left corner -> up
                    [0, height - SCALE, (width/5)*2, SCALE, (0, 255, 0)],                       # Wall Bottom left corner -> right

                    [width - SCALE, height - (height/5)*2, SCALE, (height/5)*2, (0, 0, 255)],   # Wall Bottom right corner -> up
                    [width - (width/5)*2, height - SCALE, (width/5)*2, SCALE, (0, 0, 255)]      # Wall Bottom right corner -> left
                ]

        for parameter in walls:
            wall = Wall(parameter[0], parameter[1], parameter[2], parameter[3], parameter[4])
            self.wall_list.add(wall)

class Level2(Level):
    def __init__(self, width, height):
        """ Args:
                widht, heigt: int   - scale of the window within the walls will be build in
        """
        super().__init__()
        self.background = 'space1.jpg'
        self.music = 'FF14_A_Long_Fall_The_Twinning_Theme_-_Guitar_Cover.mp3'
        self.textcolor = 'White'
        walls = [   [0, 0, SCALE, (height/9)*4, (255, 0, 0)],                                   # Wall top left corner -> down
                    [0, 0, (width/9)*4, SCALE, (255, 0, 0)],                                    # Wall top left corner -> right

                    [width - SCALE, 0, SCALE, (height/9)*4, (255, 255, 0)],                     # Wall top right corner -> down
                    [width - (width/9)*4, 0, (width/9)*4, SCALE, (255, 255, 0)],                # Wall top right corner -> left

                    [0, height - (height/9)*4, SCALE, (height/9)*4, (0, 255, 0)],               # Wall Bottom left corner -> up
                    [0, height - SCALE, (width/9)*4, SCALE, (0, 255, 0)],                       # Wall Bottom left corner -> right

                    [width - SCALE, height - (height/9)*4, SCALE, (height/9)*4, (0, 0, 255)],   # Wall Bottom right corner -> up
                    [width - (width/9)*4, height - SCALE, (width/9)*4, SCALE, (0, 0, 255)]      # Wall Bottom right corner -> left
                ]

        for parameter in walls:
            wall = Wall(parameter[0], parameter[1], parameter[2], parameter[3], parameter[4])
            self.wall_list.add(wall)

class Level3(Level):
    def __init__(self, width, height):
        """ Args:
                widht, heigt: int   - scale of the window within the walls will be build in
        """
        super().__init__()
        self.background = 'space2.png'
        self.music = 'Nyan Cat.mp3'
        self.textcolor = 'White'
        walls = [   [0, 0, SCALE, (height/9)*4, (255, 0, 0)],                                   # Wall top left corner -> down
                    [0, 0, (width/9)*4, SCALE, (255, 0, 0)],                                    # Wall top left corner -> right

                    [width - SCALE, 0, SCALE, (height/9)*4, (255, 255, 0)],                     # Wall top right corner -> down
                    [width - (width/9)*4, 0, (width/9)*4, SCALE, (255, 255, 0)],                # Wall top right corner -> left

                    [0, height - (height/9)*4, SCALE, (height/9)*4, (0, 255, 0)],               # Wall Bottom left corner -> up
                    [0, height - SCALE, (width/9)*4, SCALE, (0, 255, 0)],                       # Wall Bottom left corner -> right

                    [width - SCALE, height - (height/9)*4, SCALE, (height/9)*4, (0, 0, 255)],   # Wall Bottom right corner -> up
                    [width - (width/9)*4, height - SCALE, (width/9)*4, SCALE, (0, 0, 255)],     # Wall Bottom right corner -> left

                    [(width/6), (height/9)*3, (width/6)*4, SCALE, (255, 0, 0)],                 # Wall mid-top center -> right
                    [(width/6), (height/9)*6, (width/6)*4, SCALE, (255, 0, 0)]                  # Wall mid-bottom center -> right
                ]

        for parameter in walls:
            wall = Wall(parameter[0], parameter[1], parameter[2], parameter[3], parameter[4])
            self.wall_list.add(wall)