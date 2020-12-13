#Import lib
import pygame 
import sys
import random

#Constant
WIDTH = 576
HEIGHT = 1024
FRAMERATE = 120
GRAVITY = 0.05

#Global varibles
gravity = GRAVITY
bird_movement = 0

#Check if work correctly
print(pygame.version)
print(sys.version)

#Essential def
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + WIDTH, 900))

def create_pipe():
	random_pipe_pos = random.choice(pipe_height)
	bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
	top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_pos - 300))
	return bottom_pipe, top_pipe

def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx -= 2
	return pipes

def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.bottom >= 1024:
			screen.blit(pipe_surface, pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface, False, True)
			screen.blit(flip_pipe, pipe)

def remove_pipes(pipes):
	for pipe in pipes:
		if pipe.centerx == -600:
			pipes.remove(pipe)
	return pipes

def rotate_bird(bird):
	new_bird = pygame.transform.rotozoom(bird,-bird_movement * 3,1)
	return new_bird

def bird_animation():
	new_bird = bird_frames[bird_index]
	new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
	return new_bird, new_bird_rect

#Init game
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

bg_surface = pygame.image.load('assets/sprites/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/sprites/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap, bird_midflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, HEIGHT/2))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 180)

pipe_surface = pygame.image.load('assets/sprites/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)
pipe_height = [400,600,800]

#Run game
while True:
    for event in pygame.event.get():
        #Exit game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        #Game control
        if event.type == pygame.KEYDOWN:
            print(0)
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= GRAVITY * 50
                print(1)
        
        #Spawn pipes
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        #Change animation
        if event.type == BIRDFLAP:
            if bird_index < 3:
                bird_index += 1
                bird_surface, bird_rect = bird_animation()
            else:
                bird_index = 0
                bird_surface, bird_rect = bird_animation()
    
    screen.blit(bg_surface, (0,0))
    
    bird_movement += GRAVITY
    bird_rect.centery += bird_movement
    screen.blit(rotate_bird(bird_surface), bird_rect)

    pipe_list = move_pipes(pipe_list)
    pipe_list = remove_pipes(pipe_list)
    draw_pipes(pipe_list)

    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos < -WIDTH:
        floor_x_pos = 0

    #Render the next frame
    pygame.display.update()
    clock.tick(FRAMERATE)