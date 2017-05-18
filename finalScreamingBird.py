from pygame.locals import *
import pygame
from constants import *
from intro import Intro
from game import Game
from gameOver import GameOver
from highScore import HighScore
from settings import Setting


class ScreamingBird(object):

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        pygame.display.set_caption('Screaming Bird')
        self.pipegap = 120
        self.intro = Intro(self.screen)
        self.highScore = HighScore(self.screen)
        self.settings = Setting(self.screen)

    def run(self):
        playing = True
        mode = 'intro'
        count = 0
        while playing:
            # print(self.pipegap)
            if mode == 'intro' or mode[0] == 'intro':
                if count > 0:
                    self.__init__()
                if mode != 'intro':
                    print(mode[1])
                    self.pipegap = mode[1]
                mode = self.intro.run()
            elif mode == 'game':
                self.game = Game(self.screen, self.pipegap)
                print(self.pipegap)
                mode = self.game.run()
            elif mode == 'highscore':
                mode = self.highScore.run()
            elif mode[0] == 'gameover':
                count += 1
                self.scoreAppend = True
                self.gameOver = GameOver(self.screen, mode[1])
                mode = self.gameOver.run()
            elif mode == 'settings':
                mode = self.settings.run()
            elif mode == 'quit':
                playing = False
        pygame.quit()

if __name__ == "__main__":
    game = ScreamingBird()
    game.run()
