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
SCORE = int(config['config']['score'])
SPEED = float(config['config']['speed'])
VOLUME = float(config['config']['volume'])
WINDOW_WIDTH = int(config['config']['width']) // SCALE * SCALE
WINDOW_HEIGHT = int(config['config']['height']) // SCALE * SCALE
BACKGROUND = config['config']['background']
COLOR = config['config']['color']

BACKGROUND = pygame.image.load(os.path.join('resources', BACKGROUND)).convert()
BACKGROUND = pygame.transform.scale(BACKGROUND, (WINDOW_WIDTH, WINDOW_HEIGHT))

## Constants ##
REFRESH_CONTROLLER = pygame.time.Clock()

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
        self.image = pygame.image.load(os.path.join('resources', f'{foodimage}food.png')).convert_alpha()
        self.position = pygame.Rect(random.randrange(SCALE, WINDOW_WIDTH - SCALE, SCALE), random.randrange(SCALE, WINDOW_HEIGHT - SCALE, SCALE), SCALE, SCALE)
        
    def draw(self, screen):
        screen.blit(self.image, self.position)

class Character(Moveble_object):
    body = [[SCALE, SCALE*2]]

    def __init__(self):
        Moveble_object.__init__(self)
        self.position = [int((WINDOW_WIDTH//SCALE//2)*SCALE - (SCALE/2)), int((WINDOW_HEIGHT//SCALE//2)*SCALE - (SCALE/2))]     # middle of the screen
        self.rect = pygame.Rect(self.position[0], self.position[1], SCALE, SCALE)

    def draw(self, screen):
        for body in self.body:
            pygame.draw.circle(screen, pygame.Color(COLOR), (body[0], body[1]), int(SCALE/2))
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

def repaint(screen, snake, food, level):
    WINDOW_WIDTH = int(config['config']['width']) // SCALE * SCALE
    WINDOW_HEIGHT = int(config['config']['height']) // SCALE * SCALE
    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(BACKGROUND, (0, 0))
    level.wall_list.draw(screen)
    food.draw(screen)
    # Collision Check
    if pygame.sprite.spritecollideany(snake, level.wall_list):
        game_over(screen)

    for blob in snake.body[1:]:
        if (snake.position[0] == blob[0] and snake.position[1] == blob[1]):
            game_over(screen)
        else:
            continue

    snake.draw(screen)

def pause():
    paused = True
    while paused:
        pygame.mixer.music.set_volume(VOLUME * 0.7)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
                    pygame.mixer.music.set_volume(VOLUME)
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

## ToDo: Make it pretty, mit ein paar buttons und bessere aufteilung
def game_over_screen(screen):
    pygame.mixer.music.set_volume(VOLUME * 0.7)
    font = pygame.font.Font(os.path.join('resources', 'fonts', 'AncientModernTales-a7Po.ttf'), SCALE * 3)
    render = font.render(f'Game Over! SCORE: {SCORE}', True, pygame.Color('black'))
    rect = render.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))   
    screen.blit(render, rect) 
    pygame.display.flip()

def game_over(screen):
    game_over_screen(screen)
    pause()

def quit():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key:
                    pygame.quit()
                    sys.exit()

def paint_hud(screen):
    font = pygame.font.Font(os.path.join('resources', 'fonts', 'AncientModernTales-a7Po.ttf'), SCALE*2)
    render = font.render(f'SCORE: {SCORE}', True, pygame.Color('black'))
    rect = render.get_rect()
    screen.blit(render, rect) 
    pygame.display.flip()


def game(screen, level):    # Game Loop
    snake = Character()
    food = Food()
    direction = Direction.RIGHT    # Initial direction
    game_running = True

    while game_running:
        direction = handle_keys(direction)    # User input determines direction
        snake.move(direction)       
        snake.get_food(food)
        repaint(screen, snake, food, level)
        paint_hud(screen)
        pygame.display.update()     # Update Display
        REFRESH_CONTROLLER.tick(FPS)
        time.sleep(SPEED)