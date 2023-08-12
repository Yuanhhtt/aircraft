from time import sleep
from tkinter.messagebox import NO
import pygame
import random
from const import *
from bullet import *

#英雄飞机类
class HeroPlane(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, postion : tuple) -> None:
        super().__init__(group)
        self.group = group
        #加载飞行动画
        self.alive_frames = []
        for i in IMAGE_PATH['player']:
            self.alive_frames.append(pygame.image.load(i).convert_alpha())
        #加载炸毁时动画
        self.destroy_frames = []
        for i in IMAGE_PATH['player_destroy']:
            self.destroy_frames.append(pygame.image.load(i).convert_alpha())
        #动画帧索引
        self.frame_num = 0
        #上一帧的更新时间
        self.last_update_time = pygame.time.get_ticks()
        self.frame_rate = FPS
        #飞机是否存活
        self.is_alive = True
        self.image = self.alive_frames[self.frame_num]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.set_mask()
        #设置飞机初始位置
        self.initial_position = postion
        self.rect.midbottom = self.initial_position
        #飞机加入组
        self.add(self.group)
        self.bullet_group = pygame.sprite.Group()
        #加载炮管，初始1个，2分钟3个,4分钟5个，5分钟7个
        self.bullets = [Bullet(self.bullet_group) for i in range(BULLET_NUM)]
        self.is_powerful = False
        self.left_bullets = [BlueBullet(self.bullet_group) for i in range(BULLET_NUM)]
        self.right_bullets = [BlueBullet(self.bullet_group) for i in range(BULLET_NUM)]
        self.is_powerful_level_2 = False
        self.left_mid_bullets = [Bullet(self.bullet_group) for i in range(BULLET_NUM)]
        self.right_mid_bullets = [Bullet(self.bullet_group) for i in range(BULLET_NUM)]
        self.is_powerful_level_3 = False
        self.left_level3_bullets = [BlueBullet(self.bullet_group) for i in range(BULLET_NUM)]
        self.right_level3_bullets = [BlueBullet(self.bullet_group) for i in range(BULLET_NUM)]
        #子弹威力，初始1
        self.buullet_damage = 1
        #加载子弹声音
        self.bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
        self.bullet_sound.set_volume(0.2)
        self.destroy_sound = pygame.mixer.Sound("sound/me_down.wav")
        self.destroy_sound.set_volume(0.2)
        #子弹射速延时
        self.bullet_delay = BULLET_DELAY
        self.bullet_speed_double = False
        self.last_firing_time = pygame.time.get_ticks()
    
    def add_bullet_speed(self) -> None:
        if self.bullet_speed_double == False:
            self.bullet_speed_double = True
            self.bullet_delay = self.bullet_delay // 2
    
    def set_mask(self) -> None:
        for x in range(20):
            for y in range(self.rect.height):
                self.mask.set_at((x, y), 0)
        for x in range(self.rect.width - 20, self.rect.width):
            for y in range(self.rect.height):
                self.mask.set_at((x, y), 0)
        for x in range(20, self.rect.width - 20):
            for y in range(self.rect.height - 20, self.rect.height):
                self.mask.set_at((x, y), 0)
        for x in range(20, self.rect.width - 20):
            for y in range(0, 10):
                self.mask.set_at((x, y), 0)
    
    def restart(self) -> None:
        self.is_alive = True
        self.is_powerful = False
        self.is_powerful_level_2 = False
        self.is_powerful_level_3 = False
        self.bullet_speed_double = False
        self.bullet_delay = BULLET_DELAY
        self.buullet_damage = 1
        self.frame_num = 0
        self.mask = pygame.mask.from_surface(self.alive_frames[0])
        self.set_mask()
        self.rect.midbottom = self.initial_position
        self.add(self.group)
        self.last_update_time = pygame.time.get_ticks()
    
    def powerful(self) -> None:
        if self.is_powerful == False:
            self.is_powerful = True

    def powerful_level_2(self) -> None:
        if self.is_powerful_level_2 == False:
            self.is_powerful_level_2 = True
            
    def powerful_level_3(self) -> None:
        if self.is_powerful_level_3 == False:
            self.is_powerful_level_3 = True
            
    def firing(self) -> None:
        for b in self.bullets:
            if not b.alive():
                b.reset(self.rect.midtop)
                break
        if self.is_powerful:
            for b in self.left_bullets:
                if not b.alive():
                    b.reset((self.rect.centerx - 33,self.rect.centery))
                    break
            for b in self.right_bullets:
                if not b.alive():
                    b.reset((self.rect.centerx + 32,self.rect.centery))
                    break
        if self.is_powerful_level_2:
            for b in self.left_mid_bullets:
                if not b.alive():
                    b.reset((self.rect.centerx - 17,self.rect.centery - 10))
                    break
            for b in self.right_mid_bullets:
                if not b.alive():
                    b.reset((self.rect.centerx + 17,self.rect.centery - 10))
                    break
        if self.is_powerful_level_3:
            for b in self.left_level3_bullets:
                if not b.alive():
                    b.reset((self.rect.centerx - 48,self.rect.centery + 30))
                    break
            for b in self.right_level3_bullets:
                if not b.alive():
                    b.reset((self.rect.centerx + 47,self.rect.centery + 30))
                    break
        self.bullet_sound.play()
        self.last_firing_time = pygame.time.get_ticks()
    
    def destroy(self) -> None:
        self.is_alive = False
        self.frame_num = 0
        self.mask.clear()
        for b in self.bullet_group.sprites():
            b.kill()
        self.destroy_sound.play()
        self.last_update_time = pygame.time.get_ticks()
    
    def input(self) ->None:
        dis = pygame.mouse.get_rel()
        # dis_len = dis.length()
        # if dis_len > self.speed:
        #     dis.normalize_ip()
        #     dis = dis*self.speed

        x = self.rect.center[0] + dis[0]
        y = self.rect.center[1] + dis[1]
        if y > SCREEN_HEIGHT:
            self.rect.centery = SCREEN_HEIGHT
        elif y < 0:
            self.rect.centery = 0
        else:
            self.rect.centery = y
        
        if x > SCREEN_WIDTH:
            self.rect.centerx = SCREEN_WIDTH
        elif x < 0:
            self.rect.centerx = 0
        else:
            self.rect.centerx = x
    
    def update(self) -> None:
        #根据ticks计算frame_num
        now = pygame.time.get_ticks()
        delay = now - self.last_update_time
        if self.is_alive:
            #存活状态，循环显示存活动画
            if delay > self.frame_rate:
                self.last_update_time = now
                self.frame_num += 1
            if self.frame_num == len(self.alive_frames):
                    self.frame_num = 0
            self.image = self.alive_frames[self.frame_num]
            #延时发射子弹
            if now - self.last_firing_time > self.bullet_delay:
                self.firing()
            self.bullet_group.update()
            self.input()
        else:
            #死亡状态，显示一次炸毁动画
            if delay > self.frame_rate * 2:
                self.last_update_time = now
                self.frame_num += 1
            if self.frame_num < len(self.destroy_frames):
                self.image = self.destroy_frames[self.frame_num]
            else:
                self.kill()

#小号敌机类
class SmallEnemyPlane(pygame.sprite.Sprite):
    def __init__(
        self, group: pygame.sprite.Group, alive_frames, destroy_frames, destroy_sound, speed = 5, hp = SMALL_ENEMY_HP
    ) -> None:
        super().__init__(group)
        self.group = group
        self.destroy_sound = destroy_sound
        #加载飞行动画
        self.alive_frames = alive_frames
        #加载炸毁时动画
        self.destroy_frames = destroy_frames
        #动画帧索引
        self.frame_num = 0
        #飞机速度
        self.speed = speed
        self.hp_max = hp
        self.hp = hp
        #上一帧的更新时间
        self.last_update_time = pygame.time.get_ticks()
        self.frame_rate = FPS
        #飞机是否存活
        self.is_alive = True
        self.image = self.alive_frames[self.frame_num]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        #设置飞机初始位置
        self.set_random_xy()
        #飞机加入组
        self.add(self.group)
    
    def restart(self) -> None:
        self.reset()
    
    def be_hit(self, damage=1) -> None:
        if self.hp <= 0:
            self.destroy()
        else:
            self.hp -= damage

    def destroy(self) -> None:
        self.is_alive = False
        self.frame_num = 0
        self.hp = SMALL_ENEMY_HP
        self.mask.clear()
        self.destroy_sound.play()
        self.last_update_time = pygame.time.get_ticks()

    def set_random_xy(self):
        #随机设置敌机位置
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = - random.randint(self.rect.height, SCREEN_HEIGHT)
    
    def move(self):
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()
            self.reset()
        else:
            self.rect.y += self.speed
    
    def reset(self):
        self.is_alive = True
        self.frame_num = 0
        self.hp = SMALL_ENEMY_HP
        self.mask = pygame.mask.from_surface(self.alive_frames[0])
        self.set_random_xy()
        self.add(self.group)

    def update(self) -> None:
        #根据ticks计算frame_num
        now = pygame.time.get_ticks()
        delay = now - self.last_update_time
        if self.is_alive:
            self.move()
            #存活状态，循环显示存活动画
            self.image = self.alive_frames[0]
        else:
            #死亡状态，显示一次炸毁动画
            if delay > self.frame_rate * 2:
                self.last_update_time = now
                self.frame_num += 1
            if self.frame_num < len(self.destroy_frames):
                self.image = self.destroy_frames[self.frame_num]
            else:
                self.kill()
                self.reset()

#中号敌机类
class MidEnemyPlane(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, destroy_sound, speed = 3, hp_max = MID_ENEMY_HP) -> None:
        super().__init__(group)
        self.group = group
        self.destroy_sound = destroy_sound
        #加载飞行动画
        self.alive_frames = []
        for i in IMAGE_PATH['enemy_mid']:
            self.alive_frames.append(pygame.image.load(i).convert_alpha())
        #加载被击中时的动画
        self.hit_frame = pygame.image.load(IMAGE_PATH['enemy_mid_hit']).convert_alpha()
        #加载炸毁时动画
        self.destroy_frames = []
        for i in IMAGE_PATH['enemy_mid_destroy']:
            self.destroy_frames.append(pygame.image.load(i).convert_alpha())
        #动画帧索引
        self.frame_num = 0
        #飞机速度
        self.speed = speed
        #飞机生命值
        self.hp_max = hp_max
        self.hp = hp_max
        #上一帧的更新时间
        self.last_update_time = pygame.time.get_ticks()
        self.frame_rate = FPS
        #飞机是否存活
        self.is_alive = True
        #是否被击中
        self.hit = False
        self.image = self.alive_frames[self.frame_num]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        #设置飞机初始位置
        self.set_random_xy()
        #飞机加入组
        self.add(self.group)
    
    def restart(self) -> None:
        self.reset()
        self.hp_max = MID_ENEMY_HP
        self.hp = self.hp_max
    
    def increase_difficulty(self, num : int) -> None:
        self.hp_max += num
    
    def draw_hp_line(self, screen : pygame.Surface):
        if self.hp == self.hp_max:
            return
        line_width = self.rect.width - 20
        line_height = 5
        point_a = (self.rect.x + 10, self.rect.bottom - line_height)
        point_b = (self.rect.x + 10 + line_width, self.rect.bottom - line_height)
        line_color = (0, 0, 0)
        now = pygame.time.get_ticks()

        pygame.draw.line(screen, line_color, point_a, point_b, line_height)
        remain = self.hp / self.hp_max
        if remain > 0.3:
            line_color = (0, 255, 0)
        else:
            line_color = (255, 0, 0)
        point_c = (point_a[0] + int(line_width*remain), self.rect.bottom - line_height)
        pygame.draw.line(screen, line_color, point_a, point_c, line_height)
        
    def be_hit(self, damage=1) -> None:
        self.hit = True
        if self.hp <= 0:
            self.destroy()
        else:
            self.hp -= damage
    
    def destroy(self) -> None:
        self.is_alive = False
        self.frame_num = 0
        self.hp = self.hp_max
        self.mask.clear()
        self.destroy_sound.play()
        self.last_update_time = pygame.time.get_ticks()

    def set_random_xy(self):
        #随机设置敌机位置
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = - random.randint(self.rect.height, SCREEN_HEIGHT)
    
    def move(self):
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()
            self.reset()
        else:
            self.rect.y += self.speed
    
    def reset(self):
        self.is_alive = True
        self.frame_num = 0
        self.hp = self.hp_max
        self.mask = pygame.mask.from_surface(self.alive_frames[0])
        self.set_random_xy()
        self.add(self.group)
        self.last_update_time = pygame.time.get_ticks()

    def update(self) -> None:
        #根据ticks计算frame_num
        now = pygame.time.get_ticks()
        delay = now - self.last_update_time
        if self.is_alive:
            #存活状态
            self.move()
            if self.hit:
                #被击中时切换动画
                if delay > BULLET_DELAY/2:
                    self.image = self.hit_frame
                else:
                    self.image = self.alive_frames[self.frame_num]
                self.hit = False
            else:
                if delay > self.frame_rate:
                    self.last_update_time = now
                    self.frame_num += 1
                if self.frame_num == len(self.alive_frames):
                    self.frame_num = 0
                self.image = self.alive_frames[self.frame_num]
        else:
            #死亡状态，显示一次炸毁动画
            if delay > self.frame_rate * 2:
                self.last_update_time = now
                self.frame_num += 1
            if self.frame_num < len(self.destroy_frames):
                self.image = self.destroy_frames[self.frame_num]
            else:
                self.kill()
                self.reset()           

#大号敌机类
class BigEnemyPlane(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, destroy_sound, speed = 2, hp_max = BIG_ENEMY_HP) -> None:
        super().__init__(group)
        self.group = group
        self.destroy_sound = destroy_sound
        #加载飞行动画
        self.alive_frames = []
        for i in IMAGE_PATH['enemy_big']:
            self.alive_frames.append(pygame.image.load(i).convert_alpha())
        #加载被击中时的动画
        self.hit_frame = pygame.image.load(IMAGE_PATH['enemy_big_hit']).convert_alpha()
        #加载炸毁时动画
        self.destroy_frames = []
        for i in IMAGE_PATH['enemy_big_destroy']:
            self.destroy_frames.append(pygame.image.load(i).convert_alpha())
        #动画帧索引
        self.frame_num = 0
        #飞机速度
        self.speed = speed
        #飞机生命值
        self.hp_max = hp_max
        self.hp = hp_max
        #上一帧的更新时间
        self.last_update_time = pygame.time.get_ticks()
        self.frame_rate = FPS
        #飞机是否存活
        self.is_alive = True
        #是否被击中
        self.hit = False
        self.image = self.alive_frames[self.frame_num]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        #设置飞机初始位置
        self.set_random_xy()
        #飞机加入组
        self.add(self.group)

    def restart(self) -> None:
        self.reset()
        self.hp_max = BIG_ENEMY_HP
        self.hp = self.hp_max
    
    def increase_difficulty(self, num : int) -> None:
        self.hp_max += num

    def draw_hp_line(self, screen : pygame.Surface):
        if self.hp == self.hp_max:
            return
        line_width = self.rect.width - 20
        line_height = 5
        point_a = (self.rect.x + 10, self.rect.bottom - line_height)
        point_b = (self.rect.x + 10 + line_width, self.rect.bottom - line_height)
        line_color = (0, 0, 0)

        pygame.draw.line(screen, line_color, point_a, point_b, line_height)
        remain = self.hp / self.hp_max
        if remain > 0.3:
            line_color = (0, 255, 0)
        else:
            line_color = (255, 0, 0)
        point_c = (point_a[0] + int(line_width*remain), self.rect.bottom - line_height)
        pygame.draw.line(screen, line_color, point_a, point_c, line_height)
        
    def be_hit(self, damage=1) -> None:
        self.hit = True
        if self.hp <= 0:
            self.destroy()
        else:
            self.hp -= damage
    
    def destroy(self) -> None:
        if self.is_alive:
            self.is_alive = False
            self.frame_num = 0
            self.hp = self.hp_max
            self.mask.clear()
            self.destroy_sound.play()
            self.last_update_time = pygame.time.get_ticks()

    def set_random_xy(self):
        #随机设置敌机位置
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = - random.randint(self.rect.height, SCREEN_HEIGHT)
    
    def move(self):
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()
            self.reset()
        else:
            self.rect.y += self.speed
    
    def reset(self):
        self.is_alive = True
        self.frame_num = 0
        self.hp = self.hp_max
        self.mask = pygame.mask.from_surface(self.alive_frames[0])
        self.set_random_xy()
        self.add(self.group)
        self.last_update_time = pygame.time.get_ticks()

    def update(self) -> None:
        #根据ticks计算frame_num
        now = pygame.time.get_ticks()
        delay = now - self.last_update_time
        if self.is_alive:
            #存活状态
            self.move()
            if self.hit:
                #被击中时切换动画
                if delay > BULLET_DELAY/2:
                    self.image = self.hit_frame
                else:
                    self.image = self.alive_frames[self.frame_num]
                self.hit = False
            else:
                if delay > self.frame_rate:
                    self.last_update_time = now
                    self.frame_num += 1
                if self.frame_num == len(self.alive_frames):
                    self.frame_num = 0
                self.image = self.alive_frames[self.frame_num]
        else:
            #死亡状态，显示一次炸毁动画
            if delay > self.frame_rate * 2:
                self.last_update_time = now
                self.frame_num += 1
            if self.frame_num < len(self.destroy_frames):
                self.image = self.destroy_frames[self.frame_num]
            else:
                self.kill()
                self.reset()

#子弹补给
class BulletSupply(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, speed = 4) -> None:
        super().__init__()
        self.group = group
        self.image = pygame.image.load('images/bullet_supply.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed
        #获得音效
        self.get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
        self.get_bullet_sound.set_volume(0.2)
    
    def start(self) -> None:
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -100
        self.add(self.group)
    
    def get_supply(self) ->None:
        self.get_bullet_sound.play()
        self.kill()
    
    def update(self) -> None:
        if self.alive():
            if self.rect.y < SCREEN_HEIGHT:
                self.rect.y += self.speed
            else:
                self.kill()

#核弹补给
class BombSupply(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, speed = 4) -> None:
        super().__init__()
        self.group = group
        self.image = pygame.image.load('images/bomb_supply.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed
        #获得音效
        self.get_bullet_sound = pygame.mixer.Sound("sound/get_bomb.wav")
        self.get_bullet_sound.set_volume(0.2)
        self.use_bullet_sound = pygame.mixer.Sound("sound/use_bomb.wav")
        self.use_bullet_sound.set_volume(0.2)
        self.bomb_num = 0
    
    def start(self) -> None:
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -100
        self.add(self.group)
    
    def get_supply(self) ->None:
        if self.bomb_num < 100:
            self.bomb_num += 1
        self.get_bullet_sound.play()
        self.kill()
    
    def use_bomb(self, score_ui) -> None:
        if self.bomb_num > 0:
            self.use_bullet_sound.play()
            self.bomb_num -= 1
            for s in self.group:
                if type(s) == BigEnemyPlane or type(s) == MidEnemyPlane or type(s) == SmallEnemyPlane:
                    s.destroy()
                    score_ui.add_score(s.hp_max)
    
    def update(self) -> None:
        if self.alive():
            if self.rect.y < SCREEN_HEIGHT:
                self.rect.y += self.speed
            else:
                self.kill()