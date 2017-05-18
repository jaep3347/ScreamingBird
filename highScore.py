from time import strftime
from constants import *
from pygame.locals import *
import pygame
import shelve
import pickle


class HighScore(object):

    def __init__(self, SCREEN):
        self.screen = SCREEN
        self.messagex = int((SCREENWIDTH - IMAGES['board'].get_width()) / 2)
        self.messagey = int(SCREENHEIGHT * 0.09)
        self.buttonx = int(
            (SCREENWIDTH - IMAGES['playButton'].get_width()) / 2)
        self.buttony = int(SCREENHEIGHT * 0.85)
        self.basex = 0
        self.baseShift = (IMAGES['base'].get_width() -
                          IMAGES['background'].get_width())

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
                        return 'intro'

            self.basex = -((-self.basex + 4) % self.baseShift)

            self.screen.blit(IMAGES['background'], (0, 0))
            self.screen.blit(
                IMAGES['board'], (self.messagex + 3, self.messagey + 40))
            self.screen.blit(IMAGES['base'], (self.basex, BASEY))
            self.screen.blit(IMAGES['playButton'],
                             (self.buttonx, self.buttony))

            self.load()
            self.showScore(self.screen)
            self.screen.blit(IMAGES['highmsg'],
                             (self.messagex + 20, self.messagey - 22))
            pygame.display.update()
            FPSCLOCK.tick(FPS)

    # this showScore is my own logic
    def showScore(self, SCREEN):
        if self.scoreData != None:
            oldscoreList = sorted(self.scoreData, reverse=True)
            scoreList = []
            for score in oldscoreList:
                if score not in scoreList:
                    scoreList.append(score)
            scoreList = scoreList[:5]
            Yoffset = 0
            ranking = 0
            for score in scoreList:
                ranking += 1
                scoreDigits = []
                for x in list(str(score)):
                    scoreDigits.append(int(x))
                totalWidth = 0  # total width of all numbers to be printed

                for digit in scoreDigits:
                    totalWidth += IMAGES['numbers'][digit].get_width()

                Xoffset = (SCREENWIDTH - totalWidth) / 2
                digitCount = 0
                for digit in scoreDigits:
                    if len(scoreDigits) == 1:
                        SCREEN.blit(IMAGES['numbers'][
                                    digit], (Xoffset + 55,
                                             SCREENHEIGHT * 0.15 + Yoffset + 40))
                        rankWidth = (
                            SCREENWIDTH - IMAGES['numbers'][ranking].get_width()) / 2
                        if ranking == 1:
                            SCREEN.blit(IMAGES[
                                        'dot'], (rankWidth - 36,
                                        (SCREENHEIGHT * 0.15 + Yoffset +
                                         IMAGES['dot'].get_height() + 44)))
                        else:
                            SCREEN.blit(IMAGES[
                                        'dot'], (rankWidth - 28,
                                                 (SCREENHEIGHT * 0.15 + Yoffset
                                                  + IMAGES['dot'].get_height()
                                                  + 44)))
                        SCREEN.blit(IMAGES['numbers'][
                                    ranking], (rankWidth - 53,
                                               SCREENHEIGHT * 0.15 +
                                               Yoffset + 40))
                        Xoffset += IMAGES['numbers'][digit].get_width()
                        Yoffset += 51
                    else:
                        digitCount += 1
                        SCREEN.blit(IMAGES['numbers'][
                                    digit], ((Xoffset + 55,
                                              SCREENHEIGHT * 0.15 +
                                              Yoffset + 40)))
                        rankWidth = (SCREENWIDTH -
                                     IMAGES['numbers'][ranking].get_width()) / 2
                        if ranking == 1:
                            SCREEN.blit(IMAGES[
                                        'dot'], ((rankWidth - 36,
                                                  SCREENHEIGHT * 0.15 + Yoffset
                                                  + IMAGES['dot'].get_height()
                                                  + 44)))
                        else:
                            SCREEN.blit(IMAGES[
                                        'dot'], (rankWidth - 28,
                                                 (SCREENHEIGHT * 0.15 + Yoffset
                                                  + IMAGES['dot'].get_height()
                                                  + 44)))
                        SCREEN.blit(IMAGES['numbers'][
                                    ranking],
                                    (rankWidth - 53,
                                     SCREENHEIGHT * 0.15 + Yoffset + 40))
                        Xoffset += IMAGES['numbers'][digit].get_width()
                        if digitCount == 2:
                            Yoffset += 51

    def isInBound(self, x, y):
        if (x > self.buttonx and
            x < self.buttonx + IMAGES['playButton'].get_width() and
                y > self.buttony and
                y < self.buttony + IMAGES['playButton'].get_height()):
            return 'intro'
