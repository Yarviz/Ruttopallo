import pygame
from pygame.math import Vector2
import image
import paper
import button
import menu
from settings import *


class Mouse(object):    # Luokka hiiren arvoille
    pos = Vector2()                 # hiiren sijainti ruudulla
    button = [0, 0, 0, 0, 0, 0]     # hiiren näppäinten arvot ylhäällä\painettuna
    grap = False                    # hiiren raahaus kun piirretään viivaa
    timer = -1                      # tuplaklikkauksen ajastin


class Keyboard(object):     # Luokka näppäimistön painalluksille
    k_space = False
    k_esc   = False


class Player(object):   # Luokka pelaajan pisteille ja palloille
    balls = 0
    points = 0
    state = 0
    hiscore = -1        # pelaajan listasijoitus nimeä kirjoittaessa
    new_game = False    # onko uutta peliä vielä aloitettu
    name = ""           # pelaajan nimi
    name_len = 0        # nimen pituus
    timer = -1          # ajastin kursorin vilkkumiselle kirjoittaessa


class Game(object):     # Pelin pääluokka
    def __init__(self, display):
        self.display = display                                  # näyttö mihin piirretään
        self.clock = pygame.time.Clock()                        # Pelikello FPS:n rajoittamiseksi
        self.atlas_pic = image.Atlas("images\images.png")       # Ladataan kuvat kuva-atlakseen
        self.mouse = Mouse()                                    # määritetään hiiri
        self.keys = Keyboard()                                  # määritetään näppäimistö
        self.mouse.pos = pygame.mouse.get_pos()
        self.game_font = pygame.font.SysFont('Arial', 20)       # pelin fontti
        self.menu_font = pygame.font.SysFont("Courier New", 30) # menun fontti
        self.zoom = 1.0                                         # määritetään paperin zoomaus (1.0 - MAX_ZOOM)
        self.board = paper.Paper(display, self.atlas_pic)       # alustetaan pelilauta
        self.player = Player()                                  # määritetään pelaaja
        self.b_menu = button.Button(display, self.menu_font, SCREEN_W - 60, 20)             # menu-näppäin pelin oikeaan yläkulmaan
        self.b_menu.set_text("MENU", Color.LIGHT_GREEN, Color.GREEN, Color.DARK_GREEN)
        self.menu = menu.Menu(display, self.atlas_pic, self.menu_font, self.game_font)
        self.player.balls, self.player.points = self.board.load_paper()         # Yritetään ladata vanhaa peliä tiedostosta, jos sitä ei löydy
        if self.player.points == -1:                                            # (funktio palauttaa arvon -1), niin käynnistetään valikko
            self.player.points = 0                                              # uuden pelin aloittamiseksi, muuten jatketaan suoraan pelilaudalta.
            self.player.new_game = True
            self.player.state = State.MENU
            self.menu.set_new_game(True)
            self.menu.set_state(State.MENU)
        self.board.update_paper()                               # päivitetään pelilauta

    def text(self, txt, x, y, color=Color.BLACK):   # funktio tekstin kirjoittamiseen ruudulle
        txt_surface = self.game_font.render(txt, False, color)
        self.display.blit(txt_surface, (x, y))
        return

    def input_name(self, key, unicode):             # funktio käyttäjän nimen kysymiseen
        if key == pygame.K_ESCAPE or key == pygame.K_RETURN:
            if self.player.name.endswith("_"):
                self.player.name = self.player.name[:-1]
            self.menu.add_hiscore(self.player.hiscore, self.player.name)
            self.player.state = State.MENU
            self.menu.set_state(State.HISCORES)
        elif key == pygame.K_BACKSPACE:
            if self.player.name_len:
                self.player.name_len -= 1
                if self.player.name.endswith("_"):
                    self.player.name = self.player.name[:-2] + "_"
                else:
                    self.player.name = self.player.name[:-1]
        elif self.player.name_len < MAX_NAME_LEN:
            if self.player.name.endswith("_"):
                self.player.name = self.player.name[:-1]
                self.player.name += unicode + "_"
            else:
                self.player.name += unicode

            self.player.name_len += 1

    def play_game(self):    # pelin pääfunktio
        running = True
        while running:                          # looppi missä peliä pyöritetään kunnes käyttäjä poistuu pelistä.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEMOTION:        # eventti hiiren liikkuessa ikkunan sisällä
                    if self.player.state == State.GAME:     # tarkistetaan ollaanko pelitilassa
                        if self.mouse.button[1]:            # siirretään pelilautaa jos vasen näppäin pohjassa
                            self.board.move_paper(self.mouse.pos - Vector2(pygame.mouse.get_pos()))
                            self.mouse.timer = -1
                        elif self.mouse.grap:               # piirretään viivaa pelilaudalle jos hiiren raahaus aktiivinen
                            self.board.move_line(self.mouse.pos)

                    self.mouse.pos = pygame.mouse.get_pos()
                    self.b_menu.mouse_move(self.mouse.pos)

                    if self.player.state == State.MENU:     # tarkistetaan onko valikko avattuna
                        self.menu.mouse_move(self.mouse.pos)

                if event.type == pygame.MOUSEBUTTONDOWN:    # eventti hiiren painalluksille
                    self.mouse.button[event.button] = 1

                    if self.mouse.button[1]:
                        self.b_menu.mouse_click(self.mouse.pos)
                        if self.player.state == State.MENU:
                            self.menu.mouse_click(self.mouse.pos)

                    if self.player.state == State.GAME:
                        if event.button == 4 and self.zoom < MAX_ZOOM:
                            self.zoom += 0.25
                            self.board.scale_objects(self.zoom)
                        if event.button == 5 and self.zoom > 1.0:
                            self.zoom -= 0.25
                            self.board.scale_objects(self.zoom)

                        if self.mouse.button[1] and self.mouse.button[3]:   # molempia nappeja painaessa, palautetaan zoomi alkutilaan ja keskitetään pelilauta
                            self.zoom = 1.0
                            self.board.scale_objects(self.zoom)
                            self.board.set_xy(Vector2(0, 0))
                            self.mouse.timer = -1
                        elif self.mouse.button[1]:
                            if self.mouse.timer == -1:
                                self.mouse.timer = 0
                            else:
                                self.mouse.timer = -1       # tuplaklikkauksella lähetetään hiiren sijainti pelilaudalle
                                self.player.balls = self.board.double_click(self.mouse.pos, self.player.balls)
                        elif self.mouse.button[3]:          # oikea klikkaus lähettää tiedon viivan piirtämisen aloittamisesta\lopettamisesta
                            value = self.board.right_click(self.mouse.pos)
                            self.mouse.grap = value[0]
                            self.player.balls += value[1]
                            self.player.points += value[2]

                if event.type == pygame.MOUSEBUTTONUP:      # eventti hiiren näppäimen vapautuessa
                    self.mouse.button[event.button] = 0
                    if event.button == 1:                   # jos kyseessä on oikea nappi, lähetetään tieto aktiivisille painikkeille ruudulla\menussa
                        if self.b_menu.mouse_release(self.mouse.pos):
                            if not self.player.new_game:
                                if self.player.state == State.GAME:
                                    self.player.state = State.MENU
                                    self.menu.set_state(State.MENU)
                                else:
                                    self.player.state = State.GAME
                                    self.menu.set_state(State.NONE)

                        if self.player.state == State.MENU:     # jos valikko on aktiivinen, tarkistetaan oliko mikään painike valittuna ruudulla
                            act = self.menu.mouse_release(self.mouse.pos)   # funktio palauttaa painikkeen arvon jos pelin pitää tehdä toimenpiteitä
                            if act == 0:
                                running = False                 # pelilooppi keskeytetään jos käyttäjä poistuu pelistä
                            elif act == 1:
                                if self.player.new_game:    # uuden pelin aloitus jos pelilauta on tyhjä
                                    self.board.set_balls()
                                    self.board.update_paper()
                                    self.player.balls = 1
                                    self.player.points = 0
                                    self.player.state = State.GAME
                                    self.player.new_game = False
                                    self.menu.set_new_game(False)
                                    self.menu.set_state(State.NONE)
                                else:                       # muuten lopetetaan peli ja tarkistetaan riittääkö pisteet ennätyslistoille
                                    self.player.hiscore = self.menu.check_hiscores(self.player.points)
                                    if self.player.hiscore > -1:
                                        self.player.state = State.HISCORES
                                        self.player.name = "_"
                                        self.player.name_len = 0
                                        self.player.timer = 0
                                    self.board.remove_board()
                                    self.board.noll_balls()
                                    self.board.update_paper()
                                    self.player.balls = 0
                                    self.player.points = 0
                                    self.player.new_game = True
                                    self.menu.set_new_game(True)
                                    self.menu.set_state(State.HISCORES)
                                    self.zoom = 1.0
                                    self.board.scale_objects(self.zoom)
                                    self.board.set_xy(Vector2(0, 0))

                if event.type == pygame.KEYDOWN:        # eventti näppäimistön painalluksille
                    if self.player.state == State.GAME:
                        if event.key == pygame.K_SPACE:     # välilyönnillä tarkistetaan löytyykö pelilaudalta mahdollista vapaata viivaa
                            if self.keys.k_space == 0:
                                self.keys.k_space = 1
                                self.board.draw_free_line(self.player.balls)
                    if event.key == pygame.K_ESCAPE and not self.player.new_game:   # Esc avaa\sulkee päävalikon jos pelitilanne on käynnissä
                        if self.player.state == State.GAME:
                            self.player.state = State.MENU
                            self.menu.set_state(State.MENU)
                        else:
                            self.player.state = State.GAME
                            self.menu.set_state(State.NONE)

                    if self.player.state == State.HISCORES:         # jos käyttäjä on kirjoittamassa nimeä listoille, lähetetään näppäimen arvo funktiolle
                        self.input_name(event.key, event.unicode)

                if event.type == pygame.KEYUP:              # eventti näppäimistön painikkeen vapautuessa
                    if self.player.state == State.GAME:
                        if event.key == pygame.K_SPACE:
                            self.keys.k_space = 0
                            self.board.update_paper()

            if self.mouse.timer > -1:           # hiiren ajastimen päivitys
                self.mouse.timer += 1
                if self.mouse.timer > FPS / 4:
                    self.mouse.timer = -1

            if self.player.timer > -1:          # käyttäjän ajastimen päivitys kursorin vilkkumiselle kirjoittaessa
                self.player.timer += 1
                if self.player.timer == FPS / 2:
                    self.player.timer = 0
                    if self.player.name.endswith("_"):
                        self.player.name = self.player.name[:-1]
                    else:
                        self.player.name = self.player.name + "_"

            self.draw_screen()                  # ruudun päivitys

        if not self.player.new_game:            # tallennetaan keskeneräinen pelitilanne pelistä poistuttaessa
            self.board.save_paper(self.player.balls, self.player.points)
        return

    def draw_screen(self):
        self.display.fill((0, 0, 0))
        self.board.draw_paper()
        self.menu.draw()
        if self.player.state == State.HISCORES:     # jos käyttäjä on kirjoittamassa nimeään listoille, piirretään se oikeaan kohtaan
            self.text(self.player.name, SCREEN_W / 2 - 155, SCREEN_H / 2 - 140 + self.player.hiscore * 25, Color.RED)
        if not self.player.new_game:
            self.b_menu.draw()
        self.text("Balls:       Points:", 15, 5, Color.RED)         # piirretään pisteet\pallot näytölle
        self.text(f"{self.player.balls}", 60, 5, Color.LIGHT_BLUE)
        self.text(f"{self.player.points}", 145, 5, Color.BROWN)

        pygame.display.flip()                       # päivitetaan ruutu kerralla näytölle ns. doublebuffering
        self.clock.tick(FPS)                        # päivitetään peliä maksimissaan FPS:n verran sekunnissa
        return
