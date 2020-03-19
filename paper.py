import pygame
from pygame.math import Vector2
from settings import *
import filehandler


class Camera(object):   # luokka kameralle
    pos = Vector2()     # kameran sijanti ruudulla
    zoom = 1.0


class Line(object):     # luokka viivaimelle
    status = False
    pos1 = [0, 0]       # viivan alku- ja loppupisteet
    pos2 = [0, 0]
    col = Color.RED     # viivan väri
    direct = -1         # viivan suunta
    old_ball = 0        # aloituspisteen pallon vanha väri
    f_status = False    # vapaan viivan tilanne
    f_check = False     # vapaan viivan tarkistamisen tilanne
    f_pos1 = [0, 0]     # vapaan viivan alku- ja loppupisteet
    f_pos2 = [0, 0]


class Paper(object):     # Pelilaudan luokka
    def __init__(self, display, atlas):
        self.display = display                                  # näyttö mihin piirretään
        self.paper = pygame.Surface((PAPER_W, PAPER_H))         # pelin paperi
        self.paper_scaled = self.paper                          # pelin paperin skaalattu versio
        self.block = atlas.load_image((0, 0, 13, 13))           # kuva paperin ruudusta
        self.ball = atlas.load_images((13, 0, 5, 5), 5)         # pallojen kuvat
        self.line_pic = [None] * 5                              # viivojen kuvat
        self.line_pic[0] = atlas.load_image((38, 0, 7, 1))
        self.line_pic[1] = atlas.load_image((46, 0, 1, 7))
        self.line_pic[2] = atlas.load_image((48, 0, 9, 9))
        self.line_pic[3] = atlas.load_image((57, 0, 9, 9))
        self.line_pic[4] = atlas.load_image((66, 0, 9, 9))
        self.camera = Camera()                                  # pelikameran alustaminen
        self.camera.pos = Vector2(0, 0)
        self.camera.zoom = 1.0
        self.file = filehandler.File()                          # tallennusolion alustaminen
        self.paper_pos = self.camera.pos - Vector2(PAPER_W / 2, PAPER_H / 2)                    # paperin sijainti ikkunan keskelle
        self.board = [[0] * ((PAPER_X_BLOCK + 1) * 2) for i in range((PAPER_Y_BLOCK + 1) * 2)]  # matriisi pelilaudalle
        self.line = Line()                                       # viivaimen alustaminen

    def noll_balls(self):   # pelilaudan nollaus
        self.board = [[0] * ((PAPER_X_BLOCK + 1) * 2) for i in range((PAPER_Y_BLOCK + 1) * 2)]
        return

    def remove_board(self):     # vanhan pelitilanteen poistaminen tiedostosta
        self.file.remove_save()
        return

    def set_balls(self):    # pelilaudan alkuasetelman määrittäminen
        self.noll_balls()
        start_points = [[0, 0], [1, 0], [1, 0], [1, 0], [0, 1], [0, 1], [0, 1], [1, 0], [1, 0], [1, 0], [0, 1], [0, 1],
                        [0, 1], [-1, 0], [-1, 0], [-1, 0], [0, 1], [0, 1], [0, 1], [-1, 0], [-1, 0], [-1, 0], [0, -1], [0, -1],
                        [0, -1], [-1, 0], [-1, 0], [-1, 0], [0, -1], [0, -1], [0, -1], [1, 0], [1, 0], [1, 0], [0, -1], [0, -1]]
        x = int(int(PAPER_X_BLOCK / 2 - 1) * 2)
        y = int(int(PAPER_Y_BLOCK / 2 - 4) * 2)
        for i in range(36):
            x += start_points[i][0] * 2
            y += start_points[i][1] * 2
            self.board[x][y] = 1
        return

    def save_paper(self, balls, points):    # pelitilanteen tallentaminen tiedostoon
        self.file.save_game(balls, points, self.board)
        return

    def load_paper(self):   # pelitilanteen lataaminen tiedostosta
        balls = 0
        points = -1         # palautetaan pisteinä -1 jos tallennusta ei löydy
        if self.file.check_file(0):
            balls, points, self.board = self.file.load_game()
        return [balls, points]

    def draw_paper(self):   # Funktiolla piirretään paperi peli-ikkunaan
        rect = pygame.Rect(self.paper_scaled.get_rect())    # Ala mikä paperista piirretään

        # Skaalataan paperi sopivan kokoiseksi zoomin perusteella
        paper_xy = Vector2(SCREEN_W / 2, SCREEN_H /2) + Vector2(self.camera.pos + self.paper_pos) * self.camera.zoom

        if paper_xy.x < 0:          # Jos ala on suurempi kuin ikkuna, niin se kutistetaan sopivan kokoiseksi
            rect.x -= paper_xy.x
            paper_xy.x = 0
        if paper_xy.y < 0:
            rect.y -= paper_xy.y
            paper_xy.y = 0
        if paper_xy.x + rect.width > SCREEN_W:
            rect.width -= (paper_xy.x + rect.width - SCREEN_W)
        if paper_xy.y + rect.height > SCREEN_H:
            rect.height -= (paper_xy.y + rect.height - SCREEN_H)

        self.display.blit(self.paper_scaled, paper_xy, rect)    # Piirretään paperi ikkunaan sopivan kokoisena
        return

    def update_paper(self):     # paperin päivitys
        self.paper.fill(Color.BLACK)
        for yy in range(PAPER_Y_BLOCK):
            for xx in range(PAPER_X_BLOCK):     # piirretään ruudukko paperille
                self.paper.blit(self.block, (xx * BLOCK_SIZE + 3, yy * BLOCK_SIZE + 3))

        x = 3
        y = 3
        line_min = [[-3, 0], [0, -3], [-4, -4], [-4, -4], [-4, -4]]     # arvot mitä lisätään jotta viivan osa piirretään oikeaan kohtaan
        for yy in range(0, (PAPER_Y_BLOCK + 1) * 2):
            for xx in range(0, (PAPER_X_BLOCK + 1) * 2):    # käydään pelilauta läpi ja piirretään pallot sekä viivat paperille
                it = self.board[xx][yy]
                if it:
                    if it < 6:  # pallojen arvot 1-5
                        self.paper.blit(self.ball[it - 1], (x - 2, y - 2))
                    else:       # viivojen arvot 6-10
                        self.paper.blit(self.line_pic[it - 6], (x + line_min[it - 6][0], y + line_min[it - 6][1]))
                x += BLOCK_SIZE / 2
            y += BLOCK_SIZE / 2
            x = 3

        if self.line.status:    # jos käyttäjä on vetämässä viivaa, niin piirretään se paperille
            pygame.draw.line(self.paper, self.line.col, Vector2(self.line.pos1[0], self.line.pos1[1]) * BLOCK_SIZE / 2 + Vector2(3, 3),
                             Vector2(self.line.pos2[0], self.line.pos2[1]) * BLOCK_SIZE / 2 + Vector2(3, 3), 1)
        self.scale_objects(self.camera.zoom)    # skaalataan paperi zoomin mukaan
        return

    def scale_objects(self, zoom):  # paperin skaalaus
        self.camera.zoom = zoom
        if SMOOTH_SCALE:            # skaalataan paperi reunoja pehmentäen
            self.paper_scaled = pygame.transform.rotozoom(self.paper, 0, zoom)
        else:                       # skaalataan paperi pikselöitynä
            self.paper_scaled = pygame.transform.scale(self.paper, (int(PAPER_W * zoom), int(PAPER_H * zoom)))
        return

    def move_paper(self, xy):       # paperin liikuttaminen hiirellä
        self.camera.pos -= xy / self.camera.zoom
        return

    def set_xy(self, xy):           # kameran sijainnin määritys
        self.camera.pos = xy
        return

    def scale_mouse(self, xy):      # hiiren sijainnin skaalaminen paperille kameran sijainnin ja zoomin mukaan
        mouse_pos_scaled = xy - Vector2(SCREEN_W / 2, SCREEN_H / 2) - Vector2(self.camera.pos + self.paper_pos) * self.camera.zoom
        mouse_pos_scaled /= (float(BLOCK_SIZE / 2) * self.camera.zoom)
        px = int(mouse_pos_scaled.x)    # hiiren sijainnin muuttaminen sijainniksi paperin ruutujen mukaan
        py = int(mouse_pos_scaled.y)

        # jos hiiren sijainti on paperin ruutujen kulmien kohdilla, palautetaan koordinaatit
        if 0 <= px <= PAPER_X_BLOCK * 2 and 0 <= py <= PAPER_Y_BLOCK * 2 and not (px % 2) and not (py % 2):
            return [px, py]
        else:
            return [-1, -1]

    def double_click(self, xy, balls):      # hiiren tuplaklikkaus paperilla
        px, py = self.scale_mouse(xy)       # hiiren sijainnin skaalaus

        if px > -1:
            if self.board[px][py] == 0 and balls:   # jos kohdassa ei ole palloa ja pallot eivät ole loppu, lisätään pallo paperille
                self.board[px][py] = 3
                self.update_paper()
                self.line.f_check = False
                return balls - 1
            elif self.board[px][py] == 3:   # jos kohdassa on pallo eikä se kuulu alkuasetelmaan tai sitä kautta ei mene viivaa, niin poistetaan pallo
                self.board[px][py] = 0
                self.update_paper()
                self.line.f_check = False
                return balls + 1

        return balls    # palautetaan lisätyt\poistetut pallot pelille

    def right_click(self, xy):  # viivan piirtämisen aloitus\lopetus
        px, py = self.scale_mouse(xy) # hiiren sijainnin skaalaus
        value = [0, 0, 0]   # palautettavat arvot [viivaa piirron aloitus\lopetus, lisäpallot, lisäpisteet]
        if px > -1:     # jos hiiri on paperin sisällä
            if 0 < self.board[px][py] < 4:  # jos hiiri on pallon kohdalla
                if not self.line.status:    # jos viiva ei ole vielä aloitettu piirtämään, niin alustetaan viiva
                    self.line.old_ball = self.board[px][py]     # tallennetaan alkuperäinen pallo
                    self.board[px][py] = 4                      # tilalle laitetaan punainen pallo
                    self.line.status = True
                    self.line.pos1[0], self.line.pos1[1] = px, py   # viivan alku- ja loppukoordinaatit pallon kohdalle
                    self.line.pos2[0], self.line.pos2[1] = px, py
                    self.update_paper()
                    value[0] = 1    # asetetaan arvo viivan piirtämisen aloittamiselle
                    return value
        if self.line.status:    # jos viivan piirtäminen on menossa
            self.board[self.line.pos1[0]][self.line.pos1[1]] = self.line.old_ball
            if self.line.direct > -1:   # jos viiva on piirretty vapaaseen kohtaan
                ax = [0, 1, 1, 1, 0, -1, -1, -1]    # arvojen lisäys koordinaatteihin viivan suunnan mukaan
                ay = [-1, -1, 0, 1, 1, 1, 0, -1]
                lin = [7, 9, 6, 8, 7, 9, 6, 8]      # viivojen kuvat mitkä määritetään jos ei piirrettä toisen viivan yli
                x = self.line.pos1[0]
                y = self.line.pos1[1]
                for i in range(9):                  # viivan piirto paperille (9 askelta, joka toinen arvo on pallo, joka toinen viivan osa)
                    if self.board[x][y] == 0:       # jos kohdassa ei ole viivaa, määritetään viivan kuva pelilaudalle
                        self.board[x][y] = lin[self.line.direct]
                    elif self.board[x][y] < 6:      # jos kohdassa on pallo, niin laitetaan sen arvoksi varattu pallo (ei voi poistaa laudalta)
                        if self.board[x][y] != 1:
                            self.board[x][y] = 2
                    else:                           # viivojen risteyksessä lisätään X-viiva
                        self.board[x][y] = 10
                    x += ax[self.line.direct]
                    y += ay[self.line.direct]
                value[1] = 1
                value[2] = 1
                self.line.f_check = False           # vapaan viivan tarkistuksen arvo nollataan

            self.line.status = False                # viivan arvo nollataan ja suunta asetetaan arvoksi -1
            self.line.direct = -1
            self.update_paper()
        return value               # palautetaan arvot pelille [viivaa piirron aloitus\lopetus, lisäpallot, lisäpisteet]

    def move_line(self, xy):        # viivan liikuttaminen paperilla hiiren koordinaattien mukaan
        px, py = self.scale_mouse(xy)   # skaalataan hiiren koordinaatit paperille

        if px > -1:     # jos koordinaatit on paperin sisällä pallon paikan kohdalla
            if self.line.pos2[0] != px or self.line.pos2[1] != py:  # jos koordinaatit ovat erit kuin viivan edelliset loppukoordinaatit,
                self.line.pos2[0], self.line.pos2[1] = px, py       # niin päivitetään viiva paperille
                self.line.col = Color.LIGHT_RED
                self.board[self.line.pos1[0]][self.line.pos1[1]] = 4
                self.line.direct = self.check_line()        # tarkistetaan onko viiva vapaassa kohdassa
                self.update_paper()
        return

    def check_line(self):   # piirrettävän viivan kohdan vapaanaolon tarkistaminen (voiko viivan piirtää pelilaudalle)
        px1, py1 = self.line.pos1[0], self.line.pos1[1]     # viivan alku- ja loppukoordinaatit muuttujiin
        px2, py2 = self.line.pos2[0], self.line.pos2[1]

        if self.board[px2][py2] == 0: return -1     # jos viivan loppukohdassa ei ole palloa, palautetaan -1
        if px1 == px2 and py1 == py2: return -1     # jos alku- ja loppukohdat ovat samat, palautetaan -1

        if abs(py1 - py2) == 0 and abs(px1 - px2) == 8:     # vaakasuoran viivan tarkistaminen
            x = px1
            y = py1
            ax = 1
            dire = Dir.RIGHT
            if px1 > px2:
                ax = -1
                dire = Dir.LEFT

            for i in range (8):     # jos viivalle on este (ei palloa välissä tai viivaa edess), palautetaan -1
                if self.board[x][y] == 0 and not(x % 2): return -1
                if self.board[x][y] > 0 and x % 2: return -1
                x += ax
            self.board[px1][py1] = 5            # jos viivan voi piirtää, asetetaan sen väri vihreäksi ja palautetaan
            self.line.col = Color.LIGHT_GREEN   # suunta mihin viivan voi piirtää alkupisteestä
            return dire

        if abs(px1 - px2) == 0 and abs(py1 - py2) == 8:     # pystysuoran viivan piirtäminen
            x = px1
            y = py1
            ay = -1
            dire = Dir.UP
            if py1 < py2:
                ay = 1
                dire = Dir.DOWN

            for i in range(8):      # jos viivalle on este (ei palloa välissä tai viivaa edess), palautetaan -1
                if self.board[x][y] == 0 and not(y % 2): return -1
                if self.board[x][y] > 0 and y % 2: return -1
                y += ay
            self.board[px1][py1] = 5
            self.line.col = Color.LIGHT_GREEN
            return dire

        if abs(py1 - py2) == 8 and abs(px1 - px2) == 8:     # poikittaisen viivan piirtäminen
            exp = [0, 8, 0, 9, 0, 8, 0, 9]
            x = px1
            y = py1
            ax = -1
            ay = -1
            dire = Dir.UP_LEFT

            if px1 < px2 and py1 > py2:
                dire = Dir.UP_RIGHT
                ax = 1
            elif px1 < px2 and py1 < py2:
                dire = Dir.DOWN_RIGHT
                ax = 1
                ay = 1
            elif px1 > px2 and py1 < py2:
                dire = Dir.DOWN_LEFT
                ay = 1

            for i in range(8):
                if self.board[x][y] == 0 and not(y % 2) and not(x % 2): return -1
                if (self.board[x][y] > 0 and not(self.board[x][y] == exp[dire])) and y % 2 and x % 2: return -1
                x += ax
                y += ay
            self.board[px1][py1] = 5
            self.line.col = Color.LIGHT_GREEN
            return dire

        return -1

    def check_free_line(self, balls):       # pelilaudan vapaana olevan viivan tarkistus
        ax = [0, 1, 1, 1, 0, -1, -1, -1]    # arvojen lisäys koordinaatteihin viivan suunnan mukaan
        ay = [-1, -1, 0, 1, 1, 1, 0, -1]
        # viivojen arvot paperilla mitkä estävät viivan piirtämisen (suunnat 0-7 Settings.Dir luokasta)
        lin = [[7, 7], [9, 10], [6, 6], [8, 10], [7, 7], [9, 10], [6, 6], [8, 10]]
        x_start = 0
        x_end = PAPER_X_BLOCK * 2
        y_start = 0
        y_end = PAPER_Y_BLOCK * 2
        self.line.f_status = False
        self.line.f_check = True
        if balls > 4:   # jos pelaajalla on yli neljä palloa, asetetaan arvoksi neljä (tämä riittää aina viivan piirtämiseen pelilaudalle)
            balls = 4

        # käydään pelilauta läpi ja etsitään ensimmäinen vapaa viivan kohta aloittaen oletuksesta että palloja on nolla
        # ts. etsitään ensin vapaita viiden pallon sarjoja ja jos ei löydy, niin lisätään mahdollisia palloja jos pelaajalla niitä on.
        for ball in range(0, balls + 1):
            for y in range(y_start, y_end, 2):
                for x in range(x_start, x_end, 2):
                    if 0 < self.board[x][y] < 4:
                        for i in range(8):
                            xx = x
                            yy = y
                            ext = ball
                            self.line.f_pos1[0] = int(xx)
                            self.line.f_pos1[1] = int(yy)
                            for i2 in range(8):
                                xx += ax[i]
                                yy += ay[i]
                                if xx < 0 or xx >= PAPER_X_BLOCK * 2 or yy < 0 or yy >= PAPER_Y_BLOCK * 2:
                                    ext = -1
                                    break
                                if self.board[xx][yy] == lin[i][0] or self.board[xx][yy] == lin[i][1]:
                                    ext = -1
                                    break
                                if not(xx % 2) and not(yy % 2) and self.board[xx][yy] == 0:
                                    if ext:
                                        ext -= 1
                                    else:
                                        ext = -1
                                        break
                            # ensimmäisen mahdollisen vapaan kohdan löytyessä, lopetetaan etsintä ja alustetaan vapaan
                            # viivan arvot mikä piirretään kun välilyönti on painettuna pohjaan.
                            if ext > -1:
                                self.line.f_status = True
                                self.line.f_pos2[0] = int(xx)
                                self.line.f_pos2[1] = int(yy)
                                return True

        return False    # jos vapaata viivaa ei löydy, palautetaan arvo False

    def draw_free_line(self, balls):    # vapaan viivan piirtäminen kartalle välilyöntiä painaessa
        if not self.line.f_check:       # jos vapaata viivaa ei ole yritetty etsiä, niin etsiminen suoritetaan
            self.check_free_line(balls)
        if self.line.f_status:          # jos pelilaudalla on mahdollinen vapaa viiva, niin se piirretään
            pygame.draw.line(self.paper, Color.GREEN,
                             Vector2(self.line.f_pos1[0], self.line.f_pos1[1]) * BLOCK_SIZE / 2 + Vector2(3, 3),
                             Vector2(self.line.f_pos2[0], self.line.f_pos2[1]) * BLOCK_SIZE / 2 + Vector2(3, 3), 1)
            self.scale_objects(self.camera.zoom)  # skaalataan paperi zoomin mukaan
        return
