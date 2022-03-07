from tkinter import W
import pygame, os, configparser, argparse, sys
from button import Button

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


def font(size):
    return pygame.font.Font(os.path.join('resources', 'fonts', 'AncientModernTales-a7Po.ttf'), SCALE * size)

def play():
    screen_width = int(config['config']['width']) // SCALE * SCALE
    screen_height = int(config['config']['height']) // SCALE * SCALE
    # global WINDOW 
    # WINDOW = pygame.display.set_mode((screen_width, screen_height))
        
    pygame.display.set_caption('Snake')
    snake.game(WINDOW, levels.Level1(screen_width, screen_height))

        # PLAY_MOUSE_POS = pygame.mouse.get_pos()
        # PLAY_BACK = Button(image=None, pos=(screen_width/2, screen_height/2), text_input="BACK", font=font(2), base_color="Black", hovering_color="Green")
        # PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        # PLAY_BACK.update(WINDOW)

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         sys.exit()
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
        #             return

        # pygame.display.update()
    
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
        mouse_pos = pygame.mouse.get_pos()
        WINDOW.fill("black")
        txt_resolution = font(3).render("Resolution", True, "White")
        rect_resolution = txt_resolution.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/6))
        WINDOW.blit(txt_resolution, rect_resolution)

        btn_resolution_ultrahd = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/3), text_input="3840x2160", font=font(2), base_color="White", hovering_color="Green")
        btn_resolution_ultrahd.changeColor(mouse_pos)
        btn_resolution_ultrahd.update(WINDOW)

        btn_resolution_wqhd = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2.2), text_input="2560x1440", font=font(2), base_color="White", hovering_color="Green")
        btn_resolution_wqhd.changeColor(mouse_pos)
        btn_resolution_wqhd.update(WINDOW)
        
        btn_resolution_fullhd = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.7), text_input="1920x1080", font=font(2), base_color="White", hovering_color="Green")
        btn_resolution_fullhd.changeColor(mouse_pos)
        btn_resolution_fullhd.update(WINDOW)
        
        btn_resolution_hd = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.4), text_input="1280x720", font=font(2), base_color="White", hovering_color="Green")
        btn_resolution_hd.changeColor(mouse_pos)
        btn_resolution_hd.update(WINDOW)

        btn_resolution_sd = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.2), text_input="720x576", font=font(2), base_color="White", hovering_color="Green")
        btn_resolution_sd.changeColor(mouse_pos)
        btn_resolution_sd.update(WINDOW)

        btn_resolution_back = Button(image=None, pos=(WINDOW_WIDTH/6, WINDOW_HEIGHT/1.2), text_input="BACK", font=font(2), base_color="White", hovering_color="Green")
        btn_resolution_back.changeColor(mouse_pos)
        btn_resolution_back.update(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_resolution_ultrahd.checkForInput(mouse_pos):
                    width, height = 3840, 2160
                    
                if btn_resolution_wqhd.checkForInput(mouse_pos):
                    width, height = 2560, 1440
                
                if btn_resolution_fullhd.checkForInput(mouse_pos):
                    width, height = 1920, 1080
                    
                if btn_resolution_hd.checkForInput(mouse_pos):
                    width, height = 1280, 720
                    
                if btn_resolution_sd.checkForInput(mouse_pos):
                    width, height = 720, 576
                    
                if btn_resolution_back.checkForInput(mouse_pos):
                    resolution_update(width, height)
                    return

        pygame.display.update()

def options():
    while True:
        WINDOW_WIDTH = int(config['config']['width']) // SCALE * SCALE
        WINDOW_HEIGHT = int(config['config']['height']) // SCALE * SCALE
        WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        pygame.display.set_caption('Options')
        mouse_pos = pygame.mouse.get_pos()
        WINDOW.fill("black")
        txt_options = font(3).render("Options", True, "White")
        options_rect = txt_options.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/6))
        WINDOW.blit(txt_options, options_rect)

        btn_options_volume = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/3), text_input="Volume", font=font(2), base_color="White", hovering_color="White")
        btn_options_volume.changeColor(mouse_pos)
        btn_options_volume.update(WINDOW)

        btn_options_volume_down = Button(image=None, pos=(WINDOW_WIDTH/2 - SCALE*4, WINDOW_HEIGHT/3), text_input="-", font=font(2), base_color="White", hovering_color="Green")
        btn_options_volume_down.changeColor(mouse_pos)
        btn_options_volume_down.update(WINDOW)

        btn_options_volume_up = Button(image=None, pos=(WINDOW_WIDTH/2 + SCALE*4, WINDOW_HEIGHT/3), text_input="+", font=font(2), base_color="White", hovering_color="Green")
        btn_options_volume_up.changeColor(mouse_pos)
        btn_options_volume_up.update(WINDOW)

        btn_options_resolution = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2.2), text_input="Resolution", font=font(2), base_color="White", hovering_color="Green")
        btn_options_resolution.changeColor(mouse_pos)
        btn_options_resolution.update(WINDOW)

        btn_options_back = Button(image=None, pos=(WINDOW_WIDTH/6, WINDOW_HEIGHT/1.2), text_input="BACK", font=font(2), base_color="White", hovering_color="Green")
        btn_options_back.changeColor(mouse_pos)
        btn_options_back.update(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_options_back.checkForInput(mouse_pos):
                    return
                if btn_options_volume_down.checkForInput(mouse_pos):
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
                if btn_options_volume_up.checkForInput(mouse_pos):
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
                if btn_options_resolution.checkForInput(mouse_pos):
                    resolution()
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
    backgroundimage = pygame.image.load(os.path.join("resources", "pepe.png"))
    backgroundimage = pygame.transform.scale(backgroundimage, (WINDOW_WIDTH*1.5, WINDOW_HEIGHT*1.5))

    while True:
        if WINDOW_WIDTH != int(config['config']['width']) and WINDOW_HEIGHT != int(config['config']['height']):
            WINDOW_WIDTH = int(config['config']['width']) // SCALE * SCALE
            WINDOW_HEIGHT = int(config['config']['height']) // SCALE * SCALE
            #global 
            WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    
        pygame.display.set_caption('Main Menu')
        WINDOW.blit(backgroundimage, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        txt_menu = font(3).render("MAIN MENU", True, "#b68f40")
        rect_menu = txt_menu.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/6))
        btn_play = Button(image=pygame.image.load("resources/rect_play.png"), pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/3), text_input="PLAY", font=font(2), base_color="#d7fcd4", hovering_color="White")
        btn_options = Button(image=pygame.image.load("resources/rect_options.png"), pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2), text_input="OPTIONS", font=font(2), base_color="#d7fcd4", hovering_color="White")
        btn_quit = Button(image=pygame.image.load("resources/rect_quit.png"), pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.5), text_input="QUIT", font=font(2), base_color="#d7fcd4", hovering_color="White")
        WINDOW.blit(txt_menu, rect_menu)

        for button in [btn_play, btn_options, btn_quit]:
            button.changeColor(mouse_pos)
            button.update(WINDOW)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_play.checkForInput(mouse_pos):
                    play()
                if btn_options.checkForInput(mouse_pos):
                    options()
                if btn_quit.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()