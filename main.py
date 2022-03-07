import pygame, os, configparser, argparse, sys
from button import Button

## Read config.ini ##
config = configparser.ConfigParser()
config.read(os.path.join('config.ini'))
SCALE = int(config['config']['scale']) // 2 * 2     # To ensure that it is a multiple of 2
VOLUME = float(config['config']['volume'])
WINDOW_WIDTH = int(config['config']['width']) // SCALE * SCALE
WINDOW_HEIGHT = int(config['config']['height']) // SCALE * SCALE

## Argparse ##
parser = argparse.ArgumentParser(description='Snake Game for Python class')
parser.add_argument('-x', '--width', metavar='', type=int, help='Set specific screen width, default value: ' + str(WINDOW_WIDTH), default=WINDOW_WIDTH)        # uses default of config
parser.add_argument('-y', '--height', metavar='', type=int, help='Set specific screen height, default value: ' + str(WINDOW_HEIGHT), default=WINDOW_HEIGHT)    # uses default of config
parser.add_argument('-b', '--background', metavar='', type=str, help='Set own mainmenu background image', default='pepe.png')    
parser.add_argument('-m', '--music', metavar='', type=str, help='Set own mainmenu music', default='8_Bit_Fantasy_Adventure_Music.mp3')   
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


import snake, levels, music


def font(size):
    return pygame.font.Font(os.path.join('resources', 'fonts', 'AncientModernTales-a7Po.ttf'), SCALE * size)

def get_username():
    user_input = ''
    txt_username = font(3).render('Enter Username and press Enter:', True, "White")
    rect_txt_username = txt_username.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/6))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]    # delete last character
                elif event.key == pygame.K_RETURN:
                    return user_input
                else:
                    user_input += event.unicode
                
        WINDOW.fill("Black")
        edt_username = font(3).render(f'{user_input}', True, "White")
        rect_edt_username = edt_username.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        WINDOW.blit(txt_username, rect_txt_username)
        WINDOW.blit(edt_username, rect_edt_username)
        pygame.display.update()
        
def choose_level(screen_width, screen_height):
    txt_choose_level = font(3).render("Select Level:", True, "White")
    while True:
        btn_choose_level_0 = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/3), text_input="Fun Mode", font=font(2), base_color="White", hovering_color="Green")
        btn_choose_level_1 = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2.2), text_input="Level 1", font=font(2), base_color="White", hovering_color="Green")
        btn_choose_level_2 = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.7), text_input="Level 2", font=font(2), base_color="White", hovering_color="Green")
        btn_choose_level_3 = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.4), text_input="Level 3", font=font(2), base_color="White", hovering_color="Green")
        btn_choose_level_back = Button(image=None, pos=(WINDOW_WIDTH/6, WINDOW_HEIGHT/1.2), text_input="BACK", font=font(2), base_color="White", hovering_color="Green")
        rect_choose_level = txt_choose_level.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/6))

        WINDOW.fill("Black")
        WINDOW.blit(txt_choose_level, rect_choose_level)
        mouse_pos = pygame.mouse.get_pos()

        for button in [btn_choose_level_0, btn_choose_level_1, btn_choose_level_2, btn_choose_level_3, btn_choose_level_back]:
            button.changeColor(mouse_pos)
            button.update(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_choose_level_0.checkForInput(mouse_pos):
                    return levels.Level(screen_width, screen_height)
                if btn_choose_level_1.checkForInput(mouse_pos):
                    return levels.Level1(screen_width, screen_height)
                if btn_choose_level_2.checkForInput(mouse_pos):
                    return levels.Level2(screen_width, screen_height) 
                if btn_choose_level_3.checkForInput(mouse_pos):
                    return levels.Level3(screen_width, screen_height)
                if btn_choose_level_back.checkForInput(mouse_pos):
                    return None

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def play():
    screen_width = int(config['config']['width']) // SCALE * SCALE
    screen_height = int(config['config']['height']) // SCALE * SCALE

    username = get_username()
    level = choose_level(screen_width, screen_height)
    if level != None:
        music.fade_music(VOLUME, "out")
        pygame.mixer.music.pause()
        snake.game(WINDOW, level)

    pygame.mixer.music.play()
    music.fade_music(VOLUME, "in")
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
    global WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW
    WINDOW_WIDTH = width // SCALE * SCALE
    WINDOW_HEIGHT = height // SCALE * SCALE
    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

def resolution():
    config_changed = False
    width = (args.width)
    height = (args.height)
    txt_resolution = font(3).render("Resolution", True, "White")
    start_width = WINDOW_WIDTH
    start_height = WINDOW_HEIGHT
    init = True

    while True:
        # Update the screen with initial start and every time the resolution is changed
        if start_height != WINDOW_HEIGHT or start_width != WINDOW_WIDTH or init == True:
            rect_resolution = txt_resolution.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/6))
            btn_options_resolution_ultrahd = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/3), text_input="3840x2160", font=font(2), base_color="White", hovering_color="Green")
            btn_options_resolution_wqhd = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2.2), text_input="2560x1440", font=font(2), base_color="White", hovering_color="Green")
            btn_options_resolution_fullhd = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.7), text_input="1920x1080", font=font(2), base_color="White", hovering_color="Green")
            btn_options_resolution_hd = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.4), text_input="1280x720", font=font(2), base_color="White", hovering_color="Green")
            btn_options_resolution_sd = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.2), text_input="720x576", font=font(2), base_color="White", hovering_color="Green")
            btn_resolution_back = Button(image=None, pos=(WINDOW_WIDTH/6, WINDOW_HEIGHT/1.2), text_input="BACK", font=font(2), base_color="White", hovering_color="Green")
            start_width = WINDOW_WIDTH
            start_height = WINDOW_HEIGHT
            init = False

        WINDOW.fill("black")
        WINDOW.blit(txt_resolution, rect_resolution)
        mouse_pos = pygame.mouse.get_pos()

        for button in [btn_options_resolution_ultrahd, btn_options_resolution_wqhd, btn_options_resolution_fullhd, btn_options_resolution_hd, btn_options_resolution_sd, btn_resolution_back]:
            button.changeColor(mouse_pos)
            button.update(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_options_resolution_ultrahd.checkForInput(mouse_pos):
                    width, height = 3840, 2160
                    resolution_update(width, height)
                    config_changed = True
                    
                if btn_options_resolution_wqhd.checkForInput(mouse_pos):
                    width, height = 2560, 1440
                    resolution_update(width, height)
                    config_changed = True
                
                if btn_options_resolution_fullhd.checkForInput(mouse_pos):
                    width, height = 1920, 1080
                    resolution_update(width, height)
                    config_changed = True
                    
                if btn_options_resolution_hd.checkForInput(mouse_pos):
                    width, height = 1280, 720
                    resolution_update(width, height)
                    config_changed = True

                if btn_options_resolution_sd.checkForInput(mouse_pos):
                    width, height = 720, 576
                    resolution_update(width, height)
                    config_changed = True
                    
                if btn_resolution_back.checkForInput(mouse_pos):
                    if config_changed == True:
                        with open('config.ini', 'w') as configfile:
                            config.set('config', 'width', f'{width}')
                            config.set('config', 'height', f'{height}')
                            config.write(configfile)
                            config_changed = False
                        return

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def options():
    volume = float(config.get('config', 'volume'))
    txt_options = font(3).render("Options", True, "White")
    start_width = WINDOW_WIDTH
    start_height = WINDOW_HEIGHT
    init = True

    while True:
        # Update the screen with initial start and every time the resolution is changed
        if start_height != WINDOW_HEIGHT or start_width != WINDOW_WIDTH or init == True:
            btn_options_volume = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/3), text_input="Volume", font=font(2), base_color="White", hovering_color="White")
            btn_options_volume_down = Button(image=None, pos=(WINDOW_WIDTH/2 - SCALE*4, WINDOW_HEIGHT/3), text_input="-", font=font(2), base_color="White", hovering_color="Green")
            btn_options_volume_up = Button(image=None, pos=(WINDOW_WIDTH/2 + SCALE*4, WINDOW_HEIGHT/3), text_input="+", font=font(2), base_color="White", hovering_color="Green")
            btn_options_resolution = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2.2), text_input="Resolution", font=font(2), base_color="White", hovering_color="Green")
            btn_options_back = Button(image=None, pos=(WINDOW_WIDTH/6, WINDOW_HEIGHT/1.2), text_input="BACK", font=font(2), base_color="White", hovering_color="Green")
            rect_options = txt_options.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/6))
            start_width = WINDOW_WIDTH
            start_height = WINDOW_HEIGHT
            init = False

        WINDOW.fill("black")
        WINDOW.blit(txt_options, rect_options)
        mouse_pos = pygame.mouse.get_pos()

        for button in [btn_options_volume, btn_options_volume_down, btn_options_volume_up, btn_options_resolution, btn_options_back]:
            button.changeColor(mouse_pos)
            button.update(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                if btn_options_volume_down.checkForInput(mouse_pos):
                    if volume > 0:
                        volume -= 0.1
                    pygame.mixer.music.set_volume(volume)

                if btn_options_volume_up.checkForInput(mouse_pos):
                    if volume < 1:
                        volume += 0.1
                    pygame.mixer.music.set_volume(volume)

                if btn_options_resolution.checkForInput(mouse_pos):
                    resolution()
                
                if btn_options_back.checkForInput(mouse_pos):
                    with open('config.ini', 'w') as configfile:
                        config.set('config', 'volume', f'{volume:.1f}')
                        config.write(configfile)
                    return

            if event.type == pygame.QUIT:
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
    backgroundimage = pygame.image.load(os.path.join("resources", args.background))
    pygame.display.set_caption('Snake by LFH')
    txt_menu = font(3).render("MAIN MENU", True, "#b68f40")
    start_width = WINDOW_WIDTH
    start_height = WINDOW_HEIGHT
    init = True

    while True:
        # Update the screen with initial start and every time the resolution is changed
        if start_height != WINDOW_HEIGHT or start_width != WINDOW_WIDTH or init == True:
            btn_play = Button(image=pygame.image.load("resources/rect_play.png"), pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/3), text_input="PLAY", font=font(2), base_color="#d7fcd4", hovering_color="White")
            btn_options = Button(image=pygame.image.load("resources/rect_options.png"), pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2), text_input="OPTIONS", font=font(2), base_color="#d7fcd4", hovering_color="White")
            btn_quit = Button(image=pygame.image.load("resources/rect_quit.png"), pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.5), text_input="QUIT", font=font(2), base_color="#d7fcd4", hovering_color="White")
            rect_menu = txt_menu.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/6))
            backgroundimage = pygame.transform.scale(backgroundimage, (WINDOW_WIDTH*1.5, WINDOW_HEIGHT*1.5))
            start_width = WINDOW_WIDTH
            start_height = WINDOW_HEIGHT
            init = False
        
        WINDOW.blit(backgroundimage, (0, 0))
        WINDOW.blit(txt_menu, rect_menu)
        mouse_pos = pygame.mouse.get_pos()

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