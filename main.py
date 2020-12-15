#Import lib
import pygame 
import sys
import random

#Constant
WIDTH = 576
HEIGHT = 1024
FRAMERATE = 120
GRAVITY = 0.05
TICK = 1500
BIRD_X = 100
ISDEAD = False
SURFACE = 900
FONT_SIZE = 80

#Global varibles
gravity = GRAVITY
bird_movement = 0
score = 0

#Check if work correctly
print(pygame.version)
print(sys.version)

#Essential def
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, SURFACE))
    screen.blit(floor_surface, (floor_x_pos + WIDTH, SURFACE))

def create_pipe():
	random_pipe_pos = random.choice(pipe_height)
	bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))
	top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos - 300))
	return bottom_pipe, top_pipe

def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx -= 2
	return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.centerx > -100 and pipe.centerx < WIDTH + 100:
            if pipe.bottom >= 1024:
                screen.blit(pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(pipe_surface, False, True)
                screen.blit(flip_pipe, pipe)

def remove_pipes(pipes):
	for pipe in pipes:
		if pipe.centerx <= -50:
			pipes.remove(pipe)

	return pipes

def rotate_bird(bird):
	new_bird = pygame.transform.rotozoom(bird,-bird_movement * 3,1)
	return new_bird

def bird_animation():
	new_bird = bird_frames[bird_index]
	new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
	return new_bird, new_bird_rect

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    
    return False

#Init game
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

bg_surface = pygame.image.load(('assets/sprites/background-day.png')).convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/sprites/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/sprites/yellowbird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/sprites/yellowbird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/sprites/yellowbird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap, bird_midflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (BIRD_X/2, HEIGHT/2))
BIRDFLAP = pygame.USEREVENT
pygame.time.set_timer(BIRDFLAP, 180)

pipe_surface = pygame.transform.scale2x(pygame.image.load('assets/sprites/pipe-green.png').convert())
pipe_list = []
SPAWNPIPE = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNPIPE, TICK)
pipe_height = [400, 500, 600, 700, 800]

game_font = pygame.font.Font('04B_19__.ttf', FONT_SIZE)

#Run game
while True:
    for event in pygame.event.get():
        #Exit game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        #Game control
        if event.type == pygame.KEYDOWN:
            # print(0)
            if event.key == pygame.K_SPACE and ISDEAD == False:
                bird_movement = 0
                bird_movement -= GRAVITY * 50
                # print(1)
        
        #Spawn pipes
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        #Change animation
        if event.type == BIRDFLAP and ISDEAD == False:
            if bird_index < 3:
                bird_index += 1
                bird_surface, bird_rect = bird_animation()
            else:
                bird_index = 0
                bird_surface, bird_rect = bird_animation()

    #Render gameplay

    #Render BG
    screen.blit(bg_surface, (0,0))

    #Pipes render
    if ISDEAD == False:
        pipe_list = move_pipes(pipe_list)
    pipe_list = remove_pipes(pipe_list)
    draw_pipes(pipe_list)

    for pipe in pipe_list:
        if pipe.centerx == BIRD_X:
            #if  ISDEAD == False:
            if check_collision(pipe_list) == False and ISDEAD == False:
                score += 1
            else:
                ISDEAD = True

    #Bird render
    rotate = bird_surface
    flag = False
    if bird_rect.centery > SURFACE - 25 or bird_rect.centery < 25:
        flag = True
    elif bird_rect.centery != SURFACE - 25 and ISDEAD == False:
        bird_movement += GRAVITY
        rotate = rotate_bird(bird_surface)
    else:
        rotate = pygame.transform.rotozoom(bird_surface,-bird_movement * 3,1)
    
    if flag == False and ISDEAD == False:
        bird_rect.centery += bird_movement
    elif flag == True:
        flag = False
        if bird_rect.centery <= 25:
            bird_rect.centery = 26
        else:
            bird_rect.centery = SURFACE - 25
            ISDEAD = True
    
    if ISDEAD == True and bird_rect.centery < 900 - 26:
        bird_rect.centery += GRAVITY * 90
        rotate = pygame.transform.rotozoom(bird_surface,  bird_rect.centery, 1)

    screen.blit(rotate, bird_rect)

    #Score render

    score_surface = game_font.render(str(int(score/2)), True, (255,255,255))
    score_rect = score_surface.get_rect(center = (288,100))
    screen.blit(score_surface,score_rect)

    if ISDEAD == False:
        floor_x_pos -= 2
    draw_floor()
    if floor_x_pos < -WIDTH:
        floor_x_pos = 0

    print(len(pipe_list))

    pygame.display.update()
    clock.tick(FRAMERATE)