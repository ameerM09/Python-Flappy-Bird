from settings import *

WIN_WIDTH = 500
WIN_HEIGHT = 750
CAPTION = 'Flappy Bird'

START_SCREEN_WIDTH = 322
START_SCREEN_HEIGHT = 467.25

FPS = 30

WHITE = (255, 255, 255)
ORANGE = (215, 115, 40)

MAIN_FONT = pygame.font.SysFont('Comicsans', 30)
END_SCREEN_FONT = pygame.font.SysFont('Comicsans', 35)

CITYSCAPE_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'bg.png')), (WIN_WIDTH, WIN_HEIGHT))

START_SCREEN = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'start_screen.png')), (START_SCREEN_WIDTH, START_SCREEN_HEIGHT))

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption(CAPTION) 

def render_end_screen(bird_score, win):
	win.blit(CITYSCAPE_BG, (0, 0))

	DRAW_END_SCREEN = END_SCREEN_FONT.render(f'Game over! Your score was: {bird_score}', 1, WHITE)

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
