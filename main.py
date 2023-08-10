import pygame
import sys
from const import *
from airplane import *
from gui import *

class Game():
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('看谁打得久')
        self.screen_rect = self.screen.get_rect()
        #加载背景图片
        self.background = pygame.image.load(IMAGE_PATH['background'])
        
    
    def start(self):
        running = True
        while running:
            for event in pygame.event.get():
                #处理关闭事件
                if event.type == pygame.QUIT:
                    running = False
                    self.quit()
            self.screen.blit(self.background,(0,0))
            pygame.display.update()

            
    def stop(self):
        pass

    def quit(self):
        pygame.quit()
        sys.exit()

def main():
    pygame.init()

    screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen=pygame.display.set_mode(screen_size)

    pygame.display.set_caption('看谁打得久')
    screen_rect = screen.get_rect()

    #加载背景图片
    background=pygame.image.load(IMAGE_PATH['background'])

    #创建Sprite组对象
    all_visible_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    gui_group = pygame.sprite.Group()

    #创建Sprite对象
    ##生成player
    player = HeroPlane(player_group, screen_rect.midbottom)
    ##生成小型敌机
    small_enemy_list = [SmallEnemyPlane(enemy_group) for i in range(SMALL_ENEMY_NUM)]
    ##生成中型敌机
    mid_enemy_list = [MidEnemyPlane(enemy_group) for i in range(MID_ENEMY_NUM)]
    ##生成大型敌机
    big_enemy_list = [BigEnemyPlane(enemy_group) for i in range(BIG_ENEMY_NUM)]

    #加载声音资源
    pygame.mixer.music.load("sound/game_music.ogg")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    

    

    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    #自定义事件
    INCREASE_DIFFICULTY = pygame.USEREVENT
    pygame.time.set_timer(INCREASE_DIFFICULTY, INCREASE_DIFFICULTY_TIME)
    DOUBLE_BULLET = pygame.USEREVENT + 1
    pygame.time.set_timer(DOUBLE_BULLET, DOUBLE_BULLET_TIME)
    RESTART_GAME = pygame.USEREVENT + 2

    #定义游戏状态
    running = True
    game_going = True

    #初始化游戏提示UI
    prompt_ui = GamePrompt(gui_group)
    gameover_ui = GameOverUI(gui_group)

    #初始化时间
    clock = pygame.time.Clock()
    fps_ui = GameFps(gui_group, clock=clock)
    timer_ui = GameTimer(gui_group)
    timer_ui.start()
    while running:
        #绘制背景
        screen.blit(background,(0,0))
        
        #获取事件
        for event in pygame.event.get():
            # print(event.type)
            # print(event.__dict__)
            #处理关闭事件
            if event.type == pygame.QUIT:
                running = False
                pygame.mixer.stop()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                # print(event.pos)
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif event.type == INCREASE_DIFFICULTY:
                #每xx秒提升难度，中、大敌机血量加1
                if game_going:
                    for e in mid_enemy_list:
                        e.increase_difficulty(1)
                    for e in big_enemy_list:
                        e.increase_difficulty(5)
                    prompt_ui.show("increase difficulty!")
                # print(int(clock.get_fps()))
            elif event.type == DOUBLE_BULLET:
                #获得子弹强化
                player.powerful()
                pygame.time.set_timer(DOUBLE_BULLET, 0)
                prompt_ui.show("Fire Powerful!", color=(0, 0, 255))
            elif event.type == RESTART_GAME:
                #重新开始游戏
                game_going = not game_going
                #1.重置palyer
                player.restart()
                #2.重置敌机
                for e in small_enemy_list:
                    e.restart()
                for e in mid_enemy_list:
                    e.restart()
                for e in big_enemy_list:
                    e.restart()
                #3.重置timer_ui
                timer_ui.start()
                #4.重置定时器
                pygame.time.set_timer(INCREASE_DIFFICULTY, INCREASE_DIFFICULTY_TIME)
                pygame.time.set_timer(DOUBLE_BULLET, DOUBLE_BULLET_TIME)
        
        #判断游戏进行状态
        if not game_going:
            #游戏结束，显示结束UI
            gameover_ui.show()

        #更新状态
        player_group.update()
        enemy_group.update()
        gui_group.update()
        
        
        for p in player_group.sprites():
            #player与敌机之间的碰撞检测
            collided_list = pygame.sprite.spritecollide(p, enemy_group, False, collided=pygame.sprite.collide_mask)
            if collided_list:
                #机毁人亡，游戏结束
                timer_ui.stop()
                p.destroy()
                for col_enemy in collided_list:
                    col_enemy.destroy()
                game_going = not game_going
            #子弹与敌机之间的碰撞检测
            collided_dict = pygame.sprite.groupcollide(p.bullet_group, enemy_group, True, False, collided=pygame.sprite.collide_mask)
            for b in collided_dict.keys():
                for e in collided_dict[b]:
                    e.be_hit()
                    if not type(e) is SmallEnemyPlane:
                        e.draw_hp_line(screen)
        
        #绘制图像
        all_visible_group.add(player_group, player.bullet_group)
        for enemy in enemy_group.sprites():
            if enemy.rect.bottom > 0:
                all_visible_group.add(enemy)

        
        all_visible_group.draw(screen)
        gui_group.draw(screen)
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()
    # app = Game()
    # app.start()