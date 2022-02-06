# Basic Imports
from os import read
import pygame
from pygame import mixer
import sys
import random

# Initializing Pygane
pygame.init()
mixer.init()

# Colours
black = (0,0,0)
white = (250,250,250)

# Game Specific Variables
screen_width = 350
screen_height = 550

screen = pygame.display.set_mode((screen_width, screen_height))
title = pygame.display.set_caption("FLAPPY BIRD")

exit = False
game_over = False

background = pygame.image.load("C:\\Users\Shashank-dt\Desktop\game sprites\Flappy Bird\\bg.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

bird = pygame.image.load("C:\\Users\Shashank-dt\Desktop\game sprites\Flappy Bird\\bird3.png")
bird_rect = bird.get_rect(center = (100, 200))

pipe = pygame.image.load("C:\\Users\Shashank-dt\Desktop\game sprites\Flappy Bird\pipe.png")
pipe = pygame.transform.scale(pipe, (40, 300))

ground = pygame.image.load("C:\\Users\Shashank-dt\Desktop\game sprites\Flappy Bird\ground.png")
ground = pygame.transform.scale(ground, (400, 100))
ground_x = 0

message = pygame.image.load("C:\\Users\Shashank-dt\Desktop\game sprites\Flappy Bird\message.png")

score_sound = mixer.Sound("C:\\Users\Shashank-dt\Desktop\game sprites\Flappy Bird\score_sound.mp3")
death_sound = mixer.Sound("C:\\Users\Shashank-dt\Desktop\game sprites\Flappy Bird\death_sound.wav")
flapp_sound = mixer.Sound("C:\\Users\Shashank-dt\Desktop\game sprites\Flappy Bird\\flapp_sound.mp3")

gravity = 0.35
flapp_speed = 0
fps = 60
clock = pygame.time.Clock()
SPAWNING_TIME = pygame.USEREVENT
pygame.time.set_timer(SPAWNING_TIME, 1500)

pipe_list = []
pipe_height = [200, 300, 400]

current_score = 0
can_score = True

font = pygame.font.Font('04B_19.TTF', 30)

#################################################

def main_menu():
	def move_floor():
		screen.blit(ground, (ground_x, 450))
		screen.blit(ground, (ground_x + 350, 450))

	global exit, ground_x
	while not exit:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit = True

			if event.type == pygame.MOUSEBUTTONDOWN:
				game()

		ground_x -= 3

		if ground_x < -350:
			ground_x = 0

		screen.fill(black)
		screen.blit(background, (0,-30))
		move_floor()
		screen.blit(message, (90, 100))
		
		pygame.display.update()
		clock.tick(fps)

def game():
	def move_ground():
		screen.blit(ground, (ground_x, 450))
		screen.blit(ground, (ground_x + 350, 450))

	def draw_pipe():
		pipe_height_pos = random.choice(pipe_height)
		lower_pipe = pipe.get_rect(midtop = (500, pipe_height_pos))
		upper_pipe = pipe.get_rect(midbottom = (500, pipe_height_pos- 130))
		return lower_pipe, upper_pipe

	def move_pipe():
		for pipe in pipe_list:
			pipe.centerx -= 5

		for pipe in pipe_list:
			if pipe.centerx <= -20:
				pipe_list.remove(pipe)

		return pipe_list

	def blit_pipes():
		for pipes in pipe_list:
			if pipes.bottom >= 500:
				screen.blit(pipe, pipes)
			else:
				rotated_pipe = pygame.transform.flip(pipe, False, True)
				screen.blit(rotated_pipe, pipes)

	def collision():
		global game_over 
		for pipe in pipe_list:
			if bird_rect.colliderect(pipe):
				death_sound.play()
				game_over =  True

		if bird_rect.top <= -100 or bird_rect.bottom >= 450:
			death_sound.play()
			game_over = True

	def score_check():
		global current_score, can_score
		if pipe_list:
			for pipe in pipe_list:
				if 90 >= pipe.centerx >= 70 and can_score:
					current_score += 1
					score_sound.play()
					can_score = False

				if pipe.centerx < 20:
					can_score = True

	def display_score():
		if game_over == True:
			score_text = font.render("Score : " + str(current_score), True, white)
			screen.blit(score_text,(115, 20))

		if game_over == False:
			score_text = font.render(str(current_score), True, white)
			screen.blit(score_text,(screen_width/2, 20))

	def display_high_score():
			score_text = font.render("High score : " + str(high_score), True, white)
			screen.blit(score_text,(70, 400))

	def rotate_bird():
		new_bird = pygame.transform.rotozoom(bird, -flapp_speed * 6, 1)
		return new_bird

	global exit, ground_x, flapp_speed, gravity, pipe_list, pipe_height, game_over, current_score, can_score
	while exit== False :
		with open("C:\\Users\Shashank-dt\Desktop\Game files\high_score (for flappy bird).txt", "r") as f:
			high_score = f.read()

		for event in pygame.event.get():
			if event.type== pygame.QUIT:
				exit = True

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:	
					flapp_sound.play()
					flapp_speed = 0
					flapp_speed -= 7

				if event.key == pygame.K_SPACE and game_over == True:
					game_over = False
					current_score = 0
					
			if event.type == pygame.MOUSEBUTTONDOWN and game_over == True:
				game_over = False
				current_score = 0

			if event.type == pygame.MOUSEBUTTONDOWN:
				flapp_sound.play()
				flapp_speed = 0
				flapp_speed -= 7

			if event.type == SPAWNING_TIME:
				pipe_list.extend(draw_pipe())

		screen.fill(black)
		screen.blit(background, (0,-30))

		if current_score > int(high_score):
			high_score = current_score

		if game_over == True:
			can_score = True
			with open("C:\\Users\Shashank-dt\Desktop\Game files\high_score (for flappy bird).txt", "w") as f:
				f.write(str(high_score))
			pipe_list.clear()
			bird_rect.center = (80, 200)
			screen.blit(message, (90, 100))
			display_high_score()

		if game_over == False:
			# Pipe
			pipe_list = move_pipe()
			blit_pipes()

			# Bird
			flapp_speed += gravity
			rotated_bird = rotate_bird()
			bird_rect.centery += flapp_speed
			screen.blit(rotated_bird, bird_rect)
			collision()
		
		# Ground
		ground_x -= 2

		if ground_x < -350:
			ground_x = 0
		
		move_ground()

		# Score
		score_check()
		display_score()

		pygame.display.update()
		clock.tick(fps)

	pygame.quit()
	sys.exit()

main_menu()