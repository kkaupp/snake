import pygame, random, time, os, sys, configparser, argparse
from pygame.locals import *
from enum import Enum
## ToDo: Komentare :(
__author__ = 'Kevin Kaupp, Johannes Eulitz, Tatjana Aha'
__version__ = '4.2'

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

## Constants ##
REFRESH_CONTROLLER = pygame.time.Clock()

## Size ##
WINDOW_WIDTH = (args.width) // SCALE * SCALE
WINDOW_HEIGHT = (args.height) // SCALE * SCALE
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

BACKGROUND = pygame.image.load(os.path.join('ressources', args.background)).convert()
BACKGROUND = pygame.transform.scale(BACKGROUND, (WINDOW_WIDTH, WINDOW_HEIGHT))


class Direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4

class Moveble_object(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface((SCALE,SCALE))

class Food(Moveble_object):
    def __init__(self):
        Moveble_object.__init__(self)
        self.generate_new_food()

    def generate_new_food(self):
        foodimage = str(random.randrange(0, 3, 1))
        self.image = pygame.image.load(os.path.join('ressources', f'{foodimage}food.png')).convert_alpha()
        self.position = pygame.Rect(random.randrange(SCALE, WINDOW_WIDTH - SCALE, SCALE), random.randrange(SCALE, WINDOW_HEIGHT - SCALE, SCALE), SCALE, SCALE)
        
    def draw(self):
        WINDOW.blit(self.image, self.position)

class Character(Moveble_object):
    body = [[SCALE, SCALE*2]]

    def __init__(self):
        Moveble_object.__init__(self)
        self.position = [int((WINDOW_WIDTH//SCALE//2)*SCALE - (SCALE/2)), int((WINDOW_HEIGHT//SCALE//2)*SCALE - (SCALE/2))]     # middle of the screen
        self.rect = pygame.Rect(self.position[0], self.position[1], SCALE, SCALE)

    def draw(self):
        for body in self.body:
            pygame.draw.circle(WINDOW, pygame.Color(args.color), (body[0], body[1]), int(SCALE/2))
        self.rect = pygame.Rect(self.position[0] - SCALE/2, self.position[1] - SCALE/2, SCALE, SCALE) # /2 due to the offcenterd position

    def move(self, direction):
        if direction == Direction.UP:
            self.position[1] -= SCALE
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

def repaint(snake, food, level):
    WINDOW.blit(BACKGROUND, (0, 0))
    level.wall_list.draw(WINDOW)
    food.draw()
    # Collision Check
    if pygame.sprite.spritecollideany(snake, level.wall_list):
        game_over()

    for blob in snake.body[1:]:
        if (snake.position[0] == blob[0] and snake.position[1] == blob[1]):
            game_over()
        else:
            continue

    snake.draw()

def pause():
    paused = True
    while paused:
        pygame.mixer.music.set_volume(VOLUME * 0.7)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
                    pygame.mixer.music.set_volume(VOLUME)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

## ToDo: Make it pretty, mit ein paar buttons und bessere aufteilung
def game_over_screen():
    pygame.mixer.music.set_volume(VOLUME * 0.7)
    font = pygame.font.Font(os.path.join('ressources', 'fonts', 'AncientModernTales-a7Po.ttf'), SCALE * 3)
    render = font.render(f'Game Over! SCORE: {SCORE}', True, pygame.Color('black'))
    rect = render.get_rect()    # xD
    rect.midtop = (WINDOW_WIDTH/2-SCALE, WINDOW_HEIGHT/2-SCALE)
    WINDOW.blit(render, rect) 
    pygame.display.flip()

def game_over():
    game_over_screen()
    pause()

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
    rect = render.get_rect()
    WINDOW.blit(render, rect) 
    pygame.display.flip()

def game(level):    # Game Loop
    snake = Character()
    food = Food()
    direction = Direction.RIGHT    # Initial direction
    game_running = True
    while game_running:
        direction = handle_keys(direction)    # User input determines direction
        snake.move(direction)       
        snake.get_food(food)
        repaint(snake, food, level)
        paint_hud()
        pygame.display.update()     # Update Display
        REFRESH_CONTROLLER.tick(FPS)
        time.sleep(SPEED)