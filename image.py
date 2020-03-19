import pygame
import sys


class Atlas(object):    # luokka kuva-atlakselle
    def __init__(self, filename):
        try:    # tarkistetaan voiko kuvaa ladata
            self.sheet = pygame.image.load(filename).convert()
        except FileNotFoundError:   # jos kuvaa ei löydy, lopetetaan ohjelma
            print("Ei voi avata tiedostoa!")
            sys.exit()

    def load_image(self, rectangle):    # yksittäisen kuvan lataaminen kuva-atlaksesta
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        image.set_colorkey((255,0,255), pygame.RLEACCEL)    # määritetään väri mitä ei piirretä kuvaa renderoidessa
        return image

    def load_images(self, rectangle, num):  # usean kuvan lataaminen kuva-atlaksesta
        rect = pygame.Rect(rectangle)
        return [self.load_image((rect[0] + rect[2] * i, rect[1], rect[2], rect[3])) for i in range(num)]
