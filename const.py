import enum
from pygame.locals import *

GAME_TITLE = "是男人就打十分钟"
GAME_VERSION = "v0.1.6"

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 700
FPS = 60

FLY_SPEED = 8
SMALL_ENEMY_SPEED = 5
BULLET_NUM = 20
BULLET_DELAY = 60
BULLET_SOUND_DELAY = 120

class GAME_STATUS(enum.Enum):
    START = 0
    STOP = 1
    SHOW_QR = 2

INCREASE_DIFFICULTY = USEREVENT
DOUBLE_BULLET = USEREVENT + 1
RESTART_GAME = USEREVENT + 2
FIVE_BULLET = USEREVENT + 3
SEVEN_BULLET = USEREVENT +4
ADD_BULLET_SPEED = USEREVENT + 5
ADD_BULLET_DAMAGE = USEREVENT + 6
ADD_BIG_ENEMY = USEREVENT + 7

INCREASE_DIFFICULTY_TIME = 1000 * 5
DOUBLE_BULLET_TIME = 1000*30
FIVE_BULLET_TIME = 1000*60
SEVEN_BULLET_TIME = 1000*90
ADD_BULLET_SPEED_TIME = 1000*120
ADD_BULLET_DAMAGE_TIME = 1000*150
ADD_BULLET_DAMAGE_LOOP_TIME = 1000*30
ADD_BIG_ENEMY_TIME = 1000*60*6
ADD_BIG_ENEMY_LOOP_TIME = 1000*60*4

SMALL_ENEMY_NUM = 10
SMALL_ENEMY_HP = 1
SMALL_ENEMY_SPEED = 5

SUPPLY_SPEED = 4

MID_ENEMY_NUM = 3
MID_ENEMY_HP = 15
MID_ENEMY_SPEED = 3

BIG_ENEMY_NUM = 1
BIG_ENEMY_HP = 60
BIG_ENEMY_SPEED = 2


IMAGE_PATH = {
    'background' : 'images/background.png',
    'player' : ['images/me1.png', 'images/me2.png'],
    'player_destroy' : ['images/me_destroy_1.png', 'images/me_destroy_2.png', 'images/me_destroy_3.png', 'images/me_destroy_4.png'],
    'enemy_small' : ['images/enemy1.png'],
    'enemy_small_destroy' : ['images/enemy1_down1.png', 'images/enemy1_down2.png', 'images/enemy1_down3.png', 'images/enemy1_down4.png'],
    'enemy_mid' : ['images/enemy2.png'],
    'enemy_mid_destroy' : ['images/enemy2_down1.png', 'images/enemy2_down2.png', 'images/enemy2_down3.png', 'images/enemy2_down4.png'],
    'enemy_mid_hit' : 'images/enemy2_hit.png',
    'enemy_big' : ['images/enemy3_n1.png', 'images/enemy3_n2.png'],
    'enemy_big_destroy' : ['images/enemy3_down1.png', 'images/enemy3_down2.png', 'images/enemy3_down3.png', 'images/enemy3_down4.png', 'images/enemy3_down5.png', 'images/enemy3_down6.png'],
    'enemy_big_hit' : 'images/enemy3_hit.png',
    'bullet_red' : 'images/bullet1.png',
    'bullet_blue' : 'images/bullet2.png'
}
FONT_PATH = {
    'font_1' : 'font/font.ttf'
}