import pygame
import random
import time
import os
from enum import Enum


## General Game Settings ##
pygame.init()    # Initialize Game
pygame.display.set_caption('snoled')
refresh_controller = pygame.time.Clock()
fps = 60    # FPS
global score
global speed
score = 0
speed = 0.1

## Size ##
window_width = 1280
window_height = 720
window = pygame.display.set_mode((window_width, window_height))
scale = 30 

## Start Positions ##
snake_position = [scale, scale*2]     # Upper left corner = [0, 0]
snake_body = [[scale, scale*2]]
food_position = [0, 0]
# food_position[0] = random.randint(10, ((window_width - scale) // scale)) * scale
# food_position[1] = random.randint(10, ((window_height - scale) // scale)) * scale
food_position[0] = random.randrange(scale, window_width, scale)
food_position[1] = random.randrange(scale, window_height, scale)

class Direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4
    
def handle_keys(direction):
    new_direction = direction   # Keep direction if no event
    global speed
    for event in [e for e in pygame.event.get() if e.type == pygame.KEYDOWN]:   # Only handle key events, ignore all other events
        # Change direction
        if event.key == pygame.K_UP and direction != Direction.DOWN:    # Can't go up, if down before 
            new_direction = Direction.UP 
        if event.key == pygame.K_DOWN and direction != Direction.UP: 
            new_direction = Direction.DOWN 
        if event.key == pygame.K_LEFT and direction != Direction.RIGHT: 
            new_direction = Direction.LEFT 
        if event.key == pygame.K_RIGHT and direction != Direction.LEFT: 
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
            while speed < 1:
                speed += 0.05
                break
        # I am speed.
        if (event.key == pygame.K_UP and direction == Direction.UP) or (event.key == pygame.K_DOWN and direction == Direction.DOWN) or (event.key == pygame.K_LEFT and direction == Direction.LEFT) or (event.key == pygame.K_RIGHT and direction == Direction.RIGHT):
            while speed > 0.051:
                speed -= 0.05
                break
    return new_direction

def move_snake(direction):
    if direction == Direction.UP:
        snake_position[1] -= scale     # scale pixel per block
    if direction == Direction.DOWN:
        snake_position[1] += scale     
    if direction == Direction.LEFT:
        snake_position[0] -= scale     
    if direction == Direction.RIGHT:
        snake_position[0] += scale
    snake_body.insert(0, list(snake_position))

def generate_new_food():
    food_position[0] = random.randrange(scale, window_width, scale)
    food_position[1] = random.randrange(scale, window_height, scale)
          
def get_food():
    global score
    if abs(snake_position[0] - food_position[0]) < scale/2 and abs(snake_position[1] - food_position[1]) < scale/2:
        score += 1
        generate_new_food()
    else:
        snake_body.pop()    # enlarge snake

def repaint():
    window.fill(pygame.Color(0, 0, 0))    # Background color
    for body in snake_body:
        pygame.draw.circle(window, pygame.Color(255, 255, 255), (body[0], body[1]), int(scale/2))
    pygame.draw.rect(window, pygame.Color(255, 0, 0), pygame.Rect(food_position[0]-int(scale/2), food_position[1]-int(scale/2), int(scale), int(scale)))

def game_over_message():
    font = pygame.font.SysFont('Arial', scale * 3)
    render = font.render(f'Score: {score}', True, pygame.Color(255, 255, 255))
    rect = render.get_rect()    # xD
    rect.midtop = (int(window_width/2), int(window_height/2))
    window.blit(render, rect) 
    pygame.display.flip()

def game_over():
    if (snake_position[0] < 0 or snake_position[0] > window_width) or (snake_position[1] < 0 or snake_position[1] > window_height):
        game_over_message()
        pause()
    else:
        pass
    for blob in snake_body[1:]:
        if snake_position[0] == blob[0] and snake_position[1] == blob[1]:
            game_over_message()
            pause()
        else:
            continue

def pause():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.quit()
                    if os.path.exists('snake.py'):
                        try:
                            print('exists')
                        except: 
                            print('doesnt exist')
                if event.key:
                    pygame.quit()
        # pygame.display.update()

def paint_hud():
    font = pygame.font.SysFont('Arial', scale*2)
    render = font.render(f'Score: {score}', True, pygame.Color(255, 255, 255))
    rect = render.get_rect()    # xD
    window.blit(render, rect) 
    pygame.display.flip()

def game_loop():    # Game Loop
    direction = Direction.RIGHT    # Initial direction
    while True:
        direction = handle_keys(direction)    # User input determines direction
        move_snake(direction)       
        get_food()
        repaint()
        game_over()
        paint_hud()
        pygame.display.update()     # Update Display
        refresh_controller.tick(fps)
        time.sleep(speed)

if __name__ == '__main__':
    game_loop()