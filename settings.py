# luokka väreille
class Color:
    BLACK       = (0, 0, 0)
    WHITE       = (255, 255, 255)
    GREEN       = (0, 150, 0)
    LIGHT_GREEN = (0, 200, 0)
    DARK_GREEN  = (0, 100, 0)
    RED         = (200, 0, 0)
    LIGHT_RED   = (255, 0, 0)
    DARK_RED    = (100, 0, 0)
    BLUE        = (0, 50, 255)
    LIGHT_BLUE  = (0, 100, 255)
    DARK_BLUE   = (0, 0, 255)
    BROWN       = (130, 100, 0)
    DARK_BROWN  = (100, 70, 0)
    PINK        = (255, 0, 255)


# suuntien arvot viivojen pirtämiseen paperille
class Dir:
    UP          = 0
    UP_RIGHT    = 1
    RIGHT       = 2
    DOWN_RIGHT  = 3
    DOWN        = 4
    DOWN_LEFT   = 5
    LEFT        = 6
    UP_LEFT     = 7


# aktiivisten tilojen vakioita
class State:
    NONE            = -1
    GAME            = 0
    MENU            = 1
    INFO            = 2
    HISCORES        = 3


# pelin keskeiset vakiot
SCREEN_W = 800              # peli-ikkunan koko
SCREEN_H = 800
BLOCK_SIZE = 12             # paperin yhden ruudukon koko pikseleinä
M_BLOCK_SIZE = 12           # menun taustan palasten koko
PAPER_X_BLOCK = 51          # paperin ruudukkojen määrä
PAPER_Y_BLOCK = 51
PAPER_W = PAPER_X_BLOCK * BLOCK_SIZE + 8    # paperin koko
PAPER_H = PAPER_Y_BLOCK * BLOCK_SIZE + 8
MAX_ZOOM = 3.0              # maksimi zoom
FPS = 60                    # framejen määrä sekunnissa
SMOOTH_SCALE = False        # pehmeä skaalaus zoomatessa
FINNISH = 0                 # valikon kielen vakiot
ENGLISH = 1
MAX_HISCORES = 12           # ennätysten maksimimäärä
MAX_NAME_LEN = 25           # ennätyslistan maksimipituus nimelle
SAVE_GAME = True            # pelitilanteen tallennus lopettaessa
