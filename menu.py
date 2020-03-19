import pygame
from pygame.math import Vector2
from settings import *
import button
import random
import filehandler


class Menu(object):         # olio päävalikolle
    def __init__(self, display, atlas, font_big, font_small):
        self.display = display
        self.atlas = atlas                      # kuva-atlas mistä kuvat otetaan
        self.font = [font_big, font_small]      # menussa käytetään kahta eri fonttia
        self.border = atlas.load_images((0, 13, 12, 12), 9)     # taustapaperin osien kuvat
        self.paper = None                       # taustapaperi
        self.pos = Vector2()
        self.button = [None] * 5                # valikon painikkeet
        self.flag = [None] * 3                  # kielen valitsemisen painikkeen kuvat
        self.buttons = 0
        self.language = FINNISH                 # oletuskielenä suomi
        self.state = State.NONE
        random.seed()
        self.file = filehandler.File()          # tallennusolion märittäminen
        self.new_game = False
        self.hiscores = []                      # ennätyslista
        if self.file.check_file(1):             # jos ennätyksiä ei löydy tiedostosta, määritetään oletuslista
            self.hiscores = self.file.load_hiscores()
            self.hiscores = sorted(self.hiscores, key=lambda i: i["points"], reverse=True)  # järjestetään lista pistejärjestykseen
        else:
            self.noll_hiscores()

    def noll_hiscores(self):    # ennätyslistan määrittäminen oletuksena
        names = ["Reiska", "Kaarlo", "Ilpo", "Matti", "Ernesti", "Tarmo", "Kalle"]
        for i in range(len(names)):
            self.hiscores.append({"name": names[i], "points": random.randint(5,50)})

        self.hiscores = sorted(self.hiscores, key=lambda i: i["points"], reverse=True)  # järjestetään lista pistejärjestykseen
        return

    def check_hiscores(self, points):   # tarkistetaan oikeuttaako pistemäärä ennätyslistalle pääsyyn
        if not points:  # jos pisteet = 0, pelaaja ei pääse listalle ja palautetaan arvo -1
            return -1
        for i in range(len(self.hiscores)):
            if points > self.hiscores[i]["points"]:     # lisätään pelaaja oikeaan kohtaan listalla jos pisteet riittävät
                self.hiscores.insert(i, {"name": "", "points": points})
                if len(self.hiscores) > MAX_HISCORES:
                    del self.hiscores[-1]
                return i    # palautetaan pelaajan sijainti listalla jos pisteet riittivät
        i += 1
        if i < MAX_HISCORES:        # jos lista ei ole täynnä, lisätään pelaaja listan loppuun
            self.hiscores.append({"name": "", "points": points})
            return i
        return -1   # palautetaan -1 jos pisteet eivät riitä listalle

    def add_hiscore(self, pos, name):   # lisätään pelaajan antama nimi listalle
        self.hiscores[pos]["name"] = name
        return

    def set_paper(self, width, height):     # tehdään taustapaperi valikon pohjaksi
        self.paper = pygame.Surface((width * M_BLOCK_SIZE, height * M_BLOCK_SIZE)).convert()
        self.paper.fill(Color.PINK)
        self.paper.set_colorkey(Color.PINK)     # määritetään väri mitä ei piirretä näytölle kuvaa renderoidessa
        self.paper.set_alpha(240)               # tehdään paperista hieman läpinäkyvä

        for y in range(1, height - 1):
            for x in range(1, width - 1):
                self.paper.blit(self.border[8], (x * M_BLOCK_SIZE, y * M_BLOCK_SIZE))
        for x in range(1, width - 1):
            self.paper.blit(self.border[4], (x * M_BLOCK_SIZE, 0))
            self.paper.blit(self.border[6], (x * M_BLOCK_SIZE, (height - 1) * M_BLOCK_SIZE))
        for y in range(1, height - 1):
            self.paper.blit(self.border[7], (0, y * M_BLOCK_SIZE))
            self.paper.blit(self.border[5], ((width - 1) * M_BLOCK_SIZE, y * M_BLOCK_SIZE))
        self.paper.blit(self.border[0], (0, 0))
        self.paper.blit(self.border[1], ((width - 1) * M_BLOCK_SIZE, 0))
        self.paper.blit(self.border[2], ((width - 1) * M_BLOCK_SIZE, (height - 1) * M_BLOCK_SIZE))
        self.paper.blit(self.border[3], (0, (height - 1) * M_BLOCK_SIZE))

        # venytetään taustapaperi kaksinkertaiseksi
        self.paper = pygame.transform.scale(self.paper, (self.paper.get_width() * 2, self.paper.get_height() * 2))
        self.pos = Vector2(SCREEN_W / 2 - self.paper.get_width() / 2, SCREEN_H / 2 - self.paper.get_height() /2)
        return

    def text(self, txt, x, y, color=Color.BLACK, middle=0, fnt=0):  # funktio tekstin piirtämiselle
        txt_surface = self.font[fnt].render(txt, False, color)
        if middle == 1:     # tekstin sijoittaminen keskelle
            x -= txt_surface.get_width() / 2
            y -= txt_surface.get_height() / 2
        elif middle == 2:   # tekstin sijoittaminen oikeaan reunaan
            x -= txt_surface.get_width()
        self.paper.blit(txt_surface, (x, y))
        return

    def set_new_game(self, state):  # uuden pelin aloitus
        self.new_game = state
        return

    def set_state(self, state):     # valikon tilan määrittäminen
        self.state = state
        if self.state == -1:
            return

        cw_scr = SCREEN_W / 2       # muuttujat näytön keskikohdille
        ch_scr = SCREEN_H / 2

        if self.state == State.MENU:    # päävalikkon avaaminen
            self.set_paper(12, 12)      # määritetään taustapaperi
            cw_pap = self.paper.get_width() / 2     # muuttujat taustapaperin keskikohdille
            ch_pap = self.paper.get_height() / 2
            self.buttons = 5

            # paperin tekstien ja nappien määrittäminen käytössä olevan kielen mukaan
            if self.language == FINNISH:
                self.text("RUTTOPALLO", cw_pap, ch_pap - 100, Color.DARK_BLUE, 1)
                but_text = ["Kekeytä Peli", "Ennätykset", "Ohjeet", "Lopeta"]
                if self.new_game:
                    but_text[0] = "Uusi Peli"
                self.flag = self.atlas.load_images((0, 25, 25, 15), 3)
                self.button[0] = button.Button(self.display, self.font[0], cw_scr - 115, ch_scr - 120)
                self.button[0].set_image(self.flag)     # alustetaan nappi englannin lipun kuvalla
            else:
                self.text("PLAGUEBALL", cw_pap, ch_pap - 100, Color.DARK_BLUE, 1)
                but_text = ["End Game", "Hiscores", "Instructions", "Quit"]
                if self.new_game:
                    but_text[0] = "New Game"
                self.flag = self.atlas.load_images((0, 40, 25, 15), 3)
                self.button[0] = button.Button(self.display, self.font[0], cw_scr - 115, ch_scr - 120)
                self.button[0].set_image(self.flag)     # alustetaan nappi suomen lipun kuvalla
            for i in range(1, 5):
                self.button[i] = button.Button(self.display, self.font[0], cw_scr, ch_scr - (4 * 40 / 2) + i * 40)
                self.button[i].set_text(but_text[i - 1])

        if self.state == State.INFO:    # ohjevalikon avaaminen
            self.set_paper(22, 18)
            cw_pap = self.paper.get_width() / 2
            ch_pap = self.paper.get_width()
            self.buttons = 1
            # paperin tekstien ja nappien määrittäminen käytössä olevan kielen mukaan
            if self.language == FINNISH:
                self.text("Pelin tavoitteena on löytää viiden pallon sarjoja vaakasuunnassa,", cw_pap, 25, Color.LIGHT_BLUE, 1, 1)
                self.text("pystysuunnassa tai vinottain ja vetää viivoja niiden väliin. Jokaisesta", cw_pap, 50, Color.LIGHT_BLUE, 1, 1)
                self.text("viivasta saa uuden pallon ja yhden pisteen. Peli päättyy kunnes", cw_pap, 75, Color.LIGHT_BLUE, 1, 1)
                self.text("kaikki pallot on käytetty eikä uusia viivoja voi enää vetää. Pelitilanne", cw_pap, 100, Color.LIGHT_BLUE, 1, 1)
                self.text("tallentuu kun ohjelma lopetetaan ja jatkuu uudelleen käynnistäessä.", cw_pap, 125,Color.LIGHT_BLUE, 1, 1)
                self.text("Pelin Ohjaimet", cw_pap, 175, Color.WHITE, 1, 1)

                cy = 200
                self.text("Vasen Tuplaklikkaus", 15, cy, Color.DARK_BROWN, 0, 1)
                self.text("Oikea Klikkaus", 15, cy + 25, Color.DARK_BROWN, 0, 1)
                self.text("Riiren Rulla", 15, cy + 50, Color.DARK_BROWN, 0, 1)
                self.text("Riiren Raahaus", 15, cy + 75, Color.DARK_BROWN, 0, 1)
                self.text("Molempien Nappien Klikkaus", 15, cy + 100, Color.DARK_BROWN, 0, 1)
                self.text("Välilyönti", 15, cy + 125, Color.DARK_BROWN, 0, 1)
                self.text("Esc", 15, cy + 150, Color.DARK_BROWN, 0, 1)

                self.text("Piirrä/Poista Pallo", ch_pap - 15, cy, Color.BROWN, 2, 1)
                self.text("Piirrä Viiva", ch_pap - 15, cy + 25, Color.BROWN, 2, 1)
                self.text("Zoomaa Paperia", ch_pap - 15, cy + 50, Color.BROWN, 2, 1)
                self.text("Liikuta Paperia", ch_pap - 15, cy + 75, Color.BROWN, 2, 1)
                self.text("Palauta Zoom", ch_pap - 15, cy + 100, Color.BROWN, 2, 1)
                self.text("Etsi Vapaa Viiva", ch_pap - 15, cy + 125, Color.BROWN, 2, 1)
                self.text("Avaa/Sulje Valikko", ch_pap - 15, cy + 150, Color.BROWN, 2, 1)

                but_text = "Takaisin"
            else:
                self.text("The goal of the game is to find rows of five balls in horizontal,", cw_pap, 25, Color.LIGHT_BLUE, 1, 1)
                self.text("vertical or diagonal position and draw lines between them. Every", cw_pap, 50, Color.LIGHT_BLUE, 1, 1)
                self.text("line grants a new ball and a one point. Game ends when every ball", cw_pap, 75, Color.LIGHT_BLUE, 1, 1)
                self.text("is used and new lines can't draw anymore. Current game is saved", cw_pap, 100, Color.LIGHT_BLUE, 1, 1)
                self.text("when program ends and continues when it starts again.", cw_pap, 125, Color.LIGHT_BLUE, 1, 1)
                self.text("Game Controls", cw_pap, 175, Color.WHITE, 1, 1)

                cy = 200
                self.text("Left Doubleclick", 15, cy, Color.DARK_BROWN, 0, 1)
                self.text("Right Click", 15, cy + 25, Color.DARK_BROWN, 0, 1)
                self.text("Mouse Wheel", 15, cy + 50, Color.DARK_BROWN, 0, 1)
                self.text("Mouse Drag", 15, cy + 75, Color.DARK_BROWN, 0, 1)
                self.text("Both Buttons Click", 15, cy + 100, Color.DARK_BROWN, 0, 1)
                self.text("Space", 15, cy + 125, Color.DARK_BROWN, 0, 1)
                self.text("Esc", 15, cy + 150, Color.DARK_BROWN, 0, 1)

                self.text("Draw/Erase Ball", ch_pap - 15, cy, Color.BROWN, 2, 1)
                self.text("Draw Line", ch_pap - 15, cy + 25, Color.BROWN, 2, 1)
                self.text("Zoom Paper", ch_pap - 15, cy + 50, Color.BROWN, 2, 1)
                self.text("Move Paper", ch_pap - 15, cy + 75, Color.BROWN, 2, 1)
                self.text("Reset Zoom", ch_pap - 15, cy + 100, Color.BROWN, 2, 1)
                self.text("Find Free Line", ch_pap - 15, cy + 125, Color.BROWN, 2, 1)
                self.text("Open/Close Menu", ch_pap - 15, cy + 150, Color.BROWN, 2, 1)

                but_text = "Back"
            self.button[0] = button.Button(self.display, self.font[0], cw_scr, ch_scr + 180)
            self.button[0].set_text(but_text)

        if self.state == State.HISCORES:    # ennätyslistan avaaminen valikossa
            self.set_paper(15, 20)
            cw_pap = self.paper.get_width() / 2
            ch_pap = self.paper.get_width()
            self.buttons = 1
            # paperin tekstien ja nappien määrittäminen käytössä olevan kielen mukaan
            if self.language == FINNISH:
                self.text("Ennätykset", cw_pap, 50, Color.DARK_BLUE, 1, 0)
                but_text = "Takaisin"
            else:
                self.text("Hiscores", cw_pap, 50, Color.DARK_BLUE, 1, 0)
                but_text = "Back"

            for i in range(len(self.hiscores)):
                self.text(self.hiscores[i]["name"], 25, 100 + i * 25, Color.LIGHT_BLUE, 0, 1)
                self.text(str(self.hiscores[i]["points"]), ch_pap - 25, 100 + i * 25, Color.DARK_BROWN, 2, 1)
            self.button[0] = button.Button(self.display, self.font[0], cw_scr, ch_scr + 200)
            self.button[0].set_text(but_text)

        return

    def mouse_move(self, xy):           # hiiren liikkumisen välittäminen valikon napeille
        for i in range(self.buttons):
            self.button[i].mouse_move(xy)
        return

    def mouse_click(self, xy):          # hiiren napin klikkaamisen välittäminen valikon napeille
        for i in range(self.buttons):
            self.button[i].mouse_click(xy)
        return

    def mouse_release(self, xy):        # hiiren napin vapauttamisen välittäminen valikon napeille
        but = -1
        act = -1
        for i in range(self.buttons):
            if self.button[i].mouse_release(xy):
                but = i
        if self.state == State.MENU:
            if but == 0:    # valikon kieliasetuksen vaihtaminen
                self.language = (self.language + 1) % 2
                self.set_state(State.MENU)
                self.mouse_move(xy)
            elif but == 1:
                act = 1
            elif but == 2:
                self.set_state(State.HISCORES)
            elif but == 3:
                self.set_state(State.INFO)
            elif but == 4:
                act = 0

        if self.state == State.INFO or self.state == State.HISCORES:
            if but == 0:
                if self.state == State.HISCORES:    # ennätyslista tallennetaan levylle kun valikko suljetaan
                    self.file.save_hiscores(self.hiscores)
                self.set_state(State.MENU)

        return act      # palautetaan mahdollinen arvo mistä peli voi tehdä omat toimintansa

    def draw(self):     # valikon ja nappien piirto jos valikko on avattuna
        if self.state > State.NONE:
            self.display.blit(self.paper, self.pos)
            for i in range(self.buttons):
                self.button[i].draw()
        return
