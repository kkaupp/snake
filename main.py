import snake, configparser
import levels

config = configparser.ConfigParser()

if __name__ == '__main__':
    run = True
    while run:
        snake.game(levels.Level1())
