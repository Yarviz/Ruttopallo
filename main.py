"""
        Ruttopallo by Jussi Laitala

    Pelin ideana on löytää pelilaudalta mahdollisimman monta viiden pallon sarjaa ja vetää viivoja niiden väliin. Jokaisesta
    viivasta pelaaja saa yhden pisteen ja pallon ja peli päättyy kun vapaita paikkoja ei enää löydy mihin viivan voi vetää.
    pelitilanne tallennetaan kun pelistä poistuu ja peli jatkuu tästä tilanteesta uudelleen käynnistäessä. Pelissä on käytetty
    pygamen kirjastoja (https://www.pygame.org) ja tämä moduuli pitäisi olla asennettuna koneelle jotta ohjelman voi suorittaa.

    Pelin lähdekoodi on vapaasti muokattavissa, jaettavissa ja kopioitavissa.

    versio 1.0
"""

import pygame
import game
import os
from settings import *

pygame.init()                                              # alustetaan pygame kirjastot
pygame.font.init()                                         # Alustetaan fontit
os.environ['SDL_VIDEO_CENTERED'] = '1'                     # asetetaan peli-ikkuna näytön keskelle
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))     # alustetaan ikkuna pelille
pygame.display.set_caption("Ruttopallo")                   # määritetään nimi peli-ikkunalle
game_image = pygame.image.load("images/ruttopallo.png")
pygame.display.set_icon(game_image)                        # ladataan pelin ikoni ikkunalle

game = game.Game(screen)        # uusi olio pelille
game.play_game()                # suoritetaan peli

pygame.display.quit()           # lopetetaan peli-ikkuna
