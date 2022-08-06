from . import *

PLATFORM = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'platform.png')))

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