# import modules
import pygame
from pygame.locals import *
from sys import exit
import os
from random import randint

pygame.init()
pygame.mixer.init()
pygame.font.init()

WIDTH = pygame.display.get_desktop_sizes()[0][0]
HEIGHT = pygame.display.get_desktop_sizes()[0][1]

def loading_screen(callback):
    loading_screen = pygame.display.set_mode((800, 600), NOFRAME)
    current = 0
    font = pygame.font.SysFont("Cosmic Sans", 30) 

    word = "Loading game data..."

    while True:
        red_rect = pygame.Rect(400-350, 400, 680, 30)
        green_rect = pygame.Rect(400-350, 400, current, 30)
        text = font.render(word, 0, (160, 100, 50))
        loading_screen.fill((10, 10, 10))
        pygame.draw.rect(loading_screen, (255, 0, 0), red_rect)
        pygame.draw.rect(loading_screen, (0, 255, 0), green_rect)
        loading_screen.blit(text, (400-(text.get_width()//2), 350))
        current+=20
        if current == 100:
            word = "Creating Spaceships..."
        elif current == 300:
            word = "Loading background..."
        elif current == 400:
            word = "Creating bullets..."
        elif current > 700:
            pygame.time.delay(2000)
            callback()
        
        pygame.time.delay(100)
        pygame.display.update()

def main():
    window = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN, 32)
    pygame.display.set_caption("Space Fighter")
    pygame.display.set_icon(pygame.image.load(os.path.join("assets","you.png")))
    background = pygame.mixer.Sound(os.path.join("assets", "back.crdownload"))
    background.play()
    
    # function to run one player
    def ai():
        pygame.display.set_caption("Space Fighters")
        pygame.display.set_icon(pygame.image.load(os.path.join("assets", "you.png")))
    
        # set constants
        FPS = 100
        PLAYER_VEL = 13
        AI_VEL = 11
        screen = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN, 32)
        clock = pygame.time.Clock()
        border = pygame.Rect((WIDTH//2)-10, 0, 10, HEIGHT)
        your_bullets = []
        enemy_bullets = []
        max_bullets = 7
        full_health = 200
        background = pygame.mixer.Sound(os.path.join("assets", "back.crdownload"))
        shoot = pygame.mixer.Sound(os.path.join("assets", "laser gun.wav"))
        hit = pygame.mixer.Sound(os.path.join("assets", "explosion.wav"))
        lose = pygame.mixer.Sound(os.path.join("assets", "Game over.wav"))
        font = pygame.font.SysFont("Consolas", 30)
        joysticks = []
    
        YOU_HIT = USEREVENT + 1
        ENEMY_HIT = USEREVENT + 2
    
        background.play()

        joy = pygame.joystick.Joystick(0)
        joy.init()
        joysticks.append(joy)
    
        # function to animate pixels
        def pixels():
            for _ in range(20):
               rand_col = (randint(0, 255), randint(0, 255), randint(0, 255))
               rand_pos = (randint(0, 1199), randint(0, 599))
               rand_col2 = (randint(0, 255), randint(0, 255), randint(0, 255))
               rand_pos2 = (randint(0, 1199), randint(0, 599))
               screen.set_at(rand_pos, rand_col)
               screen.set_at(rand_pos2, rand_col2)
        
        # function to handle bullets
        def bullets(your_bullets, enemy_bullets, you_rect, enemy_rect):
            for i in your_bullets:
                i.x -= 20
                if enemy_rect.colliderect(i):
                    your_bullets.remove(i)
                    pygame.event.post(pygame.event.Event(ENEMY_HIT))
                if i.x < 0:
                    your_bullets.remove(i)
            
            for i in enemy_bullets:
                i.x += 20
                if you_rect.colliderect(i):
                    enemy_bullets.remove(i)
                    pygame.event.post(pygame.event.Event(YOU_HIT))
                if i.x > WIDTH:
                    enemy_bullets.remove(i)
            
            for i in your_bullets:
                for j in enemy_bullets:
                    if i.colliderect(j):
                        your_bullets.remove(i)
                    if j.colliderect(i):
                        enemy_bullets.remove(j)
    
        # create character class
        class Player():
            def __init__(self, name, x, y):
                img = pygame.image.load(os.path.join("assets", f"{name}.png"))
                self.img = pygame.transform.scale(img, (img.get_width()//2, img.get_height()//2))
                self.you_rect = pygame.Rect(x, y, self.img.get_width(), self.img.get_height())
                self.enemy_rect = pygame.Rect(x, y, self.img.get_width(), self.img.get_height())
    
            # functions to draw characters
            def draw_you(self):
                screen.blit(self.img, (self.you_rect.x, self.you_rect.y))
                for i in your_bullets:
                    pygame.draw.rect(screen, (100, 255, 100), i)
            def draw_enemy(self):
                screen.blit(self.img, (self.enemy_rect.x, self.enemy_rect.y))
                for i in enemy_bullets:
                    pygame.draw.rect(screen, (140, 100, 140), i)
            
            # function to move character
            def move_you(self):
                key = pygame.key.get_pressed()
    
                # condition to keep the characters in the screen
                if key[K_RIGHT]:
                    self.you_rect.x += PLAYER_VEL
                    self.enemy_rect.x += AI_VEL
                    if self.you_rect.x + PLAYER_VEL > (WIDTH-self.img.get_width())+15:
                        self.you_rect.x -= PLAYER_VEL
                    if self.enemy_rect.x + AI_VEL > (border.x-self.img.get_width())+15:
                        self.enemy_rect.x -= AI_VEL
    
                if key[K_LEFT]:
                    self.you_rect.x -= PLAYER_VEL
                    self.enemy_rect.x -= AI_VEL
                    if self.you_rect.x - PLAYER_VEL < border.x:
                        self.you_rect.x += PLAYER_VEL
                    if self.enemy_rect.x - AI_VEL < 0-15:
                        self.enemy_rect.x += AI_VEL
                
                if key[K_UP]:
                    self.you_rect.y -= PLAYER_VEL
                    self.enemy_rect.y -= AI_VEL
                    if self.you_rect.y - PLAYER_VEL < (0-15):
                        self.you_rect.y += PLAYER_VEL
                    if self.enemy_rect.y - AI_VEL < (0-10):
                        self.enemy_rect.y += AI_VEL
                
                if key[K_DOWN]:
                    self.you_rect.y += PLAYER_VEL
                    self.enemy_rect.y += AI_VEL
                    if self.you_rect.y + PLAYER_VEL > (HEIGHT-self.img.get_height())+11:
                        self.you_rect.y -= PLAYER_VEL
                    if self.enemy_rect.y + AI_VEL > (HEIGHT-self.img.get_height())+11:
                        self.enemy_rect.y -= AI_VEL
            
            # function for joystick
            def joystick_movement(self, list_of_joysticks):
                for joystick in list_of_joysticks:
                    horiz_move = joystick.get_axis(0)
                    vert_move = joystick.get_axis(1)
                    if abs(vert_move) > 0.05:
                        self.you_rect.y += vert_move * 20
                        self.enemy_rect.y += vert_move * 18

                        if self.you_rect.y + vert_move * 20 < (0-15):
                            self.you_rect.y -= vert_move * 20
                        if self.enemy_rect.y + vert_move * 18 < (0-10):
                            self.enemy_rect.y -= vert_move * 18
                        
                        if self.you_rect.y +vert_move * 20 > (HEIGHT-self.img.get_height())+11:
                            self.you_rect.y -= vert_move * 20
                        if self.enemy_rect.y + vert_move * 18 > (HEIGHT-self.img.get_height())+11:
                            self.enemy_rect.y -= vert_move * 18
                        
                    if abs(horiz_move) > 0.05:
                        self.you_rect.x += horiz_move * 20
                        self.enemy_rect.x += horiz_move * 18

                        if self.you_rect.x + horiz_move * 20 > (WIDTH-self.img.get_width())+15:
                            self.you_rect.x -= horiz_move * 20
                        if self.enemy_rect.x + horiz_move * 18 > (border.x-self.img.get_width())+15:
                            self.enemy_rect.x -= horiz_move * 18
                        
                        if self.you_rect.x + horiz_move * 20 < border.x:
                            self.you_rect.x -= horiz_move * 20
                        if self.enemy_rect.x + horiz_move * 18 < 0-15:
                            self.enemy_rect.x -= horiz_move * 18
            
        class Health():
            def __init__(self, x, y, max_hp, hp):
                self.x = x
                self.y = y
                self.max_hp = max_hp
                self.hp = hp
                
            def draw(self):
                green = (0, 255, 0)
                red = (255, 0, 0)
                hp = self.hp/self.max_hp * 200
                pygame.draw.rect(screen, red, pygame.Rect(self.x, self.y, self.max_hp, 20))
                pygame.draw.rect(screen, green, pygame.Rect(self.x, self.y, hp, 20))
    
        
        # define character and health and text
        you = Player("you", border.x + WIDTH//4, HEIGHT//2)
        enemy = Player("enemy", WIDTH//4, HEIGHT//2)
        you_text = font.render("YOU :", 1, (0, 255, 0))
        enemy_text = font.render("ENEMY :", 1, (255, 0, 255))
        your_health = Health(border.x + you_text.get_width() + 30, 10, full_health, full_health)
        enemy_health = Health(enemy_text.get_width() + 20, 10, full_health, full_health)
    
        # loop for events and draw characters 
        while True:
            # fill the screen with a background
            screen.blit(pygame.transform.scale(pygame.image.load(os.path.join("assets", "Background.png")), (WIDTH, HEIGHT)), (0, 0))
            
            # listen for events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYUP and event.key == K_ESCAPE:
                    background.stop()
                    main()
                if event.type == KEYDOWN:
                    if event.key == K_LCTRL and len(your_bullets) < max_bullets and len(enemy_bullets) < max_bullets:
                        shoot.play(1)
                        rect = pygame.Rect(you.you_rect.x, you.you_rect.y + you.you_rect.height//2, 15, 7)
                        your_bullets.append(rect)
                        rect2 = pygame.Rect(enemy.enemy_rect.x + enemy.enemy_rect.width, enemy.enemy_rect.y + enemy.enemy_rect.height//2, 15, 7)
                        enemy_bullets.append(rect2)
                if event.type == YOU_HIT:
                    hit.play()
                    your_health.hp -= 5
                if event.type == ENEMY_HIT:
                    hit.play()
                    enemy_health.hp -= 5
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                
            # loop for joystick shooting
            for joystick in joysticks:
                if joystick.get_button(15)  and len(your_bullets) < max_bullets and len(enemy_bullets) < max_bullets:
                    shoot.play(1)
                    rect = pygame.Rect(you.you_rect.x, you.you_rect.y + you.you_rect.height//2, 15, 7)
                    your_bullets.append(rect)
                    rect2 = pygame.Rect(enemy.enemy_rect.x + enemy.enemy_rect.width, enemy.enemy_rect.y + enemy.enemy_rect.height//2, 15, 7)
                    enemy_bullets.append(rect2)
            
            # draw character and border and bullets and health bar and text
            your_health.draw()
            enemy_health.draw()
            pygame.draw.rect(screen, (255, 255, 255), border)
            bullets(your_bullets, enemy_bullets, you.you_rect, enemy.enemy_rect)
            you.move_you()
            you.draw_you()
            you.joystick_movement(joysticks)
            enemy.draw_enemy()
            enemy.move_you()
            enemy.joystick_movement(joysticks)
            screen.blit(you_text, (border.x + 20, 10))
            screen.blit(enemy_text, (10, 10))
             
            #call the animation
            pixels()
    
            if your_health.hp <= 0:
                lose.play()
                your_bullets = []
                enemy_bullets = []
                pygame.event.set_blocked(KEYDOWN)
                pygame.event.set_allowed([MOUSEMOTION,MOUSEBUTTONDOWN])
                restart = pygame.Rect(WIDTH//2-200, HEIGHT//2-100, 400, 200)
                font = pygame.font.SysFont("ebrima", 23)
                text = font.render("Would you like to restart", 1, (100, 110, 120))
                text2 = font.render("YES", 1, (0, 0, 0), (12, 110, 120))
                text3 = font.render("NO", 1, (0, 0, 0), (12, 110, 120))
                winner = font.render("  YOU LOST!! ", 1, (255, 255, 255), (0, 0, 0))
                mouse = pygame.mouse.get_pressed()
                if mouse[0]:
                    if pygame.mouse.get_pos()[0] > 521 and pygame.mouse.get_pos()[0] < 549:
                        pygame.event.set_allowed(KEYDOWN)
                        background.stop()
                        ai()
                    if pygame.mouse.get_pos()[0] > 786 and pygame.mouse.get_pos()[0] <  815:
                        main()
                
                screen.blit(winner, (border.x-(winner.get_width()//2), 0))
                pygame.draw.rect(screen, (0, 0, 0), restart)
                screen.blit(text, (restart.x+ 70, restart.y+20))
                screen.blit(text2, (restart.x+ 35, restart.y+100))
                screen.blit(text3, (restart.x+ 300, restart.y+100))
            elif enemy_health.hp <= 0:
                your_bullets = []
                enemy_bullets = []
                pygame.event.set_blocked(KEYDOWN)
                pygame.event.set_allowed([MOUSEMOTION,MOUSEBUTTONDOWN])
                restart = pygame.Rect(WIDTH//2-200, HEIGHT//2-100, 400, 200)
                font = pygame.font.SysFont("ebrima", 23)
                text = font.render("Would you like to restart", 1, (100, 110, 120))
                text2 = font.render("YES", 1, (0, 0, 0), (12, 110, 120))
                text3 = font.render("NO", 1, (0, 0, 0), (12, 110, 120))
                winner = font.render("  YOU WIN!!  ", 1, (255, 255, 255), (0, 0, 0))
                mouse = pygame.mouse.get_pressed()
                if mouse[0]:
                    if pygame.mouse.get_pos()[0] > 521 and pygame.mouse.get_pos()[0] < 549:
                        pygame.event.set_allowed(KEYDOWN)
                        background.stop()
                        ai()
                    if pygame.mouse.get_pos()[0] > 786 and pygame.mouse.get_pos()[0] <  815:
                        main()
    
                screen.blit(winner, (border.x-(winner.get_width()//2), 0))
                pygame.draw.rect(screen, (0, 0, 0), restart)
                screen.blit(text, (restart.x+ 70, restart.y+20))
                screen.blit(text2, (restart.x+ 35, restart.y+100))
                screen.blit(text3, (restart.x+ 300, restart.y+100))
            
            # frame per second
            clock.tick(FPS)
    
            # update screen
            pygame.display.update()
    
    #function to run two players
    def two():
        pygame.display.set_caption("Space Fighters")
        pygame.display.set_icon(pygame.image.load(os.path.join("assets", "enemy.png")))
    
        # set constants
        FPS = 90
        PLAYER_VEL = 15
        screen = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN, 32)
        clock = pygame.time.Clock()
        border = pygame.Rect((WIDTH//2)-10, 0, 10, HEIGHT)
        player_bullets = []
        player2_bullets = []
        max_bullets = 3
        full_health = 100
        background = pygame.mixer.Sound(os.path.join("assets", "back.crdownload"))
        shoot = pygame.mixer.Sound(os.path.join("assets", "laser gun.wav"))
        hit = pygame.mixer.Sound(os.path.join("assets", "explosion.wav"))
        lose = pygame.mixer.Sound(os.path.join("assets", "Game over.wav"))
        font = pygame.font.SysFont("Consolas", 30)
    
        PLAYER_HIT = USEREVENT + 1
        PLAYER2_HIT = USEREVENT + 2
    
        background.play()
    
        # function to animate pixels
        def pixels():
            for _ in range(20):
               rand_col = (randint(0, 255), randint(0, 255), randint(0, 255))
               rand_pos = (randint(0, 1199), randint(0, 599))
               rand_col2 = (randint(0, 255), randint(0, 255), randint(0, 255))
               rand_pos2 = (randint(0, 1199), randint(0, 599))
               screen.set_at(rand_pos, rand_col)
               screen.set_at(rand_pos2, rand_col2)
        
        # function to handle bullets
        def bullets(player_bullets, player2_bullets, player_rect, player2_rect):
            for i in player_bullets:
                i.x += 20
                if player2_rect.colliderect(i):
                    player_bullets.remove(i)
                    pygame.event.post(pygame.event.Event(PLAYER2_HIT))
                if i.x > WIDTH:
                    player_bullets.remove(i)
            
            for i in player2_bullets:
                i.x -= 20
                if player_rect.colliderect(i):
                    player2_bullets.remove(i)
                    pygame.event.post(pygame.event.Event(PLAYER_HIT))
                if i.x < 0:
                    player2_bullets.remove(i)
            
            for i in player_bullets:
                for j in player2_bullets:
                    if i.colliderect(j):
                        player_bullets.remove(i)
                    if j.colliderect(i):
                        player2_bullets.remove(j)
        
        #player class
        class Player():
            def __init__(self, name, x, y):
                self.name = name
                self.x = x
                self.y = y
                img = pygame.image.load(os.path.join("assets", f"{name}.png"))
                self.img = pygame.transform.scale(img, (img.get_width()//2, img.get_height()//2))
                self.player_rect = pygame.Rect(x, y, self.img.get_width(), self.img.get_height())
                self.player2_rect = pygame.Rect(x, y, self.img.get_width(), self.img.get_height())
            
            def draw_player(self):
                screen.blit(self.img, (self.player_rect.x, self.player_rect.y))
                for i in player_bullets:
                    pygame.draw.rect(screen, (100, 255, 100), i)
            def draw_player2(self):
                screen.blit(self.img, (self.player2_rect.x, self.player2_rect.y))
                for i in player2_bullets:
                    pygame.draw.rect(screen, (140, 100, 140), i)
            
            def move_player2(self):
                key = pygame.key.get_pressed()
    
                # condition to keep the characters in the screen
                if key[K_RIGHT]:
                    self.player2_rect.x += PLAYER_VEL
                    if self.player2_rect.x + PLAYER_VEL > (WIDTH-self.img.get_width())+15:
                        self.player2_rect.x -= PLAYER_VEL
    
                if key[K_LEFT]:
                    self.player2_rect.x -= PLAYER_VEL
                    if self.player2_rect.x - PLAYER_VEL < border.x:
                        self.player2_rect.x += PLAYER_VEL
                
                if key[K_UP]:
                    self.player2_rect.y -= PLAYER_VEL
                    if self.player2_rect.y - PLAYER_VEL < (0-15):
                        self.player2_rect.y += PLAYER_VEL
                
                if key[K_DOWN]:
                    self.player2_rect.y += PLAYER_VEL
                    if self.player2_rect.y + PLAYER_VEL > (HEIGHT-self.img.get_height())+11:
                        self.player2_rect.y -= PLAYER_VEL
            
            def move_player(self):
                key = pygame.key.get_pressed()
    
                # condition to keep the characters in the screen
                if key[K_d]:
                    self.player_rect.x += PLAYER_VEL
                    if self.player_rect.x + PLAYER_VEL > (border.x-self.img.get_width())+15:
                        self.player_rect.x -= PLAYER_VEL
    
                if key[K_a]:
                    self.player_rect.x -= PLAYER_VEL
                    if self.player_rect.x - PLAYER_VEL < 0-15:
                        self.player_rect.x += PLAYER_VEL
                
                if key[K_w]:
                    self.player_rect.y -= PLAYER_VEL
                    if self.player_rect.y - PLAYER_VEL < (0-10):
                        self.player_rect.y += PLAYER_VEL
                
                if key[K_s]:
                    self.player_rect.y += PLAYER_VEL
                    if self.player_rect.y + PLAYER_VEL > (HEIGHT-self.img.get_height())+11:
                        self.player_rect.y -= PLAYER_VEL
    
        class Health():
            def __init__(self, x, y, max_hp, hp):
                self.x = x
                self.y = y
                self.max_hp = max_hp
                self.hp = hp
                
            def draw(self):
                green = (0, 255, 0)
                red = (255, 0, 0)
                hp = self.hp/self.max_hp * full_health
                pygame.draw.rect(screen, red, pygame.Rect(self.x, self.y, self.max_hp, 20))
                pygame.draw.rect(screen, green, pygame.Rect(self.x, self.y, hp, 20))
        
        player = Player("enemy", WIDTH//4, HEIGHT//2)
        player2 = Player("you", border.x+WIDTH//4, HEIGHT//2)
        player_text = font.render("PLAYER :", 1, (0, 255, 0))
        player2_text = font.render("PLAYER 2:", 1, (255, 0, 255))
        player_health = Health(player_text.get_width() + 20, 10, full_health, full_health)
        player2_health = Health(border.x + player2_text.get_width() + 30, 10, full_health, full_health)
    
        while True:
            # fill the screen with a background
            screen.blit(pygame.transform.scale(pygame.image.load(os.path.join("assets", "Background.png")), (WIDTH, HEIGHT)), (0, 0))
    
            # listen for events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYUP and event.key == K_ESCAPE:
                    background.stop()
                    main()
                if event.type == KEYDOWN:
                    if event.key == K_LCTRL and len(player_bullets) < max_bullets:
                        shoot.play(1)
                        rect = pygame.Rect(player.player_rect.x, player.player_rect.y + player.player_rect.height//2, 15, 7)
                        player_bullets.append(rect)
                    if event.key == K_RCTRL and len(player2_bullets) < max_bullets: 
                        rect = pygame.Rect(player2.player2_rect.x + player2.player_rect.width, player2.player2_rect.y + player2.player2_rect.height//2, 15, 7)
                        player2_bullets.append(rect)
                if event.type == PLAYER_HIT:
                    hit.play()
                    player_health.hp -= 5
                if event.type == PLAYER2_HIT:
                    hit.play()
                    player2_health.hp -= 5
            
            # draw character and border and bullets and health bar and text
            player_health.draw()
            player2_health.draw()
            player.draw_player()
            player2.draw_player2()
            player.move_player()
            player2.move_player2()
            pygame.draw.rect(screen, (255, 255, 255), border)
            bullets(player_bullets, player2_bullets, player.player_rect, player2.player2_rect)
            screen.blit(player_text, (10, 10))
            screen.blit(player2_text, (border.x + 20, 10))
             
            #call the animation
            pixels()
    
            if player2_health.hp <= 0:
                player_bullets = []
                player2_bullets = []
                pygame.event.set_blocked(KEYDOWN)
                pygame.event.set_allowed([MOUSEMOTION,MOUSEBUTTONDOWN])
                restart = pygame.Rect(WIDTH//2-200, HEIGHT//2-100, 400, 200)
                font = pygame.font.SysFont("ebrima", 23)
                text = font.render("Would you like to replay ?", 1, (100, 110, 120))
                text2 = font.render("YES", 1, (0, 0, 0), (12, 110, 120))
                text3 = font.render("NO", 1, (0, 0, 0), (12, 110, 120))
                winner = font.render("  PLAYER 1 WINS  ", 1, (255, 255, 255), (0, 0, 0))
    
                mouse = pygame.mouse.get_pressed()
                if mouse[0]:
                    if pygame.mouse.get_pos()[0] > 521 and pygame.mouse.get_pos()[0] < 549:
                        pygame.event.set_allowed(KEYDOWN)
                        background.stop()
                        two()
                    if pygame.mouse.get_pos()[0] > 786 and pygame.mouse.get_pos()[0] <  815:
                        main()
                
                screen.blit(winner, (border.x-(winner.get_width()//2), 0))
                pygame.draw.rect(screen, (0, 0, 0), restart)
                screen.blit(text, (restart.x+ 70, restart.y+20))
                screen.blit(text2, (restart.x+ 35, restart.y+100))
                screen.blit(text3, (restart.x+ 300, restart.y+100))
    
            elif player_health.hp <= 0:
                player_bullets = []
                player2_bullets = []
                pygame.event.set_blocked(KEYDOWN)
                pygame.event.set_allowed([MOUSEMOTION,MOUSEBUTTONDOWN])
                restart = pygame.Rect(WIDTH//2-200, HEIGHT//2-100, 400, 200)
                font = pygame.font.SysFont("ebrima", 23)
                text = font.render("Would you like to replay ?", 1, (100, 110, 120))
                text2 = font.render("YES", 1, (0, 0, 0), (12, 110, 120))
                text3 = font.render("NO", 1, (0, 0, 0), (12, 110, 120))
                winner = font.render("PLAYER 2 WINS", 1, (255, 255, 255), (0, 0, 0))
                mouse = pygame.mouse.get_pressed()
                if mouse[0]:
                    if pygame.mouse.get_pos()[0] > 521 and pygame.mouse.get_pos()[0] < 549:
                        pygame.event.set_allowed(KEYDOWN)
                        background.stop()
                        two()
                    if pygame.mouse.get_pos()[0] > 786 and pygame.mouse.get_pos()[0] <  815:
                        main()
                
                screen.blit(winner, (border.x-(winner.get_width()//2), 0))
                pygame.draw.rect(screen, (0, 0, 0), restart)
                screen.blit(text, (restart.x+ 70, restart.y+20))
                screen.blit(text2, (restart.x+ 35, restart.y+100))
                screen.blit(text3, (restart.x+ 300, restart.y+100))
            
            # frame per second
            clock.tick(FPS)
    
            # update screen
            pygame.display.update()
    
    font = pygame.font.SysFont("consolas", 40)
    heading = font.render("  SPACE FIGHTER  ", 1, (150, 150, 150))
    introduction = font.render("Choose any mode you would like to play", 1, (150, 255, 150))
    one_player = font.render("One Player", 1, (150, 150, 150))
    two_player = font.render("Two Player", 1, (150, 150, 150))
    one_player_image = pygame.image.load(os.path.join("assets", "oneplayer_image.png"))
    one_player_img = pygame.transform.scale(one_player_image, (one_player_image.get_width()//3, one_player_image.get_height()//3))
    two_player_image = pygame.image.load(os.path.join("assets", "twoplayer_image.png"))
    two_player_img = pygame.transform.scale(two_player_image, (one_player_image.get_width()//3, one_player_image.get_height()//3))
    one_player_rect = pygame.Rect(100, HEIGHT//2, one_player_img.get_width(), one_player_img.get_height())
    two_player_rect = pygame.Rect(WIDTH//2+ 100, HEIGHT//2, two_player_img.get_width(), two_player_img.get_height())

    while True:
        window.fill((10, 10, 10))
        window.blit(heading, (WIDTH//2-heading.get_width()//2,0))
        window.blit(introduction, (WIDTH//2-introduction.get_width()//2, HEIGHT//6))
        window.blit(one_player, (150, HEIGHT//2-one_player.get_height()))
        window.blit(two_player, (WIDTH//2+150, HEIGHT//2-two_player.get_height()))
        window.blit(one_player_img, (one_player_rect.x, one_player_rect.y))
        window.blit(two_player_img, (two_player_rect.x, two_player_rect.y))
    
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                exit()
            if e.type == KEYUP and e.key == K_ESCAPE:
                pygame.quit()
                exit()
            if e.type == MOUSEBUTTONDOWN:
                if e.pos[0]>one_player_rect.x and e.pos[0]<(one_player_rect.x+one_player_rect.width) and e.pos[1]>one_player_rect.y and e.pos[1]<(one_player_rect.y+one_player_rect.height):
                    background.stop()
                    loading_screen(ai)
                if e.pos[0]>two_player_rect.x and e.pos[0]<(two_player_rect.x+two_player_rect.width) and e.pos[1]>two_player_rect.y and e.pos[1]<(two_player_rect.y+two_player_rect.height):
                    background.stop()
                    loading_screen(two)
    
        pygame.display.update()

if __name__ == "__main__":
    main()