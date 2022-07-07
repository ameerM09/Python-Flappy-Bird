import pygame
import random
import sys
import os

pygame.init() 
pygame.font.init()

WIN_WIDTH = 525
WIN_HEIGHT = 750
CAPTION = 'Flappy Bird'

BIRD_WIDTH = 59.5
BIRD_HEIGHT = 42

START_SCREEN_WIDTH = 322
START_SCREEN_HEIGHT = 467.25

FPS = 30

WHITE = (255, 255, 255)
ORANGE = (215, 115, 40)

MAIN_FONT = pygame.font.SysFont('Comicsans', 30)
END_SCREEN_FONT = pygame.font.SysFont('Comicsans', 35)

CITYSCAPE_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'bg.png')), (WIN_WIDTH, WIN_HEIGHT))

START_SCREEN = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'start_screen.png')), (START_SCREEN_WIDTH, START_SCREEN_HEIGHT))

PLATFORM = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'platform.png')))

OBSTACLE = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'obstacle.png')))

BIRD_ASSETS = [
	pygame.transform.scale(pygame.image.load(os.path.join('assets', 'bird1.png')), (BIRD_WIDTH, BIRD_HEIGHT)),

	pygame.transform.scale(pygame.image.load(os.path.join('assets', 'bird2.png')), (BIRD_WIDTH, BIRD_HEIGHT)),

	pygame.transform.scale(pygame.image.load(os.path.join('assets', 'bird3.png')), (BIRD_WIDTH, BIRD_HEIGHT))
]

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption(CAPTION)

class Bird():
	ASSETS = BIRD_ASSETS
	MAX_TILT = 25
	ROTATION_VELOCITY = 20
	ANIMATION_TIME = 10

	def __init__(self, x, y):
		self.x = x 
		self.y = y

		self.tilt = 0
		self.flap_count = 0
		self.velocity = 0
		self.height = self.y 
		self.asset_count = 0
		self.asset = self.ASSETS[0]

	def flap(self):
		self.velocity = -10
		self.flap_count = 0
		self.height = self.y

	def flap_movement(self):
		self.flap_count = self.flap_count + 1

# Displacement equation which moves the bird a certain number of pixels up the screen
# This is dependent on the number of times that the flap animation has appeared on screen
		displacement = (self.velocity * (self.flap_count)) + (	1.5 * self.flap_count ** 2)

		if displacement >= 16:
			displacement = 16

		elif displacement < 0:
			displacement = displacement - 2

		self.y = self.y + displacement

		if displacement < 0 or self.y < self.height + 50:
			if self.tilt < self.MAX_TILT:
				self.tilt = self.MAX_TILT

		else:
			if self.tilt > -90:
				self.tilt = self.tilt - self.ROTATION_VELOCITY

	def draw_sprite(self, win):
		self.asset_count = self.asset_count + 1

		if self.asset_count <= self.ANIMATION_TIME:
			self.asset = self.ASSETS[0]

		elif self.asset_count <= self.ANIMATION_TIME * 2:
			self.asset = self.ASSETS[1]

		elif self.asset_count <= self.ANIMATION_TIME * 3:
			self.asset = self.ASSETS[2]

		elif self.asset_count <= self.ANIMATION_TIME * 4:
			self.asset = self.ASSETS[1]

		elif self.asset_count == self.ANIMATION_TIME * 4 + 1:
			self.asset = self.ASSETS[0]
			self.asset_count = 0

		if self.tilt <= -80:
			self.asset = self.ASSETS[1]
			self.asset_count = self.ANIMATION_TIME * 2

		flapped_asset = pygame.transform.rotate(self.asset, self.tilt)
		asset_center = flapped_asset.get_rect(center = self.asset.get_rect(topleft = (self.x, self.y)).center)

		win.blit(flapped_asset, (asset_center.topleft))

	def get_bird_mask(self):
		return pygame.mask.from_surface(self.asset)

class Obstacle():
	OBJ_SPACING = 200
	VELOCITY_SPEED = 6.5

	def __init__(self, x):
		self.x = x 

		self.height = 0
		self.spacing = 100

		self.top_obj = 0 
		self.bottom_obj = 0 

		self.TOP_OBSTACLE_ASSET = pygame.transform.rotate(OBSTACLE, 180)
		self.BOTTOM_OBSTACLE_ASSET = OBSTACLE

		self.passed = False 
		self.get_ycor()

	def get_ycor(self):
		self.height = random.randint(110, 375)

		self.top_obj = self.height - self.TOP_OBSTACLE_ASSET.get_height()
		self.bottom_obj = self.height + self.OBJ_SPACING

	def move_obstacle(self):
		self.x = self.x - self.VELOCITY_SPEED

	def obj_collision(self, bird):
		bird_mask = bird.get_bird_mask()

		top_obstacle_mask = pygame.mask.from_surface(self.TOP_OBSTACLE_ASSET)
		bottom_obstacle_mask = pygame.mask.from_surface(self.BOTTOM_OBSTACLE_ASSET)

		top_obstacle_offset = (self.x - bird.x, self.top_obj - round(bird.y))
		bottom_obstacle_offset = (self.x - bird.x, self.bottom_obj - round(bird.y))

		top_obstacle_overlap = bird_mask.overlap(top_obstacle_mask, top_obstacle_offset)
		bottom_obstacle_overlap = bird_mask.overlap(bottom_obstacle_mask, bottom_obstacle_offset)

		if top_obstacle_overlap or bottom_obstacle_overlap:
			return True

		return False

	def draw_obj(self, win):
		win.blit(self.TOP_OBSTACLE_ASSET, (self.x, self.top_obj))
		win.blit(self.BOTTOM_OBSTACLE_ASSET, (self.x, self.bottom_obj))

class Platform():
	MOVEMENT_VELOCITY = 6.5
	PLATFORM_ASSET = PLATFORM
	PLATFORM_WIDTH = PLATFORM.get_width()

	def __init__(self, y):
		self.y = y 
		self.x1 = 0 
		self.x2 = self.PLATFORM_WIDTH

	def drag_movement(self):
		self.x1 = self.x1 - self.MOVEMENT_VELOCITY
		self.x2 = self.x2 - self.MOVEMENT_VELOCITY

		if self.x1 + self.PLATFORM_WIDTH < 0:
			self.x1 = self.x2 + self.PLATFORM_WIDTH

		elif self.x2 + self.PLATFORM_WIDTH < 0:
			self.x2 = self.x1 + self.PLATFORM_WIDTH

	def draw_element(self, win):
		win.blit(self.PLATFORM_ASSET, (self.x1, self.y))
		win.blit(self.PLATFORM_ASSET, (self.x2, self.y))

def render_end_screen(bird_score, win):
	win.blit(CITYSCAPE_BG, (0, 0))

	DRAW_END_SCREEN = END_SCREEN_FONT.render(f'You lost! Your score was: {bird_score}', 1, WHITE)

	win.blit(DRAW_END_SCREEN, (WIN_WIDTH // 2 - DRAW_END_SCREEN.get_width() // 2, WIN_HEIGHT // 2 - DRAW_END_SCREEN.get_height() // 2 - 30))

	pygame.display.update()

	pygame.time.delay(5000)

def render_elements(win, bird_score, menu_bar, bird, obstacles, platform):
	win.blit(CITYSCAPE_BG, (0, 0))

	for obstacle in obstacles:
		obstacle.draw_obj(win)

	platform.draw_element(win)

	bird.draw_sprite(win)

	pygame.draw.rect(win, ORANGE, menu_bar)

	RENDER_SCORE = MAIN_FONT.render('Score: ' + str(bird_score), 1, WHITE)
	win.blit(RENDER_SCORE, (WIN_WIDTH // 2 - (RENDER_SCORE.get_width() // 2), 0))

def main_game_loop():
	run = True
	clock = pygame.time.Clock()

	bird = Bird(WIN_WIDTH // 2 - (BIRD_ASSETS[0].get_width() // 2), WIN_HEIGHT // 2 - (BIRD_ASSETS[0].get_height() + 15))
	obstacles = [Obstacle(500)]
	platform = Platform(635)

	menu_bar = pygame.Rect(0, 0, WIN_WIDTH, 45)

	bird_score = 0

	start = False
	end = False

	while run:
		clock.tick(FPS)

		removed_obstacles = []
		append_new_obstacle = False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				sys.exit()

			if event.type == pygame.KEYDOWN and not end:
				if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
					if not start:
						start = True 
					bird.flap()

			if event.type == pygame.MOUSEBUTTONDOWN and not end:
				if not start:
					start = True
				bird.flap()

		if start:
			bird.flap_movement()

			for obstacle in obstacles:
				if obstacle.obj_collision(bird) or bird.y >= 600:
					pygame.time.delay(100)

					render_end_screen(bird_score, WIN)
					main_menu()

				if obstacle.x + obstacle.TOP_OBSTACLE_ASSET.get_width() < 0:
					removed_obstacles.append(obstacle)

				if not obstacle.passed and obstacle.x < bird.x:
					obstacle.passed = True 
					append_new_obstacle = True

				obstacle.move_obstacle()

			if append_new_obstacle:
				bird_score = bird_score + 1
				obstacles.append(Obstacle(700))

			for removed_obstacle in removed_obstacles:
				obstacles.remove(removed_obstacle)

			platform.drag_movement()
			render_elements(WIN, bird_score, menu_bar, bird, obstacles, platform)

		pygame.display.update()

def main_menu():
	run = True

	while run:
		WIN.blit(CITYSCAPE_BG, (0, 0))

		WIN.blit(START_SCREEN, (WIN_WIDTH // 2 - START_SCREEN.get_width() // 2, WIN_HEIGHT // 2 - START_SCREEN.get_height() // 2))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				main_game_loop()

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					main_game_loop()

		pygame.display.update()

main_menu()

if __name__ == '__main__':
	main_menu()
