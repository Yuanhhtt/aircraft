import pygame
import random
from const import *
class DestroyAirplane(pygame.sprite.Sprite):
    def __init__(self, frames, rect, fps = 60) -> None:
        super().__init__()
        self.frames = frames
        self.frame_num = 0
        self.image = self.frames[self.frame_num]
        self.rect = rect
        self.frame_rate = fps
        self.last_update_time = pygame.time.get_ticks()
    
    def update(self) -> None:
        #根据ticks计算frame_num
        now = pygame.time.get_ticks()
        if now - self.last_update_time > self.frame_rate:
            self.last_update_time = now
            self.frame_num += 1
        if self.frame_num < len(self.frames):
            self.image = self.frames[self.frame_num]
        else:
            self.kill()
        

class Airplane(pygame.sprite.Sprite):
    def __init__(self, alive_frames : list, hp = 1, speed = 3, fps = 60, is_enemy = True) -> None:
        super().__init__()
        self.alive_frames = alive_frames
        self.hp = hp
        self.hp_max = hp
        self.speed = speed
        self.is_enemy = is_enemy
        self.frame_num = 0
        self.image : pygame.Surface = self.alive_frames[self.frame_num]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.set_random_xy()
        self.state = "alive"
        self.last_update_time = pygame.time.get_ticks()
        self.frame_rate = fps

    def set_random_xy(self):
        #随机设置敌机位置
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = - random.randint(0, SCREEN_HEIGHT - self.rect.height)

    def update(self) -> None:
        #根据hp值计算状态
        if self.hp == 0:
            self.state = "daed"

        #根据ticks计算frame_num
        now = pygame.time.get_ticks()
        if now - self.last_update_time > self.frame_rate:
            self.last_update_time = now
            self.frame_num += 1
        
        #根据state和frame_num显示动画
        if self.frame_num == len(self.alive_frames):
                self.frame_num = 0
        self.image = self.alive_frames[self.frame_num]
        
        
        #根据speed更新位置
        if self.is_enemy:
            if self.rect.y > SCREEN_HEIGHT:
                self.set_random_xy()
            else:
                self.rect.y += self.speed
            