#IMPORT LIBARY
import pygame, random, sys, configparser, distutils
from distutils import util

#READ AND LOAD THE CONFIG
config = configparser.ConfigParser()
config.read("data/config.ini")

#Game status
WIDTH = int(config.get("setting", "WIDTH"))
HEIGHT = int(config.get("setting", "HEIGHT"))
FRAMERATE = int(config.get("setting", "FRAMERATE"))

SPRITES_DIR = config.get("dir", "SPRITES_DIR")
SOUND_DIR = config.get("dir", "SOUND_DIR")
FONT_DIR = config.get("dir", "FONT_DIR")

INIT = distutils.util.strtobool(config.get("status", "INIT"))
GAMEACTIVE = distutils.util.strtobool(config.get("status", "GAMEACTIVE"))
LOCK_KEYBOARD = distutils.util.strtobool(config.get("status", "LOCK_KEYBOARD"))
IS_MUTED = distutils.util.strtobool(config.get("status", "IS_MUTED"))

#Gameplay setting
SURFACE = int(config.get("gameplay", "SURFACE"))
OUT_OF_SCREEN = int(config.get("gameplay", "OUT_OF_SCREEN"))
GRAVITY = float(config.get("gameplay", "GRAVITY"))
SPAWNRATE = int(config.get("gameplay", "SPAWNRATE"))
BIRD_X = int(config.get("gameplay", "BIRD_X"))
PIPE_HEIGHT_DISTANCE = int(config.get("gameplay", "PIPE_HEIGHT_DISTANCE"))
MOVING_SPEED = int(config.get("gameplay", "MOVING_SPEED"))
FONT_SIZE = int(config.get("gameplay", "FONT_SIZE"))

#INIT THE GAME
pygame.init()
pygame.display.set_caption('Flappy Bird')
pygame.display.set_icon(pygame.image.load('assets/icon.ico'))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#background
bg_surface = pygame.image.load(f'{SPRITES_DIR}/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

#ground
ground_surface = pygame.image.load(f'{SPRITES_DIR}/base.png').convert()
ground_surface = pygame.transform.scale2x(ground_surface)
ground_x_pos = 0

#bird
bird_downflap = pygame.transform.scale2x(pygame.image.load(f'{SPRITES_DIR}/yellowbird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load(f'{SPRITES_DIR}/yellowbird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load(f'{SPRITES_DIR}/yellowbird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap, bird_midflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (BIRD_X, HEIGHT/2))
#BIRD EVENT
BIRDFLAP = pygame.USEREVENT
pygame.time.set_timer(BIRDFLAP, 180)

#pipes
pipe_surface = pygame.transform.scale2x(pygame.image.load(f'{SPRITES_DIR}/pipe-green.png').convert())
pipe_list = []
pipe_height = [400, 450, 500, 550, 600, 650, 700, 750, 800]
#PIPE EVENT
SPAWNPIPE = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNPIPE, SPAWNRATE)

#message
message_surface = pygame.transform.scale2x(pygame.image.load(f'{SPRITES_DIR}/message.png').convert_alpha())
message_rect = message_surface.get_rect(center = (WIDTH/2, HEIGHT/2))
game_over_surface = pygame.transform.scale2x(pygame.image.load(f'{SPRITES_DIR}/gameover.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (WIDTH/2, HEIGHT/2))

#sound
flap_sound = pygame.mixer.Sound(f'{SOUND_DIR}/wing.wav')
death_sound = pygame.mixer.Sound(f'{SOUND_DIR}/wasted.wav')
score_sound = pygame.mixer.Sound(f'{SOUND_DIR}/point.wav')

#font
game_font = pygame.font.Font(f'{FONT_DIR}/04B_19__.ttf', FONT_SIZE)

#GLOBAL VARIABLES
bird_movement = 0
score = 0
high_score = 0

#Check if work correctly
print(pygame.version)
print(sys.version)
print('load successfuly...')

#FUNTIONS
def render_ground():
	screen.blit(ground_surface, (ground_x_pos, SURFACE))
	screen.blit(ground_surface, (ground_x_pos + WIDTH, SURFACE))

def spawn_pipe():
	random_pipe_pos = random.choice(pipe_height)
	bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))
	top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos - PIPE_HEIGHT_DISTANCE))
	return bottom_pipe, top_pipe

def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx -= MOVING_SPEED
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
		if pipe.centerx <= OUT_OF_SCREEN:
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

	if bird_rect.top <= OUT_OF_SCREEN or bird_rect.bottom >= 900:
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

#RUN GAME
while True:

	#GAME EVENT
	for event in pygame.event.get():
		#Exit game
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		#Game control
		if event.type == pygame.KEYDOWN and LOCK_KEYBOARD == False:
			if event.key == pygame.K_SPACE:
				INIT = False
				if GAMEACTIVE:
					bird_movement = 0
					bird_movement -= GRAVITY * 50
					flap_sound.play()
				else:
					GAMEACTIVE = True
					pipe_list.clear()
					bird_rect.center = (100, 512)
					bird_movement = 0
					score = 0
			elif event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
			elif event.key == pygame.K_m:
				IS_MUTED = True
			elif event.key == pygame.K_n:
				IS_MUTED = False

		#Check sound
		if IS_MUTED:
			#print("muted")
			flap_sound.set_volume(0.0)
			death_sound.set_volume(0.0)
			score_sound.set_volume(0.0)
		else:
			#print("unmute")
			flap_sound.set_volume(1.0)
			death_sound.set_volume(1.0)
			score_sound.set_volume(1.0)

		#Spawn pipes
		if event.type == SPAWNPIPE:
			pipe_list.extend(spawn_pipe())

		#Animate the bird
		if event.type == BIRDFLAP and GAMEACTIVE == True:
			if bird_index < 3:
				bird_index += 1
			else:
				bird_index = 0
			bird_surface, bird_rect = bird_animation()

	#RENDER GAMEPLAY
	#Render BG
	screen.blit(bg_surface, (0,0))
	
	#Gameplay
	#INIT checking is it the first launch of the game
	if INIT:
		display('main_game')

	#if GAMEACTIVE == True, game is playing. Else => lose the game.
	elif GAMEACTIVE:
		#Pipes render
		pipe_list = move_pipes(pipe_list)
		pipe_list = remove_pipes(pipe_list)
		render_pipes(pipe_list) 
		
		for pipe in pipe_list:
			if pipe.centerx == BIRD_X:
				if check_collision(pipe_list) == True:
					score += 0.5
					score_sound.play()

		#Bird render
		bird_movement += GRAVITY
		rotated_bird = rotate_bird(bird_surface)
		bird_rect.centery += bird_movement
		screen.blit(rotated_bird, bird_rect)
		GAMEACTIVE = check_collision(pipe_list)
		
		#Floor render
		ground_x_pos -= MOVING_SPEED
		render_ground()
		#Floor out of screen
		if ground_x_pos < -WIDTH:
			ground_x_pos = 0

		display('in_game')

	else:
		LOCK_KEYBOARD = True

		#Render end screen
		render_pipes(pipe_list)
		if bird_rect.bottom <= SURFACE:
			bird_movement += GRAVITY
			rotated_bird = rotate_bird(bird_surface)
			bird_rect.centery += bird_movement
		else:
			LOCK_KEYBOARD = False
		screen.blit(rotated_bird, bird_rect)
		
		render_ground()
		high_score = update_score(score, high_score)
		display('game_over')
	
	render_ground()

	#Update frame
	pygame.display.update()
	clock.tick(FRAMERATE)