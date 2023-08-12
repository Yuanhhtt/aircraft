import pygame
from const import *

#游戏计时器
class GameTimer(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group) -> None:
        super().__init__(group)
        self.font = pygame.font.SysFont(None, 30)
        self.start_time = 0
        self.end_time = 0
        self.image = self.font.render("%02d:%02d:%02d.%02d" % (0, 0, 0, 0), True, (255, 255, 255))
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
        self.image = self.font.render("%02d:%02d:%02d.%02d" % (hours, minutes,seconds, ticks % 100), True, (255, 255, 255))

#游戏得分
class GameScore(pygame.sprite.Sprite):
    def __init__(self,  group: pygame.sprite.Group) -> None:
        super().__init__(group)
        self.score = 0
        self.font = pygame.font.SysFont(None, 30)
        self.image = self.font.render("score:%d" % (self.score), True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.midtop = (SCREEN_WIDTH / 2, 0)
    
    def add_score(self, score:int):
        self.score += score
    
    def restart(self):
        self.score = 0
    
    def update(self) -> None:
        self.image = self.font.render("score:%d" % (self.score), True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.midtop = (SCREEN_WIDTH / 2, 0)

#游戏帧率
class GameFps(pygame.sprite.Sprite):
    def __init__(self,  group: pygame.sprite.Group, clock : pygame.time.Clock) -> None:
        super().__init__(group)
        self.clock = clock
        self.font = pygame.font.SysFont(None, 30)
        self.image = self.font.render("fps:%02d" % (self.clock.get_fps()), True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 410
    
    def update(self) -> None:
        self.image = self.font.render("fps:%02d" % (self.clock.get_fps()), True, (255, 255, 255))

#顶部提示信息
class GamePrompt(pygame.sprite.Sprite):
    def __init__(self,  group: pygame.sprite.Group) -> None:
        super().__init__()
        self.group = group
        self.text = ""
        self.font = pygame.font.Font("font/simkai.ttf", 30)
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

#游戏结束界面
class GameOverUI(pygame.sprite.Sprite):
    def __init__(self,  group: pygame.sprite.Group) -> None:
        super().__init__()
        self.group = group
        self.font = pygame.font.Font("font/simkai.ttf", 35)
        self.font_big = pygame.font.Font("font/simkai.ttf", 60)
        self.text_top = self.font_big.render("游戏结束", True, (255, 255, 255))
        self.text_restart = self.font.render("1.按[R]键重新开始游戏.", True, (255, 255, 255))
        self.text_exit = self.font.render("2.按[ESC]键退出游戏.", True, (255, 255, 255))
        self.text_qrcode = self.font.render("扫码上传成绩", True, (255, 255, 255))
        self.text_qrcode_rect = self.text_qrcode.get_rect()
        #二维码
        self.qrcode = pygame.image.load("images/qrcode.png").convert_alpha()
        self.qr_rect = self.qrcode.get_rect()
        self.image = pygame.Surface((480, 700))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.image.set_colorkey((0, 0, 0))
        self.qr_rect.center = self.rect.center
        self.text_qrcode_rect.midtop = self.rect.midtop
        self.text_qrcode_rect.y += 470
        
    def show(self) -> None:
        self.add(self.group)
    
    def update(self) -> None:
        self.image.blit(self.text_top, (110, 40))
        self.image.blit(self.text_restart, (40, 120))
        self.image.blit(self.text_exit, (40, 180))
        self.image.blit(self.qrcode, self.qr_rect)
        self.image.blit(self.text_qrcode, self.text_qrcode_rect)
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_r]:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT + 2))
            self.kill()
        