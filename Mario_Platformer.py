import pygame
import pyganim
from pygame.locals import *
from Constants import *
from Levels import *



class Player(pygame.sprite.Sprite):
    def __init__(self, animation):
        super().__init__()

        self.img_mario_right = pygame.image.load(img_mario_standingD)
        self.img_mario_left = pygame.image.load(img_mario_standingG)
        self.img_mario_jump_left = pygame.image.load(img_mario_jumpingG)
        self.img_mario_jump_right = pygame.image.load(img_mario_jumpingD)

        self.img_mario_jump_left = pygame.transform.scale(self.img_mario_jump_left, (16*2, 16*2))
        self.img_mario_jump_right = pygame.transform.scale(self.img_mario_jump_right, (16*2, 16*2))
        self.img_mario_left = pygame.transform.scale(self.img_mario_left, (12*2, 15*2))
        self.img_mario_right = pygame.transform.scale(self.img_mario_right, (12*2, 15*2))
        
        self.img_mario_dead = pygame.image.load(img_mario_dead)

        width = self.img_mario_right.get_size()[0]
        height = self.img_mario_right.get_size()[1]
        
        self.rect = self.img_mario_right.get_rect()

        self.animation = animation

        self.scrolling_x = 0
        self.change_x = 0
        self.change_y = 0
        self.speed = 4
        self.side = "right"
        self.is_moving = False
        self.is_jumping = False
        self.is_dead = False
        self.level = None


    def update(self):
        self.calc_grav()

        self.rect.x += self.change_x
        
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                self.change_speed(4)
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            self.change_y = 0
            

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
            self.is_jumping = False
        else:
            self.change_y += .47
            self.change_speed(3)
            self.is_jumping = True

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.change_speed(4)
            self.die()


    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10


    def change_speed(self, speed):
        self.speed = speed

        if not self.is_moving:
            self.stop()
            return
        
        if self.side == "left":
            self.change_x = -self.speed
        elif self.side == "right":
            self.change_x = self.speed
      

    def go_left(self):
        self.change_x = -self.speed

    def go_right(self):
        self.change_x = self.speed

    def stop(self):
        self.change_x = 0


    def die(self):
        #self.animation.moveConductor.stop()
        self.is_dead = True


        
class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height, image):
        super().__init__()

        self.image = pygame.image.load(image)
        
        self.rect = self.image.get_rect()



class Level:
    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
        self.num_img = 0
        self.time = 0


    def update(self):
        self.platform_list.update()
        self.enemy_list.update()


    def draw(self, win, level, img_level, player, animation):
        self.time += 1
        print(self.time)
        win.blit(img_level, [0, 0], [self.player.scrolling_x, 0, SCREEN_WIDTH, SCREEN_HEIGHT])

        if player.is_dead:
            win.blit(player.img_mario_dead, (player.rect.left - player.scrolling_x, player.rect.y))
            return

        for block in range(len(level.list_block)):
            win.blit(level.list_block[block][0], (level.list_block[block][1] - self.player.scrolling_x, level.list_block[block][2]))

        for decor in range(len(self.list_decor)):
            win.blit(level.list_decor[decor][0], (level.list_decor[decor][1] - self.player.scrolling_x, level.list_decor[decor][2]))

        if not player.is_moving and not player.is_jumping:
            if player.side == "right":
                win.blit(player.img_mario_right, (player.rect.left - player.scrolling_x, player.rect.y))
            elif player.side == "left":
                win.blit(player.img_mario_left, (player.rect.left - player.scrolling_x, player.rect.y))
                
        elif player.is_moving and not player.is_jumping:
            if self.num_img < 2: #len(animation.animObjs["\Mario" + player.side])-1:
                self.num_img += 1
            else:
                self.num_img = 0

            # win.blit(animation.animObjs["\Mario" + player.side][self.num_img], (player.rect.left - player.scrolling_x, player.rect.y))
           #  animation.animObjs["\Mario" + player.side][1].blit(win, (player.rect.left - player.scrolling_x, player.rect.y))
           # if player.side == "right":
           #     animation.animObjs["\MarioRunningD"].blit(win, (player.rect.left - player.scrolling_x, player.rect.y))
           # if player.side == "left":
           #     animation.animObjs["\MarioRunningG"].blit(win, (player.rect.left - player.scrolling_x, player.rect.y))
                
        if player.side == "right" and player.is_jumping:
            win.blit(player.img_mario_jump_right, (player.rect.left - player.scrolling_x, player.rect.y))
        elif player.side == "left" and player.is_jumping:
            win.blit(player.img_mario_jump_left, (player.rect.left - player.scrolling_x, player.rect.y))

        #self.platform_list.draw(win)
        #self.enemy_list.draw(win)


        
class Create_level(Level):
    def __init__(self, player, img_level, current_level_no):
        Level.__init__(self, player)
        
        self.LEVEL_WIDTH = img_level.get_size()[0]

        self.liste_levels = [level_0]
        
        self.list_block = []
        self.list_decor = []

        level, decors, pltf_moving = self.liste_levels[current_level_no]()

        for platform in level:
            self.block = Platform(platform[0], platform[1], platform[4])
            self.block.rect.x = platform[2]
            self.block.rect.y = platform[3]
            self.block.player = self.player
            self.platform_list.add(self.block)
            self.list_block.append([self.block.image, self.block.rect.x, self.block.rect.y])

        for m_pltf in pltf_moving:
            self.pltf = Platform(platform[0], platform[1], platform[4])
            self.pltf.rect.x = platform[2]
            self.pltf.rect.y = platform[3]
            self.pltf.player = self.player
            self.platform_list.add(self.pltf)
            self.list_block.append([self.block.image, self.block.rect.x, self.block.rect.y])            

        for decor in decors:
            self.decor = Platform(decor[0], decor[1], decor[4])
            self.decor.rect.x = decor[2]
            self.decor.rect.y = decor[3]
            self.list_decor.append([self.decor.image, self.decor.rect.x, self.decor.rect.y])



##
##class Animations:
##    def __init__(self):
##        animTypes = "\Marioright \Marioleft".split()
##        self.animObjs = {}
##        
##        for animType in animTypes:
##            images = []
##            liste_img = [pygame.image.load(mario_path + animType + str(num) + ".gif") for num in range(len(animTypes))]
##            for image in liste_img:
##                images.append(pygame.transform.scale(image, (16*2, 16*2)))
##                self.animObjs[animType] = images
##
##






        

class Animations:
    def __init__(self):
        animTypes = "\MarioRunningD \MarioRunningG".split()
        animtypes_ennemies = "\Goomba \Pyrhana".split()
        self.animObjs = {}
        
        for animType in animTypes:
            imagesAndDurations = [(mario_path + "%s%s.gif" % (animType, str(num).rjust(3, '0')), 0.1) for num in range(len(animTypes))]
            self.animObjs[animType] = pyganim.PygAnimation(imagesAndDurations)

        for animtype in animtypes_ennemies:
            imagesAndDurations = [(ennemy_path + "%s%s.gif" % (animtype, str(num).rjust(1, '0')), 0.1) for num in range(len(animtypes_ennemies))]
            self.animObjs[animtype] = pyganim.PygAnimation(imagesAndDurations)

        self.moveConductor = pyganim.PygConductor(self.animObjs)
        self.moveConductor.play()



def main():
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]

    win = pygame.display.set_mode(size)
    pygame.display.set_caption(TITRE_WIN)

    current_level_no = 0
    liste_level_image = ["\one.png"]

    img_level = pygame.image.load(levels_path + str(liste_level_image[current_level_no]))

    animation = Animations()
    player = Player(animation)
    
    level_list = []
    level_list.append(Create_level(player, img_level, current_level_no))
    
    current_level = level_list[current_level_no]
    
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 0
    player.rect.y = SCREEN_HEIGHT - player.rect.height * 3
    active_sprite_list.add(player)

    clock = pygame.time.Clock()

    fps_font = pygame.font.SysFont("Arial", 15)

    run_level = 1

    while run_level:
        for event in pygame.event.get():

            if event.type == QUIT:
                run_level = 0
                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN:
                print("e")
                if event.key == pygame.K_LEFT:
                    player.side = "left"
                    player.is_moving = True
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.side = "right"
                    player.is_moving = True
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.is_moving = False
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    print(player.change_x)
                    player.is_moving = False
                    player.stop()

        active_sprite_list.update()
        current_level.update()

        if player.rect.left < 0:
            player.rect.left = 0

        elif player.rect.right > current_level.LEVEL_WIDTH:
            player.rect.right = current_level.LEVEL_WIDTH

        if player.rect.left <= SCREEN_WIDTH / 2:
            player.scrolling_x = 0
            
        elif player.rect.left > SCREEN_WIDTH / 2:
            player.scrolling_x = player.rect.left - SCREEN_WIDTH / 2

            if player.scrolling_x > current_level.LEVEL_WIDTH - SCREEN_WIDTH:
                player.scrolling_x = current_level.LEVEL_WIDTH - SCREEN_WIDTH

        if player.rect.bottom >= size[1]:
            player.die()
            run_level = 0
            
        #active_sprite_list.draw(win)
        current_level.draw(win, current_level, img_level, player, animation)

        clock.tick(60)

        win.blit(fps_font.render(str(int(clock.get_fps())), True, (255,0,0)), (0, 0))
        
        pygame.display.flip()



if __name__ == "__main__":
    main()
