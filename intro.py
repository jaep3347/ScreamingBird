from itertools import cycle
import random
import sys
from pygame.locals import *
import pygame
from constants import *


class Intro(object):

    def __init__(self, SCREEN):
        self.screen = SCREEN
        # bird flapping animation
        self.birdFlap = 0
        self.birdFlapIndex = cycle([0, 1, 2, 1])
        self.loopIter = 0

        self.birdx = int(SCREENWIDTH * 0.18)
        self.birdy = int((SCREENHEIGHT - IMAGES['bird'][0].get_height()) / 2)
        self.messagex = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
        self.messagey = int(SCREENHEIGHT * 0.12)
        self.buttonx = int(
            2 * (SCREENWIDTH - IMAGES['playButton'].get_width()) / 7) + 35
        self.buttony = int(SCREENHEIGHT * 0.655)

        self.highx = int(
            5 * (SCREENWIDTH - IMAGES['highscore'].get_width()) / 7) - 35
        self.highy = int(SCREENHEIGHT * 0.655)

        self.basex = 0
        self.baseShift = IMAGES['base'].get_width(
        ) - IMAGES['background'].get_width()
        self.animation = 0
        self.direction = 1

    def run(self):
        playing = True
        while playing:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and
                                          event.key == K_ESCAPE):
                    return 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (x, y) = event.pos
                    if self.isInBound(x, y) == 'game':
                        return 'game'
                    if self.isInBoundScore(x, y) == 'highscore':
                        return 'highscore'
                    if self.isSetting(x, y) == 'settings':
                        return 'settings'
            # modified from https://github.com/sourabhv/FlapPyBird
            if (self.loopIter + 1) % 5 == 0:
                self.birdFlap = next(self.birdFlapIndex)
            self.loopIter = (self.loopIter + 1) % 30
            self.basex = -((-self.basex + 4) % self.baseShift)
            self.upDown()

            self.screen.blit(IMAGES['background'], (0, 0))
            self.screen.blit(IMAGES['bird'][self.birdFlap],
                             (self.birdx, self.birdy + self.animation))
            self.screen.blit(IMAGES['message'],
                             (self.messagex + 3, self.messagey))
            self.screen.blit(IMAGES['base'], (self.basex, BASEY))
            self.screen.blit(IMAGES['playButton'],
                             (self.buttonx, self.buttony))
            self.screen.blit(IMAGES['highscore'], (self.highx, self.highy))
            self.screen.blit(IMAGES['settingbutton'], (515, 10))

            pygame.display.update()
            FPSCLOCK.tick(FPS)

    def upDown(self):
        # oscillates
        if abs(self.animation) == 8:
            self.direction *= -1
        if self.direction == 1:
            self.animation += 1
        else:
            self.animation -= 1

    def isInBound(self, x, y):
        if (x > self.buttonx and
            x < self.buttonx + IMAGES['playButton'].get_width() and
                y > self.buttony and
                y < self.buttony + IMAGES['playButton'].get_height()):
            return 'game'

    def isInBoundScore(self, x, y):
        if (x > self.highx and
            x < self.highx + IMAGES['highscore'].get_width() and
                y > self.highy and
                y < self.highy + IMAGES['highscore'].get_height()):
            return 'highscore'

    def isSetting(self, x, y):
        if (x > 515 and x < 515 + IMAGES['settingbutton'].get_width() and
                y > 10 and y < 10 + IMAGES['settingbutton'].get_height()):
            return 'settings'
