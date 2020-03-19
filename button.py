import pygame
from pygame.math import Vector2
from settings import *


class Button(object):       # luokka hiirellä painettavalle napille
    def __init__(self, display, font, x, y):
        self.display = display      # alusta mihin piirretään
        self.font = font            # napin fontti
        self.pos = Vector2(x, y)    # napin sijainti
        self.rect = None            # napin koko ruudulla
        self.image = [None, None, None]     # napin kuvat [vapaana, aktiivisena, painettuna]
        self.state = -1             # napin aktiivisuustila
        self.click = False          # nappi painettuna\ei painettuna

    def set_text(self, text, col1 = Color.LIGHT_RED, col2 = Color.RED, col3 = Color.DARK_RED): # tekstin lisääminen napille
        self.image[0] = self.font.render(text, False, col1)
        self.image[1] = self.font.render(text, False, col2)
        self.image[2] = self.font.render(text, False, col3)
        self.rect = pygame.Rect(self.pos.x - self.image[0].get_width() / 2, self.pos.y - self.image[0].get_height() / 2,
                                self.image[0].get_width(), self.image[0].get_height())
        self.state = 0
        return

    def set_image(self, image):     # kuvien lisääminen napille
        self.image[0] = image[0]
        self.image[1] = image[1]
        self.image[2] = image[2]
        self.rect = pygame.Rect(self.pos.x - self.image[0].get_width() / 2, self.pos.y - self.image[0].get_height() / 2,
                                self.image[0].get_width(), self.image[0].get_height())
        self.state = 0
        return

    def set_state(self, state):     # napin tilan muutaminen
        self.state = state
        return

    def check_mouse(self, xy):      # hiiren sijainnin tarkistus napin alueella
        return self.rect.collidepoint(Vector2(xy))

    def mouse_move(self, xy):       # hiiren sijainnin tarkistus napin alueella liikuttaessa
        if self.check_mouse(xy):
            if self.click:
                self.state = 2
            else:
                self.state = 1
            return
        self.state = 0
        return

    def mouse_click(self, xy):      # hiiren sijainnin tarkistus napin alueella klikattaessa
        if self.state:
            self.state = 2
            self.click = True
        return self.state

    def mouse_release(self, xy):    # hiiren sijainnin tarkistus napin alueella hiiren napin vapautuessa
        if self.state == 2 and self.click:
            self.state = 1
            self.click = False
            return True
        self.click = False
        return False

    def draw(self):                 # napin piirto ruudulle jos aktiivinen
        if self.state == -1:
            return
        self.display.blit(self.image[self.state], self.rect)
        return
