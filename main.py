import pygame
from pygame import mouse
from const import *
from airplane import *
from bullet import *

def main():
    pygame.init()

    screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen=pygame.display.set_mode(screen_size)

    pygame.display.set_caption('飞机大战—Demo')
    screen_rect = screen.get_rect()

    #加载图片资源
    background=pygame.image.load(IMAGE_PATH['background'])

    me_alive_frames = []
    for i in IMAGE_PATH['player']:
        me_alive_frames.append(pygame.image.load(i).convert_alpha())
    me_dead_frames = []
    for i in IMAGE_PATH['player_destroy']:
        me_dead_frames.append(pygame.image.load(i).convert_alpha())
    enemy_s_alive_frames = []
    for i in IMAGE_PATH['enemy_small']:
        enemy_s_alive_frames.append(pygame.image.load(i).convert_alpha())
    enemy_s_dead_frames = []
    for i in IMAGE_PATH['enemy_small_destroy']:
        enemy_s_dead_frames.append(pygame.image.load(i).convert_alpha())
    bullet_red_img = pygame.image.load(IMAGE_PATH['bullet_red']).convert_alpha()
    bullet_blue_img = pygame.image.load(IMAGE_PATH['bullet_blue']).convert_alpha()

    #创建Sprite组对象
    # all_sprite_groups = pygame.sprite.Group()
    player_groups = pygame.sprite.Group()
    enemy_groups = pygame.sprite.Group()
    destroy_groups = pygame.sprite.Group()
    bullet_groups = pygame.sprite.Group()

    #创建Sprite对象
    ##创建player
    player = Airplane(me_alive_frames, is_enemy=False)
    player.add(player_groups)
    player.rect.midbottom = screen_rect.midbottom
    ##创建enemy_small
    for i in range(10):
        enemy_groups.add(Airplane(enemy_s_alive_frames))
        
    ##创建bullet
    bullets = []
    for i in range(5):
        bullets.append(Bullet(bullet_red_img))
  
    #加载声音资源
    pygame.mixer.music.load("sound/game_music.ogg")
    pygame.mixer.music.set_volume(0.2)
    bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
    bullet_sound.set_volume(0.2)
    pygame.mixer.music.play(-1)
    

    clock=pygame.time.Clock()

    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)


    f = pygame.font.SysFont(None, 30)
    fps_text = f.render("FPS:%s" % i, True, (255, 0, 0))
    fps_rect = fps_text.get_rect(topleft=(0, 0))
    screen.blit(fps_text, fps_rect)
    TIMER_1 = pygame.USEREVENT
    pygame.time.set_timer(TIMER_1, 1000)

    delay = 100
    running = True
    while running:
        clock.tick(60)
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
            elif event.type == pygame.MOUSEMOTION:
                # print(event.pos, event.rel)
                if 0 <= player.rect.midbottom[0] + event.rel[0] <= 480 and player.rect.height <= player.rect.midbottom[1] + event.rel[1] <= 700:
                    player.rect.midbottom = (player.rect.midbottom[0] + event.rel[0], player.rect.midbottom[1] + event.rel[1])
            elif event.type == TIMER_1:
                pass
                # print(int(clock.get_fps()))
        
        #检测鼠标输入
        mouse_rel = pygame.mouse.get_rel()
        x = player.rect.midbottom[0] + mouse_rel[0]
        y = player.rect.midbottom[1] + mouse_rel[1]
        if 0 <= x <= SCREEN_WIDTH and player.rect.height <= y <= SCREEN_HEIGHT:
            player.rect.midbottom = (x, y)
        
        #发射子弹
        if not(delay % 10):
            for b in bullets:
                if b.active == False:
                    b.reset(player.rect.midtop)
                    bullet_groups.add(b)
                    bullet_sound.play()
                    break
        #碰撞检测
        players = player_groups.sprites()
        for p in players:
            collided_list = pygame.sprite.spritecollide(p, enemy_groups, True, collided=pygame.sprite.collide_mask)
            if collided_list:
                p.hp -= 1
                p.kill()
                destroy_groups.add(DestroyAirplane(me_dead_frames, p.rect))
                for enemy in collided_list:
                    enemy.hp -= 1
                    destroy_groups.add(DestroyAirplane(enemy_s_dead_frames, enemy.rect))

        #更新状态
        ticks = pygame.time.get_ticks()
        seconds = ticks // 1000 % 60
        minutes = ticks // 60000 % 60
        hours = ticks // 3600000
        fps_text = f.render("%02d:%02d:%02d" % (hours, minutes, seconds), True, (255, 0, 0))
        player_groups.update()
        # enemy_groups.update()
        destroy_groups.update()
        bullet_groups.update()
        #绘制图像
        screen.blit(background,(0,0))
        player_groups.draw(screen)
        # enemy_groups.draw(screen)
        destroy_groups.draw(screen)
        bullet_groups.draw(screen)
        screen.blit(fps_text, fps_rect)
        
        pygame.display.update()
        delay -= 1
        if delay == 0:
            delay = 100

    pygame.quit()

if __name__ == "__main__":
    main()