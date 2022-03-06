from msilib.schema import Class
from turtle import position
from numpy import delete
import pygame, random, time, os, sys, configparser, levels
from pygame.locals import *
from enum import Enum
import argparse

__author__ = 'Kevin Kaupp, Johannes Eulitz, Tatjana Aha'
__version__ = '4.2'

## Argparse ##
parser = argparse.ArgumentParser(description='Snake Game for Python class')
parser.add_argument('-x', '--width', metavar='', type=int, help='Set specific screen width, default value: 1920', default=1260)    # Maybe use required=True
parser.add_argument('-y', '--height', metavar='', type=int, help='Set specific screen height, default value: 1080', default=720)    # Maybe use required=True
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
pygame.mixer.music.set_volume(0.03)


## Constants ##
REFRESH_CONTROLLER = pygame.time.Clock()
FPS = 60    # FPS
global SCORE
global SPEED
SCORE = 0
SPEED = 0.1
SCALE = 30 
## Size ##
WINDOW_WIDTH = (args.width) // SCALE * SCALE
WINDOW_HEIGHT = (args.height) // SCALE * SCALE
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

BACKGROUND = pygame.image.load(os.path.join('ressources', args.background)).convert()
BACKGROUND = pygame.transform.scale(BACKGROUND, (WINDOW_WIDTH, WINDOW_HEIGHT))

## Start Positions ##
current_level = levels.Level1()

class Direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4

class Moveble_object(pygame.sprite.Sprite):
    position = [0,0]

    def __init__(self):
        self.position = [int((WINDOW_WIDTH//SCALE//2)*SCALE - (SCALE/2)), int((WINDOW_HEIGHT//SCALE//2)*SCALE - (SCALE/2))]     # in der Mitte

class Food(Moveble_object):
    def __init__(self):
        self.generate_new_food()

    def generate_new_food(self):
        self.position = [random.randrange(SCALE, WINDOW_WIDTH - SCALE, SCALE), random.randrange(SCALE, WINDOW_HEIGHT - SCALE, SCALE)]

class Character(Moveble_object):
    body = [[SCALE, SCALE*2]]

    def move(self, direction):
        if direction == Direction.UP:
            self.position[1] -= SCALE     # SCALE pixel per block
        if direction == Direction.DOWN:
            self.position[1] += SCALE     
        if direction == Direction.LEFT:
            self.position[0] -= SCALE     
        if direction == Direction.RIGHT:
            self.position[0] += SCALE

        if self.position[0] > WINDOW_WIDTH:
            self.position[0] = int(0 + SCALE / 2)
        
        if self.position[0] < 0:
            self.position[0] = int(WINDOW_WIDTH - SCALE / 2)

        if self.position[1] > WINDOW_HEIGHT:
            self.position[1] = int(0 + SCALE / 2)

        if self.position[1] < 0:
            self.position[1] = int(WINDOW_HEIGHT - SCALE / 2)

        self.body.insert(0, list(self.position))

    def get_food(self, food):
        global SCORE
        if self.position[0] - SCALE/2 == food.position[0] and self.position[1] - SCALE/2 == food.position[1]:
            SCORE += 1
            food.generate_new_food()
        else:
            self.body.pop()    # enlarge snake

def handle_keys(direction):
    new_direction = direction   # Keep direction if no event
    global SPEED
    for event in [e for e in pygame.event.get() if e.type == pygame.KEYDOWN]:   # Only handle key events, ignore all other events
        # Pause
        if event.key == pygame.K_SPACE:
            pause()
        # Change direction
        if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != Direction.DOWN:    # Can't go up, if down before 
            new_direction = Direction.UP 
        if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != Direction.UP: 
            new_direction = Direction.DOWN 
        if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != Direction.RIGHT: 
            new_direction = Direction.LEFT 
        if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != Direction.LEFT: 
            new_direction = Direction.RIGHT 

        # Slow down bro
        if ((event.key == pygame.K_UP or event.key == pygame.K_w) and direction == Direction.DOWN) or ((event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction == Direction.UP) or ((event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction == Direction.RIGHT) or ((event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction == Direction.LEFT): 
            while SPEED < 1:
                SPEED += 0.05
                break
        # I am SPEED.
        if ((event.key == pygame.K_UP or event.key == pygame.K_w) and direction == Direction.UP) or ((event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction == Direction.DOWN) or ((event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction == Direction.LEFT) or ((event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction == Direction.RIGHT):
            while SPEED > 0.051:
                SPEED -= 0.05
                break
    return new_direction

def repaint(snake, food):
    #WINDOW.fill(pygame.Color(0, 0, 0))    # BACKGROUND color
    WINDOW.blit(BACKGROUND, (0, 0))
    current_level.wall_list.draw(WINDOW)
    print("snake:", snake.position[0], snake.position[1])
    for body in snake.body:
        pygame.draw.circle(WINDOW, pygame.Color(args.color), (body[0], body[1]), int(SCALE/2))
    pygame.draw.rect(WINDOW, pygame.Color(255, 0, 0), pygame.Rect(food.position[0], food.position[1], int(SCALE), int(SCALE)))

def pause():
    paused = True
    while paused:
        pygame.mixer.music.set_volume(0.2)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
                    pygame.mixer.music.set_volume(1)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        # WINDOW.fill(pygame.Color('black'))
        pygame.display.update()

def game_over_screen():
    pygame.mixer.music.pause()
    font = pygame.font.SysFont('Arial', SCALE * 3)
    render = font.render(f'Game Over! SCORE: {SCORE}', True, pygame.Color('black'))
    rect = render.get_rect()    # xD
    rect.midtop = (WINDOW_WIDTH/2-SCALE, WINDOW_HEIGHT/2-SCALE)
    WINDOW.blit(render, rect) 
    pygame.display.flip()

def game_over(snake):
    #collision = pygame.sprite.spritecollide(snake, current_level.wall_list, False)
    pass

def quit():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key:
                    pygame.quit()
                    sys.exit()

def paint_hud():
    font = pygame.font.Font(os.path.join('ressources', 'fonts', 'AncientModernTales-a7Po.ttf'), SCALE*2)
    render = font.render(f'SCORE: {SCORE}', True, pygame.Color('black'))
    rect = render.get_rect()    # xD
    WINDOW.blit(render, rect) 
    pygame.display.flip()

def game():    # Game Loop
    snake = Character()
    food = Food()
    direction = Direction.RIGHT    # Initial direction
    game_running = True
    while game_running:
        direction = handle_keys(direction)    # User input determines direction
        snake.move(direction)       
        snake.get_food(food)
        repaint(snake, food)
        game_over(snake)
        paint_hud()
        pygame.display.update()     # Update Display
        REFRESH_CONTROLLER.tick(FPS)
        time.sleep(SPEED)