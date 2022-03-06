import pygame, os, configparser, argparse


## Read config.ini ##
config = configparser.ConfigParser()
config.read(os.path.join('config.ini'))
SCALE = int(config['config']['scale']) // 2 * 2     # To ensure that it is a multiple of 2
FPS = int(config['config']['fps'])
global SCORE
global SPEED
SCORE = int(config['config']['score'])
SPEED = float(config['config']['speed'])
VOLUME = float(config['config']['volume'])
WINDOW_WIDTH = int(config['config']['width']) // SCALE * SCALE
WINDOW_HEIGHT = int(config['config']['height']) // SCALE * SCALE

##ToDo: Save changed prefferences in config file (also from settings)

## Argparse ##
parser = argparse.ArgumentParser(description='Snake Game for Python class')
parser.add_argument('-x', '--width', metavar='', type=int, help='Set specific screen width, default value: ' + str(WINDOW_WIDTH), default=WINDOW_WIDTH)    # Maybe use required=True
parser.add_argument('-y', '--height', metavar='', type=int, help='Set specific screen height, default value: ' + str(WINDOW_HEIGHT), default=WINDOW_HEIGHT)    # Maybe use required=True
parser.add_argument('-b', '--background', metavar='', type=str, help='Set own background image', default='desert.jpg')    # Maybe use required=True
parser.add_argument('-m', '--music', metavar='', type=str, help='Set own music', default='Tequila.mp3')    # Maybe use required=True
parser.add_argument('-c', '--color', metavar='', type=str, help='Set snake color, supports basic colors', default='white')    # Maybe use required=True
args = parser.parse_args()

## General Game Settings ##
pygame.init()    # Initialize Game
pygame.display.set_caption('Snake Game for Python class')

## Music
pygame.mixer.music.load(os.path.join('sounds', args.music))
pygame.mixer.music.play(-1,0.0)
pygame.mixer.music.set_volume(VOLUME)

## Size ##
WINDOW_WIDTH = (args.width) // SCALE * SCALE
WINDOW_HEIGHT = (args.height) // SCALE * SCALE
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

import snake, levels

class Mainmenu():
    pass
   
if __name__ == '__main__':
    run = True
    while run:
        snake.game(WINDOW, levels.Level1())