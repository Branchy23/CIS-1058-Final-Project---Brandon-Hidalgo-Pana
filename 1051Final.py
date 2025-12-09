import pygame
import sys
import random

pygame.init()

width, height = 600,700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("CIS 1051 Final. Treat Invaders")

clock = pygame.time.Clock()

original_dog_img = pygame.image.load("dog.png").convert_alpha()


#player
fat_meter = 0
max_fat = 5
score_value = 0
player_width = 50
player_height = 55
player_X = width // 2 - player_width // 2
player_Y = height -60
player_speed = 6
dog_img = pygame.transform.scale(original_dog_img, (player_width, player_height))

#lasers

lasers = []
laser_speed = 8
laser_width = 5
laser_height = 15
laser_cooldown = 600
last_shot_time = 0

#aliens
alien_width = 40
alien_height = 40
alien_speed = 1
aliens = []

#what "aliens" look like
original_treat_img = pygame.image.load("treat.png").convert_alpha()
treat_img = pygame.transform.scale(original_treat_img, (alien_width, alien_height))

rows = 3
cols = 6
padding = 20
offset_y = 50
offset_x = 50
alien_direction = 1

#alien bullets
alien_bullets = []
aline_bullet_speed = 11
alien_shoot_delay = 160
last_alienshot = 0

for row in range(rows):
    for col in range(cols):
        x = offset_x + col * (alien_width + padding)
        y = offset_y + row * (alien_height + padding)
        aliens.append([x,y])
#game loop
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #movement
    keys =  pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_X -= player_speed
    if keys[pygame.K_RIGHT]:
        player_X += player_speed

    player_X = max(0, min(width - player_width, player_X))

    #shooting
    current_time = pygame.time.get_ticks()
    if keys[pygame.K_SPACE] and current_time - last_shot_time >= laser_cooldown:
        lasers.append([player_X + player_width//2 - laser_width//2, player_Y])
        last_shot_time = current_time
    screen.fill((0,0,0))


    screen.blit(dog_img, (player_X, player_Y))


    #drawing aliens
    for alien in aliens:
        screen.blit(treat_img, (alien[0], alien[1]))

        
    #lasers
    for laser in lasers[:]:
        laser[1] -= laser_speed
        if laser[1] < 0:
            lasers.remove(laser)
        else:
            pygame.draw.rect(screen, (255,0,0),(laser[0], laser[1], laser_width, laser_height))

    #alien movement

    hit_wall = False
    for alien in aliens:
        alien[0] += alien_speed * alien_direction
        if alien[0] <= 0 or alien[0] + alien_width >= width:
            hit_wall = True

    if hit_wall:
        alien_direction *= -1
        for alien in aliens:
            alien[1] += 20


    #alien shooting
    current_time = pygame.time.get_ticks()
    if current_time - last_alienshot > alien_shoot_delay and aliens:
        shooting_alien = random.choice(aliens)
        bullet_x = shooting_alien[0] + alien_width // 2
        bullet_y = shooting_alien[1] + alien_height
        alien_bullets.append([bullet_x, bullet_y])
        last_alienshot = current_time

    #draw alien bullets
    for bullet in alien_bullets[:]:
        bullet[1] += aline_bullet_speed

        if bullet[1] > height:
            alien_bullets.remove(bullet)
        else:
            pygame.draw.rect(screen, (255,255,0), (bullet[0], bullet[1], 5, 10))


    #collisions b/t lasers and aliens
    for laser in lasers[:]:
        laser_rect = pygame.Rect(laser[0], laser[1], laser_width, laser_height)

        for alien in aliens[:]:
            alien_rect = pygame.Rect(alien[0], alien[1], alien_width, alien_height)

            if laser_rect.colliderect(alien_rect):
                if laser in lasers:
                    lasers.remove(laser)
                if alien in aliens:
                    aliens.remove(alien)
                break

    #collisions b/t player and bullets
    player_rect = pygame.Rect(player_X, player_Y, player_width, player_height)

    for bullet in alien_bullets[:]:
        bx, by = bullet[0], bullet[1]
        bullet_rect = pygame.Rect(bx, by, 5, 10)

        if bullet_rect.colliderect(player_rect):
            if bullet in alien_bullets:
                alien_bullets.remove(bullet)

            fat_meter += 1
            score_value +=1
            print("Fat Meter:", fat_meter)

            player_width += 20
            player_height += 20
            player_Y -= 20
            player_X -= 7
            dog_img = pygame.transform.scale(original_dog_img, (player_width, player_height))

            if fat_meter >= max_fat:
                running = False
                print("Your dog got too fat!")

                
    font = pygame.font.SysFont(None, 35)
    #dof fatness display
    score_text = font.render(f"Score: {score_value}", True, (255, 255, 255))
    screen.blit(score_text, (10, 40))



    pygame.display.update()





