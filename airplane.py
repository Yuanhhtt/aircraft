import pygame
import random
from const import *
from bullet import *

#英雄飞机类
class HeroPlane(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, postion : tuple, speed = 6) -> None:
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
        #飞机速度
        self.speed = speed
        #上一帧的更新时间
        self.last_update_time = pygame.time.get_ticks()
        self.frame_rate = FPS
        #飞机是否存活
        self.is_alive = True
        self.image = self.alive_frames[self.frame_num]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        #设置飞机初始位置
        self.initial_position = postion
        self.rect.midbottom = self.initial_position
        #飞机加入组
        self.add(self.group)
        #加载子弹
        self.bullet_group = pygame.sprite.Group()
        self.bullets = [Bullet(self.bullet_group) for i in range(BULLET_NUM)]
        self.last_firing_time = pygame.time.get_ticks()
        #子弹加强
        self.is_powerful = False
        self.left_bullets = []
        self.right_bullets = []
    
    def restart(self) -> None:
        self.is_alive = True
        self.is_powerful = False
        self.frame_num = 0
        self.mask = pygame.mask.from_surface(self.alive_frames[0])
        self.rect.midbottom = self.initial_position
        self.add(self.group)
        self.last_update_time = pygame.time.get_ticks()
    
    def powerful(self) -> None:
        self.is_powerful = True
        self.left_bullets = [BlueBullet(self.bullet_group) for i in range(BULLET_NUM)]
        self.right_bullets = [BlueBullet(self.bullet_group) for i in range(BULLET_NUM)]
    
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
                    b.reset((self.rect.centerx + 30,self.rect.centery))
                    break
        self.last_firing_time = pygame.time.get_ticks()
    
    def destroy(self) -> None:
        self.is_alive = False
        self.frame_num = 0
        self.mask.clear()
        for b in self.bullet_group.sprites():
            b.kill()
        self.last_update_time = pygame.time.get_ticks()
    
    def input(self) ->None:
        mouse_rel = pygame.mouse.get_rel()
        # x , y = 0, 0
        # if mouse_rel[0] >= 0:
        #     #鼠标x轴向左
        #     if mouse_rel[0] > self.speed:
        #         x = self.rect.midbottom[0] + self.speed
        #     else:
        #         x = self.rect.midbottom[0] + mouse_rel[0]
        # else:
        #     #鼠标x轴向右
        #     if mouse_rel[0] < -self.speed:
        #         x = self.rect.midbottom[0] - self.speed
        #     else:
        #         x = self.rect.midbottom[0] + mouse_rel[0]

        # if mouse_rel[1] >= 0:
        #     #鼠标y轴向下
        #     if mouse_rel[1] > self.speed:
        #         y = self.rect.midbottom[1] + self.speed
        #     else:
        #         y = self.rect.midbottom[1] + mouse_rel[1]
        # else:
        #     #鼠标y轴向上
        #     if mouse_rel[1] < -self.speed:
        #         y = self.rect.midbottom[1] - self.speed
        #     else:
        #         y = self.rect.midbottom[1] + mouse_rel[1]
        x = self.rect.midbottom[0] + mouse_rel[0]
        y = self.rect.midbottom[1] + mouse_rel[1]
        
        if 0 <= x <= SCREEN_WIDTH and self.rect.height <= y <= SCREEN_HEIGHT:
            self.rect.midbottom = (x, y)
    
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
            if now - self.last_firing_time > BULLET_DELAY:
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
    def __init__(self, group: pygame.sprite.Group, speed = 3) -> None:
        super().__init__(group)
        self.group = group
        #加载飞行动画
        self.alive_frames = []
        for i in IMAGE_PATH['enemy_small']:
            self.alive_frames.append(pygame.image.load(i).convert_alpha())
        #加载炸毁时动画
        self.destroy_frames = []
        for i in IMAGE_PATH['enemy_small_destroy']:
            self.destroy_frames.append(pygame.image.load(i).convert_alpha())
        #动画帧索引
        self.frame_num = 0
        #飞机速度
        self.speed = speed
        self.hp = SMALL_ENEMY_HP
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
    
    def be_hit(self) -> None:
        if self.hp == 0:
            self.destroy()
        else:
            self.hp -= 1

    def destroy(self) -> None:
        self.is_alive = False
        self.frame_num = 0
        self.hp = SMALL_ENEMY_HP
        self.mask.clear()
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
    def __init__(self, group: pygame.sprite.Group, speed = 2, hp_max = MID_ENEMY_HP) -> None:
        super().__init__(group)
        self.group = group
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
        
    def be_hit(self) -> None:
        self.hit = True
        if self.hp == 0:
            self.destroy()
        else:
            self.hp -= 1
    
    def destroy(self) -> None:
        self.is_alive = False
        self.frame_num = 0
        self.hp = self.hp_max
        self.mask.clear()
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
                self.image = self.hit_frame
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
    def __init__(self, group: pygame.sprite.Group, speed = 1, hp_max = BIG_ENEMY_HP) -> None:
        super().__init__(group)
        self.group = group
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
        
    def be_hit(self) -> None:
        self.hit = True
        if self.hp == 0:
            self.destroy()
        else:
            self.hp -= 1
    
    def destroy(self) -> None:
        self.is_alive = False
        self.frame_num = 0
        self.hp = self.hp_max
        self.mask.clear()
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
                self.image = self.hit_frame
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
            