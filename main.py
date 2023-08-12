import pygame
import sys
from const import *
from airplane import *
from gui import *

def bullet_supply_col(player : HeroPlane, bullet_supply : BulletSupply):
    bullet_supply.get_supply()
    if player.is_powerful == False:
        player.powerful()
        return
    if player.is_powerful_level_2 == False:
        player.powerful_level_2()
        return
    if player.is_powerful_level_3 == False:
        player.powerful_level_3()
        return
    if player.bullet_speed_double == False:
        player.add_bullet_speed()
        return
    player.buullet_damage = player.buullet_damage * 2

def main():
    pygame.init()

    screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen=pygame.display.set_mode(screen_size)

    pygame.display.set_caption('看谁打得久')
    screen_rect = screen.get_rect()
    #设置鼠标键盘
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    pygame.key.stop_text_input()

    #加载声音资源
    pygame.mixer.music.load("sound/game_music.ogg")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    small_enemy_destroy_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
    small_enemy_destroy_sound.set_volume(0.2)
    mid_enemy_destroy_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
    mid_enemy_destroy_sound.set_volume(0.2)
    big_enemy_destroy_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
    big_enemy_destroy_sound.set_volume(0.2)
    big_enemy_flying_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
    big_enemy_flying_sound.set_volume(0.2)
    upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
    upgrade_sound.set_volume(0.2)
    

    #加载图片
    background=pygame.image.load(IMAGE_PATH['background'])
    small_alive_frames = [pygame.image.load(i).convert_alpha() for i in IMAGE_PATH['enemy_small']]
    small_destroy_frames = [pygame.image.load(i).convert_alpha() for i in IMAGE_PATH['enemy_small_destroy']]

    #创建Sprite组对象
    all_visible_group = pygame.sprite.OrderedUpdates()
    player_group = pygame.sprite.OrderedUpdates()
    enemy_group = pygame.sprite.OrderedUpdates()
    gui_group = pygame.sprite.OrderedUpdates()

    #创建Sprite对象
    ##生成player
    player = HeroPlane(player_group, screen_rect.midbottom)
    ##生成小型敌机
    small_enemy_list = [
        SmallEnemyPlane(enemy_group, small_alive_frames, small_destroy_frames, small_enemy_destroy_sound) for i in range(SMALL_ENEMY_NUM)
    ]
    ##生成中型敌机
    mid_enemy_list = [MidEnemyPlane(enemy_group, mid_enemy_destroy_sound) for i in range(MID_ENEMY_NUM)]
    ##生成大型敌机
    big_enemy_list = [BigEnemyPlane(enemy_group, big_enemy_destroy_sound) for i in range(BIG_ENEMY_NUM)]
    ##生成子弹补给
    bullet_supply = BulletSupply(all_visible_group)
    ##生成核弹补给
    bomb_supply = BombSupply(all_visible_group)
    #初始化核弹UI
    bomb_image=pygame.image.load('images/bomb.png').convert_alpha()
    bomb_rect=bomb_image.get_rect()
    bomb_font=pygame.font.Font('font/font.ttf',48)
   
    

    #自定义事件
    #定时增加敌机血量
    INCREASE_DIFFICULTY = pygame.USEREVENT
    pygame.time.set_timer(INCREASE_DIFFICULTY, INCREASE_DIFFICULTY_TIME)
    #火力强化level_1
    DOUBLE_BULLET = pygame.USEREVENT + 1
    pygame.time.set_timer(DOUBLE_BULLET, DOUBLE_BULLET_TIME)
    #重新开始，key【R】事件
    RESTART_GAME = pygame.USEREVENT + 2
    #火力强化level_2
    FIVE_BULLET = pygame.USEREVENT + 3
    pygame.time.set_timer(FIVE_BULLET, FIVE_BULLET_TIME)
    #火力强化level_3
    SEVEN_BULLET = pygame.USEREVENT + 4
    pygame.time.set_timer(SEVEN_BULLET, SEVEN_BULLET_TIME)
    #火力强化level_4，射速加强
    ADD_BULLET_SPEED = pygame.USEREVENT + 5
    pygame.time.set_timer(ADD_BULLET_SPEED, ADD_BULLET_SPEED_TIME)
    #火力强化level_5，第一次子弹威力加强
    ADD_BULLET_DAMAGE = pygame.USEREVENT + 6
    pygame.time.set_timer(ADD_BULLET_DAMAGE, ADD_BULLET_DAMAGE_TIME)
    #火力强化level_n，以上能力全部获得后，间隔固定时间子弹威力加强
    ADD_BULLET_DAMAGE_LOOP = pygame.USEREVENT + 7
    pygame.time.set_timer(ADD_BULLET_DAMAGE_LOOP, ADD_BULLET_DAMAGE_LOOP_TIME)

    
    #定义游戏状态
    running = True
    game_going = True

    #初始化游戏提示UI
    prompt_ui = GamePrompt(gui_group)
    gameover_ui = GameOverUI(gui_group)
    score_ui = GameScore(gui_group)

    #初始化时间
    clock = pygame.time.Clock()
    # fps_ui = GameFps(gui_group, clock=clock)
    timer_ui = GameTimer(gui_group)
    timer_ui.start()
    while running:
        clock.tick_busy_loop(FPS)
        #绘制背景
        screen.blit(background,(0,0))
        
        #获取事件
        for event in pygame.event.get():
            #处理关闭事件
            if event.type == pygame.QUIT:
                running = False
                pygame.mixer.stop()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #按ESC键退出游戏
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                if event.key == pygame.K_SPACE:
                    #按空格SPACE键使用核弹清屏
                    bomb_supply.use_bomb(score_ui)
                if event.key == pygame.K_f:
                    #调试用
                    # bullet_supply.start()
                    # bomb_supply.use_bomb(score_ui)
                    prompt_ui.show("楷体，游戏结束，扫码上传成绩")
            elif event.type == INCREASE_DIFFICULTY:
                #每xx秒提升难度，中、大敌机血量加1
                if game_going:
                    for e in mid_enemy_list:
                        e.increase_difficulty(int(e.hp_max*0.1))
                    for e in big_enemy_list:
                        e.increase_difficulty(int(e.hp_max*0.1))
                    # upgrade_sound.play()
                    # prompt_ui.show("increase difficulty!")
                # print(int(clock.get_fps()))
            elif event.type == DOUBLE_BULLET:
                #获得子弹强化
                upgrade_sound.play()
                bullet_supply.start()
                pygame.time.set_timer(DOUBLE_BULLET, 0)
            elif event.type == FIVE_BULLET:
                upgrade_sound.play()
                bullet_supply.start()
                pygame.time.set_timer(FIVE_BULLET, 0)
            elif event.type == SEVEN_BULLET:
                upgrade_sound.play()
                bullet_supply.start()
                pygame.time.set_timer(SEVEN_BULLET, 0)
            elif event.type == ADD_BULLET_SPEED:
                upgrade_sound.play()
                bullet_supply.start()
                pygame.time.set_timer(ADD_BULLET_SPEED, 0)
            elif event.type == ADD_BULLET_DAMAGE:
                upgrade_sound.play()
                bullet_supply.start()
                pygame.time.set_timer(ADD_BULLET_DAMAGE, ADD_BULLET_DAMAGE_LOOP_TIME)
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
                pygame.time.set_timer(FIVE_BULLET, FIVE_BULLET_TIME)
                pygame.time.set_timer(SEVEN_BULLET, SEVEN_BULLET_TIME)
                pygame.time.set_timer(ADD_BULLET_SPEED, ADD_BULLET_SPEED_TIME)
                pygame.time.set_timer(ADD_BULLET_DAMAGE, ADD_BULLET_DAMAGE_TIME)
                #5.重置score_ui
                score_ui.restart()
                #6.核弹清零
                bomb_supply.bomb_num = 0
                bomb_supply.kill()
                #7.重置补给
                bullet_supply.kill()
        
        #判断游戏进行状态
        if not game_going:
            #游戏结束，显示结束UI
            gameover_ui.show()

        #更新状态
        player_group.update()
        enemy_group.update()
        gui_group.update()
        bullet_supply.update()
        bomb_supply.update()
        
        
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
                    #被攻击时绘制血条
                    if not type(e) is SmallEnemyPlane:
                        e.draw_hp_line(screen)
                    #计算分数
                    if not e.is_alive:
                        score_ui.add_score(e.hp_max)
                        #击毁大型敌机，获得核弹*1
                        if type(e) is BigEnemyPlane:
                            upgrade_sound.play()
                            bomb_supply.start()
            #子弹补给碰撞检测
            if bullet_supply.alive():
                if pygame.sprite.collide_mask(p, bullet_supply):
                    bullet_supply_col(p, bullet_supply)
            #核弹补给碰撞检测
            if bomb_supply.alive():
                if pygame.sprite.collide_mask(p, bomb_supply):
                    bomb_supply.get_supply()
        
        #绘制图像
        #先画大型敌机
        for e in big_enemy_list:
            if e.alive():
                if e.rect.bottom > 0:
                    e.add(all_visible_group)
        for e in mid_enemy_list:
            if e.alive():
                if e.rect.bottom > 0:
                    e.add(all_visible_group)
        for e in small_enemy_list:
            if e.alive():
                if e.rect.bottom > 0:
                    e.add(all_visible_group)
        all_visible_group.add(player_group, player.bullet_group)
        all_visible_group.draw(screen)
        gui_group.draw(screen)
        #绘制全屏炸弹数量
        bomb_text=bomb_font.render('× %d' % (bomb_supply.bomb_num),True, (255, 255, 255))
        text_rect=bomb_text.get_rect()
        screen.blit(bomb_image,(10,SCREEN_HEIGHT-10-bomb_rect.height))
        screen.blit(bomb_text,(20+bomb_rect.width,SCREEN_HEIGHT-5-text_rect.height))
        pygame.display.update()
        
    pygame.quit()

if __name__ == "__main__":
    main()
    # app = Game()
    # app.start()