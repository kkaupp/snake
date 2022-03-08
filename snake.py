import pygame, random, time, os, configparser, music
from pygame.locals import *
from enum import Enum
## ToDo: Komentare :(
__author__ = 'Kevin Kaupp, Johannes Eulitz, Tatjana Aha'
__version__ = '4.2'

## Read config.ini ##
config = configparser.ConfigParser()
config.read(os.path.join('config.ini'))
SCALE = int(config['config']['scale']) // 2 * 2     # To ensure that it is a multiple of 2
SCORE = int(config['config']['score'])
SPEED = float(config['config']['speed'])
COLOR = 'white'
gameover = False

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
    def __init__(self, screen_width, screen_height):
        Moveble_object.__init__(self)
        self.generate_new_food(screen_width, screen_height)

    def generate_new_food(self, screen_width, screen_height):
        foodimage = str(random.randrange(0, 7, 1))
        self.image = pygame.image.load(os.path.join('resources', f'{foodimage}food.png')).convert_alpha()
        self.rect = pygame.Rect(random.randrange(SCALE, screen_width - SCALE, SCALE), random.randrange(SCALE, screen_height - SCALE, SCALE), SCALE, SCALE)
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Character(Moveble_object):
    body = [[SCALE, SCALE*2]]

    def __init__(self, screen_width, screen_height):
        Moveble_object.__init__(self)
        self.position = [int((screen_width//SCALE//2)*SCALE - (SCALE/2)), int((screen_height//SCALE//2)*SCALE - (SCALE/2))]     # middle of the screen
        self.rect = pygame.Rect(self.position[0], self.position[1], SCALE, SCALE)

    def draw(self, screen):
        color = config['config']['color']
        for body in self.body:
            pygame.draw.circle(screen, pygame.Color(color), (body[0], body[1]), int(SCALE/2))
        self.rect = pygame.Rect(self.position[0] - SCALE/2, self.position[1] - SCALE/2, SCALE, SCALE) # /2 due to the offcenterd position

    def move(self, direction, screen_width, screen_height):
        if direction == Direction.UP:
            self.position[1] -= SCALE
        if direction == Direction.DOWN:
            self.position[1] += SCALE
        if direction == Direction.LEFT:
            self.position[0] -= SCALE
        if direction == Direction.RIGHT:
            self.position[0] += SCALE

        if self.position[0] > screen_width:
            self.position[0] = int(0 + SCALE / 2)
        
        if self.position[0] < 0:
            self.position[0] = int(screen_width - SCALE / 2)

        if self.position[1] > screen_height:
            self.position[1] = int(0 + SCALE / 2)

        if self.position[1] < 0:
            self.position[1] = int(screen_height - SCALE / 2)

        self.body.insert(0, list(self.position))

    def get_food(self, food, screen_width, screen_height):
        global SCORE
        SCORE += 1
        pygame.mixer.Sound(os.path.join("sounds" ,config['config']['eat'])).play()
        food.generate_new_food(screen_width, screen_height)

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
    config.read(os.path.join('config.ini'))
    screen_width = int(config['config']['width']) // SCALE * SCALE
    screen_height = int(config['config']['height']) // SCALE * SCALE
    backgroundimage = level.background
    background = pygame.transform.scale(pygame.image.load(os.path.join('resources', backgroundimage)).convert(), (screen_width, screen_height))

    screen.blit(background, (0, 0))
    level.wall_list.draw(screen)
    food.draw(screen)
    # Collision Check
    if pygame.sprite.spritecollideany(snake, level.wall_list):
        game_over(screen)

    if pygame.sprite.spritecollideany(food, level.wall_list):
        food.generate_new_food(screen_width, screen_height)

    foods = [food]
    if pygame.sprite.spritecollide(snake, foods, False):
        snake.get_food(food, screen_width, screen_height)
    else:
        snake.body.pop()

    for blob in snake.body[1:]:
        if (snake.position[0] == blob[0] and snake.position[1] == blob[1]):
            game_over(screen)
        else:
            continue

    snake.draw(screen)

def pause():
    config.read(os.path.join('config.ini'))
    volume = float(config['config']['volume'])

    while True:
        pygame.mixer.music.set_volume(volume * 0.5)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.set_volume(volume)
                    return
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

## ToDo: Make it pretty, mit ein paar buttons und bessere aufteilung    

def game_over(screen):
    config.read(os.path.join('config.ini'))
    screen_width = int(config['config']['width']) // SCALE * SCALE
    screen_height = int(config['config']['height']) // SCALE * SCALE
    volume = float(config['config']['volume'])
    pygame.mixer.music.set_volume(volume * 0.5)
    font = pygame.font.Font(os.path.join('resources', 'fonts', 'PublicPixel-0W6DP.ttf'), SCALE * 2)
    render = font.render(f'Game Over!', True, pygame.Color(COLOR))
    rect = render.get_rect(center=(screen_width/2, screen_height/2-80))
    screen.blit(render, rect)
    render = font.render(f'SCORE: {SCORE}', True, pygame.Color("Blue"))
    rect = render.get_rect(center=(screen_width/2, screen_height/2))
    screen.blit(render, rect)
    font = pygame.font.Font(os.path.join('resources', 'fonts', 'PublicPixel-0W6DP.ttf'), SCALE * 1)
    render = font.render(f'Press "Esc" for Main Menu', True, pygame.Color(COLOR))
    rect = render.get_rect(center=(screen_width/2, screen_height/2+70))
    screen.blit(render, rect)
    pygame.display.flip()
    pygame.mixer.Sound(os.path.join("sounds" ,config['config']['game_over'])).play()
    pause()
    global gameover
    gameover = True

def paint_hud(screen):
    font = pygame.font.Font(os.path.join('resources', 'fonts', 'PublicPixel-0W6DP.ttf'), SCALE*2)
    render = font.render(f'SCORE: {SCORE}', True, pygame.Color(COLOR))
    rect = render.get_rect()
    screen.blit(render, rect) 
    pygame.display.flip()

def game(screen, level):    # Game Loop
    global COLOR, gameover, SCORE
    SCORE = 0
    gameover = False
    COLOR = level.textcolor
    config.read(os.path.join('config.ini'))
    screen_width = int(config['config']['width']) // SCALE * SCALE
    screen_height = int(config['config']['height']) // SCALE * SCALE
    snake = Character(screen_width, screen_height)
    food = Food(screen_width, screen_height)
    direction = Direction.RIGHT    # Initial direction
    pygame.mixer.music.load(os.path.join('sounds', level.music))
    pygame.mixer.music.play(-1,0.0)
    music.fade_music(float(config['config']['volume']), "in")

    fps = int(config['config']['fps'])

    while True:
        direction = handle_keys(direction)    # User input determines direction
        snake.move(direction, screen_width, screen_height)       
        repaint(screen, snake, food, level)
        paint_hud(screen)
        pygame.display.update()     # Update Display
        REFRESH_CONTROLLER.tick(fps)
        time.sleep(SPEED)
        if gameover:
            return SCORE