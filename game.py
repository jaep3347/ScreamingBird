from itertools import cycle
import random
from pygame.locals import *
import pygame
import struct
from constants import *
from pyaudio import PyAudio, paInt16


class Game(object):

    def __init__(self, SCREEN, GAP):
        self.PIPEGAP = GAP
        self.NUM_SAMPLES = 2048
        self.screen = SCREEN
        self.HITMASKS = {}

        # hismask for pipes
        self.HITMASKS['pipe'] = (
            self.pixelMasks(IMAGES['pipe'][0]),
            self.pixelMasks(IMAGES['pipe'][1]),
        )

        self.score = 0
        self.birdIndex = 0
        self.loopIter = 0
        self.birdIndexGen = cycle([0, 1, 2, 1])
        self.birdx = int(SCREENWIDTH * 0.2)
        self.birdy = int((SCREENHEIGHT - IMAGES['bird'][0].get_height()) / 2)

        self.basex = 0
        self.baseShift = IMAGES['base'].get_width(
        ) - IMAGES['background'].get_width()

        # get 2 new pipes
        self.newPipe1 = self.getRandomPipe()
        self.newPipe2 = self.getRandomPipe()
        # self.newPipe3 = self.getRandomPipe()

        # list of upper pipes
        self.upperPipes = [
            {'x': SCREENWIDTH + 200, 'y': self.newPipe1[0]['y']},
            {'x': SCREENWIDTH + 200 +
                (SCREENWIDTH / 2), 'y': self.newPipe2[0]['y']},
            # {'x': SCREENWIDTH + 200 + (2*SCREENWIDTH / 3), 'y': self.newPipe3[0]['y']}
        ]

        # list of lowerpipe
        self.lowerPipes = [
            {'x': SCREENWIDTH + 200, 'y': self.newPipe1[1]['y']},
            {'x': SCREENWIDTH + 200 +
                (SCREENWIDTH / 2), 'y': self.newPipe2[1]['y']},
            # {'x': SCREENWIDTH + 200 + (2*SCREENWIDTH / 3), 'y': self.newPipe3[1]['y']}
        ]

        self.pipeVelX = -4
        self.playerVelY = -9
        self.playerMaxVelY = 10
        self.playerMinVelY = -8
        self.playerAccY = 1
        self.playerFlapAcc = -9
        self.playerFlapped = False

        self.HITMASKS['bird'] = (
            self.pixelMasks(IMAGES['bird'][0]),
            self.pixelMasks(IMAGES['bird'][1]),
            self.pixelMasks(IMAGES['bird'][2]),
        )

        self.voice_bar = IMAGES['graph']
        self.pause = False
        self.pausex = 20
        self.pausey = SCREENHEIGHT - 40
        self.messagex = int((SCREENWIDTH - IMAGES['paused'].get_width()) / 2)
        self.messagey = int(SCREENHEIGHT * 0.12)
        self.firstPipe = 0
        self.secondPipe = 0

    def run(self):
        playing = True
        pa = PyAudio()
        sampling_rate = int(pa.get_device_info_by_index(0)
                            ['defaultSampleRate'])
        self.stream = pa.open(format=paInt16, channels=1, rate=sampling_rate,
                              input=True, frames_per_buffer=self.NUM_SAMPLES)

        while playing:
            print(self.PIPEGAP)
            FPSCLOCK = pygame.time.Clock()
            SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

            for event in pygame.event.get():
                # print("pygame.event.get() == ", pygame.event.get())
                if event.type == QUIT or (event.type == KEYDOWN
                                          and event.key == K_ESCAPE):
                    return 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (x, y) = event.pos
                    if self.isInBound(x, y) == True:
                        self.pause = True
                if event.type == KEYDOWN and (event.key == K_SPACE
                                              or event.key == K_UP):
                    if self.pause == False:
                        if self.birdy > -2 * IMAGES['bird'][0].get_height():
                            self.playerVelY = self.playerFlapAcc
                            self.playerFlapped = True
                    if self.pause == True:
                        self.pause = False

            string_audio_data = self.stream.read(self.NUM_SAMPLES)
            volume = max(struct.unpack('2048h', string_audio_data))
            volume -= 6000

            # soundbar graph feature
            if volume <= 0:
                xlength = 1
            else:
                xlength = int(100 * volume / 20000)
            if xlength >= 100:
                xlength = 99
            newGraph = pygame.transform.scale(IMAGES['graph'], (xlength, 10))

            # pause feature
            if not self.pause:

                # volume control feature
                if volume > 1000:
                    if self.birdy > -2 * IMAGES['bird'][0].get_height():
                        self.playerVelY = -(volume // 2000)
                        self.playerFlapped = True

                crashTest = self.checkCrash()
                if crashTest[0]:
                    return ('gameover', self.score)

                birdMid = self.birdx + IMAGES['bird'][0].get_width() / 2
                for pipe in self.upperPipes:
                    pipeMid = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
                    if pipeMid <= birdMid < pipeMid + 4:
                        self.score += 1
                if (self.loopIter + 1) % 3 == 0:
                    self.birdIndex = next(self.birdIndexGen)
                self.loopIter = (self.loopIter + 1) % 30
                self.basex = -((-self.basex + 100) % self.baseShift)

                if self.playerVelY < self.playerMaxVelY and not self.playerFlapped:
                    self.playerVelY += self.playerAccY
                if self.playerFlapped:
                    self.playerFlapped = False
                playerHeight = IMAGES['bird'][self.birdIndex].get_height()
                self.birdy += min(self.playerVelY, BASEY -
                                  self.birdy - playerHeight)

                for uPipe in self.upperPipes:
                    uPipe['x'] += self.pipeVelX

                for lPipe in self.lowerPipes:
                    lPipe['x'] += self.pipeVelX

                if 0 < self.upperPipes[0]['x'] < 5:
                    newPipe = self.getRandomPipe()
                    self.upperPipes.append(newPipe[0])
                    self.lowerPipes.append(newPipe[1])

                if self.upperPipes[0]['x'] < -IMAGES['pipe'][0].get_width():
                    self.upperPipes.pop(0)
                    self.lowerPipes.pop(0)
                SCREEN.blit(IMAGES['background'], (0, 0))

                count = 0
                for uPipe in self.upperPipes:
                    SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
                    count += 1
                    if count % 2 == 1:
                        self.firstPipe = uPipe['x']
                    else:
                        self.secondPipe = uPipe['x']

                for lPipe in self.lowerPipes:
                    SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

                SCREEN.blit(IMAGES['base'], (self.basex, BASEY))
                self.showScore(SCREEN)
                SCREEN.blit(IMAGES['bird'][self.birdIndex],
                            (self.birdx, self.birdy))

                SCREEN.blit(newGraph, (20, 20))
                SCREEN.blit(IMAGES['pause'], (self.pausex, self.pausey))
                pygame.display.update()
                FPSCLOCK.tick(FPS)
            else:
                # paused mode
                SCREEN.blit(IMAGES['background'], (0, 0))
                for uPipe, lPipe in zip(self.upperPipes, self.lowerPipes):
                    SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
                    SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))
                SCREEN.blit(IMAGES['base'], (self.basex, BASEY))
                self.showScore(SCREEN)
                SCREEN.blit(IMAGES['bird'][self.birdIndex],
                            (self.birdx, self.birdy))
                SCREEN.blit(newGraph, (20, 20))
                SCREEN.blit(IMAGES['pause'], (self.pausex, self.pausey))
                SCREEN.blit(IMAGES['paused'],
                            (self.messagex, self.messagey + 50))
                pygame.display.update()

    # modified from
    # http://pygame-learning-environment.readthedocs.io/en/latest/user/games/flappybird.html
    def getRandomPipe(self):
        IMAGES['pipe'] = (
            pygame.transform.rotate(
                pygame.image.load('assets/sprites/pipe.png').convert_alpha(), 180),
            pygame.image.load('assets/sprites/pipe.png').convert_alpha()
        )
        gap = random.randrange(0, int(BASEY * 0.6 - self.PIPEGAP))
        gap += int(BASEY * 0.2)
        pipeHeight = IMAGES['pipe'][0].get_height()
        pipeX = SCREENWIDTH + 10

        return [
            {'x': pipeX, 'y': gap - pipeHeight},  # upper pipe
            {'x': pipeX, 'y': gap + self.PIPEGAP},  # lower pipe
        ]

    # idea from https://github.com/sourabhv/FlapPyBird but modified a lot
    def showScore(self, SCREEN):
        scoreDigits = [int(x) for x in list(str(self.score))]
        totalWidth = 0  # total width of all numbers to be printed

        for digit in scoreDigits:
            totalWidth += IMAGES['numbers'][digit].get_width()

        Xoffset = (SCREENWIDTH - totalWidth) / 2

        for digit in scoreDigits:
            SCREEN.blit(IMAGES['numbers'][digit],
                        (Xoffset, SCREENHEIGHT * 0.1))
            Xoffset += IMAGES['numbers'][digit].get_width()

    # modified from https://github.com/farizrahman4u/KerasPlaysFlappyBird
    def checkCrash(self):
        pi = self.birdIndex
        playerWidth = IMAGES['bird'][0].get_width()
        playerHeight = IMAGES['bird'][0].get_height()

        # if player crashes into ground
        if self.birdy + playerHeight >= BASEY - 1:
            return [True, True]
        else:

            playerRect = pygame.Rect(self.birdx, self.birdy,
                                     playerWidth, playerHeight)
            pipeW = IMAGES['pipe'][0].get_width()
            pipeH = IMAGES['pipe'][0].get_height()

            for uPipe, lPipe in zip(self.upperPipes, self.lowerPipes):
                # upper and lower pipe rects
                uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
                lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)

                # player and upper/lower pipe hitmasks
                pHitMask = self.HITMASKS['bird'][pi]
                uHitmask = self.HITMASKS['pipe'][0]
                lHitmask = self.HITMASKS['pipe'][1]

                # if bird collided with upipe or lpipe
                uCollide = self.pixelCollision(
                    playerRect, uPipeRect, pHitMask, uHitmask)
                lCollide = self.pixelCollision(
                    playerRect, lPipeRect, pHitMask, lHitmask)

                if uCollide or lCollide:
                    return [True, False]

        return [False, False]

    # modified from https://www.pygame.org/wiki/FastPixelPerfect
    def pixelCollision(self, rect1, rect2, hitmask1, hitmask2):
        rect = rect1.clip(rect2)

        if rect.width == 0 or rect.height == 0:
            return False

        x1 = rect.x - rect1.x
        y1 = rect.y - rect1.y
        x2 = rect.x - rect2.x
        y2 = rect.y - rect2.y

        for x in range(rect.width):
            for y in range(rect.height):
                if hitmask1[x1 + x][y1 + y] and hitmask2[x2 + x][y2 + y]:
                    return True
        return False

    # https://github.com/farizrahman4u/KerasPlaysFlappyBird
    def pixelMasks(self, image):
        mask = []
        for x in range(image.get_width()):
            mask.append([])
            for y in range(image.get_height()):
                mask[x].append(bool(image.get_at((x, y))[3]))
        return mask

    def isInBound(self, x, y):
        if (x > self.pausex and x < self.pausex + IMAGES['pause'].get_width()
            and y > self.pausey and
                y < self.pausey + IMAGES['pause'].get_height()):
            return True
