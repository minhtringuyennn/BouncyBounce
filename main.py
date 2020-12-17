#Import lib
import pygame
import sys
import random 

#Game setting
WIDTH = 576
HEIGHT = 1024
FRAMERATE = 120
INIT = True
GAMEACTIVE = False

#Gameplay setting
SURFACE = 900
GRAVITY = 0.1
TICK = 1300
BIRD_X = 100
FONT_SIZE = 60
MOVE_PIPE = 3

# Global variables
bird_movement = 0
score = 0
high_score = 0

#Check if work correctly
print(pygame.version)
print(sys.version)
print('minhtringuyennn')

#Core function
def render_ground():
	screen.blit(ground_surface, (ground_x_pos, SURFACE))
	screen.blit(ground_surface, (ground_x_pos + WIDTH, SURFACE))

def create_pipe():
	random_pipe_pos = random.choice(pipe_height)
	bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))
	top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos - 300))
	return bottom_pipe, top_pipe

def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx -= MOVE_PIPE
	return pipes

def render_pipes(pipes):
	for pipe in pipes:
		if pipe.centerx > -100 and pipe.centerx < WIDTH + 100:
			if pipe.bottom >= HEIGHT:
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
			death_sound.play()
			return False

	if bird_rect.top <= -100 or bird_rect.bottom >= 900:
		death_sound.play()
		return False

	return True

def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score

def display(game_state):
	if game_state == 'main_game':
		screen.blit(message_surface, message_rect)

	if game_state == 'in_game':
		score_surface = game_font.render(str(int(score)) , True, (255,255,255))
		score_rect = score_surface.get_rect(center = (288, 100))
		screen.blit(score_surface, score_rect)

	if game_state == 'game_over':
		screen.blit(game_over_surface, game_over_rect)
		
		score_surface = game_font.render(f'Score: {int(score)}' , True, (255,255,255))
		score_rect = score_surface.get_rect(center = (288, 100))
		screen.blit(score_surface, score_rect)

		high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255,255,255))
		high_score_rect = high_score_surface.get_rect(center = (288, 850))
		screen.blit(high_score_surface, high_score_rect)

#Load asset and init the game
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#BACKGROUND
bg_surface = pygame.image.load('assets/sprites/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

#GROUND
ground_surface = pygame.image.load('assets/sprites/base.png').convert()
ground_surface = pygame.transform.scale2x(ground_surface)
ground_x_pos = 0

#BIRD
bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/sprites/yellowbird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/sprites/yellowbird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/sprites/yellowbird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap, bird_midflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (BIRD_X, HEIGHT/2))
#BIRD EVENT
BIRDFLAP = pygame.USEREVENT
pygame.time.set_timer(BIRDFLAP, 180)

#PIPE
pipe_surface = pygame.transform.scale2x(pygame.image.load('assets/sprites/pipe-green.png').convert())
pipe_list = []
pipe_height = [400, 500, 600, 700, 800]
#PIPE EVENT
SPAWNPIPE = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNPIPE, TICK)

#MESSAGE
message_surface = pygame.transform.scale2x(pygame.image.load('assets/sprites/message.png').convert_alpha())
message_rect = message_surface.get_rect(center = (WIDTH/2, HEIGHT/2))
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/sprites/gameover.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (WIDTH/2, HEIGHT/2))

#SOUND
flap_sound = pygame.mixer.Sound('assets/sound/wing.wav')
death_sound = pygame.mixer.Sound('assets/sound/hit.wav')
score_sound = pygame.mixer.Sound('assets/sound/point.wav')

#FONT
game_font = pygame.font.Font('assets/fonts/04B_19__.ttf', FONT_SIZE)

#RUN GAME
while True:
	for event in pygame.event.get():
		#Exit game
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		#Game control
		if event.type == pygame.KEYDOWN:
			INIT = False

			if event.key == pygame.K_SPACE and GAMEACTIVE:
				bird_movement = 0
				bird_movement -= GRAVITY * 50
				flap_sound.play()
			if event.key == pygame.K_SPACE and GAMEACTIVE == False:
				GAMEACTIVE = True
				pipe_list.clear()
				bird_rect.center = (100, 512)
				bird_movement = 0
				score = 0
		
		#Spawn pipes
		if event.type == SPAWNPIPE:
			pipe_list.extend(create_pipe())

		#Animate the bird
		if event.type == BIRDFLAP:
			if bird_index < 3:
				bird_index += 1
			else:
				bird_index = 0
			bird_surface, bird_rect = bird_animation()

	#Render gameplay

	#Render BG
	screen.blit(bg_surface, (0,0))
	
	#Gameplay
	if INIT == True:
		display('main_game')
	
	if GAMEACTIVE:
		#Bird render
		bird_movement += GRAVITY
		rotated_bird = rotate_bird(bird_surface)
		bird_rect.centery += bird_movement
		screen.blit(rotated_bird, bird_rect)
		GAMEACTIVE = check_collision(pipe_list)

		#Pipes render
		pipe_list = move_pipes(pipe_list)
		pipe_list = remove_pipes(pipe_list)
		render_pipes(pipe_list)
		
		for pipe in pipe_list:
			if pipe.centerx == BIRD_X:
				if check_collision(pipe_list) == True:
					score += 0.5
					score_sound.play()
		
		display('in_game')

	elif INIT == False:
		high_score = update_score(score, high_score)
		display('game_over')

	#Floor render
	ground_x_pos -= MOVE_PIPE
	render_ground()
	if ground_x_pos < -WIDTH:
		ground_x_pos = 0
	
	#Update frame
	pygame.display.update()
	clock.tick(FRAMERATE)