from constants import *
import constants
from pygame.locals import *
import pygame
import pickle


class Setting(object):

    def __init__(self, SCREEN):
        self.screen = SCREEN
        self.messagex = int((SCREENWIDTH - IMAGES['board'].get_width()) / 2)
        self.messagey = int(SCREENHEIGHT * 0.09)
        self.buttonx = int(
            (SCREENWIDTH - IMAGES['playButton'].get_width()) / 2)
        self.buttony = int(SCREENHEIGHT * 0.85)
        self.levelx = int((SCREENWIDTH - IMAGES['easy'].get_width()) / 2)
        self.basex = 0
        self.baseShift = IMAGES['base'].get_width(
        ) - IMAGES['background'].get_width()
        self.offsety = 105
        self.PIPEGAP = 120

    def run(self):
        playing = True
        while playing:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and
                                          event.key == K_ESCAPE):
                    return 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (x, y) = event.pos
                    if self.isInBound(x, y) == 'intro':
                        return ('intro', self.PIPEGAP)
                    if self.isInEasy(x, y) == True:
                        self.PIPEGAP = 150
                    elif self.isInMedium(x, y) == True:
                        self.PIPEGAP = 120
                    elif self.isInHard(x, y) == True:
                        self.PIPEGAP = 90

            self.basex = -((-self.basex + 4) % self.baseShift)

            self.screen.blit(IMAGES['background'], (0, 0))
            self.screen.blit(IMAGES['base'], (self.basex, BASEY))
            self.screen.blit(IMAGES['playButton'],
                             (self.buttonx, self.buttony))
            self.screen.blit(IMAGES['easy'], (self.levelx, 50))
            self.screen.blit(IMAGES['medium'],
                             (self.levelx, 50 + self.offsety))
            self.screen.blit(
                IMAGES['hard'], (self.levelx, 50 + self.offsety * 2))
            pygame.display.update()
            FPSCLOCK.tick(FPS)

    def isInBound(self, x, y):
        if (x > self.buttonx and
            x < self.buttonx + IMAGES['playButton'].get_width() and
                y > self.buttony and
                y < self.buttony + IMAGES['playButton'].get_height()):
            return 'intro'

    def isInEasy(self, x, y):
        if (x > self.levelx and
            x < self.levelx + IMAGES['easy'].get_width() and
                y > 50 and y < 50 + IMAGES['easy'].get_height()):
            return True

    def isInMedium(self, x, y):
        if (x > self.levelx and x < self.levelx + IMAGES['medium'].get_width()
            and y > 50 + self.offsety
                and y < 50 + self.offsety + IMAGES['medium'].get_height()):
            return True

    def isInHard(self, x, y):
        if (x > self.levelx and x < self.levelx + IMAGES['hard'].get_width()
            and y > 50 + self.offsety * 2 and
                y < 50 + self.offsety * 2 + IMAGES['hard'].get_height()):
            return True
