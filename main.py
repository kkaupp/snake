import pygame, os, configparser, argparse, sys
from button import Button

## Read config.ini ##
config = configparser.ConfigParser()
config.read(os.path.join('resources', 'config.ini'))                # Read config.ini
SCALE = int(config['config']['scale']) // 2 * 2                     # To ensure that it is a multiple of 2
WINDOW_WIDTH = int(config['config']['width']) // SCALE * SCALE      # Read width from config.ini
WINDOW_HEIGHT = int(config['config']['height']) // SCALE * SCALE    # Read height from config.ini

## Argparse ##
parser = argparse.ArgumentParser(description='Snake Game for Python class')
parser.add_argument('-x', '--width', metavar='', type=int, help='Set specific screen width, default value: ' + str(WINDOW_WIDTH), default=WINDOW_WIDTH)        # Uses default of config.ini
parser.add_argument('-y', '--height', metavar='', type=int, help='Set specific screen height, default value: ' + str(WINDOW_HEIGHT), default=WINDOW_HEIGHT)    # Uses default of config.ini
parser.add_argument('-b', '--background', metavar='', type=str, help='Set own mainmenu background image', default='pepe.png')    
parser.add_argument('-m', '--music', metavar='', type=str, help='Set own mainmenu music', default='8_Bit_Fantasy_Adventure_Music.mp3')   
args = parser.parse_args()

## General Game Settings ##
pygame.init()    # Initialize Game

## Music ##
pygame.mixer.music.load(os.path.join('sounds', args.music))         # Loads main menu music
pygame.mixer.music.play(-1,0.0)                                     # Infinite loop of music
pygame.mixer.music.set_volume(float(config['config']['volume']))    # Sets volume of config

## Size ##
WINDOW_WIDTH = (args.width) // SCALE * SCALE                       # Overrides config width setting with argparse
WINDOW_HEIGHT = (args.height) // SCALE * SCALE                     # Overrides config width setting with argparse
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))    # Defines size of entire screen 


import snake, levels, music, scorelib


def font(size):
    """ Returns font at specific size used for displayed text 

        Args: 
            size: int - multiplies with SCALE
    """
    return pygame.font.Font(os.path.join('resources', 'fonts', 'PublicPixel-0W6DP.ttf'), SCALE * size)

def get_username():
    """ View, used to receive username from user """

    user_input = ''
    txt_username = font(1).render('Enter Username and press Enter:', True, "White")
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
        edt_username = font(2).render(f'{user_input}', True, "White")
        rect_edt_username = edt_username.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        WINDOW.blit(txt_username, rect_txt_username)
        WINDOW.blit(edt_username, rect_edt_username)
        pygame.display.update()
        
def choose_level(username, screen_width, screen_height):
    """ Returns 

        Args: 
            username: string - multiplies with SCALE
            screen_width:
            screen_height:
    """
    txt_choose_level = font(2).render("Select Level:", True, "White")
    btn_choose_level_0 = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/3), text_input="Fun Mode", font=font(1), base_color="White", hovering_color="Red")
    btn_choose_level_1 = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2.2), text_input="Level 1", font=font(1), base_color="White", hovering_color="Green")

    score = scorelib.get_score(username)
    button_enabled = [True, True]

    if score.get('level1') >= 20:
        btn_choose_level_2 = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.7), text_input="Level 2", font=font(1), base_color="White", hovering_color="Green")
    else:
        btn_choose_level_2 = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.7), text_input="Level 2", font=font(1), base_color="Dimgray", hovering_color="Dimgray")
        button_enabled[0] = False

    if score.get('level2') >= 20:
        btn_choose_level_3 = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.4), text_input="Level 3", font=font(1), base_color="White", hovering_color="Green")
    else:
        btn_choose_level_3 = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.4), text_input="Level 3", font=font(1), base_color="Dimgray", hovering_color="Dimgray")
        button_enabled[1] = False

    btn_choose_level_back = Button(image=None, pos=(WINDOW_WIDTH/6, WINDOW_HEIGHT/1.2), text_input="BACK", font=font(1), base_color="White", hovering_color="Green")
    rect_choose_level = txt_choose_level.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/6))
    WINDOW.fill("Black")
    WINDOW.blit(txt_choose_level, rect_choose_level)
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for button in [btn_choose_level_0, btn_choose_level_1, btn_choose_level_2, btn_choose_level_3, btn_choose_level_back]:
            button.changeColor(mouse_pos)
            button.update(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_choose_level_0.checkForInput(mouse_pos):
                    return levels.Level()
                if btn_choose_level_1.checkForInput(mouse_pos):
                    return levels.Level1(screen_width, screen_height)
                if btn_choose_level_2.checkForInput(mouse_pos) and button_enabled[0]:
                    return levels.Level2(screen_width, screen_height) 
                if btn_choose_level_3.checkForInput(mouse_pos) and button_enabled[1]:
                    return levels.Level3(screen_width, screen_height)
                if btn_choose_level_back.checkForInput(mouse_pos):
                    return None

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def play():
    score = 0
    screen_width = int(config['config']['width']) // SCALE * SCALE
    screen_height = int(config['config']['height']) // SCALE * SCALE

    username = get_username()
    level = choose_level(username, screen_width, screen_height)
    if level != None:
        music.fade_music(float(config['config']['volume']), "out")
        pygame.mixer.music.pause()
        score = snake.game(WINDOW, level)
        print(username, score)
        pygame.mixer.music.load(os.path.join('sounds', args.music))
        pygame.mixer.music.play()
        music.fade_music(float(config['config']['volume']), "in")

    if score > 0:
        if isinstance(level, levels.Level):
            level_name = 'level'
        if isinstance(level, levels.Level1):
            level_name = 'level1'
        if isinstance(level, levels.Level2):
            level_name = 'level2'
        if isinstance(level, levels.Level3):
            level_name = 'level3'

        scorelib.set_score(username, level_name, score)

def score_level(level):
    score_dict = scorelib.get_highscore(f'level{level}')
    count = 0
    pos = ['-', '-', '-']
    pos_score = ['-', '-', '-']

    for user, score in score_dict.items():
        pos[count] = user
        pos_score[count] = score
        count += 1

    if level == 0:
        txt_score_level = font(2).render("Scoreboard Fun Mode", True, "White")
    else:
        txt_score_level = font(2).render(f"Scoreboard Level {level}", True, "White")

    txt_score_level_pos1 = font(1).render(f"#1 | {pos_score[0]} | {pos[0]}", True, "White")
    txt_score_level_pos2 = font(1).render(f"#2 | {pos_score[1]} | {pos[1]}", True, "White")
    txt_score_level_pos3 = font(1).render(f"#3 | {pos_score[2]} | {pos[2]}", True, "White")

    rect_score_level = txt_score_level.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/6))
    rect_score_level_pos1 = txt_score_level_pos1.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/3))
    rect_score_level_pos2 = txt_score_level_pos2.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2.2))
    rect_score_level_pos3 = txt_score_level_pos3.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.7))

    btn_score_level_back = Button(image=None, pos=(WINDOW_WIDTH/6, WINDOW_HEIGHT/1.2), text_input="BACK", font=font(1), base_color="White", hovering_color="Green")

    WINDOW.fill("black")
    WINDOW.blit(txt_score_level, rect_score_level)
    WINDOW.blit(txt_score_level_pos1, rect_score_level_pos1)
    WINDOW.blit(txt_score_level_pos2, rect_score_level_pos2)
    WINDOW.blit(txt_score_level_pos3, rect_score_level_pos3)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        btn_score_level_back.changeColor(mouse_pos)
        btn_score_level_back.update(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_score_level_back.checkForInput(mouse_pos):
                    return

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def score():
    txt_score = font(2).render("Scoreboard", True, "White")
    rect_score = txt_score.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/6))
    btn_score_level0 = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/3), text_input="Fun Mode", font=font(1), base_color="White", hovering_color="Red")
    btn_score_level1 = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2.2), text_input="Level 1", font=font(1), base_color="White", hovering_color="Green")
    btn_score_level2 = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.7), text_input="Level 2", font=font(1), base_color="White", hovering_color="Green")
    btn_score_level3 = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.4), text_input="Level 3", font=font(1), base_color="White", hovering_color="Green")
    btn_score_back = Button(image=None, pos=(WINDOW_WIDTH/6, WINDOW_HEIGHT/1.2), text_input="BACK", font=font(1), base_color="White", hovering_color="Green")
    WINDOW.fill("black")

    while True:
        WINDOW.fill("black")
        WINDOW.blit(txt_score, rect_score)
        mouse_pos = pygame.mouse.get_pos()

        for button in [btn_score_level0, btn_score_level1, btn_score_level2, btn_score_level3, btn_score_back]:
            button.changeColor(mouse_pos)
            button.update(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_score_level0.checkForInput(mouse_pos):
                    score_level(0)
                if btn_score_level1.checkForInput(mouse_pos):
                    score_level(1)
                if btn_score_level2.checkForInput(mouse_pos):
                    score_level(2)
                if btn_score_level3.checkForInput(mouse_pos):
                    score_level(3)
                if btn_score_back.checkForInput(mouse_pos):
                    return

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
    
def resolution_update(width, height):
    global WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW
    WINDOW_WIDTH = width // SCALE * SCALE
    WINDOW_HEIGHT = height // SCALE * SCALE
    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

def resolution():
    config_changed = False
    width = (args.width)
    height = (args.height)
    txt_resolution = font(2).render("Resolution", True, "White")
    start_width = WINDOW_WIDTH
    start_height = WINDOW_HEIGHT
    init = True

    while True:
        # Update the screen with initial start and every time the resolution is changed
        if start_height != WINDOW_HEIGHT or start_width != WINDOW_WIDTH or init == True:
            rect_resolution = txt_resolution.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/6))
            btn_options_resolution_ultrahd = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/3), text_input="3840x2160", font=font(1), base_color="White", hovering_color="Green")
            btn_options_resolution_wqhd = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2.2), text_input="2560x1440", font=font(1), base_color="White", hovering_color="Green")
            btn_options_resolution_fullhd = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.7), text_input="1920x1080", font=font(1), base_color="White", hovering_color="Green")
            btn_options_resolution_hd = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.4), text_input="1280x720", font=font(1), base_color="White", hovering_color="Green")
            btn_resolution_back = Button(image=None, pos=(WINDOW_WIDTH/6, WINDOW_HEIGHT/1.2), text_input="BACK", font=font(1), base_color="White", hovering_color="Green")
            start_width = WINDOW_WIDTH
            start_height = WINDOW_HEIGHT
            init = False

        WINDOW.fill("black")
        WINDOW.blit(txt_resolution, rect_resolution)
        mouse_pos = pygame.mouse.get_pos()

        for button in [btn_options_resolution_ultrahd, btn_options_resolution_wqhd, btn_options_resolution_fullhd, btn_options_resolution_hd, btn_resolution_back]:
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
                    
                if btn_resolution_back.checkForInput(mouse_pos):
                    if config_changed == True:
                        with open(os.path.join('resources', 'config.ini'), 'w') as configfile:
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
    muted_volume = float(config.get('config', 'muted_volume'))
    txt_options = font(2).render("Options", True, "White")
    start_width = WINDOW_WIDTH
    start_height = WINDOW_HEIGHT
    init = True
    
    while True:
        # Update the screen with initial start and every time the resolution is changed
        if start_height != WINDOW_HEIGHT or start_width != WINDOW_WIDTH or init == True:
            btn_options_volume = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/3), text_input="Volume", font=font(1), base_color="White", hovering_color="Green")
            btn_options_volume_down = Button(image=None, pos=(WINDOW_WIDTH/2 - SCALE*4, WINDOW_HEIGHT/3), text_input="-", font=font(1), base_color="White", hovering_color="Green")
            btn_options_volume_up = Button(image=None, pos=(WINDOW_WIDTH/2 + SCALE*4, WINDOW_HEIGHT/3), text_input="+", font=font(1), base_color="White", hovering_color="Green")
            btn_options_resolution = Button(image=None, pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2.2), text_input="Resolution", font=font(1), base_color="White", hovering_color="Green")
            btn_options_back = Button(image=None, pos=(WINDOW_WIDTH/6, WINDOW_HEIGHT/1.2), text_input="BACK", font=font(1), base_color="White", hovering_color="Green")
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

                if btn_options_volume.checkForInput(mouse_pos):
                    if volume > 0:
                        muted_volume = volume
                        volume = 0
                    else:
                        volume = muted_volume
                    pygame.mixer.music.set_volume(volume)

                if btn_options_volume_down.checkForInput(mouse_pos):
                    if volume > 0 and volume <= 0.5:
                        volume -= 0.05
                    pygame.mixer.music.set_volume(volume)

                if btn_options_volume_up.checkForInput(mouse_pos):
                    if volume < 0.5 and volume >= 0:
                        volume += 0.05
                    pygame.mixer.music.set_volume(volume)

                if btn_options_resolution.checkForInput(mouse_pos):
                    resolution()
                
                if btn_options_back.checkForInput(mouse_pos):
                    with open(os.path.join('resources', 'config.ini'), 'w') as configfile:
                        config.set('config', 'volume', f'{volume:.1f}')
                        config.set('config', 'muted_volume', f'{muted_volume:.1f}')
                        config.write(configfile)
                    return

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

   
if __name__ == '__main__':
    backgroundimage = pygame.image.load(os.path.join("resources", args.background))
    pygame.display.set_caption('Snake by LFH')
    txt_menu = font(3).render("MAIN MENU", True, "#cc2936")
    start_width = WINDOW_WIDTH
    start_height = WINDOW_HEIGHT
    init = True

    while True:
        # Update the screen with initial start and every time the resolution is changed
        if start_height != WINDOW_HEIGHT or start_width != WINDOW_WIDTH or init == True:
            btn_play = Button(image=pygame.image.load("resources/button.png"), pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/3), text_input="PLAY", font=font(2), base_color="White", hovering_color="azure3")
            btn_score = Button(image=pygame.image.load("resources/button.png"), pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2), text_input="SCORE", font=font(2), base_color="White", hovering_color="azure3")
            btn_options = Button(image=pygame.image.load("resources/button.png"), pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.5), text_input="OPTIONS", font=font(2), base_color="White", hovering_color="azure3")
            btn_quit = Button(image=pygame.image.load("resources/button.png"), pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.2), text_input="QUIT", font=font(2), base_color="White", hovering_color="azure3")
            rect_menu = txt_menu.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/6))
            backgroundimage = pygame.transform.scale(backgroundimage, (WINDOW_WIDTH*1.5, WINDOW_HEIGHT*1.5))
            start_width = WINDOW_WIDTH
            start_height = WINDOW_HEIGHT
            init = False
        
        WINDOW.blit(backgroundimage, (0, 0))
        WINDOW.blit(txt_menu, rect_menu)
        mouse_pos = pygame.mouse.get_pos()

        for button in [btn_play, btn_score, btn_options, btn_quit]:
            button.changeColor(mouse_pos)
            button.update(WINDOW)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_play.checkForInput(mouse_pos):
                    play()
                if btn_score.checkForInput(mouse_pos):
                    score()
                if btn_options.checkForInput(mouse_pos):
                    options()
                if btn_quit.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()