import pygame, os, configparser, argparse

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

##ToDo: Save changed prefferences in config file (also from settings)

## Argparse ##
parser = argparse.ArgumentParser(description='Snake Game for Python class')
parser.add_argument('-x', '--width', metavar='', type=int, help='Set specific screen width, default value: ' + str(WINDOW_WIDTH), default=WINDOW_WIDTH)        # uses default of config
parser.add_argument('-y', '--height', metavar='', type=int, help='Set specific screen height, default value: ' + str(WINDOW_HEIGHT), default=WINDOW_HEIGHT)    # uses default of config
parser.add_argument('-b', '--background', metavar='', type=str, help='Set own background image', default='desert.jpg')    
parser.add_argument('-m', '--music', metavar='', type=str, help='Set own music', default='Tequila.mp3')   
parser.add_argument('-c', '--color', metavar='', type=str, help='Set snake color, supports basic colors', default='white')    
args = parser.parse_args()

## General Game Settings ##
pygame.init()    # Initialize Game

## Music ##
pygame.mixer.music.load(os.path.join('sounds', args.music))
pygame.mixer.music.play(-1,0.0)
pygame.mixer.music.set_volume(VOLUME)

## Size ##
WINDOW_WIDTH = (args.width) // SCALE * SCALE      # overrides config setting with argparse
WINDOW_HEIGHT = (args.height) // SCALE * SCALE    # overrides config setting with argparse
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

import snake, levels
from button import Button

def font(size):
    return pygame.font.Font(os.path.join('resources', 'fonts', 'AncientModernTales-a7Po.ttf'), SCALE * size)

def play():
    while True:
        WINDOW_WIDTH = int(config['config']['width']) // SCALE * SCALE
        WINDOW_HEIGHT = int(config['config']['height']) // SCALE * SCALE
        WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        pygame.display.set_caption('Snake')
        snake.game(WINDOW, levels.Level1())

        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        PLAY_BACK = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2), text_input="BACK", font=font(2), base_color="Black", hovering_color="Green")
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()
    
def resolution_update(width, height):
    with open('config.ini', 'w') as configfile:
        config.set('config', 'width', f'{width}')
        config.set('config', 'height', f'{height}')
        config.write(configfile)

def resolution():
    while True:
        WINDOW_WIDTH = int(config['config']['width']) // SCALE * SCALE
        WINDOW_HEIGHT = int(config['config']['height']) // SCALE * SCALE
        WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        pygame.display.set_caption('Resolution')
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        WINDOW.fill("black")
        RESOLUTION_TEXT = font(3).render("Resolution", True, "White")
        RESOLUTION_RECT = RESOLUTION_TEXT.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/6))
        WINDOW.blit(RESOLUTION_TEXT, RESOLUTION_RECT)

        RESOLUTION_ULTRAHD = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/3), text_input="3840x2160", font=font(2), base_color="White", hovering_color="Green")
        RESOLUTION_ULTRAHD.changeColor(OPTIONS_MOUSE_POS)
        RESOLUTION_ULTRAHD.update(WINDOW)

        RESOLUTION_WQHD = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2.2), text_input="2560x1440", font=font(2), base_color="White", hovering_color="Green")
        RESOLUTION_WQHD.changeColor(OPTIONS_MOUSE_POS)
        RESOLUTION_WQHD.update(WINDOW)
        
        RESOLUTION_FULLHD = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.7), text_input="1920x1080", font=font(2), base_color="White", hovering_color="Green")
        RESOLUTION_FULLHD.changeColor(OPTIONS_MOUSE_POS)
        RESOLUTION_FULLHD.update(WINDOW)
        
        RESOLUTION_HD = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.4), text_input="1280x720", font=font(2), base_color="White", hovering_color="Green")
        RESOLUTION_HD.changeColor(OPTIONS_MOUSE_POS)
        RESOLUTION_HD.update(WINDOW)

        RESOLUTION_SD = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.2), text_input="720x576", font=font(2), base_color="White", hovering_color="Green")
        RESOLUTION_SD.changeColor(OPTIONS_MOUSE_POS)
        RESOLUTION_SD.update(WINDOW)

        RESOLUTION_BACK = Button(image=None, pos=(WINDOW_WIDTH/6, WINDOW_HEIGHT/1.2), text_input="BACK", font=font(2), base_color="White", hovering_color="Green")
        RESOLUTION_BACK.changeColor(OPTIONS_MOUSE_POS)
        RESOLUTION_BACK.update(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RESOLUTION_ULTRAHD.checkForInput(OPTIONS_MOUSE_POS):
                    width, height = 3840, 2160
                    resolution_update(width, height)
                if RESOLUTION_WQHD.checkForInput(OPTIONS_MOUSE_POS):
                    width, height = 2560, 1440
                    resolution_update(width, height)
                if RESOLUTION_FULLHD.checkForInput(OPTIONS_MOUSE_POS):
                    width, height = 1920, 1080
                    resolution_update(width, height)
                if RESOLUTION_HD.checkForInput(OPTIONS_MOUSE_POS):
                    width, height = 1280, 720
                    resolution_update(width, height)
                if RESOLUTION_SD.checkForInput(OPTIONS_MOUSE_POS):
                    width, height = 720, 576
                    resolution_update(width, height)
                if RESOLUTION_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    options()

        pygame.display.update()

def options():
    while True:
        WINDOW_WIDTH = int(config['config']['width']) // SCALE * SCALE
        WINDOW_HEIGHT = int(config['config']['height']) // SCALE * SCALE
        WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        pygame.display.set_caption('Options')
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        WINDOW.fill("black")
        OPTIONS_TEXT = font(3).render("Options", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/6))
        WINDOW.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_VOLUME = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/3), text_input="Volume", font=font(2), base_color="White", hovering_color="White")
        OPTIONS_VOLUME.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_VOLUME.update(WINDOW)

        OPTIONS_VOLUME_DOWN = Button(image=None, pos=(WINDOW_WIDTH/2 - SCALE*4, WINDOW_HEIGHT/3), text_input="-", font=font(2), base_color="White", hovering_color="Green")
        OPTIONS_VOLUME_DOWN.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_VOLUME_DOWN.update(WINDOW)

        OPTIONS_VOLUME_UP = Button(image=None, pos=(WINDOW_WIDTH/2 + SCALE*4, WINDOW_HEIGHT/3), text_input="+", font=font(2), base_color="White", hovering_color="Green")
        OPTIONS_VOLUME_UP.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_VOLUME_UP.update(WINDOW)

        OPTIONS_RESOLUTION = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2.2), text_input="Resolution", font=font(2), base_color="White", hovering_color="Green")
        OPTIONS_RESOLUTION.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_RESOLUTION.update(WINDOW)

        OPTIONS_BACK = Button(image=None, pos=(WINDOW_WIDTH/6, WINDOW_HEIGHT/1.2), text_input="BACK", font=font(2), base_color="White", hovering_color="Green")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if OPTIONS_VOLUME_DOWN.checkForInput(OPTIONS_MOUSE_POS):
                    with open('config.ini', 'w') as configfile:
                        volume = float(config.get('config', 'volume'))
                        if volume > 0:
                            volume -= 0.1
                        else: 
                            pass
                        config.set('config', 'volume', f'{volume:.1f}')
                        config.write(configfile)
                    VOLUME = float(config['config']['volume'])
                    pygame.mixer.music.set_volume(VOLUME)
                if OPTIONS_VOLUME_UP.checkForInput(OPTIONS_MOUSE_POS):
                    with open('config.ini', 'w') as configfile:
                        volume = float(config.get('config', 'volume'))
                        if volume < 1:
                            volume += 0.1
                        else: 
                            pass
                        config.set('config', 'volume', f'{volume:.1f}')
                        config.write(configfile)
                    VOLUME = float(config['config']['volume'])
                    pygame.mixer.music.set_volume(VOLUME)
                if OPTIONS_RESOLUTION.checkForInput(OPTIONS_MOUSE_POS):
                    resolution()
        pygame.display.update()

def main_menu():
    while True:
        WINDOW_WIDTH = int(config['config']['width']) // SCALE * SCALE
        WINDOW_HEIGHT = int(config['config']['height']) // SCALE * SCALE
        WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        BG = pygame.image.load("resources/pepe.png")
        BG = pygame.transform.scale(BG, (WINDOW_WIDTH*1.5, WINDOW_HEIGHT*1.5))

        pygame.display.set_caption('Main Menu')
        WINDOW.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = font(3).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/6))
        PLAY_BUTTON = Button(image=pygame.image.load("resources/rect_play.png"), pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/3), text_input="PLAY", font=font(2), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("resources/rect_options.png"), pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2), text_input="OPTIONS", font=font(2), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("resources/rect_quit.png"), pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.5), text_input="QUIT", font=font(2), base_color="#d7fcd4", hovering_color="White")
        WINDOW.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WINDOW)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# fullscreen handling
# monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
# for event in pygame.event.get():
#     if event.type == pygame.VIDEORESIZE:
#         if not fullscreen:
#             print('test')
#             WINDOW = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
#         if event.type == pygame.K_f:
#             fullscreen = not fullscreen
#         if fullscreen:
#             WINDOW = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
#         else:
#             WINDOW = pygame.display.set_mode((WINDOW.get_width(), WINDOW.get_height()), pygame.RESIZABLE)

   
if __name__ == '__main__':
    main_menu()
    # run = True
    # while run:
    #     snake.game(WINDOW, levels.Level1())