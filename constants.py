import pygame

SCREENWIDTH = 576
SCREENHEIGHT = 512
FPS = 30
PIPEGAP = 120
BASEY = SCREENHEIGHT * 0.79
IMAGES = dict()

pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Screaming Bird')
FPSCLOCK = pygame.time.Clock()

# number images for displaying score
# citation: https://github.com/sourabhv/FlapPyBird/tree/master/assets/sprites
IMAGES['numbers'] = (
    pygame.image.load('assets/sprites/0.png').convert_alpha(),
    pygame.image.load('assets/sprites/1.png').convert_alpha(),
    pygame.image.load('assets/sprites/2.png').convert_alpha(),
    pygame.image.load('assets/sprites/3.png').convert_alpha(),
    pygame.image.load('assets/sprites/4.png').convert_alpha(),
    pygame.image.load('assets/sprites/5.png').convert_alpha(),
    pygame.image.load('assets/sprites/6.png').convert_alpha(),
    pygame.image.load('assets/sprites/7.png').convert_alpha(),
    pygame.image.load('assets/sprites/8.png').convert_alpha(),
    pygame.image.load('assets/sprites/9.png').convert_alpha()
)

# game over image
IMAGES['gameover'] = pygame.image.load(
    'assets/sprites/gameover.png').convert_alpha()

# welcome screen image
# modified
IMAGES['message'] = pygame.image.load(
    'assets/sprites/message.png').convert_alpha()

# base image
# citation: https://github.com/sourabhv/FlapPyBird/tree/master/assets/sprites
IMAGES['base'] = pygame.image.load(
    'assets/sprites/base.png').convert_alpha()

# background image
# citation: https://github.com/sourabhv/FlapPyBird/tree/master/assets/sprites
IMAGES['background'] = pygame.image.load(
    'assets/sprites/background.png').convert()

# bird image with three flap positions
# modified
IMAGES['bird'] = (
    pygame.image.load('assets/sprites/redbird-upflap.png').convert_alpha(),
    pygame.image.load(
        'assets/sprites/redbird-midflap.png').convert_alpha(),
    pygame.image.load(
        'assets/sprites/redbird-downflap.png').convert_alpha(),
)

# two pipes (rotate one)
# citation: https://github.com/sourabhv/FlapPyBird/tree/master/assets/sprites
IMAGES['pipe'] = (
    pygame.transform.rotate(
        pygame.image.load('assets/sprites/pipe.png').convert_alpha(), 180),
    pygame.image.load('assets/sprites/pipe.png').convert_alpha()
)

# play button
IMAGES['playButton'] = pygame.image.load(
    'assets/sprites/play.png').convert_alpha()

# bar graph with transform
IMAGES['graph'] = pygame.image.load(
    'assets/sprites/block.png').convert_alpha()
IMAGES['graph'] = pygame.transform.scale(IMAGES['graph'], (100, 10))

# ingame pause button
# http://www.mrferrante.com/flappybird/flappybird_sprite_sheet_1.png
IMAGES['pause'] = pygame.image.load(
    'assets/sprites/pause.png').convert_alpha()

# paused message
IMAGES['paused'] = pygame.image.load(
    'assets/sprites/paused.png').convert_alpha()

# highscore buttons
# http://www.mrferrante.com/flappybird/flappybird_sprite_sheet_1.png
IMAGES['highscore'] = pygame.image.load(
    'assets/sprites/highscore.png').convert_alpha()

# highscore board
# modified
IMAGES['board'] = pygame.image.load('assets/sprites/board.png').convert_alpha()

# dot after ranking in highscore
IMAGES['dot'] = pygame.image.load('assets/sprites/dot.png').convert_alpha()

# high score message
IMAGES['highmsg'] = pygame.image.load(
    'assets/sprites/highscoremsg.png').convert_alpha()

# level chooser
IMAGES['easy'] = pygame.image.load('assets/sprites/easy.png').convert_alpha()
IMAGES['medium'] = pygame.image.load(
    'assets/sprites/medium.png').convert_alpha()
IMAGES['hard'] = pygame.image.load('assets/sprites/hard.png').convert_alpha()

# setting message
IMAGES['setting'] = pygame.image.load(
    'assets/sprites/setting.png').convert_alpha()

# intro settin button with transform
IMAGES['settingbutton'] = pygame.image.load(
    'assets/sprites/settingbutton.png').convert_alpha()
IMAGES['settingbutton'] = pygame.transform.scale(
    IMAGES['settingbutton'], (50, 50))
