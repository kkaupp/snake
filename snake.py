import pygame, random, time, os, configparser, music, sys
from pygame.locals import *
from enum import Enum
from button import Button

__author__ = 'Kevin Kaupp, Johannes Eulitz, Tatjana Aha'
__version__ = '4.2'

## Read config.ini ##
config = configparser.ConfigParser()
config.read(os.path.join('resources', 'config.ini'))
SCALE = int(config['config']['scale']) // 2 * 2     # To ensure that it is a multiple of 2
SCORE = int(config['config']['score'])
SPEED = float(config['config']['speed'])
COLOR = 'White'
RETURN_TO_MENU = False

## Constants ##
REFRESH_CONTROLLER = pygame.time.Clock()

class Direction(Enum):
    """ Enums for the direction. Defined by userinput """
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4

class Moveble_object(pygame.sprite.Sprite):
    """ Parentcalss for all  Movable objects. Movable means that the object can appear random on the screen and has no fixed position """
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface((SCALE,SCALE))

class Food(Moveble_object):
    """ Initalize the food. Child of Moveble_object() """
    def __init__(self, screen_width, screen_height):
        Moveble_object.__init__(self)
        self.generate_new_food(screen_width, screen_height)

    def generate_new_food(self, screen_width, screen_height):
        """ Generates new food with a random image at a random position

            Args:
                screen_width, screen_height: int    - dimensions of the screen
        """
        foodimage = str(random.randrange(0, 7, 1))
        self.image = pygame.image.load(os.path.join('resources', f'{foodimage}food.png')).convert_alpha()
        self.rect = pygame.Rect(random.randrange(SCALE, screen_width - SCALE, SCALE), random.randrange(SCALE, screen_height - SCALE, SCALE), SCALE, SCALE)
        
    def draw(self, screen):
        """ Draws the Food on the screen

            Args:
                screen: pygame.Display  - Screen/Window of the game
        """
        screen.blit(self.image, self.rect)

class Character(Moveble_object):
    """ Class to build a object, that can be moved by the user """
    body = []   # List of the Snakeparts

    # Circle Mode without Pictures
    # def __init__(self, screen_width, screen_height):
    #     Moveble_object.__init__(self)
    #     self.position = [int((screen_width//SCALE//2)*SCALE - (SCALE/2)), int((screen_height//SCALE//2)*SCALE - (SCALE/2))]     # middle of the screen
    #     self.rect = pygame.Rect(self.position[0], self.position[1], SCALE, SCALE)
    #     self.body = [[SCALE, SCALE*2]]

    # def draw(self, screen):
    #     self.rect = pygame.Rect(self.position[0] - SCALE/2, self.position[1] - SCALE/2, SCALE, SCALE) # /2 due to the offcenterd position
    #     for body in self.body:
    #         pygame.draw.circle(screen, pygame.Color(COLOR), (body[0], body[1]), int(SCALE/2))
    
    def __init__(self, screen_width, screen_height):
        Moveble_object.__init__(self)
        self.position = [int((screen_width//SCALE//2)*SCALE), int((screen_height//SCALE//2)*SCALE)]     # middle of the screen
        self.rect = pygame.Rect(self.position[0], self.position[1], SCALE, SCALE)
        self.body = [[SCALE, SCALE*2]]

    def draw(self, screen):
        """ Draws the Snake on the Screen

            Args:
                screen: pygame.Display  - Screen/Window of the game
        """
        body_img = pygame.image.load(os.path.join('resources', 'rainbow.png')).convert_alpha()
        body_corner_img = pygame.image.load(os.path.join('resources', 'rainbow_corner.png')).convert_alpha()


        for part in range(0, len(self.body), 1):            # Iterate through all bodyparts
            if part == 0:       # First part is always the Head
                self.image = pygame.image.load(os.path.join('resources', 'cat.png')).convert_alpha()
            else:
                if len(self.body) - part > 1: #len(self.body) > 2: # More than 2 Parts left
                    # Decide wich image of the body needs to be printed and in witch angle
                    if self.body[part-1][0] == self.body[part][0] and self.body[part-1][1] < self.body[part][1]:# and self.body[part][0] == self.body[part+1][0] and self.body[part][0] > self.body[part+1][0]:    # Vertical up
                        self.image = pygame.transform.rotate(body_img, 90)
                    if self.body[part-1][0] == self.body[part][0] and self.body[part-1][1] > self.body[part][1]:# and self.body[part][0] == self.body[part+1][0] and self.body[part][0] < self.body[part+1][0]:    # Vertical down
                        self.image = pygame.transform.rotate(body_img, -90)
                    if self.body[part-1][0] > self.body[part][0] and self.body[part-1][1] == self.body[part][1]:# and self.body[part][0] < self.body[part+1][0] and self.body[part][0] == self.body[part+1][0]:    # to right (x_bodybefore > x_body, y_bodybefore = y_body)
                        self.image = pygame.transform.rotate(body_img, 180)
                    if self.body[part-1][0] < self.body[part][0] and self.body[part-1][1] == self.body[part][1]:# and self.body[part][0] > self.body[part+1][0] and self.body[part][0] == self.body[part+1][0]:    # to left (x_bodybefore < x_body, y_bodybefore = y_body)
                        self.image = body_img
                    # ToDO: Cornerparts facing into the right direction 
                    if self.body[part-1][0] > self.body[part][0] and self.body[part-1][1] == self.body[part][1] and self.body[part][0] == self.body[part+1][0] and self.body[part][0] > self.body[part+1][0]:
                        self.image = pygame.transform.rotate(body_corner_img, 0)
                #   if self.body[part-1][0] == self.body[part][0] and self.body[part-1][1] < self.body[part][1]:
                #       self.image = pygame.transform.rotate(body_corner_img, 90)
                #   if self.body[part-1][0] > self.body[part][0] and self.body[part-1][1] == self.body[part][1]:
                #       self.image = pygame.transform.rotate(body_corner_img, 180)
                #   if self.body[part-1][0] < self.body[part][0] and self.body[part-1][1] == self.body[part][1]:
                #       self.image = pygame.transform.rotate(body_corner_img, -90)
                else:   # End of the snake will be allways a body_img
                    if self.body[part-1][0] == self.body[part][0] and self.body[part-1][1] < self.body[part][1]:    # Vertical up
                        self.image = pygame.transform.rotate(body_img, 90)
                    if self.body[part-1][0] == self.body[part][0] and self.body[part-1][1] > self.body[part][1]:    # Vertical down
                        self.image = pygame.transform.rotate(body_img, -90)
                    if self.body[part-1][0] > self.body[part][0] and self.body[part-1][1] == self.body[part][1]:    # to right (x_bodybefore > x_body, y_bodybefore = y_body)
                        self.image = pygame.transform.rotate(body_img, 180)
                    if self.body[part-1][0] < self.body[part][0] and self.body[part-1][1] == self.body[part][1]:    # to left (x_bodybefore < x_body, y_bodybefore = y_body)
                        self.image = body_img
               

            self.rect = pygame.Rect(self.body[part][0], self.body[part][1], SCALE, SCALE)
            screen.blit(self.image, self.rect)
        self.rect = pygame.Rect(self.position[0], self.position[1], SCALE, SCALE)

    def move(self, direction, screen_width, screen_height):
        """ Changes the Position of each Snakepart relative to the moving direction
        
            Args:
                direction: enum                     - direction inwich the snake is moving
                screen_width, screen_height: int    - dimensions of the screen
        """
        # Change Position
        if direction == Direction.UP:
            self.position[1] -= SCALE
        if direction == Direction.DOWN:
            self.position[1] += SCALE
        if direction == Direction.LEFT:
            self.position[0] -= SCALE
        if direction == Direction.RIGHT:
            self.position[0] += SCALE

        # Come back on the other side of the screen if you leave it to the other
        # The Commented Code is for the circle mode
        if self.position[0] > screen_width - SCALE:
            #self.position[0] = SCALE
            self.position[0] = 0
        if self.position[0] < 0:
            self.position[0] = screen_width - SCALE
            #self.position[0] = int(screen_width - SCALE)
        if self.position[1] > screen_height - SCALE:
            #self.position[1] = int(0 + SCALE)
            self.position[1] = 0
        if self.position[1] < 0:
            self.position[1] = screen_height - SCALE
            #self.position[1] = int(screen_height - SCALE)

        # Circle Mode without Pictures. Just comment the block of 4 if clausels above
        # if self.position[0] > screen_width:
        #     self.position[0] = int(0 + SCALE / 2)
        
        # if self.position[0] < 0:
        #     self.position[0] = int(screen_width - SCALE / 2)

        # if self.position[1] > screen_height:
        #     self.position[1] = int(0 + SCALE / 2)

        # if self.position[1] < 0:
        #     self.position[1] = int(screen_height - SCALE / 2)

        self.body.insert(0, list(self.position))

    def get_food(self, food, screen_width, screen_height):
        """ increments the score by 1 and triggers the generation of a new food

            Args:
                food: Food                          - eatable object
                screen_width, screen_height: int    - dimensions of the screen
        """
        global SCORE
        SCORE += 1
        pygame.mixer.Sound(os.path.join("sounds" ,config['config']['eat'])).play()
        food.generate_new_food(screen_width, screen_height)

def handle_keys(screen, direction):
    """ Handles userinput (w, a, s, d, ↑ ,↓ , →, ←) and setes moving direction

        Args:
            screen: pygame.Display  - Screen/Window of the game
            direction: enum         - direction inwich the snake is moving
    """
    new_direction = direction   # Keep direction if no event
    global SPEED
    for event in [e for e in pygame.event.get() if e.type == pygame.KEYDOWN]:   # Only handle key events, ignore all other events
        # Pause
        if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
            pause_screen(screen)
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
            if SPEED < 1:
                SPEED += 0.05
        # I am SPEED.
        if ((event.key == pygame.K_UP or event.key == pygame.K_w) and direction == Direction.UP) or ((event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction == Direction.DOWN) or ((event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction == Direction.LEFT) or ((event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction == Direction.RIGHT):
            if SPEED > 0.051:
                SPEED -= 0.05
    return new_direction

def repaint(screen, snake, food, level):
    """ Paints the screen the momentary game situation

        Args:
            screen: pygame.Display              - Screen/Window of the game
            snake: Character                    - the char object we play with
            food: Food                          - the food object
            level: Level/Level1/Level2/Level3   - level we play in
    """
    config.read(os.path.join('resources', 'config.ini'))
    screen_width = int(config['config']['width']) // SCALE * SCALE
    screen_height = int(config['config']['height']) // SCALE * SCALE
    backgroundimage = level.background
    background = pygame.transform.scale(pygame.image.load(os.path.join('resources', backgroundimage)).convert(), (screen_width, screen_height))

    screen.blit(background, (0, 0))
    level.wall_list.draw(screen)
    food.draw(screen)
    snake.draw(screen)

def pause_screen(screen):
    """ Displays the pause screen Loop with buttons
    
        Args:
            screen: pygame.Display  - Screen/Window of the game
    """
    config.read(os.path.join('resources', 'config.ini'))
    screen_width = int(config['config']['width']) // SCALE * SCALE
    screen_height = int(config['config']['height']) // SCALE * SCALE
    font = pygame.font.Font(os.path.join('resources', 'fonts', 'PublicPixel-0W6DP.ttf'), SCALE * 2)
    render = font.render(f'Pause', True, pygame.Color(COLOR))
    rect = render.get_rect(center=(screen_width/2, screen_height/2 - 30))
    btn_pause_screen_back = Button(image=None, pos=(screen_width/6, screen_height/1.2), text_input="MENU", font=font, base_color=COLOR, hovering_color="Green") 
    pygame.mixer.music.set_volume(float(config['config']['volume']) * 0.5)
    screen.blit(render, rect)

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for button in [btn_pause_screen_back]:
            button.changeColor(mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_pause_screen_back.checkForInput(mouse_pos):
                    global RETURN_TO_MENU
                    RETURN_TO_MENU = True
                    return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.set_volume(float(config['config']['volume']))
                    return

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def lose_logic(snake, level):
    """ contains the lose logic of our game (colide with a wall or one of your bodyparts
    
        Args:
            snake: Character    - the char object we play with
            food: Food          - the food object

    """
    # Collision Check
    if pygame.sprite.spritecollideany(snake, level.wall_list):
        return True

    for blob in snake.body[1:]:
        if (snake.position[0] == blob[0] and snake.position[1] == blob[1]):
            return True
        else:
            continue

def game_over(screen):
    """ Displays the game over screen Loop with buttons
    
        Args:
            screen: pygame.Display  - Screen/Window of the game
    """
    config.read(os.path.join('resources', 'config.ini'))
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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    return

def paint_hud(screen):
    """ Paints the hud with the score onto the screen

        Args:
            screen: pygame.Display  - Screen/Window of the game
    """
    font = pygame.font.Font(os.path.join('resources', 'fonts', 'PublicPixel-0W6DP.ttf'), SCALE*2)
    render = font.render(f'SCORE: {SCORE}', True, pygame.Color(COLOR))
    rect = render.get_rect()
    screen.blit(render, rect) 
    pygame.display.flip()

def game(screen, level):    # Game Loop
    """ The Main gameloop. Handles Userinput, checks gamelogic, paints the screen
        Args:
            screen: pygame.Display              - Screen/Window of the game
            level: Level/Level1/Level2/Level3   - level we play in
    """
    global COLOR, SCORE, RETURN_TO_MENU
    RETURN_TO_MENU = False
    SCORE = 0
    COLOR = level.textcolor
    config.read(os.path.join('resources', 'config.ini'))
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
        direction = handle_keys(screen, direction)    # User input determines direction
        snake.move(direction, screen_width, screen_height)  

        # Generate new food when the food spawned within a wall
        if pygame.sprite.spritecollideany(food, level.wall_list):
            food.generate_new_food(screen_width, screen_height)

        # Check if the snake colides with a food and ate it
        foods = [food]
        if pygame.sprite.spritecollide(snake, foods, False):
            snake.get_food(food, screen_width, screen_height)
        else:
            snake.body.pop()

        repaint(screen, snake, food, level)
        paint_hud(screen)
        pygame.display.update()     # Update Display      
        REFRESH_CONTROLLER.tick(fps)
        time.sleep(SPEED)           # Used to display the speed of the game

        if lose_logic(snake, level) or RETURN_TO_MENU:
            game_over(screen)
            return SCORE