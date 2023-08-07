import pygame
from const import *
from airplane import *

def main():
    pygame.init()

    screen_width, screen_height = screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen=pygame.display.set_mode(screen_size)

    pygame.display.set_caption('飞机大战—Demo')
    screen_rect = screen.get_rect()

    #加载图片资源
    background=pygame.image.load('images/background.png')

    me_alive_frames = []
    for i in range(2):
        img = pygame.image.load('images/me%s.png' % str(i+1)).convert_alpha()
        me_alive_frames.append(img)
    me_dead_frames = []
    for i in range(4):
        img = pygame.image.load('images/me_destroy_%s.png' % str(i+1)).convert_alpha()
        me_dead_frames.append(img)
    enemy_s_alive_frames = []
    img = pygame.image.load('images/enemy1.png').convert_alpha()
    enemy_s_alive_frames.append(img)
    enemy_s_dead_frames = []
    for i in range(4):
        img = pygame.image.load('images/enemy1_down%s.png' % str(i+1))
        enemy_s_dead_frames.append(img)
    
    #创建Sprite组对象
    all_sprite_groups = pygame.sprite.Group()
    player_groups = pygame.sprite.Group()
    enemy_groups = pygame.sprite.Group()
    destroy_groups = pygame.sprite.Group()

    #创建Sprite对象
    player = Airplane(me_alive_frames, is_enemy=False)
    player.add(player_groups, all_sprite_groups)
    player.rect.midbottom = screen_rect.midbottom

    for i in range(10):
        enemy_s = Airplane(enemy_s_alive_frames)
        enemy_s.add(enemy_groups, all_sprite_groups)

    #加载声音资源
    pygame.mixer.music.load("sound/game_music.ogg")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    clock=pygame.time.Clock()

    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)


    i = 0
    f = pygame.font.SysFont(None, 30)
    fps_text = f.render("FPS:%s" % i, True, (255, 0, 0))
    fps_rect = fps_text.get_rect(topleft=(0, 0))
    screen.blit(fps_text, fps_rect)
    TIMER_1 = pygame.USEREVENT
    pygame.time.set_timer(TIMER_1, 1000)

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
        all_sprite_groups.update()
        destroy_groups.update()
        #绘制图像
        screen.blit(background,(0,0))
        all_sprite_groups.draw(screen)
        destroy_groups.draw(screen)
        screen.blit(fps_text, fps_rect)
        
        pygame.display.update()
        i += 1

    pygame.quit()

if __name__ == "__main__":
    main()