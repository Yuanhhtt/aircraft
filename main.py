import pygame
import sys, os, uuid, json, base64, rsa, qrcode
from const import *
from airplane import *
from gui import *

class GameManage:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF | pygame.HWSURFACE)
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption(f"{GAME_TITLE}--{GAME_VERSION}")
        #设置鼠标键盘
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        pygame.key.stop_text_input()
        #加载背景音乐
        pygame.mixer.init()
        pygame.mixer.set_reserved(1)
        pygame.mixer.set_reserved(2)
        pygame.mixer.music.load("sound/game_music.ogg")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
        #获取用户信息
        self.userinfo = {}
        self.get_userinfo()
        #背景动画
        self.bg_group = pygame.sprite.OrderedUpdates()
        self.bg_sprites = [BGSprite(self.bg_group, (0, 0)), BGSprite(self.bg_group, (0, -SCREEN_HEIGHT))]
        #UI精灵组
        self.gui_group = pygame.sprite.OrderedUpdates()
        self.timer_ui = GameTimer(self.gui_group)
        self.score_ui = GameScore(self.gui_group)
        self.username_ui = GameUser(self.gui_group, self.userinfo["name"])
        self.bomb_ui = BombUI(self.gui_group)
        self.bomb_icon = Bomb_Icon(self.gui_group)
        self.gameover_ui = GameOverUI(self.gui_group)
        #玩家飞机精灵
        self.player_group = pygame.sprite.OrderedUpdates()
        self.player = HeroPlane(self.player_group, self.screen_rect.midbottom)
        #敌机精灵组
        ##生成小型敌机
        self.small_enemy_group = pygame.sprite.OrderedUpdates()
        self.small_enemy_list = [SmallEnemyPlane(self.small_enemy_group) for i in range(SMALL_ENEMY_NUM)]
        ##生成中型敌机
        self.mid_enemy_group = pygame.sprite.OrderedUpdates()
        self.mid_enemy_list = [MidEnemyPlane(self.mid_enemy_group) for i in range(MID_ENEMY_NUM)]
        ##生成大型敌机
        self.big_enemy_group = pygame.sprite.OrderedUpdates()
        self.big_enemy_list = [BigEnemyPlane(self.big_enemy_group) for i in range(BIG_ENEMY_NUM)]
        #补给组
        self.supply_group = pygame.sprite.OrderedUpdates()
        ##生成子弹补给
        self.bullet_supply = BulletSupply(self.supply_group)
        ##生成核弹补给
        self.bomb_supply = BombSupply(self.supply_group)
        #设置游戏状态
        self.status = GAME_STATUS.START
        #开始计时
        self.init_timer()
        self.clock = pygame.time.Clock()
        self.timer_ui.start()
    
    def init_timer(self):
        pygame.time.set_timer(INCREASE_DIFFICULTY, INCREASE_DIFFICULTY_TIME)
        pygame.time.set_timer(DOUBLE_BULLET, DOUBLE_BULLET_TIME)
        pygame.time.set_timer(FIVE_BULLET, FIVE_BULLET_TIME)
        pygame.time.set_timer(SEVEN_BULLET, SEVEN_BULLET_TIME)
        pygame.time.set_timer(ADD_BULLET_SPEED, ADD_BULLET_SPEED_TIME)
        pygame.time.set_timer(ADD_BULLET_DAMAGE, ADD_BULLET_DAMAGE_TIME)
        pygame.time.set_timer(ADD_BIG_ENEMY, ADD_BIG_ENEMY_TIME)

    def check_event(self):
        for event in pygame.event.get():
            #处理关闭事件
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                #按ESC键退出游戏
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                if event.key == pygame.K_SPACE:
                    #按空格SPACE键使用核弹清屏
                    self.bomb_ui.use_bomb(self.score_ui, self.screen_rect, self.big_enemy_list, self.mid_enemy_list, self.small_enemy_list)
            elif event.type == RESTART_GAME:
                self.restart()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.bomb_ui.use_bomb(self.score_ui, self.screen_rect, self.big_enemy_list, self.mid_enemy_list, self.small_enemy_list)
            elif event.type == INCREASE_DIFFICULTY:
                #每xx秒提升难度，中、大敌机血量加1
                if self.status == GAME_STATUS.START:
                    for e in self.mid_enemy_list:
                        e.increase_difficulty(int(e.hp_max*0.1))
                    for e in self.big_enemy_list:
                        e.increase_difficulty(int(e.hp_max*0.1))
            elif event.type == ADD_BIG_ENEMY:
                self.big_enemy_list.append(BigEnemyPlane(self.big_enemy_group, hp_max=self.big_enemy_list[0].hp_max))
                pygame.time.set_timer(ADD_BIG_ENEMY, ADD_BIG_ENEMY_LOOP_TIME)
                self.bg_sprites[0].add_speed()
                self.bg_sprites[1].add_speed()
                for e in self.small_enemy_list:
                    e.speed += 1
                for e in self.mid_enemy_list:
                    e.speed += 1
                for e in self.big_enemy_list:
                    e.speed += 1
                self.bomb_supply.speed += 1
                self.bullet_supply.speed += 1
            elif event.type == DOUBLE_BULLET:
                #获得子弹强化
                self.bullet_supply.start()
                pygame.time.set_timer(DOUBLE_BULLET, 0)
                self.mid_enemy_list.append(MidEnemyPlane(self.mid_enemy_group, hp_max=self.mid_enemy_list[0].hp_max))
            elif event.type == FIVE_BULLET:
                self.bullet_supply.start()
                pygame.time.set_timer(FIVE_BULLET, 0)
                self.mid_enemy_list.append(MidEnemyPlane(self.mid_enemy_group, hp_max=self.mid_enemy_list[0].hp_max))
            elif event.type == SEVEN_BULLET:
                self.bullet_supply.start()
                pygame.time.set_timer(SEVEN_BULLET, 0)
                self.mid_enemy_list.append(MidEnemyPlane(self.mid_enemy_group, hp_max=self.mid_enemy_list[0].hp_max))
            elif event.type == ADD_BULLET_SPEED:
                self.bullet_supply.start()
                pygame.time.set_timer(ADD_BULLET_SPEED, 0)
                self.mid_enemy_list.append(MidEnemyPlane(self.mid_enemy_group, hp_max=self.mid_enemy_list[0].hp_max))
            elif event.type == ADD_BULLET_DAMAGE:
                self.bullet_supply.start()
                pygame.time.set_timer(ADD_BULLET_DAMAGE, ADD_BULLET_DAMAGE_LOOP_TIME)
                self.mid_enemy_list.append(MidEnemyPlane(self.mid_enemy_group, hp_max=self.mid_enemy_list[0].hp_max))
    
    def bullet_supply_col(self, player : HeroPlane):
        self.bullet_supply.get_supply()
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
        player.buullet_damage = self.big_enemy_list[0].hp_max // (50 * 7 * 2)
        return

    def player_collide_check(self):
        for p in self.player_group.sprites():
             #player与敌机之间的碰撞检测
            collided_list = pygame.sprite.spritecollide(p, self.small_enemy_group, False, collided=pygame.sprite.collide_mask)
            collided_list = collided_list + pygame.sprite.spritecollide(p, self.mid_enemy_group, False, collided=pygame.sprite.collide_mask)
            collided_list = collided_list + pygame.sprite.spritecollide(p, self.big_enemy_group, False, collided=pygame.sprite.collide_mask)
            if collided_list:
                #机毁人亡，游戏结束
                self.timer_ui.stop()
                p.destroy()
                for col_enemy in collided_list:
                    col_enemy.destroy()
                self.status = GAME_STATUS.STOP
            
            #player与补给碰撞检测
            if self.bullet_supply.alive():
                if pygame.sprite.collide_mask(p, self.bullet_supply):
                    self.bullet_supply_col(p)

            #核弹补给碰撞检测
            if self.bomb_supply.alive():
                if pygame.sprite.collide_mask(p, self.bomb_supply):
                    self.bomb_supply.get_supply(self.bomb_ui)

    def bullet_collide_check(self):
        #子弹与敌机之间的碰撞检测
        collided_dict = pygame.sprite.groupcollide(self.player.bullet_group, self.small_enemy_group, True, False, collided=pygame.sprite.collide_mask)
        for b in collided_dict.keys():
            for e in collided_dict[b]:
                e.be_hit(self.player.buullet_damage)
                if not e.is_alive:
                    self.score_ui.add_score(1)
        collided_dict = pygame.sprite.groupcollide(self.player.bullet_group, self.mid_enemy_group, True, False, collided=pygame.sprite.collide_mask)
        for b in collided_dict.keys():
            for e in collided_dict[b]:
                e.be_hit(self.player.buullet_damage)
                if not e.is_alive:
                    self.score_ui.add_score(3)
                else:
                    #绘制血条
                    self.draw_hp_line(e)
        collided_dict = pygame.sprite.groupcollide(self.player.bullet_group, self.big_enemy_group, True, False, collided=pygame.sprite.collide_mask)
        for b in collided_dict.keys():
            for e in collided_dict[b]:
                e.be_hit(self.player.buullet_damage)
                if not e.is_alive:
                    self.score_ui.add_score(10)
                    self.bomb_supply.start()
                else:
                    #绘制血条
                    self.draw_hp_line(e)

    def get_userinfo(self):
        #获取MAC_ID
        self.userinfo["mac_id"] = hex(uuid.getnode()).upper()[2:]
        #检测"config.json"文件是否存在
        config_file = "config.json"
        if os.path.exists(config_file):
            with open(config_file, "r", encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except Exception as e:
                    f.close()
                    os.remove(config_file)
                    self.userinfo["name"]= os.getlogin()
                    return
            self.userinfo["name"] = data["name"].encode()[:12].decode()
        else:
            #使用系统用户名
            self.userinfo["name"] = os.getlogin().encode()[:12].decode()
            #写入"config.json"文件
            with open(config_file, "w", encoding='utf-8') as f:
                json.dump({"name" : self.userinfo["name"]}, f, ensure_ascii=False)

    def encrypt(self, message: str):
        with open("s_public.pem") as f:
            p = f.read()
        pubkey = rsa.PublicKey.load_pkcs1(p)
        c = rsa.encrypt(message.encode(), pubkey)
        c_text = base64.b32encode(c)
        return c_text.decode()

    def stop(self):
        #对mac_id, name, duration, score进行加密,返回密文
        m = f'{self.userinfo["mac_id"]};{self.userinfo["name"]};{self.timer_ui.duration()};{self.score_ui.score}'
        c = self.encrypt(m)
        url = f'http://www.autojy.fun/aircraft/submit?c={c}'
        # print(url)
        #使用url生成QRCODE二维码图片，传给self.gameover_ui.show()
        os.remove('images/qrcode.png')
        qr = qrcode.QRCode(box_size=5 ,border=2)
        qr.add_data(url)
        qr.make()
        img = qr.make_image(fill_color = 'green', back_color = 'white')
        img.save('images/qrcode.png')
        self.gameover_ui.show()
    
    def restart(self):
        #1.重置BG speed
        self.bg_sprites[0].speed = FLY_SPEED
        self.bg_sprites[1].speed = FLY_SPEED
        #2.重置palyer
        self.player.restart()
        #3.重置敌机
        for e in self.small_enemy_list:
            e.restart()
        for i in range(len(self.mid_enemy_list) - MID_ENEMY_NUM):
            self.mid_enemy_list.pop().kill()
        for e in self.mid_enemy_list:
            e.restart()
        for i in range(len(self.big_enemy_list) - BIG_ENEMY_NUM):
            self.big_enemy_list.pop().kill()
        for e in self.big_enemy_list:
            e.restart()
        #4.重置score_ui
        self.score_ui.restart()
        #5.核弹清零
        self.bomb_ui.bomb_num = 0
        self.bomb_supply.kill()
        self.bomb_supply.speed = SUPPLY_SPEED
        #6.重置子弹补给
        self.bullet_supply.kill()
        self.bullet_supply.speed = SUPPLY_SPEED
        #7.重置定时器
        self.init_timer()
        #8.删除上次生成的二维码图片
        pass
        #9.重新开始计时
        self.timer_ui.start()
        #10.重置游戏状态
        self.status = GAME_STATUS.START

    def draw_hp_line(self, enemy):
        line_width = enemy.rect.width - 20
        line_height = 5
        line_y = enemy.rect.y + enemy.rect.height - 5
        point_a = (enemy.rect.x + 10, line_y)
        point_b = (enemy.rect.x + enemy.rect.width - 10, line_y)
        line_color = (0, 0, 0)

        pygame.draw.line(self.screen, line_color, point_a, point_b, line_height)
        remain = enemy.hp / enemy.hp_max
        if remain > 0.3:
            line_color = (0, 255, 0)
        else:
            line_color = (255, 0, 0)
        point_c = (point_a[0] + int(line_width*remain), line_y)
        pygame.draw.line(self.screen, line_color, point_a, point_c, line_height)

    def run(self):
        while True:
            #设置帧率
            self.clock.tick(FPS)
            #事件检测
            self.check_event()
            #结束状态判断
            if self.status == GAME_STATUS.STOP:
                #游戏结束
                self.stop()
                self.status = GAME_STATUS.SHOW_QR
            #更新
            self.bg_group.update()
            self.big_enemy_group.update()
            self.mid_enemy_group.update()
            self.small_enemy_group.update()
            self.player_group.update()
            self.supply_group.update()
            self.gui_group.update()

            #绘制背景
            self.bg_group.draw(self.screen)
            #碰撞检测
            self.player_collide_check()
            self.bullet_collide_check()
            #绘制
            self.big_enemy_group.draw(self.screen)
            self.mid_enemy_group.draw(self.screen)
            self.small_enemy_group.draw(self.screen)
            self.player_group.draw(self.screen)
            self.supply_group.draw(self.screen)
            self.player.bullet_group.draw(self.screen)
            self.gui_group.draw(self.screen)
            pygame.display.flip()
            
if __name__ == "__main__":
    app = GameManage()
    app.run()