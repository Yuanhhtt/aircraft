import pygame
from const import *

#游戏背景
class BGSprite(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, postion : tuple, speed = FLY_SPEED) -> None:
        super().__init__(group)
        self.image = pygame.image.load(IMAGE_PATH["background"])
        self.rect = self.image.get_rect()
        self.rect.topleft = postion
        self.speed = speed
    
    def add_speed(self):
        self.speed += 5

    def update(self) -> None:
        self.rect.top += self.speed
        if self.rect.top >= SCREEN_HEIGHT:
            self.rect.top = -SCREEN_HEIGHT
        return super().update()


#游戏计时器
class GameTimer(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group) -> None:
        super().__init__(group)
        self.font = pygame.font.Font("font/simkai.ttf", 20)
        self.start_time = 0
        self.end_time = 0
        self.image = self.font.render("%02d:%02d:%02d.%03d" % (0, 0, 0, 0), True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.working = False
    
    def start(self) -> None:
        self.working = True
        self.start_time = pygame.time.get_ticks()
    
    def stop(self) -> None:
        self.working = False
        self.end_time = pygame.time.get_ticks()
    
    def duration(self) -> int:
        return self.end_time - self.start_time

    def update(self) -> None:
        if self.working:
            self.end_time = pygame.time.get_ticks()
        ticks = self.duration()
        seconds = ticks // 1000 % 60
        minutes = ticks // 60000 % 60
        hours = ticks // 3600000
        self.image = self.font.render("%02d:%02d:%02d.%03d" % (hours, minutes, seconds, ticks % 1000), True, (255, 255, 255))

#游戏得分
class GameScore(pygame.sprite.Sprite):
    def __init__(self,  group: pygame.sprite.Group) -> None:
        super().__init__(group)
        self.score = 0
        self.font = pygame.font.Font("font/simkai.ttf", 20)
        self.image = self.font.render("得分:%d" % (self.score), True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.midtop = (SCREEN_WIDTH / 2, 0)
    
    def add_score(self, score:int):
        self.score += score
    
    def restart(self):
        self.score = 0
    
    def update(self) -> None:
        self.image = self.font.render("得分:%d" % (self.score), True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.midtop = (SCREEN_WIDTH / 2, 0)

#游戏用户名
class GameUser(pygame.sprite.Sprite):
    def __init__(self,  group: pygame.sprite.Group, username) -> None:
        super().__init__(group)
        self.username = username
        self.font = pygame.font.Font("font/simkai.ttf", 20)
        self.image = self.font.render(self.username, True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topright = (SCREEN_WIDTH, 0)
    
    def update(self) -> None:
        # self.image = self.font.render(self.username, True, (255, 255, 255))
        return super().update()

#顶部提示信息
class GamePrompt(pygame.sprite.Sprite):
    def __init__(self,  group: pygame.sprite.Group) -> None:
        super().__init__()
        self.group = group
        self.text = ""
        self.font = pygame.font.Font("font/simkai.ttf", 20)
        self.image = self.font.render(self.text, True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.last_show_ticks = 0
    
    def show(self, text: str, color = (255, 255, 255)) -> None:
        self.text = text
        self.image = self.font.render(self.text, True, color)
        self.rect = self.image.get_rect()
        self.rect.midtop = (SCREEN_WIDTH / 2, 20)
        self.add(self.group)
        self.last_show_ticks = pygame.time.get_ticks()
    
    def update(self) -> None:
        now = pygame.time.get_ticks()
        if now - self.last_show_ticks > 3000:
            self.kill()

#核弹UI
class Bomb_Icon(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group) -> None:
        super().__init__(group)
        self.image = pygame.image.load('images/bomb.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (0, SCREEN_HEIGHT)
    
    def update(self) -> None:
        return super().update()

class BombUI(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group) -> None:
        super().__init__(group)
        self.bomb_num = 0
        self.bomb_font = pygame.font.Font('font/font.ttf',48)
        self.image = self.bomb_font.render('× %d' % (self.bomb_num),True, (255, 255, 255))
        self.rect = self.image.get_rect()
        #核弹使用音效
        self.mix_channel = pygame.mixer.Channel(2)
        self.use_bullet_sound = pygame.mixer.Sound("sound/use_bomb.wav")
        self.use_bullet_sound.set_volume(0.4)
    
    def get_bomb(self):
        if self.bomb_num < 100:
            self.bomb_num += 1
    
    def use_bomb(self, score_ui : GameScore, screen_rect : pygame.Rect, big_enemy_list, mid_enemy_list, small_enemy_list) -> None:
        if self.bomb_num > 0:
            self.mix_channel.play(self.use_bullet_sound)
            self.bomb_num -= 1
            for e in big_enemy_list:
                if screen_rect.colliderect(e.rect):
                    e.destroy()
                    score_ui.add_score(10)
            for e in mid_enemy_list:
                if screen_rect.colliderect(e.rect):
                    e.destroy()
                    score_ui.add_score(3)
            for e in small_enemy_list:
                if screen_rect.colliderect(e.rect):
                    e.destroy()
                    score_ui.add_score(1)
    
    def update(self) -> None:
        self.image = self.bomb_font.render('× %d' % (self.bomb_num),True, (255, 255, 255))
        self.rect= self.image.get_rect()
        self.rect.x = 83
        self.rect.centery = SCREEN_HEIGHT -  24
        return super().update()

#游戏结束界面
class GameOverUI(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group) -> None:
        super().__init__()
        self.group = group
        self.font = pygame.font.Font("font/simkai.ttf", 35)
        self.font_big = pygame.font.Font("font/simkai.ttf", 60)
        self.text_top = self.font_big.render("游戏结束", True, (255, 255, 255))
        self.text_restart = self.font.render("1.按[R]键重新开始.", True, (255, 255, 255))
        self.text_exit = self.font.render("2.按[ESC]键退出游戏.", True, (255, 255, 255))
        self.text_qrcode = self.font.render("手机浏览器扫码上传得分", True, (255, 255, 255))
        self.text_qrcode_rect = self.text_qrcode.get_rect()
        
        self.image = pygame.Surface((480, 700))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.image.set_colorkey((0, 0, 0))
        
        self.text_qrcode_rect.midtop = self.rect.midtop
        self.text_qrcode_rect.y += 480
        
    def show(self) -> None:
        #二维码
        self.qrcode = pygame.image.load("images/qrcode.png").convert_alpha()
        self.qr_rect = self.qrcode.get_rect()
        self.qr_rect.center = self.rect.center
        self.add(self.group)
    
    def update(self) -> None:
        self.image.blit(self.text_top, (110, 40))
        self.image.blit(self.text_restart, (60, 120))
        self.image.blit(self.text_exit, (60, 180))
        self.image.blit(self.qrcode, self.qr_rect)
        self.image.blit(self.text_qrcode, self.text_qrcode_rect)
        pygame.mouse.set_pos((SCREEN_HEIGHT - 20, SCREEN_WIDTH / 2))
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_r]:
            pygame.event.post(pygame.event.Event(RESTART_GAME))
            self.kill()