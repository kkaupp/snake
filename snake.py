import pygame, random, time, os, sys, json
from pygame.locals import *
from enum import Enum
import argparse

__author__ = 'Kevin Kaupp, Johannes Eulitz, Tatjana Aha'
__version__ = '4.2'

## Argparse ##
parser = argparse.ArgumentParser(description='Snake Game for Python class')
parser.add_argument('-x', '--width', metavar='', type=int, help='Set specific screen width, default value: 1920', default=1000)    # Maybe use required=True
parser.add_argument('-y', '--height', metavar='', type=int, help='Set specific screen height, default value: 1080', default=1080)    # Maybe use required=True
parser.add_argument('-b', '--background', metavar='', type=str, help='Set own background image', default='desert.png')    # Maybe use required=True
args = parser.parse_args()

## General Game Settings ##
pygame.init()    # Initialize Game
pygame.display.set_caption('Snake Game for Python class')

## Music
# pygame.mixer.music.load(os.path.join('sounds', '8_Bit_Fantasy_Adventure_Music.mp3'))
# pygame.mixer.music.play(-1,0.0)
# pygame.mixer.music.set_volume(.3)

## Constants ##
REFRESH_CONTROLLER = pygame.time.Clock()
FPS = 60    # FPS
global SCORE
global SPEED
SCORE = 0
SPEED = 0.1

## Size ##
WINDOW_WIDTH = args.width
WINDOW_HEIGHT = args.height
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
BACKGROUND = pygame.image.load(os.path.join('assets', args.background)).convert()
BACKGROUND = pygame.transform.scale(BACKGROUND, (WINDOW_WIDTH, WINDOW_HEIGHT))
SCALE = 30 

## Start Positions ##
snake_position = [SCALE, SCALE*2]     # Upper left corner = [0, 0]
snake_body = [[SCALE, SCALE*2]]
food_position = [0, 0]
# food_position[0] = random.randint(10, ((WINDOW_WIDTH - SCALE) // SCALE)) * SCALE
# food_position[1] = random.randint(10, ((WINDOW_HEIGHT - SCALE) // SCALE)) * SCALE
food_position[0] = random.randrange(SCALE, WINDOW_WIDTH, SCALE)
food_position[1] = random.randrange(SCALE, WINDOW_HEIGHT, SCALE)

class Direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4
    
def handle_keys(direction):
    new_direction = direction   # Keep direction if no event
    global SPEED
    for event in [e for e in pygame.event.get() if e.type == pygame.KEYDOWN]:   # Only handle key events, ignore all other events
        # Change direction
        if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != Direction.DOWN:    # Can't go up, if down before 
            new_direction = Direction.UP 
        if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != Direction.UP: 
            new_direction = Direction.DOWN 
        if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != Direction.RIGHT: 
            new_direction = Direction.LEFT 
        if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != Direction.LEFT: 
            new_direction = Direction.RIGHT 
        # Reverse direction
        # if (event.key == pygame.K_UP and direction == Direction.DOWN):
        #     new_direction = Direction.UP
        # if (event.key == pygame.K_DOWN and direction == Direction.UP):
        #     new_direction = Direction.DOWN
        # if (event.key == pygame.K_LEFT and direction == Direction.RIGHT):
        #     new_direction = Direction.LEFT
        # if (event.key == pygame.K_RIGHT and direction == Direction.LEFT):
        #     new_direction = Direction.RIGHT
        # Slow down bro
        if (event.key == pygame.K_UP and direction == Direction.DOWN) or (event.key == pygame.K_DOWN and direction == Direction.UP) or (event.key == pygame.K_LEFT and direction == Direction.RIGHT) or (event.key == pygame.K_RIGHT and direction == Direction.LEFT): 
            while SPEED < 1:
                SPEED += 0.05
                break
        # I am SPEED.
        if (event.key == pygame.K_UP and direction == Direction.UP) or (event.key == pygame.K_DOWN and direction == Direction.DOWN) or (event.key == pygame.K_LEFT and direction == Direction.LEFT) or (event.key == pygame.K_RIGHT and direction == Direction.RIGHT):
            while SPEED > 0.051:
                SPEED -= 0.05
                break
    return new_direction

def move_snake(direction):
    if direction == Direction.UP:
        snake_position[1] -= SCALE     # SCALE pixel per block
    if direction == Direction.DOWN:
        snake_position[1] += SCALE     
    if direction == Direction.LEFT:
        snake_position[0] -= SCALE     
    if direction == Direction.RIGHT:
        snake_position[0] += SCALE
    snake_body.insert(0, list(snake_position))

def generate_new_food():
    food_position[0] = random.randrange(SCALE, WINDOW_WIDTH, SCALE)
    food_position[1] = random.randrange(SCALE, WINDOW_HEIGHT, SCALE)
          
def get_food():
    global SCORE
    if abs(snake_position[0] - food_position[0]) < SCALE/2 and abs(snake_position[1] - food_position[1]) < SCALE/2:
        SCORE += 1
        generate_new_food()
    else:
        snake_body.pop()    # enlarge snake

def repaint():
    #WINDOW.fill(pygame.Color(0, 0, 0))    # BACKGROUND color
    WINDOW.blit(BACKGROUND, (0, 0))
    for body in snake_body:
        pygame.draw.circle(WINDOW, pygame.Color(255, 255, 255), (body[0], body[1]), int(SCALE/2))
    pygame.draw.rect(WINDOW, pygame.Color(255, 0, 0), pygame.Rect(food_position[0]-int(SCALE/2), food_position[1]-int(SCALE/2), int(SCALE), int(SCALE)))

def game_over_screen():
    pygame.mixer.music.pause()
    font = pygame.font.SysFont('Arial', SCALE * 3)
    render = font.render(f'Game Over! SCORE: {SCORE}', True, pygame.Color(255, 255, 255))
    rect = render.get_rect()    # xD
    rect.midtop = (int(WINDOW_WIDTH/2), int(WINDOW_HEIGHT/2))
    WINDOW.blit(render, rect) 
    pygame.display.flip()

def game_over():
    if (snake_position[0] < 0 or snake_position[0] > WINDOW_WIDTH) or (snake_position[1] < 0 or snake_position[1] > WINDOW_HEIGHT) :
        game_over_screen()
        quit()
    else:
        pass
    for blob in snake_body[1:]:
        if (snake_position[0] == blob[0] and snake_position[1] == blob[1]):
            game_over_screen()
            pause()
        else:
            continue

def quit():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key:
                    pygame.quit()
                    sys.exit()

def pause():
    paused = True
    while paused: 
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
    # WINDOW.blit(BACKGROUND, (0, 0))
    WINDOW.fill(white)
    message_paused = 'Paused'
    message

def paint_hud():
    font = pygame.font.SysFont('Arial', SCALE*2)
    render = font.render(f'SCORE: {SCORE}', True, pygame.Color(255, 255, 255))
    rect = render.get_rect()    # xD
    WINDOW.blit(render, rect) 
    pygame.display.flip()

def game():    # Game Loop
    direction = Direction.RIGHT    # Initial direction
    game_running = True
    while game_running:
        direction = handle_keys(direction)    # User input determines direction
        move_snake(direction)       
        get_food()
        repaint()
        game_over()
        paint_hud()
        pygame.display.update()     # Update Display
        REFRESH_CONTROLLER.tick(FPS)
        time.sleep(SPEED)

if __name__ == '__main__':
    while True:
        #WINDOW.fill((0,0,0))
        #font = pygame.font.SysFont('Arial', SCALE*2)
        #font.render('Main Menu', True, pygame.Color(255, 255, 255))

        #btn_startGame = pygame.Rect(50, 100, 200, 50)
        #btn_settings = pygame.Rect(50, 200, 200, 50)
        #btn_credits = 
        #btn_exit =
        game()