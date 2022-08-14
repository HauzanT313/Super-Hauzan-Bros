from turtle import left
import pygame

pygame.init()
pygame.mixer.init()

fps = 60
logo = pygame.image.load('source\logo.png')
img_bg = pygame.image.load('source\\bg.png')
title = 'Hauzan The Adventurer'

fullScreen = pygame.display.get_desktop_sizes()
display = pygame.display.set_mode(fullScreen[1])
clock = pygame.time.Clock()

pygame.display.set_icon(logo)
pygame.display.set_caption(title)

class obj_world:
    def __init__(self) -> None:
        self.pos_x = 0

    def CreateWorld(self, world_pos_x):
        self.pos_x -= world_pos_x
        display.fill((109, 237, 165))
        display.blit(img_bg, (self.pos_x,0))

class obj_player:
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.state_player = []
        self.state_stand = []
        self.state_walk = []
        self.state_jump = []
        self.state_lose = []

        self.state_player.append(self.state_stand)
        self.state_player.append(self.state_walk)
        self.state_player.append(self.state_jump)
        self.state_player.append(self.state_lose)

        #0
        self.state_stand.append(pygame.image.load('source\Stand\pixil-frame-0 (2).png').convert_alpha())
        self.state_stand.append(pygame.image.load('source\Stand\pixil-frame-1.png').convert_alpha())
        self.state_stand.append(pygame.image.load('source\Stand\pixil-frame-2.png').convert_alpha())

        #1
        self.state_walk.append(pygame.image.load('source\Walk\pixil-frame-0 (2).png').convert_alpha())
        self.state_walk.append(pygame.image.load('source\Walk\pixil-frame-1.png').convert_alpha())
        self.state_walk.append(pygame.image.load('source\Walk\pixil-frame-2.png').convert_alpha())
        self.state_walk.append(pygame.image.load('source\Walk\pixil-frame-3.png').convert_alpha())
        self.state_walk.append(pygame.image.load('source\Walk\pixil-frame-4.png').convert_alpha())
        self.state_walk.append(pygame.transform.flip(pygame.image.load('source\Walk\pixil-frame-0 (2).png').convert_alpha(), True, False))
        self.state_walk.append(pygame.transform.flip(pygame.image.load('source\Walk\pixil-frame-1.png').convert_alpha(), True, False))
        self.state_walk.append(pygame.transform.flip(pygame.image.load('source\Walk\pixil-frame-2.png').convert_alpha(), True, False))
        self.state_walk.append(pygame.transform.flip(pygame.image.load('source\Walk\pixil-frame-3.png').convert_alpha(), True, False))
        self.state_walk.append(pygame.transform.flip(pygame.image.load('source\Walk\pixil-frame-4.png').convert_alpha(), True, False))
        
        #2
        self.state_jump.append(pygame.image.load('source\Jump\pixil-frame-0 (2).png').convert_alpha())
        self.state_jump.append(pygame.image.load('source\Jump\pixil-frame-1.png').convert_alpha())
        self.state_jump.append(pygame.image.load('source\Jump\pixil-frame-2.png').convert_alpha())
        self.state_jump.append(pygame.image.load('source\Jump\pixil-frame-3.png').convert_alpha())
        self.state_jump.append(pygame.transform.flip(pygame.image.load('source\Jump\pixil-frame-0 (2).png').convert_alpha(), True, False))
        self.state_jump.append(pygame.transform.flip(pygame.image.load('source\Jump\pixil-frame-1.png').convert_alpha(), True, False))
        self.state_jump.append(pygame.transform.flip(pygame.image.load('source\Jump\pixil-frame-2.png').convert_alpha(), True, False))
        self.state_jump.append(pygame.transform.flip(pygame.image.load('source\Jump\pixil-frame-3.png').convert_alpha(), True, False))

        #3
        self.state_lose.append(pygame.image.load('source\lose\pixil-frame-0 (2).png').convert_alpha())
        self.state_lose.append(pygame.image.load('source\lose\pixil-frame-1.png').convert_alpha())
        self.state_lose.append(pygame.image.load('source\lose\pixil-frame-2.png').convert_alpha())

        self.num_state = 0
        self.state = 0
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.fly = True
        self.comd_lose = False
        
        self.border_back = False
        self.border_front = False
        self.border_world_x = [0,1440]
        self.world_pos_x = 0

        self.font = pygame.font.SysFont('impact', 60)
        self.text_lose = self.font.render('You Loser :p', True, (255, 51, 51))
        self.text_win = self.font.render('You Won:D', True, (82, 255, 79))

        self.transparant_screen = pygame.Surface((1440, 900))
        self.transparant_screen.set_alpha(150)
        self.transparant_screen.fill((64, 64, 64))
        self.show_screen_lose = False
        self.show_screen_win = False

        #Sound Effect
        self.jump_sound = pygame.mixer.Sound('source\sound\jump_sf.mp3')
        self.run_sound = pygame.mixer.Sound("source\sound\\run_sf_cut.wav")
        self.won_sound = pygame.mixer.Sound('source\sound\won_notif.mp3')
        self.lose_sound = pygame.mixer.Sound('source\sound\lose_notif.wav')
        self.replay_sound = False

    def move(self, left_key, right_key, up_key):
        self.player_rect = pygame.Rect(self.pos_x, self.pos_y, 180, 240)
        #pygame.draw.rect(display,(255, 117, 107), (0,0,450,770))
        #pygame.draw.rect(display,(107, 235, 255), (990,0,450,770))
        self.rect_back = pygame.Rect(0,0,450,770)
        self.rect_front = pygame.Rect(990,0,450,770)

        # Fungsi ketika kalah
        if self.comd_lose == True:
            self.state = 3
            left_key == False
            right_key == False
            if self.fly == False:
                self.pos_y -= 10
                if self.pos_y <= 400:
                    self.num_state = 3
                    self.fly = True
                elif self.pos_y <= 450:
                    self.num_state = 2
                elif self.pos_y <= 500:
                    self.num_state = 1
                elif self.pos_y <= 520:
                    self.num_state = 0
            if self.fly == True:
                self.pos_y += 10
                if self.pos_y <= 400:
                    self.num_state = 3
                elif self.pos_y <= 450:
                    self.num_state = 2
                elif self.pos_y <= 500:
                    self.num_state = 1
                elif self.pos_y <= 540:
                    self.num_state = 0
                    self.show_screen_lose = True

            print(right_key)
            #print(self.state)
            #print(float(self.num_state))

        # Fungsi ketika menang 
        elif self.comd_lose == False:

            #Gerakan ketika menang
            if self.show_screen_win == True:
                left_key = False
                right_key = False
                up_key = True
                if self.replay_sound == False:
                    self.won_sound.play()
                    self.replay_sound = True
                elif self.replay_sound == True:
                    pass

            # Pendeteksi player menyentuh tanah
            if ground.colliderect(self.player_rect):
                self.fly = False
                self.state = 0
            
            # Gerakan ketika terbang/ tidak ditanah
            else:
                self.fly = True
                self.pos_y += 10
                self.state = 2
                if left_key == False and right_key == False:
                    if self.pos_y <= 400:
                        self.num_state = 3
                    elif self.pos_y <= 450:
                        self.num_state = 2
                    elif self.pos_y <= 500:
                        self.num_state = 1
                    elif self.pos_y <= 540:
                        self.num_state = 0
                elif left_key == True:
                    if self.border_back == True:
                        pass
                    else:
                        if self.pos_x > 0:
                            self.pos_x -= 5
                    if self.pos_y <= 400:
                        self.num_state = 7
                    elif self.pos_y <= 450:
                        self.num_state = 6
                    elif self.pos_y <= 500:
                        self.num_state = 5
                    elif self.pos_y <= 520:
                        self.num_state = 4
                elif right_key == True:
                    if self.border_front == True:
                        pass
                    else:
                        if self.pos_x < 1240:
                            if self.comd_lose == False:
                                self.pos_x += 5
                        else:
                            self.show_screen_win = True
                    if self.pos_y <= 400:
                        self.num_state = 3
                    elif self.pos_y <= 450:
                        self.num_state = 2
                    elif self.pos_y <= 500:
                        self.num_state = 1
                    elif self.pos_y <= 520:
                        self.num_state = 0

            # Pendeteksi Border
            if self.rect_back.colliderect(self.player_rect):
                if self.world_pos_x <= 0:
                    pass
                else:
                    self.border_back = True
            elif self.rect_front.colliderect(self.player_rect):
                if self.world_pos_x >= 960:
                    pass
                else:
                    self.border_front = True
            else:
                self.border_back = False
                self.border_front = False

            # Gerakan ketika ditanah
            if self.fly == False:
                if left_key == False and right_key == False and up_key == False:
                    self.num_state += 0.4
                    if self.num_state >= len(self.state_stand):
                        self.num_state = 0
                    self.border_back = False
                    self.border_front = False
                    self.run_sound.stop()
                if left_key == True:
                    self.state = 1
                    self.num_state += 0.5
                    self.run_sound.play()
                    pygame.mixer.set_num_channels(1)
                    if self.num_state >= len(self.state_walk)/2:
                        self.num_state = 0

                    if self.border_back == True:
                        pass
                    else:
                        if self.pos_x >0:
                            self.pos_x -= 10
                if right_key == True:
                    self.state = 1
                    self.num_state += 0.5
                    self.run_sound.play()
                    pygame.mixer.set_num_channels(1)
                    if self.num_state <= len(self.state_walk)/2:
                        self.num_state = len(self.state_walk)/2
                    elif self.num_state >= len(self.state_walk):
                        self.num_state = len(self.state_walk)/2

                    if self.border_front == True:
                        pass
                    else:
                        if self.pos_x < 1240:
                            if self.comd_lose == False:
                                self.pos_x += 10
                        else:
                            self.show_screen_win = True
                if up_key == True:
                    self.pos_y -= 160
                    self.run_sound.stop()
                    if self.show_screen_win == False:
                        self.jump_sound.play()

        if self.state == 3:
            if self.num_state > 3:
                self.num_state = 3
            if self.num_state < 0:
                self.num_state = 0

            # Tampilan dilayar
            
        print(self.state)
        print(float(self.num_state))
        try:
            display.blit(self.state_player[self.state][int(self.num_state)], (self.pos_x,self.pos_y))
        except IndexError as e:
            print('error cok')
            print(self.state)
            print(float(self.num_state))
            self.lose_sound.play()


    def make_rect(self):
        if self.comd_lose == True:
            player_rect = pygame.Rect(self.pos_x, self.pos_y, 0, 0)
        else:
            player_rect = pygame.Rect(self.pos_x, self.pos_y, 180, 240)
        return player_rect

    def BorderMove(self):
        if self.border_back == False and self.border_front == False:
            pass
        elif self.border_back == True:
            if self.world_pos_x <= 0:
                pass
            else:
                self.world_pos_x -= 10
        elif self.border_front == True:
            if self.world_pos_x >= 960:
                pass
            else:
                self.world_pos_x += 10
        
        return self.world_pos_x
            
    def lose(self):
        self.lose_sound.play()
        self.comd_lose = True

    def LoseScreen(self):
        if self.show_screen_lose == True:
            display.blit(self.transparant_screen, (0,0))
            display.blit(self.text_lose, (450, 300))

    def WinScreen(self):
        if self.show_screen_win == True:
            display.blit(self.transparant_screen, (0,0))
            display.blit(self.text_win, (450, 300))

class obj_mobs:
    def __init__(self, pos_x, pos_y) -> None:
        self.state_mobs = []
        self.state_mobs.append(pygame.transform.scale(pygame.image.load('source\Mobs\pixil-frame-0 (3).png').convert_alpha(), (140, 140)))
        self.state_mobs.append(pygame.transform.scale(pygame.image.load('source\Mobs\pixil-frame-1.png').convert_alpha(), (140, 140)))
        self.state_mobs.append(pygame.transform.scale(pygame.image.load('source\Mobs\pixil-frame-2.png').convert_alpha(), (140, 140)))
        self.state_mobs.append(pygame.transform.scale(pygame.transform.flip(pygame.image.load('source\Mobs\pixil-frame-0 (3).png').convert_alpha(), True, False), (140, 140)))
        self.state_mobs.append(pygame.transform.scale(pygame.transform.flip(pygame.image.load('source\Mobs\pixil-frame-1.png').convert_alpha(), True, False), (140, 140)))
        self.state_mobs.append(pygame.transform.scale(pygame.transform.flip(pygame.image.load('source\Mobs\pixil-frame-2.png').convert_alpha(), True, False), (140, 140)))

        self.pos_x = pos_x
        self.pos_y = pos_y
        
        self.state = 0
        self.num_step = 3
        self.loop = True
        self.comd_lose = False

    def move(self, world_pos_x):
        display.blit(self.state_mobs[int(self.state)], (self.pos_x - world_pos_x, self.pos_y))

        if self.comd_lose == True:
            if self.num_step >= 0 and self.num_step <= 2.8:
                self.num_step = 0
                if self.loop == False:
                    self.pos_y -= 10
                    self.loop = True
                else:
                    self.pos_y += 10
            else:
                self.num_step = 3
                if self.loop == False:
                    self.pos_y -= 10
                    self.loop = True
                else:
                    self.pos_y += 10

        else:
            if self.num_step >= 0:
                if self.state <= 0.2:
                    self.state += 0.04
                elif self.state < 1:    
                    self.pos_x += 5
                    self.state += 0.2
                elif self.state < 2:
                    self.pos_x += 5
                    self.state += 0.2
                elif self.state < 2.8:
                    self.pos_x += 5
                    self.state += 0.2
                elif self.state >= 2.8:    
                    self.state = 0
                    self.num_step -= 1
            else:
                if self.state <= 2:
                    self.state = 3
                elif self.state <= 3.2:
                    self.state += 0.04
                elif self.state < 4:    
                    self.pos_x -= 5
                    self.state += 0.2
                elif self.state < 5:
                    self.pos_x -= 5
                    self.state += 0.2
                elif self.state < 5.8:
                    self.pos_x -= 5
                    self.state += 0.2
                elif self.state >= 5.8:    
                    self.state = 3
                    self.num_step -= 1

                if self.num_step == -5:
                    self.num_step = 4

    def make_rect(self, world_pos_x):
        mobs_rect = []
        if self.comd_lose == False:
            top = pygame.Rect(self.pos_x+25 - world_pos_x, self.pos_y+53, 80, 25)
            bottom = pygame.Rect(self.pos_x+10 - world_pos_x, self.pos_y+75, 115, 40)
            mobs_rect.append(top)
            mobs_rect.append(bottom)
            #pygame.draw.rect(display, (77, 227, 224), (self.pos_x+10, self.pos_y+75, 115, 40))
            #pygame.draw.rect(display, (247, 64, 116), (self.pos_x+25, self.pos_y+53, 80, 25))
        elif self.comd_lose == True:
            mobs_none = pygame.Rect(0, 0, 0, 0)
            mobs_rect.append(mobs_none)
            mobs_rect.append(mobs_none)
        return mobs_rect

    def lose(self):
        self.comd_lose = True
        self.loop = False
 

def BuildSurface(left_key, right_key, up_key):
    global world_pos_x
    world1 = obj_world()
    world_pos_x = player.BorderMove()

    world1.CreateWorld(world_pos_x)
    mobs1.move(world_pos_x)
    player.move(left_key, right_key, up_key)
    

def Main():
    global player, mobs1, ground, left_key, right_key, up_key
    player = obj_player(600, 300)
    mobs1 = obj_mobs(900, 660)
    ground = pygame.Rect(0,770, 2400,300)
    

    clock.tick(fps)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                run = False
            
            keys = pygame.key.get_pressed()
            left_key = False
            right_key = False
            up_key = False
            if keys[pygame.K_LEFT]:
                left_key = True
            if keys[pygame.K_UP]:
                up_key = True
            if keys[pygame.K_RIGHT]:
                right_key = True


        BuildSurface(left_key, right_key, up_key)

        mobs_rect = mobs1.make_rect(world_pos_x)
        player_rect = player.make_rect()

        if player_rect.colliderect(mobs_rect[0]):
            mobs1.lose()
        elif player_rect.colliderect(mobs_rect[1]):
            player.lose()
        else:
            pass

        player.LoseScreen()
        player.WinScreen()

        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    Main()