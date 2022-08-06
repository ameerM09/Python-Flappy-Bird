from . import *

OBSTACLE = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'obstacle.png')))

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