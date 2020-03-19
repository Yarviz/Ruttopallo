import pickle
import os.path
import json
from settings import *


class File(object):     # olio pelitilanteen ja ennätysten tallentamisee\lataamiseen
    def __init__(self):
        self.file_name = ["game.sav", "hiscores.txt"]   # tiedostojen nimet

    def check_file(self, file):     # tarkistetaan löytyykö tiedostoa levyltä
        if not SAVE_GAME:
            return False
        if os.path.isfile(self.file_name[file]):
            return True
        else:
            return False

    def remove_save(self):          # pelitallennuksen poisto levyltä
        if self.check_file(0):
            os.remove(self.file_name[0])
        return

    def save_game(self, balls, points, board):  # pelitilanteen tallentaminen levylle
        if not SAVE_GAME:
            return
        file = open(self.file_name[0], "wb")    # avataan tiedosto binäärisessä muodossa tallentamista varten
        pickle.dump(balls, file)                # tallennetaan ensin pallot ja pisteet
        pickle.dump(points, file)
        num = board[0][0]
        count = 0
        for y in range(0, (PAPER_Y_BLOCK + 1) * 2):         # pakataan pelilautaa pienempään tilaan tiedoston sisälle
            for x in range(0, (PAPER_X_BLOCK + 1) * 2):     # jos pelilaudalla toistuu monta kertaa sama arvo esim 0, tallennetaan
                if board[x][y] == num:                      # ensin kappalemäärä ja sitten arvo. Näin se ei vie tilaa kuin kahden
                    count += 1                              # arvon verran tiedostossa, eikä samaa arvoa kirjoiteta kymmeniä kertoja peräkkäin.
                else:
                    if count == 1:
                        pickle.dump(num, file)
                    else:
                        count += 10
                        pickle.dump(count, file)
                        pickle.dump(num, file)
                    num = board[x][y]
                    count = 1
        if count == 1:
            pickle.dump(num, file)
        else:
            count += 10
            pickle.dump(count, file)
            pickle.dump(num, file)
        file.close()                             # suljetaan lopuksi tiedosto
        return

    def load_game(self):        # pelitilanteen lataaminen levyltä
        if self.check_file(0):
            file = open(self.file_name[0], "rb")    # avataan tiedosto binäärisenä lukemista varten
            balls = pickle.load(file)               # ladataan ensin pallot\pisteet
            points = pickle.load(file)
            board = [[0] * ((PAPER_X_BLOCK + 1) * 2) for i in range((PAPER_Y_BLOCK + 1) * 2)]   # määritetään tyhjä pelilauta
            num = 0
            count = 0
            for y in range(0, (PAPER_Y_BLOCK + 1) * 2):
                for x in range(0, (PAPER_X_BLOCK + 1) * 2):     # puretaan pakattu tiedosto ja tallennetaan se pelilaudalle
                    if count == 0:
                        count = pickle.load(file)
                        if count < 11:
                            board[x][y] = count
                            count = 0
                        else:
                            num = pickle.load(file)
                            count -= 10
                    if count:
                        board[x][y] = num
                        count -= 1
            file.close()                # suljetaan tiedosto lopuksi
            return [balls, points, board]       # palautetaan pallot, pisteet ja pelilauta
        return -1

    def save_hiscores(self, hiscore):   # ennätysten tallentaminen levylle
        file = open(self.file_name[1], "w")     # avaataan tiedosto tekstitilassa kirjoittamista varten
        for i in range(len(hiscore)):
            file.write(json.dumps(hiscore[i]) + "\n")   # tallennetaan ennätyslista riveittäin JSON-muodossa
        file.close()
        return

    def load_hiscores(self):        # ennätysten lataaminen levyltä
        if self.check_file(1):
            hiscore = []            # tehdään tyhjä lista ennätyksille
            file = open(self.file_name[1], "r") # avataan tiedosto tekstimuodossa lukemista varten
            lines = file.readlines()    # luetaan tiedosto rivi kerrallaan
            count = 0
            for i in lines:
                i = i.replace("\n", "")     # poistetaan rivinvaihdon merkit
                hiscore.append(json.loads(i))   # käännetään rivi pois JSON-muodosta normaaliin listamuotoon
                count += 1
                if count == MAX_HISCORES:   # luetaan vain maksimimäärä rivejä
                    break
            file.close()    # lopuksi suljetaan tiedosto ja palautetaan ennätyslista
            return hiscore
        return -1
