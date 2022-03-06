import snake, configparser

config = configparser.ConfigParser()

if __name__ == '__main__':
    run = True
    while run:
        snake.game()
