from game import Game
from pygame.locals import *
import pygame
from constants import *
import pickle


class GameOver(object):

    def __init__(self, SCREEN, score):
        self.score = score
        self.screen = SCREEN
        self.basex = 0
        self.baseShift = IMAGES['base'].get_width(
        ) - IMAGES['background'].get_width()
        self.messagex = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
        self.messagey = int(SCREENHEIGHT * 0.12)
        self.buttonx = int(
            (SCREENWIDTH - IMAGES['playButton'].get_width()) / 2)
        self.buttony = int(SCREENHEIGHT * 0.655)
        self.saved = False

    def load(self):
        try:
            with open('score.dat', 'rb') as dataFile:
                self.scoreData = []
                while True:
                    try:
                        data = pickle.load(dataFile)
                        if isinstance(data, list):
                            self.scoreData += data
                        else:
                            self.scoreData.append(data)
                    except EOFError:
                        break
        except:
            self.scoreData = None

    def record(self):
        self.load()
        scoreData = self.score
        if self.scoreData is None:
            self.scoreData = scoreData
        else:
            self.scoreData.append(scoreData)
        with open('score.dat', 'wb') as dataFile:
            pickle.dump(self.scoreData, dataFile)

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
                        return 'intro'
            self.basex = -((-self.basex + 4) % self.baseShift)
            self.screen.blit(IMAGES['background'], (0, 0))
            self.screen.blit(IMAGES['base'], (self.basex, BASEY))
            self.screen.blit(IMAGES['gameover'],
                             (self.messagex, self.messagey))
            self.screen.blit(IMAGES['playButton'],
                             (self.buttonx, self.buttony))
            self.showScore(self.screen)
            if not self.saved:
                self.record()
                self.saved = True
            pygame.display.update()
            FPSCLOCK.tick(FPS)

    # idea from https://github.com/sourabhv/FlapPyBird but modified
    def showScore(self, SCREEN):
        scoreDigits = [int(x) for x in list(str(self.score))]
        totalWidth = 0  # total width of all numbers to be printed

        for digit in scoreDigits:
            totalWidth += IMAGES['numbers'][digit].get_width()

        Xoffset = (SCREENWIDTH - totalWidth) / 2

        for digit in scoreDigits:
            SCREEN.blit(IMAGES['numbers'][digit],
                        (Xoffset, SCREENHEIGHT * 0.3))
            Xoffset += IMAGES['numbers'][digit].get_width()

    def isInBound(self, x, y):
        if (x > self.buttonx and
            x < self.buttonx + IMAGES['playButton'].get_width() and
                y > self.buttony and
                y < self.buttony + IMAGES['playButton'].get_height()):
            return 'game'
